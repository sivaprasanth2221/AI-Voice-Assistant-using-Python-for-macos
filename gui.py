import os
import tkinter as tk
from tkinter import messagebox
from gtts import gTTS
import requests
import speech_recognition as sr
import datetime
from requests import get
import pyjokes
import smtplib
from email.mime.text import MIMEText
from translate import Translator
import time
from PIL import Image, ImageTk
import json
import webbrowser
import wikipedia
import openai

openai.api_key = "your_openai_api_key"

brain_file = "Brain.json"
try:
    with open(brain_file, "r") as file:
        brain_data = json.load(file)
except FileNotFoundError:
    brain_data = {}

# Save to Brain.json
def save_to_brain():
    with open(brain_file, "w") as file:
        json.dump(brain_data, file, indent=4)

# Initialize GUI
root = tk.Tk()
root.title("Advanced AI Voice Assistant")
root.geometry("700x600")
root.configure(bg="#2c3e50")

# Load and set the icon
try:
    icon_image = Image.open("assistant_icon.png")  # Replace with your icon file path
    icon = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False, icon)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load icon: {e}")

# Styling for the greeting label
greeting_label = tk.Label(root, text="AI Voice Assistant", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
greeting_label.pack(pady=20)

# Display output in a text box without scroll bar
output_text = tk.Text(root, wrap=tk.WORD, width=80, height=20, font=("Helvetica", 14), bg="#34495e", fg="#ecf0f1", borderwidth=2, relief="groove")
output_text.pack(pady=20, padx=20)

# Function to print text letter by letter
def type_text(text, delay=0.05):
    output_text.delete(1.0, tk.END)  # Clear previous text
    for char in text:
        output_text.insert(tk.END, char)
        output_text.update()
        time.sleep(delay)
    output_text.insert(tk.END, "\n\n")  # Ensure space after completing the text

# Speak function
def speak(audio):
    type_text(f"Assistant: {audio}\n\n")
    os.system(f'say -r 185 "{audio}"')  # macOS-specific command


# Function to handle voice recognition with GPT integration
def recognize():
    reco = sr.Recognizer()
    with sr.Microphone() as source:
        type_text("Listening...\n\n")
        reco.pause_threshold = 1
        try:
            audio = reco.listen(source, timeout=5, phrase_time_limit=5)
            query = reco.recognize_google(audio, language='en-in').lower()
            output_text.insert(tk.END, f"You: {query}\n\n")  # Display user input with spacing

            # Use GPT for more complex understanding and response
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Respond to this query as an intelligent assistant: {query}",
                max_tokens=150
            )

            gpt_response = response.choices[0].text.strip()
            speak(gpt_response)
            return gpt_response

        except sr.UnknownValueError:
            speak("Sorry, I did not understand. Can you please repeat?")
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
        except Exception as e:
            speak(f"Sorry, something went wrong. {e}")
        return 'none'

# Wishing function
def wish():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Das, your personal Assistant. How can I assist you today?")

# Weather Information
def get_weather():
    api_key = 'a6c2ac70c7249be4d5364b3cc9e41229'
    location = 'madurai'  # Replace with your location
    try:
        response = get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}')
        data = response.json()
        if data['cod'] == 200:
            weather_description = data['weather'][0]['description']
            temp = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
            speak(f'The weather in {location} is {weather_description} with a temperature of {temp:.2f}°C')
        else:
            speak('Sorry, I could not fetch the weather information.')
    except Exception as e:
        speak(f'Sorry, I could not fetch the weather information. {e}')

# Set Reminders
def set_reminder():
    speak('What should I remind you about?')
    reminder = recognize()
    if reminder == 'none':
        speak('No reminder set.')
        return
    speak('When should I remind you? Please specify the time in minutes.')
    try:
        minutes = int(recognize())
        if minutes == 'none':
            speak('No time specified.')
            return
        speak(f'Reminder set for {minutes} minutes. I will notify you then.')
        time.sleep(minutes * 60)
        speak(f'Reminder: {reminder}')
    except ValueError:
        speak('Invalid time format.')

# Send an email
def send_email():
    speak('Please provide the recipient email address.')
    recipient = recognize()
    if recipient == 'none':
        speak('No recipient specified.')
        return

    speak('What is the subject of the email?')
    subject = recognize()
    if subject == 'none':
        speak('No subject specified.')
        return

    speak('What is the body of the email?')
    body = recognize()
    if body == 'none':
        speak('No body specified.')
        return

    sender = 'sivabhuvan20_bai25@mepcoeng.ac.in'
    password = 'Sivamalar2221'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
            speak('Email sent successfully.')
    except Exception as e:
        speak(f'Sorry, I could not send the email. Error: {e}')

# Function to speak text in a specific language
def speak_text_in_language(text, lang):
    lang_code = {
        'english': 'en',
        'french': 'fr',
        'spanish': 'es',
        'german': 'de',
        'japanese': 'ja',
        'chinese': 'zh',
        'korean': 'ko',
        'russian': 'ru'
    }.get(lang.lower(), 'en')  # Default to English if language not supported

    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save("temp.mp3")
        os.system("afplay temp.mp3")  # macOS command to play audio files
    except ValueError as e:
        speak(f'Sorry, the language you selected is not supported. {e}')

# Translate text
def translate_text():
    speak('Which language do you want to translate to?')
    target_language = recognize()
    if target_language == 'none':
        speak('No language specified.')
        return

    speak('What text do you want to translate?')
    text = recognize()
    if text == 'none':
        speak('No text provided.')
        return

    translator = Translator(to_lang=target_language)
    try:
        translation = translator.translate(text)
        speak(f'Translated text: {translation}')

        # Speak the translated text in the target language
        speak_text_in_language(translation, target_language)
    except Exception as e:
        speak(f'Sorry, I could not translate the text. Error: {e}')

# Play local music
def play_music():
    speak('Which music file would you like to play?')
    file_name = recognize()
    if file_name == 'none':
        speak('No file specified.')
        return

    try:
        os.system(f'afplay "{file_name}"')  # macOS command to play audio files
    except Exception as e:
        speak(f'Sorry, I could not play the music. Error: {e}')

# Tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Simple calculator
def calculator():
    speak('Please tell me the arithmetic operation you want to perform.')
    operation = recognize()
    if operation == 'none':
        speak('No operation specified.')
        return

    try:
        result = eval(operation)
        speak(f'The result of {operation} is {result}')
    except Exception as e:
        speak(f'Sorry, I could not perform the calculation. Error: {e}')

# Open web browser with specific URL
def open_website():
    speak('Which website would you like to open?')
    website = recognize()
    if website == 'none':
        speak('No website specified.')
        return

    try:
        webbrowser.open(f'https://{website}')
        speak(f'Opening {website}')
    except Exception as e:
        speak(f'Sorry, I could not open the website. Error: {e}')

# Wikipedia Search
def search_wikipedia():
    speak('What do you want to search on Wikipedia?')
    query = recognize()
    if query == 'none':
        speak('No query provided.')
        return

    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f'There are multiple results for {query}. Please be more specific.')
    except wikipedia.exceptions.PageError:
        speak(f'Sorry, I could not find a page for {query}.')
    except Exception as e:
        speak(f'Sorry, something went wrong. {e}')

def get_news():
    api_key = '5290942623304f37b8ae6d4f22c81a76'  # Replace with your News API key
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
    try:
        response = requests.get(url)
        news_data = response.json()
        headlines = [article['title'] for article in news_data['articles'][:5]]
        speak("Here are the top headlines:")
        for i, headline in enumerate(headlines, 1):
            speak(f"{i}. {headline}")
    except Exception as e:
        speak(f'Sorry, I could not fetch the news. Error: {e}')
        
def get_stock_price():
    speak('Please tell me the stock symbol.')
    symbol = recognize()
    if symbol == 'none':
        speak('No symbol provided.')
        return

    try:
        stock_price = get(f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey=your_api_key').json()[0]['price']
        speak(f'The current price of {symbol} is {stock_price} USD')
    except Exception as e:
        speak(f'Sorry, I could not fetch the stock price. Error: {e}')

# Clear the output
def clear_output():
    output_text.delete(1.0, tk.END)

# Execute the assistant commands
def execute_assistant():
    query = recognize()

    if 'weather' in query:
        get_weather()
    elif 'reminder' in query:
        set_reminder()
    elif 'email' in query:
        send_email()
    elif 'translate' in query:
        translate_text()
    elif 'joke' in query:
        tell_joke()
    elif 'music' in query:
        play_music()
    elif 'website' in query:
        open_website()
    elif 'wikipedia' in query:
        search_wikipedia()
    elif 'news' in query:
        get_news()
    elif 'stock' in query:
        get_stock_price()
    else:
        # Let GPT handle more complex or unrecognized commands
        speak("Let me think...")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Respond intelligently to this command: {query}",
            max_tokens=150
        )
        speak(response.choices[0].text.strip())

# Start the assistant with the wish function
wish()

# Button to start listening
listen_button = tk.Button(root, text="Listen", command=execute_assistant, font=("Helvetica", 16, "bold"), bg="#2980b9", fg="#ecf0f1", activebackground="#3498db", activeforeground="#ecf0f1")
listen_button.pack(pady=20)

# Run the GUI loop
root.mainloop()