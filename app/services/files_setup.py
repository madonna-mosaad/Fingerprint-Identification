import os
import json
import matplotlib.pyplot as plt
from app.models.feature_extractor import FeatureExtractor


class FeatureFoldersProcessor:
    def __init__(self, base_path='static/songs'):
        self.base_path = base_path
        self.features_path = os.path.join(os.path.dirname(base_path), "features")
        self.fingerprints_path = os.path.join(os.path.dirname(base_path), "fingerprints")
        self.spectrograms_path = os.path.join(os.path.dirname(base_path), "spectrograms")
        self.feature_extractor = FeatureExtractor()
        self.ensure_directories()
        self.all_results, self.all_fingerprints = self.process_all_songs()

    def ensure_directories(self):
        """Ensure that the features, fingerprints, and spectrograms directories exist."""
        os.makedirs(self.features_path, exist_ok=True)
        os.makedirs(self.fingerprints_path, exist_ok=True)
        os.makedirs(self.spectrograms_path, exist_ok=True)

    def get_song_folders(self):
        """Retrieve all song folders in the base path."""
        return [
            os.path.join(self.base_path, folder)
            for folder in os.listdir(self.base_path)
            if os.path.isdir(os.path.join(self.base_path, folder))
        ]

    def save_to_json(self, folder_name, data, data_type):
        """Save data to a JSON file in the appropriate directory."""
        if data_type == "features":
            file_path = os.path.join(self.features_path, f"{folder_name}.json")
        elif data_type == "fingerprints":
            file_path = os.path.join(self.fingerprints_path, f"{folder_name}.json")
        else:
            raise ValueError("Invalid data type specified")

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def save_spectrogram(self, folder_name, file_name, spectrogram):
        """Save spectrogram data to the spectrograms directory as a PNG image."""
        folder_path = os.path.join(self.spectrograms_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        spectrogram_file = os.path.join(folder_path, f"{file_name}.png")

        # Plot the spectrogram
        plt.figure(figsize=(10, 4))
        plt.imshow(spectrogram, aspect='auto', origin='lower', interpolation='none')
        plt.colorbar(format='%+2.0f dB')
        plt.title(f"Spectrogram - {file_name}")
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.tight_layout()

        # Save the plot as a PNG file
        plt.savefig(spectrogram_file, dpi=300)
        plt.close()  # Close the plot to free up memory

    def process_song_folder(self, folder_path):
        folder_name = os.path.basename(folder_path)
        results = {}
        fingerprints = {}

        features_file = os.path.join(self.features_path, f"{folder_name}.json")
        fingerprints_file = os.path.join(self.fingerprints_path, f"{folder_name}.json")

        if os.path.exists(features_file):
            with open(features_file, "r") as f:
                results = json.load(f)

        if os.path.exists(fingerprints_file):
            with open(fingerprints_file, "r") as f:
                fingerprints = json.load(f)

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) \
                    and file_name.endswith(('.wav', '.mp3')) \
                    and file_name not in results \
                    and file_name not in fingerprints:

                spectrogram, sr = self.feature_extractor.generate_mel_spectrogram(file_path)
                if spectrogram is None or sr is None:
                    print(f"[Error] Skipping {file_path} due to failed spectrogram generation.")
                    continue

                # Save spectrogram data
                self.save_spectrogram(folder_name, file_name, spectrogram)

                # Extract features
                features = self.feature_extractor.extract_features(spectrogram, sr)
                if not features:
                    print(f"[Error] Skipping {file_path} due to empty features.")
                    continue

                # Generate fingerprint
                fingerprint = self.feature_extractor.generate_perceptual_hash(spectrogram)
                if not fingerprint:
                    print(f"[Error] Skipping {file_path} due to failed fingerprint generation.")
                    continue

                results[file_name] = features
                fingerprints[file_name] = fingerprint

        self.save_to_json(folder_name, results, "features")
        self.save_to_json(folder_name, fingerprints, "fingerprints")
        return results, fingerprints

    def process_all_songs(self):
        """Process all song folders and generate a comprehensive result."""
        all_results = {}
        all_fingerprints = {}
        for folder_path in self.get_song_folders():
            folder_name = os.path.basename(folder_path)
            results, fingerprints = self.process_song_folder(folder_path)
            all_results[folder_name] = results
            all_fingerprints[folder_name] = fingerprints
        return all_results, all_fingerprints
