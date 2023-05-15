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

    def save_text(self, text: str, suffix: str):
        """
        Save a text to the output folder with a specific suffix.

        Args:
            text (str): The text to be saved.
            suffix (str): The suffix to use for the saved text file name.
        """

        # Get the name of the audio file
        audio_file_name = os.path.basename(self.original_audio_file[0])

        # Create the output directory if it does not exist
        output_dir = os.path.join(os.path.dirname("./"), "outputs")
        os.makedirs(output_dir, exist_ok=True)

        # Use the name of the audio file and the given suffix for the text file
        file_path = os.path.join(output_dir, os.path.splitext(audio_file_name)[0] + f"_{suffix}.txt")

        # Write the formatted transcript text to a file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

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

        self.transcript = None
        self.formatted_transcript = []
        self.original_audio_file = []
        self.audio_files = []
        self.transcript_files = []

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
        else:
            sub_audio_file = False

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

        while self.audio_files:
            transcript_text = self.transcribe_audio()
            transcript_texts.append(transcript_text)
            # Delete the sub audio file
            if sub_audio_file:
                os.remove(self.audio_files[0])
            self.audio_files.pop(0)

        # Concatenate the transcript texts into a single string
        self.transcript = " ".join(transcript_texts)

        # Save the transcript to the output directory
        self.save_text(self.transcript, "French_transcript")

        return self.transcript

    def manipulate_text(self, prompt, temperature):
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
            temperature=temperature
        )

        formatted_transcript = content = response['choices'][0]['message']['content']
        self.formatted_transcript = formatted_transcript

        return formatted_transcript



    def translate_to(self, text:str, post_suffix:str, language:str):
        """
        Translates the transcript to the specified language using OpenAI's API.

        Args:
            text (str): the text to be translated
            post_suffix (str): The suffix for the name of the output which define the nature of text
            language (str): The language code for the target language (e.g., "en", "de", "es", "it", "fr", "pt").
        """

        # Check if a transcript file already exists
        file_path = self.original_audio_file[0]
        transcript_file = f"./outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{language}_{post_suffix}.txt"
        if os.path.exists(transcript_file):
            print("already there")
            return

        # Split the text into < 1000 token chunks while preserving sentences/paragraphs
        chunks = split_text_into_chunks(text)

        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            prompt = f"translate the following transcript into {language}, ensuring all sentences are accurately translated in the output because it will be used as substitles. Therefore the output must have the same structure has the original transcript: '{chunk}'"
            temperature = 0.2
            translated_chunk = self.manipulate_text(prompt, temperature)
            translated_chunks.append(translated_chunk)

        # Merge all translated output into a single string
        translated_text = "\n".join(translated_chunks)

        # Save the result in a txt file
        suffix = f"{language}_{post_suffix}"
        self.save_text(translated_text, suffix)


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

        # Check if essential points file already exists
        file_path = self.original_audio_file[0]
        essential_points_file = f"./outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{language}_essential_points.txt"
        if os.path.exists(essential_points_file):
            print("essential points already there")
            with open(essential_points_file, 'r', encoding='utf-8') as f:
                essential_points_string = f.read()
        else:
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
                prompt = f"make a small list of the essential points from the following transcript. It will later used for writing a lecture. You must write in {language} and be hyper conscice: '{chunk}'"
                temperature = 0.8
                essential_point = self.manipulate_text(prompt, temperature)
                essential_points.append(essential_point)

            # Join the essential points into a single string
            essential_points_string = " ".join(essential_points)

            # Save the essential points
            suffix = f"{language}_essential_points"
            self.save_text(essential_points_string, suffix)

        # Check if outline file already exists
        file_path = self.original_audio_file[0]
        outline_file = f"./outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{language}_outline.txt"
        if os.path.exists(outline_file):
            print("outline already there")
            with open(outline_file, 'r', encoding='utf-8') as f:
                outline = f.read()
        else:
            # Create an outline from the essential points
            prompt = f"Based on the given key points, write only the three main sections title for a lecture with no subsection, no introduction nor conclusion. The outline should be written in {language}: '{essential_points_string}'"
            temperature = 0.2
            outline = self.manipulate_text(prompt, temperature)

            # Save the essential points
            suffix = f"{language}_outline"
            self.save_text(outline, suffix)

        # Check if outline file already exists
        file_path = self.original_audio_file[0]
        lecture_file = f"./outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{language}_lecture.txt"
        if os.path.exists(lecture_file):
            print("lecture already there")
            with open(lecture_file, 'r', encoding='utf-8') as f:
                lecture = f.read()
        else:
            prompt = f"Compose a comprehensive lecture in '{language}', adhering strictly to the structural outline: '{outline}'. Each section must stand independently, with zero repetition, and be distinctly specified using markdown syntax. Your discourse should draw inspiration and factual substantiation from the key points furnished in the list: '{essential_points_string}'. Construct your narrative to convey these points effectively."
            temperature = 0.8
            lecture = self.manipulate_text(prompt, temperature)

            # Join the lecture parts into a single string and save it as a markdown file
            suffix = f"{language}_lecture"
            self.save_text(lecture, suffix)

        return lecture

