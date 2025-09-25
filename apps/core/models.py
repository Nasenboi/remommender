import uuid
from typing import List

from django.db import models


class SongFeatures(models.Model):
    valence = models.FloatField(null=True, blank=True)
    arousal = models.FloatField(null=True, blank=True)
    authenticity = models.FloatField(null=True, blank=True)
    timeliness = models.FloatField(null=True, blank=True)
    complexity = models.FloatField(null=True, blank=True)
    danceability = models.FloatField(null=True, blank=True)
    tonal = models.FloatField(null=True, blank=True)
    voice = models.FloatField(null=True, blank=True)
    bpm = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Features(valence={self.valence}, arousal={self.arousal})"

    def to_dict(self, include: List[str] = None) -> dict:
        """
        Convert the features to a dictionary, optionally including only specified fields.
        :param include: List of fields to include in the dictionary.
        :return: Dictionary representation of the features.
        """
        if include is None:
            include = [
                "valence",
                "arousal",
                "authenticity",
                "timeliness",
                "complexity",
                "danceability",
                "tonal",
                "voice",
                "bpm",
            ]
        return {
            field: getattr(self, field) for field in include if hasattr(self, field)
        }


class SongGenres(models.Model):
    top3_genres = models.JSONField(default=dict)
    all_genres = models.JSONField(default=dict)


class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artwork_file = models.FileField(upload_to="Album_Art/")
    album = models.CharField(max_length=255, null=True, blank=True)
    artist = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Artwork {self.id}"
    
    @property
    def artwork_url(self):
        if self.artwork_file:
            return self.artwork_file.url
        return None

class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    duration_s = models.FloatField()
    features = models.OneToOneField(
        SongFeatures, on_delete=models.CASCADE, related_name="song"
    )
    genres = models.OneToOneField(
        SongGenres, on_delete=models.CASCADE, related_name="song"
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="songs",
        null=True,
        blank=True,
    )
    audio_file = models.FileField(upload_to="Audio/")

    def __str__(self):
        return f"{self.title} by {self.artist}" + (
            f" from {self.album_name}" if self.album_name else ""
        )

    @property
    def album_name(self):
        if self.album:
            return self.album.album
        return None

    @property
    def song_url(self):
        if self.audio_file:
            return self.audio_file.url
        return None

    @property
    def artwork_url(self):
        if self.album:
            return self.album.artwork_file.url
        return None
