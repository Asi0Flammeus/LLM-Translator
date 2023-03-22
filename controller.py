from model import TranscriptionModel
from view import TranscriptionView

class TranscriptionController:
    def __init__(self, model, view, args):
        self.model = model
        self.view = view
        self.audio_file = args.audio_file
        self.prompt = args.prompt

    def run(self):
        # Load the audio file
        audio_data = self.model.load_audio(self.audio_file)

        # Transcribe the audio file
        transcript = self.model.transcribe_audio(audio_data)

        # Manipulate the transcript
        formatted_transcript = self.model.manipulate_text(transcript, self.prompt)

        # Save the formatted transcript
        output_file = f"{os.path.splitext(self.audio_file)[0]}.txt"
        self.model.save_transcript(formatted_transcript, output_file)

if __name__ == '__main__':
    # Create the model, view, and controller objects
    model = TranscriptionModel()
    view = TranscriptionView()
    args = view.get_user_input()
    controller = TranscriptionController(model, view, args)

    # Run the controller
    controller.run()

