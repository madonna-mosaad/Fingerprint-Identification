from PyQt5 import QtWidgets
import os

from app.utils.clean_cache import remove_directories
from app.ui.Design import Ui_MainWindow
from app.services.files_setup import FeatureFoldersProcessor
from app.services.upload_wav import AudioFileUploader
from app.models.fingerprint_matcher import SongMatcher
from app.services.song_mixer import SongMixer


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.connect_signals()

        # Create a processor for features/fingerprints; it scans folders upon init
        self.service = FeatureFoldersProcessor()

        # Initialize mixer filepaths
        self.mixer_filepath01 = None
        self.mixer_filepath02 = None

    def connect_signals(self):
        self.ui.quit_app_button.clicked.connect(self.quit_app)
        self.ui.recognize_song_button.clicked.connect(self.upload_unkonw_sound)
        self.ui.uploaded_song_01_button.clicked.connect(self.set_mixer_first_song_filepath)
        self.ui.uploaded_song_02_button.clicked.connect(self.set_mixer_second_song_filepath)
        self.ui.reset_button.clicked.connect(self.reset_filepaths)
        self.ui.songs_weight_slider.valueChanged.connect(self.ui.update_song_weight_slider_label)
        self.ui.songs_weight_slider.sliderReleased.connect(self.generate_mixed_song)

        self.reset_filepaths()

    def upload_unkonw_sound(self):
        file_path = AudioFileUploader().upload_audio_signal_file()
        if file_path:
            self.match_and_display_similar_songs(file_path)

    def match_and_display_similar_songs(self, file_path):
        # Create a SongMatcher with the new audio file & known fingerprints
        self.matcher = SongMatcher(file_path, self.service.all_fingerprints)

        # Compute all similarities
        similarity_list = self.matcher.compute_all_similarities()

        # Sort the list by similarity index (descending order)
        Table = sorted(similarity_list, key=lambda x: x[1], reverse=True)

        # Clear any previous entries in the UI table
        self.ui.clear_index_table_data()

        # If Table is empty, handle gracefully
        if not Table:
            self.ui.update_recognized_song_data("No match found")
            return

        _, _, best_match_song_type = Table[0]
        # Populate the table with results
        for song_name, similarity_index, song_type in Table:
            # if best_match_song_type == song_type:
            self.ui.add_row_to_index_table(
                    song_name,
                    f"{similarity_index * 100:.2f}%",  # Convert to percentage
                    song_type
                )

        # The top match (first in sorted list) is the recognized song
        best_match, _, _ = Table[0]
        self.ui.update_recognized_song_data(best_match)

    def set_mixer_first_song_filepath(self):
        file_path = AudioFileUploader().upload_audio_signal_file()
        if file_path:
            self.mixer_filepath01 = file_path
            self.ui.uploaded_song_01_button.setText("Uploaded")

            file_name = os.path.splitext(os.path.basename(file_path))[0]  # File name without extension
            file_name = file_name.replace("_", " ")
            # Format the song name
            song_name = f"{file_name}"

            # Update the UI with the formatted song name
            self.ui.update_uploaded_fisrt_song_name(song_name)

    def set_mixer_second_song_filepath(self):
        file_path = AudioFileUploader().upload_audio_signal_file()
        if file_path:
            self.mixer_filepath02 = file_path
            self.ui.uploaded_song_02_button.setText("Uploaded")

            file_name = os.path.splitext(os.path.basename(file_path))[0]  # File name without extension
            file_name = file_name.replace("_", " ")
            # Format the song name
            song_name = f"{file_name}"

            # Update the UI with the formatted song name
            self.ui.update_uploaded_second_song_name(song_name)

    def reset_filepaths(self):
        self.mixer_filepath01 = None
        self.mixer_filepath02 = None

        self.ui.clear_index_table_data()
        self.ui.clear_recognized_song_data()

    def generate_mixed_song(self):
        if self.mixer_filepath01 and self.mixer_filepath02:
            # Create a SongMixer to blend the two tracks
            self.mixer = SongMixer(
                filepath01=self.mixer_filepath01,
                filepath02=self.mixer_filepath02
            )
            # Use the slider value for mixing weight
            path = self.mixer.save_mixed_audio(self.ui.songs_weight_slider.value())

            # Now check which known song the mixed track most closely matches
            self.match_and_display_similar_songs(path)

    def quit_app(self):
        self.app.quit()
        remove_directories()
