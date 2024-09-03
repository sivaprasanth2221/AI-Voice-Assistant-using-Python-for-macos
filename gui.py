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

def save_to_brain():
    with open(brain_file, "w") as file:
        json.dump(brain_data, file, indent=4)

root = tk.Tk()
root.title("Advanced AI Voice Assistant")
root.geometry("700x600")
root.configure(bg="#2c3e50")

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
            return query

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
    api_key = 'your_weather_api_key'
    location = 'your_location'  # Replace with your location
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

    sender = 'sender_mail_id'
    password = 'sender_mail_id_password'

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

# Get IP address
def get_ip():
    try:
        ip_address = get('https://api64.ipify.org').text
        speak(f'Your IP address is {ip_address}')
    except Exception as e:
        speak(f'Sorry, I could not retrieve your IP address. {e}')
        
def get_news():
    api_key = 'your_news_api_key'  # Replace with your News API key
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
    api_key = 'your_stock_api_key'
    try:
        stock_price = get(f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}').json()[0]['price']
        speak(f'The current price of {symbol} is {stock_price} USD')
    except Exception as e:
        speak(f'Sorry, I could not fetch the stock price. Error: {e}')

# Exit assistant
def exit_assistant():
    speak("Goodbye, have a great day!")
    root.quit()

# Button command function to handle various commands
def execute_assistant(command=None):
    if not command:
        command = recognize()
    if 'play music' in command:
        play_music()
    elif 'send email' in command:
        send_email()
    elif 'set reminder' in command:
        set_reminder()
    elif 'get weather' in command:
        get_weather()
    elif 'get news' in command:
        get_news()
    elif 'get stock price' in command:
        get_stock_price()
    elif 'tell me a joke' in command:
        tell_joke()
    elif 'get ip' in command:
        get_ip()
    elif 'translate' in command:
        translate_text()
    elif 'exit' in command:
        exit_assistant()
    else:
        speak("I'm sorry, I didn't understand that command.")

# Voice Input Button
voice_input_button = tk.Button(root, text="Speak", command=lambda: execute_assistant(), font=("Helvetica", 16), bg="#3498db", fg="#ecf0f1")
voice_input_button.pack(pady=20)

# Start the assistant
wish()

# Run the GUI loop
root.mainloop()
