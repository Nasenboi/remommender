import math
from typing import List, Tuple

import numpy as np
from welford import Welford

from apps.core.consts import SLOPE_DETECTOR_GAIN, SLOPE_DETECTOR_THRESHOLD


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
    valence: float, arousal: float, samples: Tuple[List[float], List[float]]
) -> Tuple[List[float], List[float]]:
    """
    Update the samples with the new valence and arousal values.
    :param valence: Valence value
    :param arousal: Arousal value
    :param samples: Tuple of lists containing valence and arousal values
    :return: Updated samples
    """
    samples_valence = samples[0][1:] + [valence]
    samples_arousal = samples[1][1:] + [arousal]
    return samples_valence, samples_arousal


def get_slope_probability(
    samples: Tuple[List[float], List[float]], old_mean: Tuple[float, float], arousal_weight: float = 0.5, valence_weight: float = 0.5
) -> Tuple[Tuple[float, float], float]:
    """
    Get the slope probability based on the valence and arousal values.
    :param samples: Tuple of lists containing valence and arousal values
    :param old_mean: Tuple of old mean values for valence and arousal
    :param arousal_weight: Weight for arousal value (default: 0.5)
    :param valence_weight: Weight for valence value (default: 0.5)
    :return: Tuple of the mean values and the slope probability
    """

    samples_array = np.column_stack(samples)

    mean: np.ndarray = _get_welford_values(samples_array)[0]

    if arousal_weight != 0.5 or valence_weight != 0.5:
        arousal_weight = arousal_weight / (arousal_weight + valence_weight)
        valence_weight = 1 - arousal_weight

    delta = valence_weight * abs(mean[0] - old_mean[0]) + arousal_weight * abs(mean[1] - old_mean[1])

    slope_probability = math.tanh((delta - SLOPE_DETECTOR_THRESHOLD) * SLOPE_DETECTOR_GAIN)
    slope_probability = min(max(slope_probability, 0), 1.0)

    return tuple(mean.tolist()), slope_probability
