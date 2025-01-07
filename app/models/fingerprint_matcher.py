from app.models.feature_extractor import FeatureExtractor


class SongMatcher:
    def __init__(self, file_path, fingerprints):
        self.feature_extractor = FeatureExtractor()
        self.fingerprint = self.__generate_fingerprint(file_path)
        self.similarities = []  # Initialize as an empty list
        self.all_fingerprints = fingerprints
        self.__compute_all_similarities()  # Compute similarities during initialization

    def __generate_fingerprint(self, file_path):
        """Generate a fingerprint for the provided audio file."""
        # Generate spectrogram
        spectrogram, sr = self.feature_extractor.generate_mel_spectrogram(file_path)
        if spectrogram is None or sr is None:
            raise ValueError(f"Failed to generate spectrogram for file: {file_path}")

        # Generate perceptual hash fingerprint
        fingerprint = self.feature_extractor.generate_perceptual_hash(spectrogram)
        if not fingerprint:
            raise ValueError(f"Failed to generate fingerprint for file: {file_path}")

        return fingerprint

    def __compute_similarity(self, fingerprint1, fingerprint2):
        """Compute a similarity metric between two perceptual hashes."""
        # Use Hamming distance for perceptual hashes
        return sum(c1 == c2 for c1, c2 in zip(fingerprint1, fingerprint2)) / max(len(fingerprint1), len(fingerprint2))

    def __compute_all_similarities(self):
        """Compute similarity for the fingerprint against all songs and store results."""
        for song_name, stored_files in self.all_fingerprints.items():
            for file_type, stored_fingerprint in stored_files.items():
                # Remove '.wav' from file_type if desired
                file_type = file_type.replace(".wav", "")

                # Compute similarity
                similarity = self.__compute_similarity(self.fingerprint, stored_fingerprint)

                # Append the results as a tuple
                self.similarities.append((song_name, similarity, file_type))

        # Sort similarities in descending order during computation
        self.similarities.sort(key=lambda x: x[1], reverse=True)

    def compute_all_similarities(self):
        """Return all precomputed similarities."""
        return self.similarities

    def get_best_match(self):
        """Find the best match from precomputed similarities."""
        if not self.similarities:
            raise ValueError("Similarities have not been computed.")

        # The best match is the first item in the sorted list
        best_match, best_similarity, best_file_type = self.similarities[0]
        return best_match
