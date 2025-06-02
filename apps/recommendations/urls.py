from django.urls import re_path

from apps.recommendations.views import (
    RecommendFromSpeechView,
    RecommendFromEmotionFeatures,
)

app_name = "recommendations"
urlpatterns = [
    re_path(r"from-speech/(?P<filename>[^/]+)$", RecommendFromSpeechView.as_view()),
    re_path(r"from-emotion-features$", RecommendFromEmotionFeatures.as_view()),
]
