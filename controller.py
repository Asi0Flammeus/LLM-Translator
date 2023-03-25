from model import TranscriptionModel

class TranscriptionController:
    def __init__(self):
        self.model = TranscriptionModel()

    def translate_transcript(self):
        # Prompt the user to choose a language
        print("Select a language to translate the transcript:")
        print("1. English")
        print("2. German")
        print("3. Spanish")
        print("4. Italian")
        print("5. French")
        print("6. Portuguese")

        # Get the user's choice
        choice = int(input("Enter the number of the language: "))

        # Translate the transcript to the chosen language
        if choice == 1:
            language = "en"
        elif choice == 2:
            language = "de"
        elif choice == 3:
            language = "es"
        elif choice == 4:
            language = "it"
        elif choice == 5:
            language = "fr"
        elif choice == 6:
            language = "pt"
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            return

        translated_text = self.model.translate_to(language)
        print(f"Transcript translated to {language}:")
