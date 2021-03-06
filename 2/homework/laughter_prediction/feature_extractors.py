import scipy.io.wavfile as wav
import librosa
import pandas as pd
import numpy as np


class FeatureExtractor:

    def extract_features(self, wav_path, frame_sec=0.01):
        """
        Extracts features for classification ny frames for .wav file

        :param wav_path: string, path to .wav file
        :return: pandas.DataFrame with features of shape (n_chunks, n_features)
        """

        rate, audio = wav.read(wav_path)

        # Let's make and display a mel-scaled power (energy-squared) spectrogram
        frame_size = int(rate * frame_sec)

        filterbanks = []
        mfccs = []

        for i in range(0, len(audio) - frame_size, frame_size):
            # Convert to log scale (dB). We'll use the peak power (max) as reference.
            cur_filterbank = librosa.feature.melspectrogram(y=audio.astype(np.float)[i: i + frame_size], sr=rate)
            filterbanks.append(np.mean(np.log(cur_filterbank), axis=1))
            # Next, we'll extract the top 13 Mel-frequency cepstral coefficients (MFCCs)
            cur_mfcc = librosa.feature.mfcc(y=audio.astype(np.float)[i: i + frame_size], sr=rate)
            mfccs.append(np.mean(cur_mfcc, axis=1))

        filterbank = np.vstack(filterbanks)
        mfcc = np.vstack(mfccs)

        columns_mfcc = list(map(lambda num: 'mfcc_' + str(num), list(range(mfcc.shape[1]))))
        columns_filter = list(map(lambda num: 'filterbank_' + str(num), list(range(filterbank.shape[1]))))
        return pd.DataFrame(mfcc, columns=columns_mfcc), columns_mfcc, \
               pd.DataFrame(filterbank, columns=columns_filter), columns_filter
