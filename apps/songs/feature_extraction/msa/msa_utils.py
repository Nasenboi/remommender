import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from scipy.ndimage import filters

def compute_kernel_checkerboard_gaussian(L, var=0.5, normalize=True):
    taper = np.sqrt(1/2) / (L * var)
    axis = np.arange(-L, L+1)
    gaussian1D = np.exp(-taper**2 * (axis**2))
    gaussian2D = np.outer(gaussian1D, gaussian1D)
    kernel_box = np.outer(np.sign(axis), np.sign(axis))
    kernel = kernel_box * gaussian2D
    if normalize:
        kernel = kernel / np.sum(np.abs(kernel))
    return kernel

def compute_gaussian_krnl(M):
    """Creates a gaussian kernel following Foote's paper."""
    g = signal.gaussian(M, M // 3., sym=True)
    G = np.dot(g.reshape(-1, 1), g.reshape(1, -1))
    G[M // 2:, :M // 2] = -G[M // 2:, :M // 2]
    G[:M // 2, M // 2:] = -G[:M // 2, M // 2:]
    return G

def compute_novelty_ssm(S, kernel=None, L=5, var=0.5, exclude=False):
    if kernel is None:
        kernel = compute_kernel_checkerboard_gaussian(L=L, var=var)
    N = S.shape[0]
    M = 2*L + 1
    nov = np.zeros(N)
    # np.pad does not work with numba/jit
    S_padded = np.pad(S, L, mode='constant')

    for n in range(N):
        # Does not work with numba/jit
        nov[n] = np.sum(S_padded[n:n+M, n:n+M] * kernel)
    if exclude:
        right = np.min([L, N])
        left = np.max([0, N-L])
        nov[0:right] = 0
        nov[left:N] = 0
    
    return nov

def compute_nc(X, kernel=None):
    """Computes the novelty curve from the self-similarity matrix X and
        the gaussian kernel G."""
    if kernel is None:
        kernel = compute_gaussian_krnl(66)
    G = kernel
    N = X.shape[0]
    M = G.shape[0]
    nc = np.zeros(N)

    for i in range(M // 2, N - M // 2 + 1):
        nc[i] = np.sum(X[i - M // 2:i + M // 2, i - M // 2:i + M // 2] * G)

    # Normalize
    nc += nc.min()
    nc /= nc.max()
    return nc

def pick_peaks(nc, L=16, mean=8, name_of_png=None):
    """Obtain peaks from a novelty curve using an adaptive threshold."""
    offset = nc.mean() / float(mean) ##200

    nc = filters.gaussian_filter1d(nc, sigma=1)  # Smooth out nc

    th = filters.median_filter(nc, size=L) + offset
    #th = filters.gaussian_filter(nc, sigma=L/2., mode="nearest") + offset

    peaks = []
    for i in range(1, nc.shape[0] - 1):
        # is it a peak?
        if nc[i - 1] < nc[i] and nc[i] > nc[i + 1]:
            # is it above the threshold?
            if nc[i] > th[i]:
                peaks.append(i)
    
    if name_of_png is not None:
        plt.plot(nc)
        plt.plot(th)
        a = name_of_png.split('/')[-3]
        b = name_of_png.split('/')[-2]
        c = name_of_png.split('/')[-1]
   
        for peak in peaks:
            plt.axvline(peak)
        
        plt.savefig('/Users/maed/Desktop/Backend_AudioProcess/plots/' + a + '_' + b + '_' + c.split('.')[0])
        plt.close()

    return peaks

def compute_time_lag_representation(S, circular=True):
    """Computation of (circular) time-lag representation

    Notebook: C4/C4S4_StructureFeature.ipynb

    Args:
        S (np.ndarray): Self-similarity matrix
        circular (bool): Computes circular version (Default value = True)

    Returns:
        L (np.ndarray): (Circular) time-lag representation of S
    """
    N = S.shape[0]
    if circular:
        L = np.zeros((N, N))
        for n in range(N):
            L[:, n] = np.roll(S[:, n], -n)
    else:
        L = np.zeros((2*N-1, N))
        for n in range(N):
            L[((N-1)-n):((2*N)-1-n), n] = S[:, n]
    return L

def novelty_structure_feature(L, padding=True):
    """Computation of the novelty function from a circular time-lag representation

    Notebook: C4/C4S4_StructureFeature.ipynb

    Args:
        L (np.ndarray): Circular time-lag representation
        padding (bool): Padding the result with the value zero (Default value = True)

    Returns:
        nov (np.ndarray): Novelty function
    """
    N = L.shape[0]
    if padding:
        nov = np.zeros(N)
    else:
        nov = np.zeros(N-1)
    for n in range(N-1):
        nov[n] = np.linalg.norm(L[:, n+1] - L[:, n])
    return nov