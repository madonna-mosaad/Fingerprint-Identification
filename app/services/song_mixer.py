import numpy as np
import soundfile as sf
import os
from scipy.signal import resample


class SongMixer:
    def __init__(self, filepath01, filepath02):
        """
        Initialize the SongMixer with two audio file paths.
        Resamples, normalizes, and trims audio to match lengths, sample rates, and intensities.
        """
        self.filepath01 = filepath01
        self.filepath02 = filepath02

        # Read the audio files
        self.audio01, self.samplerate01 = sf.read(filepath01)
        self.audio02, self.samplerate02 = sf.read(filepath02)

        # Resample if sample rates do not match
        target_samplerate = min(self.samplerate01, self.samplerate02)
        self.audio01 = self._resample_audio(self.audio01, self.samplerate01, target_samplerate)
        self.audio02 = self._resample_audio(self.audio02, self.samplerate02, target_samplerate)
        self.samplerate = target_samplerate
        # Normalize intensities
        self.audio01 = self._normalize_audio(self.audio01)
        self.audio02 = self._normalize_audio(self.audio02)

        # Trim to the shorter length
        self._trim_to_match_length()

    def _resample_audio(self, audio, original_rate, target_rate):
        """
        Resamples audio to the target sample rate.
        """
        num_samples = int(len(audio) * target_rate / original_rate)
        return resample(audio, num_samples)

    def _normalize_audio(self, audio):
        """
        Normalizes audio intensity to the range [-1.0, 1.0].
        """
        return audio / np.max(np.abs(audio))

    def _trim_to_match_length(self):
        """
        Trims the longer audio file to match the length of the shorter one.
        """
        min_length = min(len(self.audio01), len(self.audio02))
        self.audio01 = self.audio01[:min_length]
        self.audio02 = self.audio02[:min_length]

    def mix(self, weight):
        """
        Mix the two audio files based on the given weight.
        :param weight: Weight of the first song (0-100). The second song weight will be (100 - weight).
        :return: Mixed audio signal as a NumPy array.
        """
        if not (0 <= weight <= 100):
            raise ValueError("Weight must be in the range 0 to 100.")

        # Calculate weights proportionally based on the slider value
        weight01 = weight  # Weight for the first song (e.g., 75 if slider is at 75%)
        weight02 = 100 - weight  # Weight for the second song (e.g., 25 if slider is at 75%)

        # Normalize weights so the larger weight is 100%
        max_weight = max(weight01, weight02)
        weight01 = (weight01 / max_weight) * 100
        weight02 = (weight02 / max_weight) * 100

        # Scale audio signals according to the adjusted weights
        mixed_audio = (weight01 / 100 * self.audio01) + (weight02 / 100 * self.audio02)
        mixed_audio = np.clip(mixed_audio, -1.0, 1.0)  # Normalize to avoid clipping

        return mixed_audio

    def save_mixed_audio(self, weight, output_filename='mixed song.wav'):
        """
        Save the mixed audio to a file.
        :param weight: Weight of the first song (0-100).
        :param output_filename: Name of the output file.
        :return: Path to the saved mixed audio file.
        """
        output_folder = 'static/generated mixed song'

        # Check if the folder exists, and create it if it doesn't
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_path = os.path.join(output_folder, output_filename)
        mixed_audio = self.mix(weight)

        # Save the mixed audio file
        sf.write(output_path, mixed_audio, self.samplerate, subtype='FLOAT')
        return output_path
