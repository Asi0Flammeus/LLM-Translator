import os

class ViewCLI():
    def __init__(self, controller):
        self.controller = controller

    def get_audio_folder(self):
        root_dir = "./audio/" # or specify your root directory if different
        folders = [f.path for f in os.scandir(root_dir) if f.is_dir()]

        print()
        print("Select a folder to process:")
        for i, folder in enumerate(folders):
            print(f"{i+1}. {folder}")

        choice = int(input("Enter the number of the folder: "))
        audio_folder = folders[choice-1]

        return audio_folder

    def update_progress_bar(self, current, total, description=''):
        progress = current / total * 100
        print(f'{description} Progress: [{current}/{total}] {progress:.2f}%')

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

    def estimated_time_remaining(self, seconds_remaining):
        m, s = divmod(seconds_remaining, 60)
        h, m = divmod(m, 60)
        print(f'Estimated time remaining: {int(h)} hours, {int(m)} minutes, and {int(s)} seconds')

