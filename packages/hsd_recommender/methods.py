from annoy import AnnoyIndex
from sklearn.neighbors import KDTree
from typing import List, Tuple, Dict
import numpy as np
from pymongo.collection import Collection
from collections import defaultdict
import time


from .models import (
    Playlist,
    Song,
    SongFeatures,
)
from .consts import (
    MUSIC_SERVER_URL,
    ALBUM_ART_SERVER_URL,
    PLAYLIST_LENGTH,
    GENRE_DATA_BASE,
    GENRE_CORR,
    SONG_FEATURES_SEARCH,
)


def normalize_data(data: np.ndarray) -> np.ndarray:
    """
    Normalize the input data to the range [0, 1].
    :param data: Input data as a NumPy array.
    :return: Normalized data as a NumPy array.
    """
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def get_song_id(collection: Collection) -> List[str]:
    """
    Get all song IDs from the MongoDB collection.
    :param collection: MongoDB collection object.
    :return: List of song IDs.
    """
    song_ID = []
    for document in collection.find():
        song_ID.append(document["_id"])
    return song_ID


def get_song_id_and_dimensions(
    collection: Collection,
    genre: GENRE_DATA_BASE,
    features: Dict[str, int] = SONG_FEATURES_SEARCH,
) -> Tuple[List[str], List[List[float]]]:
    """
    Get song IDs and their corresponding dimensions from the MongoDB collection.
    :param collection: MongoDB collection object.
    :param genre: Genre of the songs (e.g., rock, pop, none).
    :return: List containing song IDs and their dimensions.
    """

    song_ID = []
    song_Dimensions = []

    if genre == "none":
        for doc in collection.find({}, features):
            song_ID.append(doc["_id"])
            song_Dimensions.append(list(doc["features"].values()))
    else:
        # find all documents that contain the genre in the top 3 genres
        query = "features.genres.top3_genres." + str(genre)
        for doc in collection.find({query: {"$exists": True}}, features):
            song_ID.append(doc["_id"])
            song_Dimensions.append(list(doc["features"].values()))
    return [song_ID, song_Dimensions]


def sort_genres_according_to_correlation(song: Song) -> Song:
    """
    sort the genre index from db according to correlation of Genre Rock (see data_types.py)
    genres[10] gets deleted, no one needs indie pop, genre chill gets send to web app, but it
    is least correlated and does not get displayed in bubble chart
    :param song: Song object containing features and genres.
    :return: Song object with sorted genres.
    """
    genres = [0] * 33

    for index, feature in enumerate(song["features"]["genres"]["all_genres"]):
        val = song["features"]["genres"]["all_genres"][feature]
        genres[GENRE_CORR.index(GENRE_DATA_BASE[index])] = val

    # normalize color of genres
    genres = list(normalize_data(np.array(genres)))
    del genres[
        10
    ]  # delete genre indie pop, genre chill is least correlated and also not in web app
    song["features"]["genres"]["all_genres"] = genres

    return song


def find_duplicate_songs_in_playlist(artist: List[str], playlist: Playlist) -> Playlist:
    """
    Remove duplicate songs from the playlist based on the artist name.
    :param artist: List of artist names.
    :param playlist: List of songs in the playlist.
    :return: Playlist with duplicates removed.
    """
    l = []
    playlist_new = playlist.copy()

    tally = defaultdict(list)
    for i, item in enumerate(artist):
        tally[item].append(i)

    for dup in sorted(((key, locs) for key, locs in tally.items() if len(locs) > 1)):
        l.append(dup[1][1:])

    l = [item for sublist in l for item in sublist]

    for index in sorted(l, reverse=True):
        del playlist_new[index]

    while len(playlist_new) < PLAYLIST_LENGTH:
        playlist_new = playlist.copy()
        l.remove(min(l))
        for index in sorted(l, reverse=True):
            del playlist_new[index]

    while len(playlist_new) > PLAYLIST_LENGTH:
        playlist_new = playlist_new[:-1]

    return playlist_new


def get_song_information(collection: Collection, top_ID: str) -> Playlist:
    """
    Get song information from the MongoDB collection based on the top song IDs.
    :param collection: MongoDB collection object.
    :param top_ID: List of top song IDs.
    :return: List of Song objects with detailed information.
    """
    playlist = []

    for i, val in enumerate(top_ID):
        song = collection.find_one({"_id": val})
        if song is None:
            continue

        # song = sort_genres_according_to_correlation(song)
        song["ids"]["track_id"] = MUSIC_SERVER_URL + song["ids"]["track_id"]
        song["ids"]["artwork_id"] = ALBUM_ART_SERVER_URL + song["ids"]["artwork_id"]

        playlist.append(song)

    return playlist


def generate_playlist(
    collection: Collection,
    features: SongFeatures,
    genre: GENRE_DATA_BASE = "none",
) -> Playlist:
    """
    Generate a playlist based on the input vector and playlist type.
    :param collection: MongoDB collection object.
    :param features: Input vector of different kinds of features.
    :param genre: Genre of the songs (e.g., rock, pop, none).
    :return: List of Song objects in the generated playlist.
    """

    # Use only features that are present in the features object
    features_search = {
        "features." + key: 1
        for key, value in features.model_dump().items()
        if value is not None
    }

    song_id_dimensions = get_song_id_and_dimensions(
        collection, genre, features=features_search
    )
    # top_songs_ids = k_d_tree(song_id_dimensions, inputVector, PLAYLIST_LENGTH)

    top_songs_ids = k_d_tree(
        data=song_id_dimensions, features=features, numClosestNeighbours=PLAYLIST_LENGTH
    )

    end = time.time()
    playlist = get_song_information(collection=collection, top_ID=top_songs_ids)
    return playlist


def generate_songs(collection: Collection, text: str) -> Playlist:
    """
    Search for songs in the MongoDB collection based on the input text.
    :param collection: MongoDB collection object.
    :param text: Input text for searching songs.
    :return: List of Song objects matching the search criteria.
    """
    searchResults = []
    cursor = collection.find(
        {"$text": {"$search": str(text)}}, {"score": {"$meta": "textScore"}}
    )
    cursor = cursor.sort([("score", {"$meta": "textScore"})])

    for song in cursor:
        song = sort_genres_according_to_correlation(song)
        song["ids"]["track_id"] = MUSIC_SERVER_URL + song["ids"]["track_id"]
        song["ids"]["artwork_id"] = ALBUM_ART_SERVER_URL + song["ids"]["artwork_id"]
        searchResults.append(song)

    return searchResults


def k_d_tree(
    data: Tuple[List[str], List[List[float]]],
    features: SongFeatures,
    numClosestNeighbours: int,
) -> List[str]:
    """
    takes as input the id, dimensions and length of Playlist, returns the song ids of the closest neighbours
    :param data: List containing song IDs and their dimensions.
    :param features: Input vector for the query.
    :param numClosestNeighbours: Number of closest neighbours to find.
    :return: List of song IDs of the closest neighbours.
    """
    # knearest extrahiert die doppelte größe der eigentlichen playlist, um später doppelte artists entfernen zu können
    # data = [[songAdresse1, songAdresse2, ...], [[InputVector], [5DimVektor], [5DimVektor2], ...]]

    features = list(features.model_dump(exclude_none=True).values())

    data[1].insert(0, features)
    songList = []

    # ensure number of requested songs is as big as the actual song list
    if numClosestNeighbours > len(data[0]):
        numClosestNeighbours = len(data[0])

    tree = KDTree(data[1], leaf_size=3)
    dist, ind = tree.query(data[1][:1], k=numClosestNeighbours + 1)
    ind = np.array(ind).flatten().tolist()

    # erase query point (is always 0th element in data array) queryPoint = InputVector
    for i, val in enumerate(ind):
        if val == 0:
            del ind[i]
        # subtract array index and get the Songadress (subtract because inputVector is deleted)
        ind[i] = ind[i] - 1
        songList.append(data[0][ind[i]])

    return songList


def annoy(
    song_id_dimensions: Tuple[List[str], List[List[float]]],
    inputVector: List[float],
    numClosestNeighbours: int,
) -> List[str]:
    """
    Takes as input the id, dimensions and length of Playlist, returns the song ids of the closest neighbours
    :param song_id_dimensions: List containing song IDs and their dimensions.
    :param inputVector: Input vector for the query.
    :param numClosestNeighbours: Number of closest neighbours to find.
    :return: List of song IDs of the closest neighbours.
    """

    ids = song_id_dimensions[0]
    dimensions = song_id_dimensions[1]

    dimensions.insert(0, inputVector)
    songList = []

    dimension_length = len(dimensions[0])  # Length of item vector that will be indexed
    annoy = AnnoyIndex(dimension_length, "euclidean")
    for i, val in enumerate(dimensions):
        annoy.add_item(i, val)

    annoy.build(40)  # 10 trees
    ind = annoy.get_nns_by_item(0, numClosestNeighbours)

    # erase query point (is always 0th element in data array) queryPoint = InputVector
    for i, val in enumerate(ind):
        if val == 0:
            del ind[i]
        # subtract array index and get the Songadress (subtract because inputVector is deleted)
        ind[i] = ind[i] - 1
        songList.append(ids[ind[i]])

    return songList
