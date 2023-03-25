# Core idea 

Produce a *simple* and *modular* program that takes as input an audio file and gives as output a transcript.
This program can also re-format the transcript to get different elements needed for post-production and for the production of educational content about the academy.

The program performs the blue part of this diagram.

![](./figure/post-production-formation-DB.png)

## High level structure 

The design pattern of the program has to be a Model-View-Controller architecture in order to facilitate the iteration on the program.

Initially the view can be done with the terminal, then from a window. 
Ideally the user, when launching the program, interacts with a window that asks him for an audio file, and then to choose between a prompt or a set of pre-defined outputs.

The model will be based on the use of the OpenAI API to produce the script with Whisper and the different manipulation of this text with GPT4.

The controller will link the different elements of the model to those of the view.

1.  **Model**: Create a `TranscriptionModel` class that will use the OpenAI API to produce the transcript with Whisper and perform the various manipulations of the text with GPT-4. This class should include methods for:
    
    - Load an audio file
    - Transcribe the audio file using the OpenAI Whisper API
    - Manipulate the transcript with the OpenAI GPT-4 API
    - Save the formatted transcript
2.  **View**: Start by creating a command line interface (CLI) to interact with the user. Later, you can replace it with a graphical user interface (GUI). The view should allow the user to:
    
    - Select an audio file
    - Choose between a custom prompt or a set of predefined outputs
3.  **Controller**: Create a `TranscriptionController` class that will act as a link between the model and the view. The controller should include methods for:
    
    - Get information from the user via the view (audio file and output choices)
    - Call the appropriate methods in the model to perform transcription and text manipulation
    - Update the view with the results obtained from the model

# OPENAI-TAO (Transcript And Others) project

This project provides functionality for transcribing audio files using OpenAI's Whisper API and manipulating the resulting transcript using OpenAI's GPT-3.5 API. The project can also translate the transcript into different languages using GPT-3.5.

## Requirements

Before using the project, you must have the following installed:

- Python 3.7 or higher
- The OpenAI Python library (`openai`) - you can install this library using pip: `pip install openai`
- An OpenAI API key - you can obtain an API key from the OpenAI website: https://beta.openai.com/docs/api-reference/introduction

## Usage

To use the project, follow these steps:

1. Clone or download the project code to your local machine.
2. Set your OpenAI API key as an environment variable with the name `OPENAI_API_KEY`.
3. Install the `openai` library using pip: `pip install openai`.
4. Navigate to the project directory in your terminal or command prompt.
5. Run the `view.py` file using Python: `python view.py`.
6. Follow the prompts to choose an audio file, transcribe the audio, save the transcript to a file, and translate the transcript to a chosen language.

Note: The audio files should be located in the `audio` folder of the project directory. The transcripts and translations will be saved to the `outputs` folder.

## Contributing

If you would like to contribute to the project, please fork the repository and create a pull request with your changes. Before submitting a pull request, make sure to test your changes and ensure that they do not break any existing functionality.


You can tip me via LN through this [link](https://getalby.com/p/asi0).

## License

This project is licensed under the MIT License - see the [LICENSE file](./license.md) for details.


