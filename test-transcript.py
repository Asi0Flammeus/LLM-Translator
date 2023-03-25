import os
from model import TranscriptionModel

def main():
    model = TranscriptionModel()
    audio_file = "./audio/output.mp3"
    transcript_file = f"./transcripts/{os.path.splitext(os.path.basename(audio_file))[0]}.txt"

    model.load_audio(audio_file)
    transcript = model.transcribe_audio()
    model.save_transcript()

    formatted_transcript = model.manipulate_text(prompt=input("Enter a prompt: "))
    model.save_manipulated(suffix=input("Enter a suffix for the formatted transcript file name: "))

if __name__ == "__main__":
    main()

