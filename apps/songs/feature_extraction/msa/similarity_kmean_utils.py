import copy
import numpy as np
import scipy.fftpack
import pylab as plt

def resample_mx(X, incolpos, outcolpos):
    """
    Y = resample_mx(X, incolpos, outcolpos)
    X is taken as a set of columns, each starting at 'time'
    colpos, and continuing until the start of the next column.
    Y is a similar matrix, with time boundaries defined by
    outcolpos.  Each column of Y is a duration-weighted average of
    the overlapping columns of X.
    2010-04-14 Dan Ellis dpwe@ee.columbia.edu  based on samplemx/beatavg
    -> python: TBM, 2011-11-05, TESTED
    """
    noutcols = len(outcolpos)
    Y = np.zeros((X.shape[0], noutcols))
    # assign 'end times' to final columns
    if outcolpos.max() > incolpos.max():
        incolpos = np.concatenate([incolpos,[outcolpos.max()]])
        X = np.concatenate([X, X[:,-1].reshape(X.shape[0],1)], axis=1)
    outcolpos = np.concatenate([outcolpos, [outcolpos[-1]]])
    # durations (default weights) of input columns)
    incoldurs = np.concatenate([np.diff(incolpos), [1]])

    for c in range(noutcols):
        firstincol = np.where(incolpos <= outcolpos[c])[0][-1]
        firstincolnext = np.where(incolpos < outcolpos[c+1])[0][-1]
        lastincol = max(firstincol,firstincolnext)
        # default weights
        wts = copy.deepcopy(incoldurs[firstincol:lastincol+1])
        # now fix up by partial overlap at ends
        if len(wts) > 1:
            wts[0] = wts[0] - (outcolpos[c] - incolpos[firstincol])
            wts[-1] = wts[-1] - (incolpos[lastincol+1] - outcolpos[c+1])
        wts = wts * 1. / float(sum(wts))
        Y[:,c] = np.dot(X[:,firstincol:lastincol+1], wts)
    # done
    return Y

def magnitude(X):
    """Magnitude of a complex matrix."""
    r = np.real(X)
    i = np.imag(X)
    return np.sqrt(r * r + i * i)

def compute_ffmc2d(X):
    """Computes the 2D-Fourier Magnitude Coefficients."""
    # 2d-fft
    fft2 = scipy.fftpack.fft2(X)

    # Magnitude
    fft2m = magnitude(fft2)

    # FFTshift and flatten
    fftshift = scipy.fftpack.fftshift(fft2m).flatten()

    # cmap = plt.cm.get_cmap('hot')
    # plt.imshow(np.log1p(scipy.fftpack.fftshift(fft2m)).T, interpolation="nearest",
    #    aspect="auto", cmap=cmap)
    # plt.show()


    # Take out redundant components
    return fftshift[:fftshift.shape[0] // 2 + 1]