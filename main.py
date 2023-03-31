from controller import TranscriptionController
from view import ViewCLI
import os

def main():
    # Create a new controller instance
    controller = TranscriptionController()

    # Determine whether to use a CLI or GUI view
    use_gui = input("Use GUI view? (y/n)" ).lower() == "y"
    if use_gui:
        print("not implemented yet, so it's CLI or nothing")
        view = ViewCLI(controller)
    else:
        view = ViewCLI(controller)

    while True:
        # Get an audio file from the user
        audio_file = view.get_audio_file()

        # Load the audio file and transcribe the audio
        controller.model.load_audio(audio_file)
        view.transcribing_in_progress()
        transcript = controller.model.transcribe_audio()

        # Show the transcript to the user
        view.show_transcript(transcript)

        # Save the transcript to a file and show the message to the user
        transcript_file = os.path.join("transcripts", os.path.splitext(os.path.basename(audio_file))[0] + ".txt")
        controller.model.save_transcript()
        view.save_transcript(transcript_file)

        # Translate the transcript to a chosen language and show it to the user
        translation_language = view.get_translation_language()
        print(translation_language)
        translation = controller.model.translate_to(translation_language)
        view.show_translated_transcript()

        # Ask the user if they want to manipulate another audio file
        choice = input("Manipulate another audio file? (y/n) ").lower()
        if choice != "y":
            break

if __name__ == "__main__":
    main()

