import os
import json
from model import OpenaiTranslationModel

class Language:
    def __init__(self, name, code, translation_prompt):
        self.name = name
        self.code = code
        self.translation_prompt = translation_prompt

class SupportedLanguages:
    def __init__(self):
        self.origin_language = None
        self.languages = []
        self.load_language_prompts()
        self.update_prompts_if_needed()

    def load_language_prompts(self):
        languages_info = [
            {"name": "English", "code": "en"},
            {"name": "German", "code": "de"},
            {"name": "Spanish", "code": "es"},
            {"name": "Italian", "code": "it"},
            {"name": "Portuguese", "code": "pt"},
            {"name": "French", "code": "fr"},
            {"name": "Swedish", "code": "sv"},
            {"name": "Arabic", "code": "ar"},
            {"name": "Japanese", "code": "ja"}
        ]

        for lang_info in languages_info:
            prompt = self.read_prompt_from_file(lang_info["code"])
            self.languages.append(Language(lang_info["name"], lang_info["code"], prompt))

    def read_prompt_from_file(self, language_code):
        file_path = os.path.join('supported_languages', f'{language_code}.json')
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data.get("prompt", "")
        except FileNotFoundError:
            with open(file_path, 'w') as file:
                json.dump({"prompt": ""}, file, indent=4)
            return ""

    def set_origin_language_to(self, origin_language):
        self.origin_language = origin_language

    def get_translation_prompt_for_destination(self, destination_language):
        for language in self.languages:
            if language.name == destination_language:
                return language.translation_prompt

    def update_prompts_if_needed(self):
        current_english_prompt = self.read_prompt_from_file("en")

        with open('./supported_languages/english_prompt_last_version.txt', 'r') as file:
            stored_prompt = file.read().strip()

        if current_english_prompt != stored_prompt:
            print("Updating the prompt translation ...")
            model = OpenaiTranslationModel(stored_prompt, [])
            total_languages = len(self.languages)
            for index, language in enumerate(self.languages):
                # Check if the language is English
                if language.code == "en":
                    language.prompt = stored_prompt
                else:
                    prompt = f"You are a professional translator and your task is to precisely translate this text in {language.name}:\n\n {stored_prompt}"
                    translated_prompt = model.get_response_from_OpenAI_API_with(prompt)
                    language.prompt = translated_prompt

                file_path = os.path.join('supported_languages', f'{language.code}.json')
                with open(file_path, 'w') as json_file:
                    json.dump({"prompt": language.prompt}, json_file, ensure_ascii=False, indent=4)

                # Update and print the progress bar
                progress = (index + 1) / total_languages
                bar_length = 20  # Adjust the length of the progress bar
                bar = '[' + '=' * int(progress * bar_length) + '>' + ' ' * (bar_length - int(progress * bar_length) - 1) + ']'
                print(f'\r{bar} {int(progress * 100)}%', end='')
            print("\nUpdate complete.\n")

