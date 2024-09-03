# Das - Personal Voice Assistant

Das is a personal voice assistant built using Python. It can recognize and respond to voice commands, perform various tasks such as opening applications, playing songs on YouTube, fetching the current time, and searching the internet. Das can also learn new phrases and responses, making it more interactive and useful over time.

## Features

- **Voice Recognition**: Uses Google Speech Recognition to interpret spoken commands.
- **Text-to-Speech**: Uses `gTTS` to convert text responses into speech.
- **Open Applications**: Can open Notepad and Command Prompt.
- **Play Music**: Plays songs on YouTube using `pywhatkit`.
- **Fetch IP Address**: Retrieves the current IP address using an API.
- **Tell Time**: Provides the current time.
- **Wikipedia Search**: Fetches summaries from Wikipedia.
- **Web Search**: Opens a web browser and searches for user queries.
- **Learn New Phrases**: Can learn new phrases and responses, stored in a JSON file.
- **Get News**: Fetches the latest news headlines.
- **Get Stock Price**: Provides the current stock price for a given company.

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/sivaprasanth2221/AI-Voice-Assistant-using-Python-macos.git
    cd AI-Voice-Assistant-using-Python-macos
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Dependencies

- `pyttsx3`
- `speechrecognition`
- `requests`
- `pywhatkit`
- `wikipedia`
- `scikit-learn`
- `pyjokes`
- `translate`
- `pillow`
- `gtts`
- `openai`
- `pyaudio`
- `smtplib`
- `datetime`
- `tkinter`
- `json`
- `webbrowser`
- `pandas` (if required for data manipulation)
- `yfinance` (for fetching stock data)

## Install these dependencies using pip:
```sh
pip install pyttsx3 speechrecognition requests pywhatkit wikipedia scikit-learn pyjokes translate pillow gtts openai pyaudio pandas yfinance
```

## Usage
**Run the Assistant**:
    ```sh
    python gui.py
    ```
**Use Voice Commands**:

 - "Play music" to play songs.
 - "Send email" to compose and send an email.
 - "Set reminder" to set a reminder.
 - "Get weather" to fetch the weather information.
 - "Tell me a joke" to hear a joke.
 - "Get IP" to get your IP address.
 - "Translate" to translate text to another language.
 - "Get news" to fetch the latest news headlines.
 - "Get stock price" to fetch the current stock price of a company.

**Note**: This project works on macOS.