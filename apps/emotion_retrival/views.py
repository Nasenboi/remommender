import dataclasses

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from packages.emotion_recognition.processor import SERProcessor


class RetrieveEmotionFromSpeechView(APIView):
    parser_classes = [FileUploadParser]
    speech_processor = SERProcessor()

    def post(self, request, filename, format=None):
        file = request.data["file"]
        speech_emotion_result = self.speech_processor.process_audio_file(file)

        return Response(status=200, data=dataclasses.asdict(speech_emotion_result))
