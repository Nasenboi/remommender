import dataclasses

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from packages.emotion_recognition.processor import SERProcessor


class RetrieveEmotionFromSpeechView(APIView):
    parser_classes = [FileUploadParser]
    speech_processor = SERProcessor()
    window_size_s = 10
    hop_size_s = 5

    def post(self, request, filename, format=None):
        file = request.data["file"]

        speech_emotion_result = self.speech_processor.process_audio_file(file)

        if isinstance(speech_emotion_result, list):
            speech_emotion_result = [
                dataclasses.asdict(result) for result in speech_emotion_result
            ]
        else:
            speech_emotion_result = dataclasses.asdict(speech_emotion_result)

        return Response(status=200, data=speech_emotion_result)
