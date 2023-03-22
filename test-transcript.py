import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
audio_file= open("./audio/output.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
# Extract the transcript text
text = transcript["text"]

# Write the text to a file
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("done!")
