import os
import json
import numpy as np
import logging
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import librosa

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtractAudioAndTranscribeVideo:
    def __init__(self, video_path: str, output_dir: str):
        self.video_path = video_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.audio_path = os.path.join(self.output_dir, "audio.wav")

    def extract_audio(self):
        try:
            video = VideoFileClip(self.video_path)
            if video.audio is None:
                raise Exception("No audio track found in the video")
            video.audio.write_audiofile(self.audio_path)
        except Exception as e:
            raise Exception(f"Error extracting audio: {str(e)}")

    def classify_audio(self, audio_chunk_path):
        y, sr = librosa.load(audio_chunk_path, sr=16000)
        n_fft = min(512, len(y))

        # Extract features
        zcr = np.mean(librosa.feature.zero_crossing_rate(y, frame_length=n_fft, hop_length=n_fft//2))
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=n_fft, hop_length=n_fft//2))
        spectral_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr, n_fft=n_fft, hop_length=n_fft//2))
        tonnetz = np.mean(librosa.feature.tonnetz(y=y, sr=sr))
        chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr, n_fft=n_fft, hop_length=n_fft//2))
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
        rms = np.mean(librosa.feature.rms(y=y))

        logger.info(f"Features for chunk {audio_chunk_path} - ZCR: {zcr}, Spectral Centroid: {spectral_centroid}, Spectral Contrast: {spectral_contrast}, Tonnetz: {tonnetz}, Chroma: {chroma}, MFCC: {mfcc}, RMS: {rms}")

        # Adjusted thresholds for classification
        if zcr < 0.03 and spectral_centroid < 1500 and spectral_contrast < 20 and tonnetz < 0.1 and rms < 0.01:
            classification = "Silence"
        elif zcr > 0.1 and spectral_centroid > 2000 and chroma > 0.4:
            classification = "Music"
        else:
            classification = "Speech"

        logger.info(f"Classification for chunk {audio_chunk_path}: {classification}")
        return classification

    def transcribe_audio(self):
        recognizer = sr.Recognizer()
        try:
            audio = AudioSegment.from_wav(self.audio_path)
            chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=audio.dBFS-14, keep_silence=500)

            if len(chunks) == 0:
                raise Exception("No transcribable audio found")

            transcript = []
            current_time = 0  # Initialize current time tracker

            for i, chunk in enumerate(chunks):
                chunk_silent = AudioSegment.silent(duration=10)
                audio_chunk = chunk_silent + chunk + chunk_silent
                chunk_path = os.path.join(self.output_dir, f"chunk{i}.wav")
                audio_chunk.export(chunk_path, format="wav")

                # Get the duration of the current chunk
                chunk_duration = len(chunk) / 1000.0  # Convert to seconds

                # Classify the audio chunk
                classification = self.classify_audio(chunk_path)

                if classification == "Speech":
                    with sr.AudioFile(chunk_path) as source:
                        audio_listened = recognizer.record(source)
                        try:
                            text = recognizer.recognize_google(audio_listened)
                            timestamp = {
                                "start": current_time,
                                "end": current_time + chunk_duration,
                                "text": text,
                                "classification": classification
                            }
                            logger.info(f"Transcription for chunk {chunk_path}: {text}")
                            transcript.append(timestamp)

                            # Save individual chunk transcript as JSON
                            chunk_json_path = os.path.join(self.output_dir, f"chunk{i}.json")
                            with open(chunk_json_path, 'w') as json_file:
                                json.dump(timestamp, json_file, indent=4)

                        except sr.UnknownValueError:
                            error_info = {
                                "start": current_time,
                                "end": current_time + chunk_duration,
                                "text": "",
                                "error": "Could not understand audio",
                                "classification": classification
                            }
                            logger.info(f"Error for chunk {chunk_path}: Could not understand audio")
                            transcript.append(error_info)

                            # Save individual chunk error as JSON
                            chunk_json_path = os.path.join(self.output_dir, f"chunk{i}.json")
                            with open(chunk_json_path, 'w') as json_file:
                                json.dump(error_info, json_file, indent=4)
                else:
                    logger.info(f"Skipping transcription for chunk {chunk_path} classified as {classification}")
                    non_speech_info = {
                        "start": current_time,
                        "end": current_time + chunk_duration,
                        "text": "",
                        "classification": classification
                    }
                    transcript.append(non_speech_info)

                    # Save non-speech chunk info as JSON
                    chunk_json_path = os.path.join(self.output_dir, f"chunk{i}.json")
                    with open(chunk_json_path, 'w') as json_file:
                        json.dump(non_speech_info, json_file, indent=4)

                # Update current time tracker
                current_time += chunk_duration

            # Save the entire transcript as a single JSON
            transcript_json_path = os.path.join(self.output_dir, "transcript.json")
            with open(transcript_json_path, 'w') as json_file:
                json.dump(transcript, json_file, indent=4)

            return transcript
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")

    def process(self):
        self.extract_audio()
        return self.transcribe_audio()
