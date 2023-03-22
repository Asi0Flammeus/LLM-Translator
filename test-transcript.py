import openai

open.api_key_path = "./api_key.txt"

audio_file= open("./audio/output.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript)
