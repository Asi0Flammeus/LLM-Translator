from controller import TranscriptionController
import os

def main():
    # Create a new controller instance
    controller = TranscriptionController()

    # Get a list of audio files in the audio directory
    audio_dir = "./audio"
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3") or f.endswith(".wav")]

    # Prompt the user to choose an audio file
    print("Select an audio file to transcribe:")
    for i, f in enumerate(audio_files):
        print(f"{i+1}. {f}")

    # Get the user's choice
    choice = int(input("Enter the number of the audio file: "))
    audio_file = os.path.join(audio_dir, audio_files[choice-1])

    # Load the audio file and transcribe the audio
    controller.model.load_audio(audio_file)
    transcript = controller.model.transcribe_audio()
    print("Transcript generated:")
    print(transcript)

    # Save the transcript to a file
    transcript_file = os.path.join("transcripts", os.path.splitext(os.path.basename(audio_file))[0] + ".txt")
    controller.model.save_transcript()
    print(f"Transcript saved to {transcript_file}")

    # Translate the transcript to a chosen language
    controller.translate_transcript()

if __name__ == "__main__":
    main()

