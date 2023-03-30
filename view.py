import os
class TranscriptionViewCLI:
    def __init__(self, controller):
        self.controller = controller

    def get_audio_file(self):
        audio_dir = "./audio"
        audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3") or f.endswith(".wav")]

        print("Select an audio file to transcribe:")
        for i, f in enumerate(audio_files):
            print(f"{i+1}. {f}")

        choice = int(input("Enter the number of the audio file: "))
        audio_file = os.path.join(audio_dir, audio_files[choice-1])

        return audio_file

    def show_transcript(self, transcript):
        print("Transcript generated:")
        print(transcript)

    def save_transcript(self, transcript_file):
        print(f"Transcript saved to {transcript_file}")

    def get_translation_language(self):
        # Define a dictionary of language codes and names
        language_codes = {
            "en": "English",
            "de": "German",
            "es": "Spanish",
            "it": "Italian",
            "fr": "French",
            "pt": "Portuguese"
        }

        # Print the list of available languages
        print("Select a language to translate the transcript to:")
        for i, (code, name) in enumerate(language_codes.items()):
            print(f"{i+1}. {name} ({code})")

        # Get the user's choice
        choice = int(input("Enter the number of the language: "))
        print(choice)
        # Convert the user's choice to a language code
        language_code = list(language_codes.keys())[choice-1]
        return language_code

    def show_translated_transcript(self):
        print("Translated transcript saved!")

