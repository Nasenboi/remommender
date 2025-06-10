from pymongo import MongoClient

from .models import (
    Playlist,
    AllFeatures,
    EmotionFeatures,
    EssentiaFeatures,
)
from .consts import MONGO_URL, MONGO_DB, MONGO_COLLECTION
from .methods import generate_random_playlist, generate_playlist, generate_songs


class HSDRecommender:
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

        if not self._is_connected():
            raise ConnectionError("Failed to connect to MongoDB")

    def generate_random_playlist(self) -> Playlist:
        """
        Generate a random playlist
        :return: A random Playlist
        """
        if not self._is_connected():
            raise ConnectionError("Failed to connect to MongoDB")

        return generate_random_playlist(self.collection)

    def generate_emotional_playlist(self, emotionFeatures: EmotionFeatures) -> Playlist:
        """
        Generate a playlist based on emotion features
        :param emotionFeatures: Emotion features
        :return: A playlist based on emotion features
        """
        if not self._is_connected():
            raise ConnectionError("Failed to connect to MongoDB")

        return generate_playlist(
            collection=self.collection, playlistType="emotion", features=emotionFeatures
        )

    def generate_essentia_playlist(
        self, essentiaFeatures: EssentiaFeatures
    ) -> Playlist:
        """
        Generate a playlist based on Essentia features
        :param essentiaFeatures: Essentia features
        :return: A playlist based on Essentia features
        """
        if not self._is_connected():
            raise ConnectionError("Failed to connect to MongoDB")

        return generate_playlist(
            collection=self.collection,
            playlistType="essentia",
            features=essentiaFeatures,
        )

    def generate_all_features_playlist(self, allFeatures: AllFeatures) -> Playlist:
        """
        Generate a playlist based on all features
        :param allFeatures: All features
        :return: A playlist based on all features
        """
        if not self._is_connected():
            raise ConnectionError("Failed to connect to MongoDB")

        return generate_playlist(
            collection=self.collection,
            playlistType="allFeatures",
            features=allFeatures,
        )

    def generate_songs(self, query: str) -> Playlist:
        """
        Search for songs in the database
        :param query: The query to search for
        :return: A list of songs that match the query
        """
        if not self._is_connected():
            raise ConnectionError("Failed to connect to MongoDB")

        return generate_songs(self.collection, query)

    def _is_connected(self) -> bool:
        """
        Check if the MongoDB connection is established
        :return: True if connected, False otherwise
        """
        try:
            self.client.admin.command("ping")
            return True
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            return False