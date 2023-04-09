import openai
import requests
import os

class TranscriptionModel:
    """
    This class provides functionality to transcribe audio files using OpenAI's Whisper API
    and manipulate the resulting transcript using OpenAI's GPT-3.5 API.
    """

    # Define constants
    MODEL_ENGINE = "gpt-3.5-turbo"
    AUDIO_EXTENSIONS = ('.wav', '.mp3')
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def __init__(self):
        """
        Initializes the TranscriptionModel instance with the OpenAI API key.
        """
        self.transcript = None
        self.formatted_transcript = []
        self.audio_files = []
        self.transcript_files = []

    # Define constants
    MODEL_ENGINE = "gpt-3.5-turbo"
    AUDIO_EXTENSIONS = ('.wav', '.mp3')
    MAX_AUDIO_SIZE_MB = 20  # (a bit smaller than the) Maximum audio size supported by Whisper API in MB
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def __init__(self):
        """
        Initializes the TranscriptionModel instance with the OpenAI API key.
        """
        self.transcript = None
        self.formatted_transcript = []
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

        # Check the size of the audio file
        audio_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if audio_size_mb > self.MAX_AUDIO_SIZE_MB:
            # Split the audio file into chunks of MaximumSizeFile MB
            chunk_size_mb = self.MAX_AUDIO_SIZE_MB
            with open(file_path, "rb") as f:
                chunk = f.read(chunk_size_mb * 1024 * 1024)
                i = 0
                while chunk:
                    chunk_file_path = f"{os.path.splitext(file_path)[0]}_{i}{os.path.splitext(file_path)[1]}"
                    print(chunk_file_path)
                    with open(chunk_file_path, "wb") as chunk_file:
                        chunk_file.write(chunk)
                    self.audio_files.append(chunk_file_path)
                    i += 1
                    chunk = f.read(chunk_size_mb * 1024 * 1024)
        else:
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

            # Check if a transcript file already exists
            transcript_file = f"./outputs/{os.path.splitext(os.path.basename(file_path))[0]}_VO_transcript.txt"
            if os.path.exists(transcript_file):
                with open(transcript_file, 'r') as f:
                    transcript_text = f.read()
                self.transcript = transcript_text
                print("already there")
                return transcript_text

            # Transcribe the audio file
            audio_file = open(file_path, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            audio_file.close()

            # Extract the transcript text
            transcript_text = transcript["text"]

            return transcript_text

    def transcribe_multiple_chunks_audio(self):
        """
        Transcribes all the audio chunks into a single transcript

        Returns:
            str: The transcript of the audio data in text format.
        """
        if not self.audio_files:
            raise ValueError("No audio files have been loaded.")

        # Transcribe each audio file
        transcript_texts = []
        while self.audio_files:
            transcript_text = transcribe_audio
            transcript_texts.append(transcript_text)
            self.audio_files.pop(0)

        # Concatenate the transcript texts into a single string
        self.transcript = " ".join(transcript_texts)

        return self.transcript

    def save_transcript(self):
        """
        Saves the transcript to a file at the specified file path.

        Args:
            file_path (str): The path where the transcript file should be saved.
        """
        if not self.transcript:
            raise ValueError("No transcript has been generated.")

        # Get the name of the audio file
        audio_file_name = os.path.basename(self.audio_files[0])

        # Create the transcripts directory if it does not exist
        transcripts_dir = os.path.join(os.path.dirname("./"), "outputs")
        os.makedirs(transcripts_dir, exist_ok=True)

        # Use the name of the audio file for the transcript file
        transcript_file_path = os.path.join(transcripts_dir, os.path.splitext(audio_file_name)[0] + "_VO_transcript.txt")

        # Write the transcript text to a file
        with open(transcript_file_path, "w", encoding="utf-8") as f:
            f.write(self.transcript)

        self.transcript_files.append(transcript_file_path)


    def manipulate_text(self, prompt=None):
        """
        Manipulates the transcript text using OpenAI's GPT-3.5 API.

        Args:
            prompt (str, optional): The prompt to use for text manipulation. Defaults to None.

        Returns:
            str: The formatted transcript in text format.
        """
        if not self.transcript:
            raise ValueError("No transcript has been generated.")

        # Use the OpenAI GPT-3.5 API to manipulate the transcript
        prompt = prompt or "Format the following transcript:\n\n"
        prompt += f"{self.transcript}"

        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        formatted_transcript = content = response['choices'][0]['message']['content']
        self.formatted_transcript = formatted_transcript

        return formatted_transcript


    def save_manipulated_text(self, text, suffix):
        """
        Manipulates the transcript text using OpenAI's GPT-4 API and saves the resulting formatted transcript to a file.

        Args:
            suffix (str): The suffix to use for the saved transcript file name.
        """
        # Manipulate the transcript text
        formatted_transcript = text

        # Get the name of the audio file
        audio_file_name = os.path.basename(self.audio_files[0])

        # Create the transcripts directory if it does not exist
        transcripts_dir = os.path.join(os.path.dirname("./"), "outputs")
        os.makedirs(transcripts_dir, exist_ok=True)

        # Use the name of the audio file and the given suffix for the transcript file
        transcript_file_path = os.path.join(transcripts_dir, os.path.splitext(audio_file_name)[0] + f"_{suffix}.txt")

        # Write the formatted transcript text to a file
        with open(transcript_file_path, "w", encoding="utf-8") as f:
            f.write(formatted_transcript)

        self.transcript_files.append(transcript_file_path)


    def translate_to(self, language):
        """
        Translates the transcript to the specified language using OpenAI's GPT-4 API.

        Args:
            language (str): The language code for the target language (e.g., "en", "de", "es", "it", "fr", "pt").

        Returns:
            str: The translated transcript in text format.
        """

        prompt=f"Translate the following transcript to {language}:\n\n"
        suffix=f"{language}_transcript_translation"
        self.save_manipulated_text(self.manipulate_text(prompt),suffix)

    def write_synthetic_lecture(self):
        """
        writes a synthetic lecture that would be based on the transcript text in a markdown format.

        Returns:
            str: The transcript formatted into a synthetic lecture.
        """

        prompt=f"Reformulate the following transcript into a synthetic and structured lecture in markdown format:"
        suffix=f"cours_academic_FR"
        self.save_manipulated_text(self.manipulate_text(prompt),suffix)
