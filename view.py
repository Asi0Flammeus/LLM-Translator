import argparse

class TranscriptionView:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Transcription MVP')
        self.parser.add_argument('audio_file', type=str, help='Path to audio file')
        self.parser.add_argument('--prompt', type=str, help='Custom prompt for GPT-4')

    def get_user_input(self):
        return self.parser.parse_args()

