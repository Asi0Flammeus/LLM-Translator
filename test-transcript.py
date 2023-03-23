from model import TranscriptionModel

def main():
    model = TranscriptionModel()
    audio_file = "./audio/output.mp3"

    model.load_audio(audio_file)
    transcript = model.transcribe_audio()
    model.save_transcript()

if __name__ == "__main__":
    main()

