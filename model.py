import openai
import os

# Define constants
OPENAI_API_KEY = 'your_openai_api_key'
MODEL_ENGINE = 'text-davinci-002'
AUDIO_EXTENSIONS = ('.wav', '.mp3')

class TranscriptionModel:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def load_audio(self, file_path):
        if not os.path.isfile(file_path) or not file_path.endswith(AUDIO_EXTENSIONS):
            raise ValueError(f"Invalid audio file: {file_path}")
        # Code to load the audio file goes here

    def transcribe_audio(self, audio_data):
        # Code to transcribe the audio file using the OpenAI Whisper API goes here
        # The result should be a transcript in text format

    def manipulate_text(self, text, prompt=None):
        # Code to manipulate the transcript using the OpenAI GPT-4 API goes here
        # The result should be a formatted transcript in text format

    def save_transcript(self, transcript, file_path):
        with open(file_path, 'w') as f:
            f.write(transcript)

