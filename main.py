import os
import speech_recognition as sr
import webbrowser
import pyttsx3  # to convert text to speech.
import musicLibrary
import requests
from dotenv import load_dotenv
import pygame
from gtts import gTTS
def configure():
    load_dotenv()



recognizer = sr.Recognizer()  # to recognise what we say
engine = pyttsx3.init()

# Note: For making it bigger, integrate OPENAI into it. You'll need to buy OPENAI subscription.
# Note: also try to use Google's tts service, its also paid service after some time.
def speak(text):  # speaker 1
    engine.say(text)
    engine.runAndWait()

def speak_new(text):  # speaker 2
    tts = gTTS(text)
    tts.save("reply.mp3")

    # Initialize Pygame
    pygame.init()

    # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('reply.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running to allow the music to play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("reply.mp3")

# To carry out the commands said by us
def process_command(c):
    if "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/feed/")
    elif c.lower().startswith("play"):  # only those songs which are stored in musicLibrary file
        # We'll always say "play [song name]". song name starts from the 5th index in that command.
        song = str(c.lower())[5:]
        musicURL = musicLibrary.music[song]
        webbrowser.open(musicURL)
    elif "news" in c.lower():
        configure()
        res = sr.Recognizer()
        while True:
            speak("Sure thing master! Tell me...Which country do you want the news from? America or India")
            try:
                with sr.Microphone() as src:
                    aud = res.listen(src, timeout=3, phrase_time_limit=2)
                    com = res.recognize_google(aud)
                    if "america" in com.lower():
                        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={os.getenv('NEWS_API')}")
                        break
                    elif "india" in com.lower():
                        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={os.getenv('NEWS_API')}")
                        break
            except Exception as e:
                continue

        if response.status_code == 200:
            # Parse the JSON response into a Python dictionary
            data = response.json()

            # extract the articles
            articles = data.get('articles', [])

            # speak the headlines
            print(f"1. Next --> next news\n"
                  f"2. Stop --> Stop news broadcasting")
            for article in articles:
                speak_new(article['title'])
                speak_new("Do you want me to stop or read to the next one")
                try:
                    with sr.Microphone() as src:
                        au = res.listen(src, timeout=3, phrase_time_limit=2)
                        co = res.recognize_google(au)
                        if "next" in co.lower():
                            continue
                        elif "stop" in co.lower():
                            speak_new("End of News Broadcasting!")
                            break
                except Exception as e:   # if audio not received, tell user to choose an option again.
                    continue

        else:
            print("Error")



# MAIN Program tu run the Assistant.

if __name__ == "__main__":
    speak("Booting RAMAKANT....")
    while True:
        # Listen for the wake-word JARVIS
        # obtain audio from the microphone

        print("recognizing...")
        # recognize speech using Google
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
                # timeout --> wait this seconds before giving up and throwing wait timeout error
                # phrase_time_limit --> listen for the audio for this many seconds and return whatever received till then before time limit.
            wakeWord = r.recognize_google(audio)
            if wakeWord.lower() == "ramakant":
                speak("Yes Master!")
                # Listen for command
                with sr.Microphone() as source:
                    print("Waiting for your command")
                    audio = r.listen(source, timeout=4, phrase_time_limit=3)
                    command = r.recognize_google(audio)
                    print(command)
                    if "sleep" in command.lower():
                        speak("See you soon Master! Ramakant... OUT!....")
                        break
                    process_command(command)

        except Exception as e:
            print("Error; {0}".format(e))

