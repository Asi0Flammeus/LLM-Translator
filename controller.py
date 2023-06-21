from model import TranscriptionModel
from view import ViewCLI
import os
import time

class TranscriptionController:
    def __init__(self):
        self.model = TranscriptionModel()
        self.view = ViewCLI(self)
        self.translation_languages = ["English",  "German", "Spanish", "Italian", "Portuguese"]
        self.code_languages = ["en",  "de", "es", "it", "pt"]

    def run(self):
        choice = input("Enter 1 to transcribe audio files, 2 to translate texts or 3 to make a lecture of audio files: ")

        if choice == "1":
            self.transcribing_a_folder_full_of_audio_file()
        elif choice == "2":
            self.translate_a_folder_full_of_text_files()
        elif choice == "3":
            self.make_lecture_of_audio_files()
        else:
            print("Invalid choice. Please enter either 1, 2 or 3.")


    def translate_a_folder_full_of_text_files(self):
        # ask which folder to process
        text_folder = self.view.get_text_folder()
        md_files = [f for f in os.listdir(text_folder) if f.endswith(".md")]
        total_translations = len(md_files)*len(self.translation_languages)
        processing_times = []
        idx = 0

        for md_file in md_files:
            start_time = time.time()
            file_path = os.path.join(text_folder, md_file)
            with open(file_path, 'r', encoding="utf-8") as f:
                text = f.read()

            # translate the text file in all languages
            for lang in self.translation_languages:
                self.view.update_progress_bar(idx, total_translations, 'Translations')
                self.view.work_in_progress(f'Translating in {lang}')
                translated_text = self.model.simple_translate_to(text, file_path, '', lang)
                self.model.save_md(translated_text, file_path, lang)
                self.view.work_done(f'Translating in {lang}')

                end_time = time.time()
                processing_times.append(end_time - start_time)

                if idx > 0:
                    avg_time = sum(processing_times) / len(processing_times)
                    remaining_translations = total_translations - (idx + 1)
                    remaining_time = avg_time * remaining_translations
                    self.view.estimated_time_remaining(remaining_time)

                idx += 1

    def transcribing_a_folder_full_of_audio_file(self):
        # ask which folder to process
        audio_folder = self.view.get_audio_folder()
        mp3_files = [f for f in os.listdir(audio_folder) if f.endswith(".mp3")]
        total_files = len(mp3_files)
        processing_times = []

        for idx, mp3_file in enumerate(mp3_files):
            start_time = time.time()
            self.view.update_progress_bar(idx+1, total_files, 'Files')
            file_path = os.path.join(audio_folder, mp3_file)

            # transcribe audio
            transcript = self.load_and_transcribe_audio(file_path)

    def make_lecture_of_audio_files(self):
        # ask which folder to process
        audio_folder = self.view.get_audio_folder()
        mp3_files = [f for f in os.listdir(audio_folder) if f.endswith(".mp3")]
        total_files = len(mp3_files)
        processing_times = []

        for idx, mp3_file in enumerate(mp3_files):
            start_time = time.time()
            self.view.update_progress_bar(idx+1, total_files, 'Files')
            file_path = os.path.join(audio_folder, mp3_file)

            # transcribe audio
            transcript = self.load_and_transcribe_audio(file_path)

            # create lecture in French and translate it
            self.create_and_translate_lecture('French')

            end_time = time.time()
            processing_times.append(end_time - start_time)

            if idx > 0:
                avg_time = sum(processing_times) / len(processing_times)
                remaining_files = total_files - (idx + 1)
                remaining_time = avg_time * remaining_files
                self.view.estimated_time_remaining(remaining_time)

    def load_and_transcribe_audio(self, audio_file):
        self.model.load_audio(audio_file)
        self.view.work_in_progress('Transcribing audio')
        transcript = self.model.transcribe_multiple_chunks_audio()
        self.view.work_done('Transcribing audio')

        return transcript

    def translate_and_save_transcript(self, transcript, language):
        self.view.work_in_progress(f'Translating transcript to {language}')
        translation = self.model.translate_to(transcript, 'transcript', language)
        self.view.work_done(f'Translating transcript to {language}')
        #self.view.show_translated_transcript(translation)

    def create_and_translate_lecture(self, language):
        self.view.work_in_progress(f'Creating lecture in {language}')
        lecture = self.model.write_synthetic_lecture(language)
        self.view.work_done(f'Creating lecture in {language}')
        #for lang in self.translation_languages:
        #    self.view.work_in_progress(f'Creating lecture in {lang}')
        #    translated_lecture = self.model.translate_to(lecture, 'lecture', lang)
        #    self.view.work_done(f'Creating lecture in {lang}')
            #self.view.show_translated_lecture(translated_lecture)

