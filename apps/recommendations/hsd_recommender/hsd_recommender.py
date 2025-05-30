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

    def generate_random_playlist(self) -> Playlist:
        """
        Generate a random playlist
        :return: A random Playlist
        """
        return generate_random_playlist(self.collection)

    def generate_emotional_playlist(self, emotionFeatures: EmotionFeatures) -> Playlist:
        """
        Generate a playlist based on emotion features
        :param emotionFeatures: Emotion features
        :return: A playlist based on emotion features
        """
        return generate_playlist(self.collection, "emotion", emotionFeatures)

    def generate_essentia_playlist(self, essentiaFeatures: EssentiaFeatures) -> Playlist:
        """
        Generate a playlist based on Essentia features
        :param essentiaFeatures: Essentia features
        :return: A playlist based on Essentia features
        """
        return generate_playlist(self.collection, "essentia", essentiaFeatures)

    def generate_all_features_playlist(self, allFeatures: AllFeatures) -> Playlist:
        """
        Generate a playlist based on all features
        :param allFeatures: All features
        :return: A playlist based on all features
        """
        return generate_playlist(self.collection, "allFeatures", allFeatures)

    def generate_songs(self, query: str) -> Playlist:
        """
        Search for songs in the database
        :param query: The query to search for
        :return: A list of songs that match the query
        """
        return generate_songs(self.collection, query)
