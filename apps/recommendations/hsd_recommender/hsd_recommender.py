from pymongo import MongoClient

from .models import (
    Playlist,
    AllFeatures,
    EmotionFeatures,
    EssentiaFeatures,
)
from .consts import MONGO_URL, MONGO_DB, MONGO_COLLECTION
from .methods import generateRandomPlaylist, generatePlaylist, searchSongs


class HSD_Recommender:
    """
    The HSD Recommender class
    This class wrapps all the logic of the original HSD recommender api backend
    into a single class.
    """

    def __init__(self):
        """
        Initialize the HSD Recommender class
        """
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

        self.collection.create_index([("title", "text")])

    def generateRandomPlaylist(self) -> Playlist:
        """
        Generate a random playlist
        :return: A random Playlist
        """
        return generateRandomPlaylist(self.collection)

    def generateEmotionalPlaylist(self, emotionFeatures: EmotionFeatures) -> Playlist:
        """
        Generate a playlist based on emotion features
        :param emotionFeatures: Emotion features
        :return: A playlist based on emotion features
        """
        return generatePlaylist(self.collection, "emotion", emotionFeatures)

    def generateEssentiaPlaylist(self, essentiaFeatures: EssentiaFeatures) -> Playlist:
        """
        Generate a playlist based on Essentia features
        :param essentiaFeatures: Essentia features
        :return: A playlist based on Essentia features
        """
        return generatePlaylist(self.collection, "essentia", essentiaFeatures)

    def generateAllFeaturesPlaylist(self, allFeatures: AllFeatures) -> Playlist:
        """
        Generate a playlist based on all features
        :param allFeatures: All features
        :return: A playlist based on all features
        """
        return generatePlaylist(self.collection, "allFeatures", allFeatures)

    def searchSongs(self, query: str) -> Playlist:
        """
        Search for songs in the database
        :param query: The query to search for
        :return: A list of songs that match the query
        """
        return searchSongs(self.collection, query)
