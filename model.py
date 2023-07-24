import os
import re
import time
import requests
import openai
import tiktoken
from dotenv import load_dotenv
from openai.error import RateLimitError, Timeout, APIError

def count_token_length(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    TOKEN_LENGTH = len(encoding.encode(string))
    return TOKEN_LENGTH

def split_text_in_chunks(text: str, MAX_TOKENS: int = 1000, encoding_NAME: str = "cl100k_base") -> list:

    """
    Description:
        Splits the input text in chunks that are less than MAX_TOKENS.
        The orginal layout is preserved.

    Args:
        text (str): The input text to be split.
        MAX_TOKENS (int): The maximum token count for each chunk (default: 1000).
        encoding_NAME (str): The encoding name to be used for tokenization (default: "cl100k_base").

    Returns:
        list: The list of the spliting chunks of the original text.
    """

    chunks = []
    current_chunk = ""
    paragraphs = text.splitlines()
    for paragraph in paragraphs:
        PARAGRAPH_TOKENS = count_token_length(paragraph, encoding_NAME)
        CHUNK_TOKENS = count_token_length(current_chunk, encoding_NAME)
        if PARAGRAPH_TOKENS + CHUNK_TOKENS <= MAX_TOKENS:
            current_chunk += paragraph + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

class TranslationModel:
    """
    This class provides functionality to translate audio files using an Large Language Model (LLM)
    like ones provided by OpenAI API or LLaMa lib.
    """

    # Load environment variables from .env file
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    TEXT_EXTENSIONS = ('.txt', '.md')

    def __init__(self):
        """
        Initializes the TranscriptionModel instance with the OpenAI API key.
        """
        self.transcript = None
        self.original_audio_file = []
        self.audio_files = []
        self.model_engine = "gpt-3.5-turbo"

    def save_file(self, text: str, file_path:str, suffix: str, extension: str):
        """
        Save a text to the output folder with a specific suffix.

        Args:
            text (str): The text to be saved.
            suffix (str): The suffix to use for the saved text file name.
        """

        file_name = os.path.basename(file_path)

        destination = os.path.join(os.path.dirname("./"), "outputs")
        os.makedirs(destination, exist_ok=True)

        file_path = os.path.join(destination, os.path.splitext(file_name)[0] + f"_{suffix}.{extension}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

    def manipulate_text(self, prompt, temperature):
        """
        Manipulates the transcript text using OpenAI's GPT API.

        Args:
            prompt (str, optional): The prompt to use for text manipulation. Defaults to None.

        Returns:
            str: The formatted transcript in text format.
        """

        # Use the OpenAI GPT API to manipulate the transcript
        response = openai.ChatCompletion.create(
            model = self.model_engine,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        formatted_transcript = content = response['choices'][0]['message']['content']
        self.formatted_transcript = formatted_transcript

        return formatted_transcript


    def translate_to(self, text:str, file_path:str, language:str):
        """
        Translates any text to the specified language using an LLM.

        Args:
            text (str): the text to be translated
            put which define the nature of text
            language (str): The language code for the target language (e.g., "en", "de", "es", "it", "fr", "pt").

        Returns:
            translated_text (str): the translated text in the corresponding language.
        """

        # Check if a transcript file already exists
        text_file = f"./outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{language}.md"
        if os.path.exists(text_file):
            print("already there")
            with open(text_file, 'r', encoding='utf-8') as f:
                translated_text = f.read()
            return translated_text

        # Split the text into chunks of less than MAX_TOKENS length
        chunks = split_text_in_chunks(text, MAX_TOKENS=750)

        # Translate each chunk
        translated_chunks = []
        NUM_CHUNKS = len(chunks)  # Get total number of chunks before starting loop
        for i, chunk in enumerate(chunks):
            prompt = f"translate the following text into {language}. Do not translate path links. The output must have the same markdown layout has the original text:\n '{chunk}'"
            temperature = 0.1
            while True:
                try:
                    translated_chunk = self.manipulate_text(prompt, temperature)
                    translated_chunks.append(translated_chunk)
                    print(f'Progress: {(((i+1)/NUM_CHUNKS)*100):.2f}% of chunks translated.')
                    break
                except RateLimitError as e:
                    print("Rate limit error occurred. Retrying in 5 seconds...")
                    time.sleep(5)
                except Timeout as e:
                    print("Timeout error occurred. Retrying in 5 seconds...")
                    time.sleep(5)
                except APIError as e:
                    print("API error occurred. Retrying in 5 seconds...")
                    time.sleep(5)
        # Merge all translated output into a single string
        translated_text = "\n".join(translated_chunks)

        return translated_text

