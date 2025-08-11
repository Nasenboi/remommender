import math
from typing import List, Tuple

import numpy as np
from welford import Welford

from apps.core.consts import EMOTION_VALUES_WINDOW_SIZE, SLOPE_DETECTOR_GAIN, SLOPE_DETECTOR_THRESHOLD


def _get_welford_values(samples: np.ndarray) -> np.ndarray:
    """
    Get the Welford statistics for the given samples.
    :param samples: Input samples of shape (N, 2)
    :return: Welford statistics (mean, sample variance, population variance)
    """
    welford = Welford(samples)

    mean = welford.mean
    var_s = welford.var_s
    var_p = welford.var_p

    return np.stack([mean, var_s, var_p])


def update_samples(
    valence: float, arousal: float, samples: Tuple[List[float], List[float]], sample_index: int
) -> Tuple[List[float], List[float]]:
    """
    Update the samples with the new valence and arousal values.
    :param valence: Valence value
    :param arousal: Arousal value
    :param samples: Tuple of lists containing valence and arousal values
    :param sample_index: Current sample index
    :return: Updated samples
    """
    samples[0][sample_index] = valence
    samples[1][sample_index] = arousal
    return samples


def update_sample_index(sample_index: int) -> int:
    """
    Update the sample index for the circular buffer.
    :param sample_index: Current sample index
    :return: Updated sample index
    """
    return (sample_index + 1) % EMOTION_VALUES_WINDOW_SIZE


def get_slope_probablity(
    samples: Tuple[List[float], List[float]], old_mean: Tuple[float, float]
) -> Tuple[float, float]:
    """
    Get the slope probability based on the valence and arousal values.
    :param valence: Valence value
    :param arousal: Arousal value
    :return: Tuple of the mean and the slope probability
    """

    samples_array = np.column_stack(samples)

    mean = _get_welford_values(samples_array)[0]

    delta = np.sum(np.abs(mean - old_mean)) / 2

    slope_probability = math.tanh((delta - SLOPE_DETECTOR_THRESHOLD) * SLOPE_DETECTOR_GAIN)
    slope_probability = min(max(slope_probability, 0), 1.0)

    return mean, slope_probability
