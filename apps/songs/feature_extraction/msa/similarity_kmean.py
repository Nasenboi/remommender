import librosa
import numpy as np
import six
import logging
import scipy.cluster.vq as vq
from sklearn import mixture
from sklearn.cluster import KMeans

import msa.similarity_kmean_utils as utils
from msa.xmeans import *

def min_max_normalize(F, floor=0.001):
    """Normalizes features such that each vector is between floor to 1."""
    F += -F.min() + floor
    F = F / F.max(axis=0)
    return F

def lognormalize(F, floor=0.1, min_db=-80):
    """Log-normalizes features such that each vector is between min_db to 0."""
    assert min_db < 0
    F = min_max_normalize(F, floor=floor)
    F = np.abs(min_db) * np.log10(F)  # Normalize from min_db to 0
    return F

def normalize(X, norm_type, floor=0.0, min_db=-80):
    if isinstance(norm_type, six.string_types):
        if norm_type == "min_max":
            return min_max_normalize(X, floor=floor)
        if norm_type == "log":
            return lognormalize(X, floor=floor, min_db=min_db)
    return librosa.util.normalize(X, norm=norm_type, axis=1)

def get_feat_segments(F, bound_idxs):

    # Make sure bound_idxs are not empty
    assert len(bound_idxs) > 0, "Boundaries can't be empty"

    # Make sure that boundaries are sorted
    bound_idxs = np.sort(bound_idxs)

    # Make sure we're not out of bounds
    assert bound_idxs[0] >= 0 and bound_idxs[-1] == F.shape[0], \
        "Boundaries are not correct for the given feature dimensions."

    # Obtain the segments
    feat_segments = []
    for i in range(len(bound_idxs) - 1):
        feat_segments.append(F[bound_idxs[i]:bound_idxs[i + 1], :])

    return feat_segments


def feat_segments_to_2dfmc_max(feat_segments, offset=4):

    if len(feat_segments) == 0:
        return []

    # Get maximum segment size
    max_len = max([feat_segment.shape[0] for feat_segment in feat_segments])

    fmcs = []
    for feat_segment in feat_segments:
        # Zero pad if needed
        X = np.zeros((max_len, feat_segment.shape[1]))

        # Remove a set of frames in the beginning an end of the segment
        if feat_segment.shape[0] <= offset or offset == 0:
            X[:feat_segment.shape[0], :] = feat_segment
        else:
            X[:feat_segment.shape[0] - offset, :] = \
                feat_segment[offset // 2:-offset // 2, :]

        # Compute the 2D-FMC
        try:
            fmcs.append(utils.compute_ffmc2d(X))
        except:
            logging.warning("Couldn't compute the 2D Fourier Transform")
            fmcs.append(np.zeros((X.shape[0] * X.shape[1]) // 2 + 1))

        # Normalize
        # fmcs[-1] = fmcs[-1] / float(fmcs[-1].max())

    return np.asarray(fmcs)


def compute_labels_kmeans(fmcs, k):
    # Removing the higher frequencies seem to yield better results
    fmcs = fmcs[:, fmcs.shape[1] // 2:]

    # Pre-process
    fmcs = np.log1p(fmcs)
    wfmcs = vq.whiten(fmcs)

    # Make sure we are not using more clusters than existing segments
    if k > fmcs.shape[0]:
        k = fmcs.shape[0]

    # K-means
    kmeans = KMeans(n_clusters=k, n_init=200)
    kmeans.fit(wfmcs)

    # store labels and indices
    idxs_labels = {'label' + str(i): np.where(kmeans.labels_ == i)[0] for i in range(k)}

    dist_to_centroid = kmeans.transform(wfmcs)**2
    
    return kmeans.labels_, idxs_labels, dist_to_centroid

def compute_similarity(F, bound_idxs, dirichlet=False, xmeans=False, k=5,
                       offset=4):
    # Get the feature segments
    feat_segments = get_feat_segments(F, bound_idxs)

    # Get the 2D-FMCs segments
    fmcs = feat_segments_to_2dfmc_max(feat_segments, offset)
    if len(fmcs) == 0:
        return np.arange(len(bound_idxs) - 1)

    # Compute the labels using kmeans
    if dirichlet:
        k_init = np.min([fmcs.shape[0], k])
        # Only compute the dirichlet method if the fmc shape is small enough
        if fmcs.shape[1] > 500:
            est_labels, sorted_labels, dist_to_centroid = compute_labels_kmeans(fmcs, k=k)
        else:
            dpgmm = mixture.DPGMM(n_components=k_init, covariance_type='full')
            # dpgmm = mixture.VBGMM(n_components=k_init, covariance_type='full')
            dpgmm.fit(fmcs)
            k = len(dpgmm.means_)
            est_labels = dpgmm.predict(fmcs)
            #print("Estimated with Dirichlet Process:", k)
    if xmeans:
        xm = XMeans(fmcs, plot=False)
        k = xm.estimate_K_knee(th=0.01, maxK=8)
        est_labels, idxs_labels, dist_to_centroid = compute_labels_kmeans(fmcs, k=k)
        #print("Estimated with Xmeans:", k)
    else:
        est_labels, idxs_labels, dist_to_centroid = compute_labels_kmeans(fmcs, k=k)

    return est_labels, idxs_labels, dist_to_centroid