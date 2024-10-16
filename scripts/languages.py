import json
import os

from model import OpenaiTranslationModel


script_directory = os.path.dirname(os.path.abspath(__file__))
supported_languages_directory = os.path.join(os.path.dirname(script_directory), "supported_languages")

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
            {"name": "Romanian", "code": "ro"},
            {"name": "Swedish", "code": "sv"},
            {"name": "Arabic", "code": "ar"},
            {"name": "Japanese", "code": "ja"},
            {"name": "Swahili", "code": "sw"},
            {"name": "Afrikaans", "code": "af"},
            {"name": "Greek", "code": "el"},
            {"name": "Georgian", "code": "ka"},
            {"name": "Turkish", "code": "tr"},
            {"name": "Thai", "code": "th"},
            {"name": "Danish", "code": "da"},
            {"name": "Ukranian", "code": "uk"},
            {"name": "Finnish", "code": "fi"},
            {"name": "Farsi", "code": "fa"},
            {"name": "Hungarian", "code": "hu"},
            {"name": "Vietnamese", "code": "vi"},
            {"name": "Wolof", "code": "wo"},
            {"name": "Russian", "code": "ru"},
            {"name": "Korean", "code": "ko"},
            {"name": "Czech", "code": "cs"},
            {"name": "Hebrew", "code": "hb"},
            {"name": "Norwegian Bokmål", "code": "nb-NO"},
            {"name": "Polish", "code": "pl"},
            {"name": "Latvian", "code": "lv"},
            {"name": "Estonian", "code": "et"},
            {"name": "Indonesian", "code": "id"},
            {"name": "Simplified chinese", "code": "zh-Hans"},
            {"name": "Traditional chinese", "code": "zh-Hant"},
            
        ]

        for lang_info in languages_info:
            prompt = self.read_prompt_from_file(lang_info["code"])
            self.languages.append(
                Language(lang_info["name"], lang_info["code"], prompt)
            )

    def read_prompt_from_file(self, language_code):
        file_path = os.path.join(supported_languages_directory, f"{language_code}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("prompt", "")
        except FileNotFoundError:
            with open(file_path, "w", encoding="utf-8") as file:
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
        template_file_path = os.path.join(supported_languages_directory, "prompt_template.txt")
        with open(
            template_file_path, "r", encoding="utf-8"
        ) as file:
            stored_prompt = file.read().strip()

        # Case 1: If the English version has changed
        if current_english_prompt != stored_prompt:
            print("Updating prompt for supported languages ...\n")
            self.update_all_prompts(stored_prompt)

        # Case 2: If any language's prompt is empty
        elif any(language.translation_prompt == "" for language in self.languages):
            print("Updating prompt for new supported languages ...\n")
            self.update_all_prompts(stored_prompt, update_empty_only=True)

    def update_all_prompts(self, stored_prompt, update_empty_only=False):
        model = OpenaiTranslationModel(stored_prompt, [])

        if update_empty_only:
            total_languages = sum(
                1 for language in self.languages if language.translation_prompt == ""
            )
        else:
            total_languages = len(self.languages)

        INDEX = 0

        for language in self.languages:
            # Skip updating non-empty prompts if update_empty_only is True
            if update_empty_only and language.translation_prompt != "":
                continue

            if language.code == "en":
                language.translation_prompt = stored_prompt
            else:
                prompt = f"You are a professional translator and your task is to precisely translate this text in {language.name}:\n\n {stored_prompt}"
                translated_prompt = model.get_response_from_OpenAI_API_with(prompt)
                language.translation_prompt = translated_prompt

            file_path = os.path.join(supported_languages_directory, f"{language.code}.json")
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(
                    {"prompt": language.translation_prompt},
                    json_file,
                    ensure_ascii=False,
                    indent=4,
                )

            # Update and print the progress bar
            progress = (INDEX + 1) / total_languages
            INDEX += 1
            bar_length = 20
            bar = (
                "["
                + "=" * int(progress * bar_length)
                + ">"
                + " " * (bar_length - int(progress * bar_length) - 1)
                + "]"
            )
            print(f"\r{bar} {int(progress * 100)}%", end="")
        print("\nUpdate complete.\n")
