# LLM-Translator

LLM-Translator is a simple CLI tool to translate any `.txt` and `.md` files of any length in the supported languages by leveraging ChatGPT's API. 

## Supported Languages 

Texts and documents are translated into the Modern Standard version of the following languages:
- [X] English
- [X] German
- [X] Spanish
- [X] Italian
- [X] Portuguese
- [X] French
- [X] Swedish
- [X] Arabic
- [X] Japanese
- [X] Swahili
- [X] Hausa
- [X] Afrikaans

You can manually add new languages by modifying `language_info` in `languages.py`.
You can also change the prompt template by modifying `supported_languages/prompt_template.txt`. 
Once modified, the program will automatically update the prompt of every supported languages.


## Installation and Setup 

### Prerequisites

Before utilizing this tool, ensure that you have an OpenAI account and an OpenAI [API key](https://beta.openai.com/docs/api-reference/introduction) and to follow the installation procedure. 
#### Installation for Linux Users

LLM-Translator has been successfully tested on Ubuntu 20.04. 

0. **Open a Terminal** 
1. **Check that Python 3 and git are installed**
   - `python3 --version` 
   - most of the time they are installed by default, if not install them with:
    - `sudo apt install python3 python3-pip python3-env git`
2. **Clone the Repository**  
   - `git clone https://github.com/Asi0Flammeus/LLM-Translator.git`

3. **Navigate to the Project Directory**:  
   - `cd LLM-Translator/`

4. **Set Up OpenAI API Key**:  
   - Create a `.env` file.
    - `nano .env` 
    - press `Ctrl+X` and then `y` and `Enter` to quit nano and save file. 
   - Add the following line, replacing `"YOUR_API_KEY"` with your actual OpenAI API key (go [here](https://platform.openai.com/account/api-keys) for futher details).
    - `OPENAI_API_KEY="YOUR_API_KEY"`

4. **Create a Python Virtual Environment**:  
   - `python3 -m venv env`

5. **Activate the Virtual Environment**:  
   - `source env/bin/activate`

6. **Install Required Libraries**:  
   - `pip3 install -r requirements.txt`


#### Installation for Windows Users

LLM-Translator has been successfully tested on Windows 11. 

By default, Python 3 and git are not already installed on Windows so I will also explain how to install them. If you already have those installed you can directly jump to step 4. 

1. **Download [Python](https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe) on official website** 
  - Execute the installer wizard, `python-3.11.5-amd64.exe` for example.
    - ⚠️  Beware to tick the `Add python.exe to PATH` option on the first installation page before cliking the `Install Now` button.
    - Follow the installation procedure and choose default settings.

2. **Download [GitBash](https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe) on official website**
  - Execute the wizard installer, `git-2.42.0.2-64-bit.exe` for example.
  - Follow the installation procedure and choose default settings.
3. **Open Git Bash**

4. **Clone the Repository**  
   - `git clone https://github.com/Asi0Flammeus/LLM-Translator.git`

5. **Navigate to the Project Directory**:  
   - `cd LLM-Translator/`

6. **Set Up OpenAI API Key**:  
   - Create a `.env` file.
    - `nano .env` 
   - Add the following line, replacing `"YOUR_API_KEY"` with your actual OpenAI API key (go [here](https://platform.openai.com/account/api-keys) for futher details).
    - `OPENAI_API_KEY="YOUR_API_KEY"`
    - Press `Ctrl+X` and then `y` and `Enter` to quit nano and save file. 

4. **Create a Python Virtual Environment**:  
   - `python -m venv env`

5. **Activate the Virtual Environment**:  
   - `source env/Scripts/activate`

6. **Install Required Libraries**:  
   - `pip install -r requirements.txt`

## LLM-Translator Usage

Please follow these steps *each time* you want to run LLM-Translator:

0. **Open a terminal (or Gitbash for windows users)**
  - Go to LLM-Translator directory
   - `cd LLM-Translator`
  - Update the repository
   - `git pull` 

1. **activate the Python Environment**  
   - `source env/bin/activate` 
   - or `source env/Scripts/activate` for windows users

2. **Prepare Input Files**:  
   - Before running the program, you have to create subfolders inside the `/inputs/` directory and populate them with `.txt` and `.md` files that you wish to translate.
   - All the files in a subfolder should be written in the same language. 

3. **Execute the Program**:  
   - `python3 main.py` for linux users
   - `python main.py` for windows users

4. **Follow the On-screen Instructions** 
   

**Note**: Translations will be automatically stored in an associated subfolder into the `/outputs/` folder. 
**Note 2:** A better installation process will be done soon™ with executable files for windows and linux.

## Roadmap

- [X] Language Selection
- [X] Improved Output Organization
- [ ] Comprehensive Testing and Continuous Integration
- [ ] Integration with ChatGPT-4 Model
- [ ] Development of a User-Friendly GUI
- [ ] Integration with Additional LLM Models

## Contributing

Contributions are welcome. To contribute, please fork the repository and create a pull request with your changes. Ensure that changes are tested and existing functionality is maintained.

Here we promote [*Value for Value*](https://dergigi.com/2021/12/30/the-freedom-of-value/) model so if you find value in this humble script tips are welcomed via [LN](https://getalby.com/p/asi0) or by scanning directly this QR code with a Lightning wallet 👇. 

<img src="./figure/LN-address-asi0-tip.png" width="175">

## License

This project is governed by the MIT License. For more information, refer to the [LICENSE file](./license.md).
