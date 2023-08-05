import os

class ViewCLI():
    def __init__(self, supported_languages):
        self.supported_languages = supported_languages

    def get_languages(self):
        print()
        print("Select languages for translation:")
        for i, language in enumerate(self.supported_languages):
            print(f"{i+1}. {language}")

        while True:
            choices_input = input("Enter the numbers of the languages, separated by commas: ")
            if self.validate_language(choices_input):
                choices = [int(choice) for choice in choices_input.split(",")]
                break

        selected_languages = [self.supported_languages[int(choice)-1] for choice in choices]
        return selected_languages

    def validate_language(self, choices_input):
        try:
            choices = [int(choice) for choice in choices_input.split(",")]
            if all(1 <= choice <= len(self.supported_languages) for choice in choices):
                return True
            else:
                print("Invalid choice. Please enter numbers corresponding to the languages. \n")
                return False
        except ValueError:
            print("Invalid input format. \n")
            return False

    def get_folder_to_translate_path(self):
        root_dir = "./text/"
        folders = [f.path for f in os.scandir(root_dir) if f.is_dir()]

        print()
        print("Select a folder to translate:")
        for i, folder in enumerate(folders):
            print(f"{i+1}. {folder}")

        choice = int(input("Enter the number of the folder: "))
        folder_path = folders[choice-1]

        return folder_path

    def update_progress_bar(self, current, total):
        progress = current / total * 100
        print(f'Translations in Progress: [{current}/{total}] {progress:.2f}%')

    def work_in_progress(self, task):
        print()
        print(f"{task}...")

    def work_done(self, task):
        print()
        print(f"{task} done!")

    def show_translated_transcript(self, translated_transcript):
        print()
        print(f"Translated transcript: {translated_transcript}")

    def show_translated_lecture(self, translated_lecture):
        print()
        print(f"Translated lecture: {translated_lecture}")

    def estimated_remaining_time(self, seconds_remaining):
        m, s = divmod(seconds_remaining, 60)
        h, m = divmod(m, 60)
        print(f'Estimated time remaining: {int(h)} hours, {int(m)} minutes, and {int(s)} seconds')

    def user_request_stop(self):
        response = input("Do you want another batch translation? (y/n): ")
        return response.lower() == "n"
