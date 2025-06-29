from pymongo import MongoClient

from .models import (
    Playlist,
    SongFeatures,
)
from .consts import MONGO_URL, MONGO_DB, MONGO_COLLECTION, IP_MUSIC_SERVER
from .methods import generate_playlist


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
        self.base_url = IP_MUSIC_SERVER

        self.collection.create_index([("title", "text")])

        if not self._is_connected():
            raise ConnectionError("Failed to connect to MongoDB")

    def generate_playlist(
        self, songFeatures: SongFeatures, genre: str = "none"
    ) -> Playlist:
        """
        Generate a playlist based on emotion features
        :param emotionFeatures: Emotion features
        :return: A playlist based on emotion features
        """
        if not self._is_connected():
            raise ConnectionError("Failed to connect to MongoDB")

        playlist = generate_playlist(
            collection=self.collection, features=songFeatures, genre=genre
        )

        return playlist

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
