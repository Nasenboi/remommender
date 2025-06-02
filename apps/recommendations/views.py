import dataclasses

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from packages.emotion_recognition.processor import SERProcessor

from packages.hsd_recommender.models import EmotionFeatures
from packages.hsd_recommender.hsd_recommender import HSDRecommender


class RecommendFromSpeechView(APIView):
    parser_classes = [FileUploadParser]
    speech_processor = SERProcessor()
    hsd_recommender = HSDRecommender()

    def post(self, request, filename, format=None):
        file = request.data["file"]
        speech_emotion_result = self.speech_processor.process_audio_file(file)
        if isinstance(speech_emotion_result, list):
            speech_emotion_result = speech_emotion_result[0]
        speech_emotion_result = dataclasses.asdict(speech_emotion_result)

        valence = float(speech_emotion_result["valence"])
        arousal = float(speech_emotion_result["arousal"])
        dominance = float(speech_emotion_result["dominance"])
        authenticity = valence * dominance
        timeliness = arousal * dominance
        complexity = dominance

        emotion_features = EmotionFeatures(
            valence=valence,
            arousal=arousal,
            dominance=dominance,
            authenticity=authenticity,
            timeliness=timeliness,
            complexity=complexity,
        )

        playlist = self.hsd_recommender.generate_emotional_playlist(
            emotionFeatures=emotion_features
        )

        return Response(status=200, data=playlist)


class RecommendFromEmotionFeatures(APIView):
    hsd_recommender = HSDRecommender()

    def post(self, request, format=None):
        emotion_features_data = request.data
        emotion_features = EmotionFeatures(**emotion_features_data)

        playlist = self.hsd_recommender.generate_emotional_playlist(
            emotionFeatures=emotion_features
        )

        return Response(status=200, data=playlist)
