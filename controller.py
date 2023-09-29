from model import OpenaiTranslationModel
from languages import SupportedLanguages
from view import ViewCLI
import os
import time

class Controller():
    def __init__(self):
        self.supported_languages_instance = SupportedLanguages()

        self.supported_languages = [language.name for language in self.supported_languages_instance.languages]
        self.code_languages = [language.code for language in self.supported_languages_instance.languages]

        self.view = ViewCLI(self.supported_languages)
        self.translation_languages = self.view.get_languages()
        self.origin_language = self.view.get_origin_language()
        self.supported_languages_instance.set_origin_language_to(self.origin_language)

        self.extensions = ['md', 'txt']
        self.folder_to_translate_path = self.view.get_folder_to_translate_path()
        self.input_subfolder_name = os.path.basename(self.folder_to_translate_path)
        self.text_to_translate_names = [f for f in os.listdir(self.folder_to_translate_path) if any(f.endswith(ext) for ext in self.extensions)]

        self.text_to_translate_path = ""
        self.text_to_translate = ""

        self.translated_text = ""
        self.translated_text_path = ""

        self.NUM_TRANSLATIONS = len(self.text_to_translate_names)*len(self.translation_languages)
        self.start_time = time.time()
        self.processing_times = []
        self.index = 0

        self.model = None # A model is instanciated for each translated text

    def translate_the_folder(self):

        for text_to_translate_name in self.text_to_translate_names:
            self.text_to_translate_path = os.path.join(self.folder_to_translate_path, text_to_translate_name)
            self.load_text_to_translate()
            self.load_translation_model()
            self.batch_translate_the_text()


    def load_text_to_translate(self):
        with open(self.text_to_translate_path, 'r', encoding="utf-8") as f:
            self.text_to_translate = f.read()


    def load_translation_model(self):
        self.model = OpenaiTranslationModel(self.text_to_translate, self.supported_languages_instance)


    def batch_translate_the_text(self):
        for destination_language in self.translation_languages:

            self.view.update_progress_bar(self.index, self.NUM_TRANSLATIONS)
            self.view.work_in_progress(f'Translating in {destination_language}')

            self.create_translated_text_path_for(destination_language)
            if not self.check_existence_of_translated_text():
                self.translated_text = self.model.get_translated_text_from_to(self.origin_language, destination_language)
                self.save_translated_text()

            self.view.work_done(f'Translating in {destination_language}')
            self.update_processing_times()
            self.estimate_remaining_time()

    def create_translated_text_path_for(self, destination_language):
        extension = self.get_file_extension()
        self.translated_text_path = f"./outputs/{self.input_subfolder_name}/{os.path.splitext(os.path.basename(self.text_to_translate_path))[0]}_{destination_language}.{extension}"

    def get_file_extension(self):
        return os.path.splitext(self.text_to_translate_path)[1][1:]

    def check_existence_of_translated_text(self):
        return os.path.exists(self.translated_text_path)

    def save_translated_text(self):
        self.create_destination_if_needed()
        with open(self.translated_text_path, "w", encoding="utf-8") as f:
            f.write(self.translated_text)

    def create_destination_if_needed(self):
        destination = f"./outputs/{self.input_subfolder_name}"
        os.makedirs(destination, exist_ok=True)

    def update_processing_times(self):
        end_time = time.time()
        self.processing_times.append(end_time - self.start_time)


    def estimate_remaining_time(self):
        if self.index > 0:
            average_time = self.get_average_time()
            remaining_translations = self.NUM_TRANSLATIONS - (self.index + 1)
            SECONDS = average_time * remaining_translations
            self.view.estimated_remaining_time(SECONDS)
        self.index += 1

    def get_average_time(self):
        SUM = sum(self.processing_times)
        TOTAL = len(self.processing_times)
        average_time = SUM / TOTAL
        return average_time
