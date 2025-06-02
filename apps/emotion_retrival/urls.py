from django.urls import re_path

from apps.emotion_retrival.views import RetrieveEmotionFromSpeechView

app_name = "recommendations"
urlpatterns = [
    re_path(
        r"from-speech/(?P<filename>[^/]+)$", RetrieveEmotionFromSpeechView.as_view()
    )
]
