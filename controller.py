from model import TranscriptionModel
from view import ViewCLI
import os

class TranscriptionController:
    def __init__(self):
        self.model = TranscriptionModel()
        self.view = ViewCLI(self)

    def run(self):
        while True:
            audio_file = self.view.get_audio_file()
            self.load_and_transcribe_audio(audio_file)
            translation_language = self.view.get_translation_language()
            self.translate_and_show_transcript(translation_language)

            if not self.view.ask_continue():
                break

    def load_and_transcribe_audio(self, audio_file):
        self.model.load_audio(audio_file)
        self.view.work_in_progress()
        transcript = self.model.transcribe_multiple_chunks_audio()
        self.view.show_transcript(transcript)
        transcript_file = os.path.join("transcripts", os.path.splitext(os.path.basename(audio_file))[0] + ".txt")
        self.model.save_transcript()
        self.view.save_transcript(transcript_file)

    def translate_and_show_transcript(self, language):
        self.view.work_in_progress()
        translation = self.model.translate_to(language)
        self.view.show_translated_transcript()

