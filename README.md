# **Soundprints: Audio Fingerprinting App**

Soundprints is a Shazam-like app for identifying audio files (songs, vocals, or music) using spectrogram-based fingerprinting. This application supports audio mixing with similarity analysis, enabling efficient audio recognition from a pre-saved database.

---

## **Video Demo**

https://github.com/user-attachments/assets/e653a6b5-856f-4ca1-af2c-8bf816d91121

---

## **Overview**

Below is a screenshot showcasing the app's interface, featuring the **Weighted Blender** and the **Similarity Index Table**:

![App Design Overview](https://github.com/user-attachments/assets/62a3dc31-24bf-4580-854d-340c81e2407d)

---

## **Features**

### **Core Features**
1. **Audio Fingerprinting**:
   - Generate spectrograms for audio files (songs, music, and vocals) using the first 30 seconds of each track.
   - Extract features (spectral, tonal, and temporal) and create perceptual hashes for efficient audio recognition.

2. **Similarity Analysis**:
   - Compare a given audio file with the database.
   - Display similarity scores for each match in a clean table.
   - Sort results by similarity index.

3. **Audio Mixing**:
   - Combine two audio files with adjustable weight sliders.
   - Treat the mixed file as a new entry for similarity analysis.

4. **Efficient Data Handling**:
   - Automatically generates spectrograms, features, and fingerprints upon the first run.
   - Reuses generated files in subsequent runs to save time.

5. **Database Structure**:
   - Each song is stored in its own folder containing up to three audio files: `song.wav`, `vocals.wav`, and `instruments.wav`. 
   - The app can process any subset of these files, not requiring all three for a song.

6. **Future Scalability**:
   - Currently, the database is saved locally as folders within the project.
   - Future enhancements include moving the database to a server for real-time performance, like the real Shazam app.

---

## **Scenarios**

### **1. Identify an Audio File**
Upload an audio file (song, vocals, or music), and the app generates its fingerprint. The **Similarity Index Table** displays the closest matches from the database with similarity percentages and song details.

### **2. Audio Mixing and Recognition**
Use the **Weighted Blender** to combine two audio files. The app calculates a new fingerprint for the mixed audio and determines the most similar files in the database. Below is an example of mixing "FE!N vocals" with "Please Please Please song":

![Mixer Example](https://github.com/user-attachments/assets/03c0c329-ff26-4ec5-bfbc-db4e7fa3f55b)

- **Similarity Index Table**:
  - Displays similarity scores for all database entries.
- **Recognized Song**:
  - Displays the most likely match for the mixed audio.

---

## **Technical Details**

### **Features Example**
Below is an example of extracted features for three audio files of a song:

```json
{
        "spectral_centroid_mean": 0.5528992238416036,
        "spectral_bandwidth_mean": 0.5268320358136851,
        "spectral_contrast_mean": 0.10529028384467565,
        "spectral_rolloff_mean": 1.0,
        "tonnetz_mean": 0.10322825644131509,
        "zero_crossing_rate_mean": 0.1032304331109077,
        "mfcc_0_mean": 0.0,
        "mfcc_1_mean": 0.13177107585666026,
        "mfcc_2_mean": 0.102267788640439,
        "mfcc_3_mean": 0.1069292240807807,
        "mfcc_4_mean": 0.1048039126503005,
        "mfcc_5_mean": 0.1039056650539509,
        "mfcc_6_mean": 0.10368084224529522,
        "mfcc_7_mean": 0.10405067745595514,
        "mfcc_8_mean": 0.10269303553993522,
        "mfcc_9_mean": 0.10174654772092014,
        "mfcc_10_mean": 0.10171992499833234,
        "mfcc_11_mean": 0.10243432740720006,
        "mfcc_12_mean": 0.10228256609387294
}
```
---
### **Fingerprints Example**
The app generates perceptual hashes for the audio files:
```json
{
    "812dea55aa55aa57",
}
```
---

### **Features Explained**

1. **Spectral Features**:
   - **Spectral Centroid Mean**: Represents the center of gravity of the spectrum, indicating where the energy is concentrated.
   - **Spectral Bandwidth Mean**: Measures the width of the spectrum, showing how spread out the frequencies are.
   - **Spectral Contrast Mean**: Captures the difference in amplitudes between peaks and valleys in the spectrum, useful for identifying timbre.
   - **Spectral Rolloff Mean**: The frequency below which a specific percentage (e.g., 85%) of the spectral energy is concentrated.

2. **Tonal Features**:
   - **Tonnetz Mean**: Quantifies the tonal stability and harmonic content of the audio using tonal centroid features.

3. **Temporal Features**:
   - **Zero Crossing Rate Mean**: Measures how frequently the audio signal changes its sign, often used to distinguish between percussive and tonal sounds.

4. **MFCCs (Mel-Frequency Cepstral Coefficients)**:
   - Capture the shape of the audio spectrum by breaking it down into a series of coefficients (e.g., `mfcc_0_mean`, `mfcc_1_mean`).
   - Essential for identifying unique audio characteristics like pitch, tone, and rhythm.

5. **Perceptual Hashing**:
   - Converts extracted features into compact hash strings for efficient comparison and matching.
   - Ensures robust recognition even when audio has slight variations.

---

## **How to Run the Project**

1. Clone the repository:
   ```bash
   git clone https://github.com/YassienTawfikk/Soundprints.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Soundprints
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. Upon the first run, the app will generate spectrograms, features, and fingerprints, which may take 30 seconds. Subsequent runs will reuse these files for faster performance.
---

## **Team**

This project wouldn’t have been possible without the hard work and collaboration of my amazing team. Huge shout-out to:

- [Nancy Mahmoud](https://github.com/nancymahmoud1)  
- [Madonna Mosaad](https://github.com/madonna-mosaad)  
- [Yassien Tawfik](https://github.com/YassienTawfikk)

---

## **Contact**

For any questions or suggestions, feel free to reach out:

- **Name**: Yassien Tawfik  
- **Email**: [Yassien.m.m.tawfik@gmail.com](mailto:Yassien.m.m.tawfik@gmail.com)

