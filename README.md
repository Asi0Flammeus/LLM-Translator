# LLM-Translator

LLM-Translator is a comprehensive tool designed to transcribe audio files utilizing OpenAI's Whisper API and subsequently manipulate the generated transcript through OpenAI's GPT-3.5 API. Additionally, the project offers the capability to translate the transcript into various languages utilizing GPT-3.5.

## Prerequisites

Before utilizing this tool, ensure the installation of:

- Python 3.7 or higher
- OpenAI Python library (`openai`)
- An OpenAI [API key](https://beta.openai.com/docs/api-reference/introduction).

## Installation and Configuration

LLM-Translator has been successfully tested on Ubuntu 20.04, with planned compatibility for MacOS and Windows.

To install and configure the project, follow these steps:

1. **Clone the Repository**:
   - `git clone https://github.com/Asi0Flammeus/LLM-Translator.git`
2. **Navigate to the Directory**:
   - `cd LLM-Translator/`
3. **Create a `.env` File with OpenAI API Key**:
   - `vim .env`
   - Add the line:
      - `OPENAI_API_KEY="YOUR_API_KEY"`
4. **Install Required Libraries**:
   - `pip install -r requirements.txt`
5. **Create an Input Folder for Texts**:
   - `mkdir text/`
6. **Place Text Files to Translate in the Input Folder**:
   - (`.txt` and `.md` files must be within a subfolder in `LLM-Translator/text/`)
7. **Execute the Program**:
   - `python3 main.py`
8. **Follow On-screen Instructions**:
   - Select folders to translate in English, German, Italian, Spanish, French, and Portuguese.

**Note**: Translations will be stored in the `outputs` folder.

## Roadmap

- [ ] Comprehensive Testing and Continuous Integration
- [ ] Improved Output Organization
- [ ] Enhanced Language Selection and Translation Features
- [ ] Integration with ChatGPT-4 Model
- [ ] Development of a User-Friendly GUI
- [ ] Integration with Additional LLM Models

## Contributing

Contributions are welcome. To contribute, please fork the repository and create a pull request with your changes. Ensure that changes are tested and existing functionality is maintained.

Tips are accepted via LN through this [link](https://getalby.com/p/asi0).

## License

This project is governed by the MIT License. For more information, refer to the [LICENSE file](./license.md).
