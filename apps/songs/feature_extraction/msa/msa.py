from msa.msa_utils import *
from msa.similarity_kmean_utils import *
from msa.similarity_kmean import *
from msa.ssm import *

from scipy import ndimage
from essentia.standard import MonoLoader

class MusicStructureAnalysis():

    def __init__(self, file_path):
        self.file_path = file_path
        self.sr = 22050
        self.hop_length = 2205
        self.n_fft = 4410
        self.audio = MonoLoader(filename=self.file_path, sampleRate=self.sr)()
        self.duration = len(self.audio) / float(self.sr)
        self.chroma = None
        self.s_thresh = None
        self.timeLagRepresentation = None
        self.novelty = None
        self.est_nov_peaks = None
    
    def compute_ssm(self, L=40, H=10, L_smooth=4, tempo_rel_set=np.array([1]),
                             shift_set=np.array([0]), strategy='relative', scale=True, thresh=0.15,
                             penalty=0.0, binarize=False):

        # Chroma Feature Sequence and SSM (10 Hz)
        Chroma = librosa.feature.chroma_stft(y=self.audio, sr=self.sr, tuning=0, norm=2, hop_length=self.hop_length, n_fft=self.n_fft)
        Fs_C = self.sr / 2205

        # Chroma Feature Sequence and SSM
        X, Fs_feature = smooth_downsample_feature_sequence(Chroma, Fs_C, filt_len=L, down_sampling=H)
        X = normalize_feature_sequence(X, norm='2', threshold=0.001)

        # Compute SSM
        S, I = compute_sm_ti(X, X, L=L_smooth, tempo_rel_set=tempo_rel_set, shift_set=shift_set, direction=2)
        S_thresh = threshold_matrix(S, thresh=thresh, strategy=strategy,
                                            scale=scale, penalty=penalty, binarize=binarize)
        
        self.chroma = Chroma
        self.s_thresh = S_thresh

        # plt.imshow(S_thresh, origin='lower', interpolation='none')
        # plt.show()

        return X, Fs_feature, S_thresh, I, Chroma
    
    def compute_time_lag_representation(self, circular=True):
        self.timeLagRepresentation = compute_time_lag_representation(self.s_thresh, circular=circular)

        # plt.imshow(self.timeLagRepresentation, origin='lower', interpolation='none')
        # plt.show()
        return self.timeLagRepresentation
    
    def compute_novelty_function(self):
        L_filter = ndimage.median_filter(self.timeLagRepresentation, (2,15))
        L_filter = ndimage.gaussian_filter(L_filter, 2)

        # compute novelty function and pick peaks
        self.novelty = novelty_structure_feature(L_filter)
    
        # plot novelty function
        # plt.plot(self.novelty)
        # plt.show()
        return self.novelty
    
    def pick_peaks_from_noveltyFunction(self, L=10, mean=200):
        est_idxs = np.array(pick_peaks(self.novelty, L, mean, name_of_png=None)) # peaks function for plotting self.file_path
        
        # add 0 to beginning and length of novelty function to end of list
        est_idxs = np.concatenate([[0], est_idxs, [len(self.novelty)]])
        self.est_nov_peaks = est_idxs

        return self.est_nov_peaks
    
    def noveltyPeaks_scaled(self, duration):
        """
        Convert the novelty peaks to different time scales (Dreisatz)
        Args:
            est_noveltyPeaks: time indeces of the novelty peaks
            noveltyFunction: the novelty function   
            duration: the duration of the feature the time indeces are computed for. E.g. chroma (frames) or audio (sec) duration
        Returns:
            novPeaks_sec: the time indeces of the novelty peaks in seconds or frames, depending on the duration argument
        """
        b = np.multiply(self.est_nov_peaks, duration)
        novPeaks_scaled = np.divide(b, len(self.novelty))
        
        return novPeaks_scaled

    def labelElements(self):

        chroma_features = normalize(self.chroma, norm_type=np.inf, floor=0.1, min_db=-80)
        chroma_features = np.reshape(chroma_features, (chroma_features.shape[1], chroma_features.shape[0]))
        novPeaks_scaled_to_chroma = np.rint(self.noveltyPeaks_scaled(chroma_features.shape[0])).astype(int)

        est_labels, segments_labels, dist_to_KMean_centroid = compute_similarity(chroma_features, novPeaks_scaled_to_chroma, 
                                                                              dirichlet=False,xmeans=True, k=5, offset=4)
        
        dist_to_KMean_centroid = self.scale_distances_to_KMeanCentroid(segments_labels, dist_to_KMean_centroid)
        
        return est_labels, segments_labels, dist_to_KMean_centroid

    def scale_distances_to_KMeanCentroid(self, segments_labels, dist_to_KMean_centroid):
        """
        Maps the distance between the points and its centroid of the KMean to 0-1

        Args:
        indices_labels: dictionary with the time indices of the segments
        dist_to_KMean_centroid: distance between the points in each cluster and the centroid

        Returns:
            indeces and the distance to centroid in a sorted array (starting at segment 0, 1, ...)
        """
        indices_distance = {}
        for i in segments_labels:
            distance = []
            for item in segments_labels[i]:
                distance.append(dist_to_KMean_centroid[item][0])

            if(min(distance) == max(distance)):
                distance = [0 for x in distance]
            else:
                distance = [(x - min(distance)) / (max(distance) - min(distance)) for x in distance]

            indices_distance[i] = np.column_stack((segments_labels[i], np.array(distance)))

        u = list(indices_distance.values())
        out = np.concatenate(u)
        indices_distance_sorted = out[out[:,0].argsort()] # chronological order of segments

        return indices_distance_sorted
    
    def process_boundaries_labels(self):
        self.compute_ssm()
        self.compute_time_lag_representation()
        self.compute_novelty_function()
        self.pick_peaks_from_noveltyFunction()
        est_labels, _, _ = self.labelElements()
        boundaries = self.noveltyPeaks_scaled(self.duration)

        return boundaries.tolist(), est_labels.tolist()
    
    def process_boundaries_labels_kmeanDistance(self):
        self.compute_ssm()
        self.compute_time_lag_representation()
        self.compute_novelty_function()
        self.pick_peaks_from_noveltyFunction()
        est_labels, _, dist_to_KMean_centroid = self.labelElements()
        
        boundaries = self.noveltyPeaks_scaled(self.duration)

        return boundaries, est_labels, dist_to_KMean_centroid
        
    def storeResults_to_txtFile(self, est_labels, indices_distance_sorted):
        id_label = []
        noveltyPeaks_sec = self.noveltyPeaks_scaled(self.duration)

        for i in range(len(noveltyPeaks_sec) - 1):
            id_label.append(['Label: ' + str(est_labels[i]), str(round(noveltyPeaks_sec[i], 2)), str(round(indices_distance_sorted[i][1], 2))])

        # write to txt file
        with open('output.txt', 'w') as f:
            for item in id_label:
                f.write(str(item))
                f.write('\n')

        print('done')