import whisper
import requests
import os

class TranscriptionModel:
    """
    This class provides functionality to transcribe audio files using OpenAI's Whisper API and manipulate the resulting transcript using OpenAI's GPT-4 API.
    """

    # Define constants
    OPENAI_API_KEY = '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'
    MODEL_ENGINE = 'text-davinci-002'
    AUDIO_EXTENSIONS = ('.wav', '.mp3')

    def __init__(self):
        """
        Initializes the TranscriptionModel instance with the OpenAI API key.
        """
        self.headers = {'Authorization': f'Bearer {self.OPENAI_API_KEY}'}
        self.transcript = None
        self.formatted_transcript = None
        self.audio_files = []
        self.transcript_files = []

    def load_audio(self, file_path):
        """
        Loads an audio file from the specified file path.

        Args:
            file_path (str): The path to the audio file.

        Raises:
            ValueError: If the file path is not valid or does not have a valid audio file extension.
        """
        if not os.path.isfile(file_path) or not file_path.endswith(self.AUDIO_EXTENSIONS):
            raise ValueError(f"Invalid audio file: {file_path}")

        self.audio_files.append(file_path)

    def transcribe_audio(self):
        """
        Transcribes the audio data using OpenAI's Whisper API.

        Returns:
            str: The transcript of the audio data in text format.
        """
        if not self.audio_files:
            raise ValueError("No audio files have been loaded.")

        file_path = self.audio_files[0]
        file_type = os.path.splitext(file_path)[1].lstrip('.')
        url = "https://transcribe.whisperapi.com"
        data = {
            "fileType": file_type,
            "language": "auto",
            "task": "transcribe"
        }
        files = {'file': open(file_path, 'rb')}

        response = requests.post(url, headers=self.headers, files=files, data=data)
        response.raise_for_status()

        transcript = response.json()['text']
        self.transcript = transcript

        return transcript

    def manipulate_text(self, prompt=None):
        """
        Manipulates the transcript text using OpenAI's GPT-4 API.

        Args:
            prompt (str, optional): The prompt to use for text manipulation. Defaults to None.

        Returns:
            str: The formatted transcript in text format.
        """
        if not self.transcript:
            raise ValueError("No transcript has been generated.")

        # Use the OpenAI GPT-4 API to manipulate the transcript
        prompt = prompt or "Format the following transcript:\n\n"
        prompt += f"{self.transcript}\n\nFormatted transcript:"

        response = openai.Completion.create(
            engine=self.MODEL_ENGINE,
            prompt=prompt,
            max_tokens=2048,
            temperature=0.5
        )

        formatted_transcript = response.choices[0].text.strip()
        self.formatted_transcript = formatted_transcript

        return formatted_transcript

    def save_transcript(self, file_path):
        """
        Saves the transcript to a file at the specified file path.

        Args:
            file_path (str): The path where the transcript file should be saved.
        """
        if not self.formatted_transcript:
            raise ValueError("No formatted transcript has been generated.")

        with open(file_path, 'w') as f:
            f.write(self.formatted_transcript)

        self.transcript_files.append(file_path)

