import uuid

from django.db import models

from apps.core.models import Album, Song


class RecommendationStatistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    switch_probability = models.FloatField()
    valence = models.FloatField()
    arousal = models.FloatField()
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Statistic {self.id} for session {self.session_id} from {self.timestamp}"

    @property
    def song_id(self):
        return self.song.id if self.song else None

    @property
    def song_title(self):
        return self.song.title if self.song else None

    @property
    def song_artist(self):
        return self.song.artist if self.song else None

    @property
    def song_duration_s(self):
        return self.song.duration_s if self.song else None

    @property
    def song_valence(self):
        return self.song.features.valence if self.song and self.song.features else None

    @property
    def song_arousal(self):
        return self.song.features.arousal if self.song and self.song.features else None

    @property
    def song_authenticity(self):
        return self.song.features.authenticity if self.song and self.song.features else None

    @property
    def song_timeliness(self):
        return self.song.features.timeliness if self.song and self.song.features else None

    @property
    def song_complexity(self):
        return self.song.features.complexity if self.song and self.song.features else None

    @property
    def song_danceability(self):
        return self.song.features.danceability if self.song and self.song.features else None

    @property
    def song_tonal(self):
        return self.song.features.tonal if self.song and self.song.features else None

    @property
    def song_voice(self):
        return self.song.features.voice if self.song and self.song.features else None

    @property
    def song_bpm(self):
        return self.song.features.bpm if self.song and self.song.features else None

    @property
    def song_top_1_genre(self):
        if self.song and self.song.genres and self.song.genres.top3_genres:
            keys = list(self.song.genres.top3_genres.keys())
            return keys[0] if len(keys) > 0 else None
        return None

    @property
    def song_top_2_genre(self):
        if self.song and self.song.genres and self.song.genres.top3_genres:
            keys = list(self.song.genres.top3_genres.keys())
            return keys[1] if len(keys) > 1 else None
        return None

    @property
    def song_top_3_genre(self):
        if self.song and self.song.genres and self.song.genres.top3_genres:
            keys = list(self.song.genres.top3_genres.keys())
            return keys[2] if len(keys) > 2 else None
        return None

    @property
    def song_url(self):
        return self.song.song_url if self.song else None

    @property
    def album_id(self):
        return self.album.id if self.album else None

    @property
    def album_name(self):
        return self.album.album_name if self.album else None

    @property
    def album_artist(self):
        return self.album.artist if self.album else None

    @property
    def album_artwork_url(self):
        return self.album.artwork_url if self.album else None
