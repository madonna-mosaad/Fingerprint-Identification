import librosa
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import imagehash
from io import BytesIO


class FeatureExtractor:
    def generate_mel_spectrogram(self, file_path, duration=30, sr=None, n_mels=128):
        """
        Generate a log-scaled Mel spectrogram for a given audio file.
        """
        try:
            y, sr = librosa.load(file_path, sr=sr, duration=duration)
            mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
            log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
            return log_mel_spectrogram, sr
        except Exception as e:
            print(f"Error generating mel spectrogram: {e}")
            return None, None

    def extract_features(self, spectrogram, sr):
        """
        Extract a variety of features from a log-scaled Mel spectrogram.
        """
        if spectrogram is None or sr is None:
            return {}

        features = {}
        try:
            amplitude_spectrogram = librosa.db_to_amplitude(spectrogram)

            # Spectral features
            features['spectral_centroid_mean'] = float(np.mean(
                librosa.feature.spectral_centroid(S=amplitude_spectrogram, sr=sr)
            ))
            features['spectral_bandwidth_mean'] = float(np.mean(
                librosa.feature.spectral_bandwidth(S=amplitude_spectrogram, sr=sr)
            ))
            features['spectral_contrast_mean'] = float(np.mean(
                librosa.feature.spectral_contrast(S=amplitude_spectrogram, sr=sr)
            ))
            features['spectral_rolloff_mean'] = float(np.mean(
                librosa.feature.spectral_rolloff(S=amplitude_spectrogram, sr=sr)
            ))

            # Tonal features
            chroma = librosa.feature.chroma_stft(S=amplitude_spectrogram, sr=sr)
            tonnetz = librosa.feature.tonnetz(chroma=chroma, sr=sr)
            features['tonnetz_mean'] = float(np.mean(tonnetz))

            # Temporal features
            zero_crossings = librosa.feature.zero_crossing_rate(amplitude_spectrogram)
            features['zero_crossing_rate_mean'] = float(np.mean(zero_crossings))

            # MFCCs
            mfcc = librosa.feature.mfcc(S=spectrogram, sr=sr, n_mfcc=13)
            for i in range(mfcc.shape[0]):
                features[f'mfcc_{i}_mean'] = float(np.mean(mfcc[i, :]))

            features = self._normalize_features(features)

        except Exception as e:
            print(f"Error extracting features: {e}")

        return features

    def generate_perceptual_hash(self, spectrogram):
        """
        Generate a perceptual hash (pHash) from a spectrogram without saving the image.
        """
        try:
            # Create a spectrogram image in memory
            fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
            ax.axis('off')  # Remove axes
            ax.imshow(spectrogram, aspect='auto', origin='lower', cmap='viridis')

            # Save the image to a BytesIO buffer
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            plt.close(fig)
            buf.seek(0)

            # Load the image from the buffer and compute its hash
            image = Image.open(buf)
            phash = imagehash.phash(image)
            buf.close()

            return str(phash)

        except Exception as e:
            print(f"Error generating perceptual hash: {e}")
            return None

    def _normalize_features(self, features):
        """
        Normalize feature values to a range of [0, 1].
        """
        try:
            max_val = max(features.values())
            min_val = min(features.values())
            return {key: (val - min_val) / (max_val - min_val) for key, val in features.items()}
        except Exception as e:
            print(f"Error normalizing features: {e}")
            return features
