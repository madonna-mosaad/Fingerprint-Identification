import os
from PyQt5.QtWidgets import QFileDialog


class AudioFileUploader:
    last_opened_folder = "/"


    @classmethod
    def upload_audio_signal_file(cls):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                None,
                "Select Audio File",
                cls.last_opened_folder,
                "Audio Files (*.wav *.mp3);;All Files (*)",
                options=options
            )

            # If a file is selected, update the last opened folder and return the file path
            if file_path:
                cls.last_opened_folder = os.path.dirname(file_path)
                return file_path
            else:
                print("No file was selected.")
                return None
        except Exception as e:
            raise Exception(f"An error occurred while uploading the file: {str(e)}")
