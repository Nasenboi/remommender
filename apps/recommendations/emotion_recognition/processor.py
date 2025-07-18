from dataclasses import dataclass
from typing import List, Union

import librosa
import numpy as np
import torch
from ninja.errors import ValidationError
from soundfile import LibsndfileError
from transformers import Wav2Vec2Processor
from typing_extensions import Final

from .classifier import EmotionModel

# based on: https://huggingface.co/audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim


class SERProcessor:
    SAMPLE_RATE: Final[int] = 16000

    @dataclass
    class SpeechEmotionResult:
        arousal: np.float32
        dominance: np.float32
        valence: np.float32

    def __init__(self, max_length: int = 30):
        self._device = "cuda:0" if torch.cuda.is_available() else "cpu"
        model_name = "audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim"
        self._processor = Wav2Vec2Processor.from_pretrained(model_name)
        self._model = EmotionModel.from_pretrained(model_name).to(self._device)
        self._max_length = max_length
        self._max_length_samples = max_length * self.SAMPLE_RATE

    def process_audio_file(
        self, file, window_size_s: int = 10, hop_size_s: int = 5
    ) -> SpeechEmotionResult:
        """
        Process audio file
        :param file: Path to the audio file or a file-like object
        :param window_size_s: Size of the window in seconds
        :param hop_size_s: Size of the hop in seconds
        :return: SpeechEmotionResult or list of SpeechEmotionResults
        """
        try:
            samples = librosa.load(file, sr=self.SAMPLE_RATE, mono=True)[0]
        except LibsndfileError as e:
            raise ValidationError(f"Audio file could not be parsed: {e.error_string}")

        if len(samples) > self._max_length_samples:
            raise ValidationError(
                f"Audio file is longer than the maximum specified length ({self._max_length} seconds)"
            )

        return self._audio_to_speech_emotion(samples)

    def _audio_to_speech_emotion(self, samples: np.ndarray) -> SpeechEmotionResult:
        """
        Process a single audio snippet
        :param samples: Audio samples as a numpy array
        :return: SpeechEmotionResult
        """

        processed_signal = self._processor(samples, sampling_rate=self.SAMPLE_RATE)
        processed_signal = processed_signal["input_values"][0]
        processed_signal = processed_signal.reshape(1, -1)
        processed_signal = torch.from_numpy(processed_signal).to(self._device)

        with torch.no_grad():
            result = self._model(processed_signal)[1]

        # convert to numpy
        result = result.detach().cpu().numpy()[0]

        return self.SpeechEmotionResult(
            arousal=result[0], dominance=result[1], valence=result[2]
        )
