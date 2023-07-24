from model import TranslationModel
from view import ViewCLI
import os
import time

class TranscriptionController:
    def __init__(self):
        self.model = TranslationModel()
        self.view = ViewCLI(self)
        self.translation_languages = ["English",  "German", "Spanish", "Italian", "Portuguese"]
        self.code_languages = ["en",  "de", "es", "it", "pt"]

    def run(self):
        self.translate_a_folder_full_of_text_files()

    def translate_a_folder_full_of_text_files(self):
        # ask which folder to process
        text_folder = self.view.get_text_folder()
        extension = 'md'
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
                translated_text = self.model.translate_to(text, file_path, lang)
                self.model.save_file(translated_text, file_path, lang, extension)
                self.view.work_done(f'Translating in {lang}')

                end_time = time.time()
                processing_times.append(end_time - start_time)

                if idx > 0:
                    avg_time = sum(processing_times) / len(processing_times)
                    remaining_translations = total_translations - (idx + 1)
                    remaining_time = avg_time * remaining_translations
                    self.view.estimated_time_remaining(remaining_time)

                idx += 1
