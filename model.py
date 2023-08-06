import os
import time
import openai
import tiktoken
from dotenv import load_dotenv
from openai.error import RateLimitError, Timeout, APIError, ServiceUnavailableError

class OpenaiTranslationModel:
    """
    This class provide the methods for using a LLM specifically for translation.
    """
    def __init__(self, text_to_translate):
        self.text_to_translate = TextToTranslate(text_to_translate)

        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model_engine = "gpt-3.5-turbo"
        self.error_handler = APIErrorHandler()

        self.prompt = ""
        self.temperature = 0.1

    def get_translated_text_in(self, language):
        self.update_prompt_to(language)
        translated_chunks = []
        NUM_CHUNKS = len(self.text_to_translate.chunks)
        for i, chunk in enumerate(self.text_to_translate.chunks):
            translated_chunk = self.translate_a_single(chunk)
            translated_chunks.append(translated_chunk)
            print(f'Progress: {(((i+1)/NUM_CHUNKS)*100):.2f}% of chunks translated.')
        translated_text = "\n".join(translated_chunks)
        return translated_text

    def update_prompt_to(self, language):

        self.prompt = (f"translate the following text into {language}.\
                        Do not translate path links. \
                        The output must have the same markdown layout has the original text:\n")

    def translate_a_single(self, chunk):
        try:
            current_prompt = self.prompt + chunk
            return self.get_response_from_OpenAI_API_with(current_prompt)
        except Exception as e:
            self.error_handler.handle_error(e)
            return self.translate_a_single(chunk)

    def get_response_from_OpenAI_API_with(self, current_prompt):
        response = openai.ChatCompletion.create(
            model = self.model_engine,
            messages=[
                {"role": "user", "content": current_prompt}
            ],
            temperature=self.temperature
        )
        return response['choices'][0]['message']['content']


class TextToTranslate():
    def __init__(self, text_to_translate):
        self.text_to_translate = text_to_translate
        self.chunks = []
        self.current_chunk = ""
        self.encoding_name = "cl100k_base"
        self.MAX_TOKENS = 750

        self.create_chunks()

    def create_chunks(self):
        paragraphs = self.text_to_translate.splitlines()
        for paragraph in paragraphs:
            if self.can_add_another(paragraph):
                self.current_chunk += paragraph + "\n"
            else:
                self.chunks.append(self.current_chunk.strip())
                self.current_chunk = paragraph
        if self.current_chunk:
           self.chunks.append(self.current_chunk.strip())

    def can_add_another(self, paragraph):
        CHUNK_TOKENS = self.count_the_token_length_of(self.current_chunk)
        PARAGRAPH_TOKENS = self.count_the_token_length_of(paragraph)
        return CHUNK_TOKENS + PARAGRAPH_TOKENS <= self.MAX_TOKENS

    def count_the_token_length_of(self, string):
        encoding = tiktoken.get_encoding(self.encoding_name)
        NUM_TOKENS = len(encoding.encode(string))
        return NUM_TOKENS


class APIErrorHandler:
    def __init__(self):
        self.error_handlers = {
            RateLimitError: "Rate limit",
            Timeout: "Timeout",
            APIError: "API error",
            ServiceUnavailableError: "Service Unavailable",
        }
        self.sleep_time = 5

    def handle_error(self, error):
        error_type = type(error)
        handler = self.error_handlers.get(error_type, f"An unknown error {error} occurred.")
        error_message = handler()
        print(f"An {error_message} error occured. Retry in {self.sleep_time} seconds...")
        time.sleep(self.sleep_time)

