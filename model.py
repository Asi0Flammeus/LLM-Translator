import re
import openai
import tiktoken
import requests
import os
from pydub import AudioSegment

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def split_text_into_chunks(text: str, MAX_TOKENS: int = 1000, ENCODING_NAME: str = "cl100k_base") -> list:
    """
    Splits the input text into chunks with a maximum token count.

    Args:
        text (str): The input text to be split.
        MAX_TOKENS (int): The maximum token count for each chunk (default: 1000).
        ENCODING_NAME (str): The encoding name to be used for tokenization (default: "cl100k_base").

    Returns:
        list: The list of chunks.
    """
    # Split the transcript into < 1000 token chunks while preserving sentences/paragraphs
    chunks = []
    sentences = re.split(r'\.\s+', text)  # Split the long string into sentences
    current_chunk = ""

    for sentence in sentences:
        sentence_tokens = num_tokens_from_string(sentence, ENCODING_NAME)

        if sentence_tokens + num_tokens_from_string(current_chunk, ENCODING_NAME) <= MAX_TOKENS:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    # Add the last remaining chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

class TranscriptionModel:
    """
    This class provides functionality to transcribe audio files using OpenAI's Whisper API
    and manipulate the resulting transcript using OpenAI's GPT-3.5 API.
    """

    # Define constants
    MODEL_ENGINE = "gpt-3.5-turbo"
    AUDIO_EXTENSIONS = ('.wav', '.mp3', '.m4a', '.webm', '.mp4', '.mpga', '.mpeg')
    MAX_AUDIO_SIZE_MB = 20  # (a bit smaller than the) Maximum audio size supported by Whisper API in MB
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def __init__(self):
        """
        Initializes the TranscriptionModel instance with the OpenAI API key.
        """
        self.transcript = None
        self.formatted_transcript = []
        self.original_audio_file = []
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
        self.original_audio_file.append(file_path)

        # Check the size of the audio file
        audio_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if audio_size_mb > self.MAX_AUDIO_SIZE_MB:
            # Split the audio file into chunks of MaximumSizeFile MB
            chunk_size_ms = self.MAX_AUDIO_SIZE_MB * 1024 * 1024 * 8 // 1000  # Chunk size in milliseconds

            audio = AudioSegment.from_file(file_path)
            duration_ms = len(audio)
            for i in range(0, duration_ms, chunk_size_ms):
                chunk = audio[i:i + chunk_size_ms]
                chunk_file_path = f"{os.path.splitext(file_path)[0]}_{i // chunk_size_ms}{os.path.splitext(file_path)[1]}"
                chunk.export(chunk_file_path, format=file_path.split('.')[-1])
                self.audio_files.append(chunk_file_path)
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

            # Transcribe the audio file
            file_path = self.audio_files[0]
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

        # Make sure that sub audio files will be deleted
        if len(self.audio_files) > 1:
            sub_audio_file = True

        # Check if a transcript file already exists
        file_path = self.original_audio_file[0]
        transcript_file = f"./outputs/{os.path.splitext(os.path.basename(file_path))[0]}_French_transcript.txt"

        if os.path.exists(transcript_file):
            with open(transcript_file, 'r') as f:
                transcript_text = f.read()
            self.transcript = transcript_text
            print("already there")
            while self.audio_files:
                # Delete the sub audio file
                if sub_audio_file:
                    os.remove(self.audio_files[0])
                self.audio_files.pop(0)
            return transcript_text

        # Transcribe each audio file
        transcript_texts = []
<<<<<<< Updated upstream
=======


>>>>>>> Stashed changes
        while self.audio_files:
            transcript_text = self.transcribe_audio()
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
        audio_file_name = os.path.basename(self.original_audio_file[0])

        # Create the transcripts directory if it does not exist
        transcripts_dir = os.path.join(os.path.dirname("./"), "outputs")
        os.makedirs(transcripts_dir, exist_ok=True)

        # Use the name of the audio file for the transcript file
        transcript_file_path = os.path.join(transcripts_dir, os.path.splitext(audio_file_name)[0] + "_French_transcript.txt")

        # Write the transcript text to a file
        with open(transcript_file_path, "w", encoding="utf-8") as f:
            f.write(self.transcript)

        self.transcript_files.append(transcript_file_path)


    def manipulate_text(self, prompt):
        """
        Manipulates the transcript text using OpenAI's GPT-3.5 API.

        Args:
            prompt (str, optional): The prompt to use for text manipulation. Defaults to None.

        Returns:
            str: The formatted transcript in text format.
        """

        # Use the OpenAI GPT-3.5 API to manipulate the transcript
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
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
        audio_file_name = os.path.basename(self.original_audio_file[0])

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
        Translates the transcript to the specified language using OpenAI's API.

        Args:
            language (str): The language code for the target language (e.g., "en", "de", "es", "it", "fr", "pt").
        """

        # Check if a transcript file already exists
        file_path = self.original_audio_file[0]
        transcript_file = f"./outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{language}_transcript.txt"
        if os.path.exists(transcript_file):
            print("already there")
            return

        # Split the transcript into < 1000 token chunks while preserving sentences/paragraphs
        chunks = split_text_into_chunks(self.transcript)

        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            prompt = f"translate the following transcript into {language}, ensuring all sentences are accurately translated in the output because it will be used as substitles. Therefore the output must have the same structure has the original transcript: '{chunk}'"
            translated_chunk = self.manipulate_text(prompt)
            translated_chunks.append(translated_chunk)

        # Merge all translated output into a single string
        translated_transcript = "\n".join(translated_chunks)

        # Save the result in a txt file
        suffix = f"{language}_transcript"
        self.save_manipulated_text(translated_transcript, suffix)


    def write_synthetic_lecture(self, language):
        """
        Writes a synthetic lecture that would be based on the transcript text in a markdown format.
        Uses the GPT-3.5 API to generate essential points from the transcript, create an outline,
        and then elaborate the outline into a full lecture.

        Args:
            language (str): The language code for the language in which the lecture is to be written.

        Returns:
            str: The transcript formatted into a synthetic lecture.
        """

        # Load the transcript from the output folder
        audio_file_name = os.path.basename(self.original_audio_file[0])
        transcript_file_path = os.path.join("./outputs", os.path.splitext(audio_file_name)[0] + f"_{language}_transcript.txt")

        with open(transcript_file_path, 'r', encoding='utf-8') as f:
            input_transcript = f.read()

        # Create multiple chunks of the transcript
        chunks = split_text_into_chunks(input_transcript)

        # Extract essential points from each chunk
        essential_points = []
        for chunk in chunks:
            prompt = f"Extract the essential points from the following transcript. It will later used for writing a lecture. You must writre in {language} and be hyper conscice: '{chunk}'"
            essential_point = self.manipulate_text(prompt)
            print(essential_point)
            essential_points.append(essential_point)

        # Join the essential points into a single string
        essential_points_string = " ".join(essential_points)

        # Create an outline from the essential points
        prompt = f"Based on the given key points, enumerate an outline for a lecture divided into three sections, no introduction nor conclusion. The outline should be written in {language}: '{essential_points_string}'"
        outline = self.manipulate_text(prompt)
        print("outline:")
        print(outline)

        # Split the outline into parts
        parts = [line for line in outline.splitlines() if line.strip() != '']
        print(len(parts))
        # For each part, use GPT-3.5 to generate a section of the lecture
        lecture_parts = []
        for i, part in enumerate(outline.split("\n")):
            prompt = f"Craft a succinct, reader-friendly course in '{language}'. You must use Markdown syntax and begin with the section heading. Focus on the following section '{part[i]}'. You will only choose the most relevant points from these key points: '{essential_points_string}'"
            lecture_part = self.manipulate_text(prompt)
            print(part[i],":")
            print(lecture_part)
            lecture_parts.append(lecture_part)

        # Join the lecture parts into a single string and save it as a markdown file
        lecture = '\n'.join(lecture_parts)
        suffix = f"{language}_lecture"
        self.save_manipulated_text(lecture, suffix)

        return lecture

