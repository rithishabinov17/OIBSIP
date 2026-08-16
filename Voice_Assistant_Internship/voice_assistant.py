import subprocess
import speech_recognition as sr
import webbrowser
import datetime
import os
import urllib.parse
import re

def speak(text):
    command = f'''
    Add-Type -AssemblyName System.Speech
    $voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $voice.Speak("{text}")
    '''

    subprocess.run([
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        "-Command",
        command
    ])

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()

    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return ""

    except sr.WaitTimeoutError:
        print("No speech detected.")
        return ""

def calculate(command):
    expression = command.replace("calculate", "").strip()

    expression = expression.replace("plus", "+")
    expression = expression.replace("minus", "-")
    expression = expression.replace("multiply", "*")
    expression = expression.replace("multiplied by", "*")
    expression = expression.replace("divide", "/")
    expression = expression.replace("divided by", "/")

    if re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        try:
            result = eval(expression)
            print("Result:", result)
            speak("The answer is " + str(result))
        except:
            speak("Sorry, I could not calculate that.")
    else:
        speak("Please give me a valid calculation.")

print("Voice Assistant Started")

speak("Hello, I am your voice assistant")

while True:
    try:
        command = listen()

        if not command:
            continue

        if "hello" in command or "hi" in command:
            speak("Hello! How can I help you?")

        elif "how are you" in command:
            speak("I am fine. How can I help you?")

        elif "what is your name" in command:
            speak("My name is your voice assistant.")

        elif "open google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "search google" in command:
            search_text = command.replace("search google", "").strip()

            if search_text:
                speak("Searching Google.")
                url = "https://www.google.com/search?q=" + urllib.parse.quote(search_text)
                webbrowser.open(url)
            else:
                speak("What should I search for?")

        elif "search youtube" in command:
            search_text = command.replace("search youtube", "").strip()

            if search_text:
                speak("Searching YouTube.")
                url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(search_text)
                webbrowser.open(url)
            else:
                speak("What should I search for?")

        elif "what time is it" in command or "current time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            print("Current Time:", current_time)
            speak("The current time is " + current_time)

        elif "what is the date" in command or "today's date" in command:
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            print("Today's Date:", current_date)
            speak("Today's date is " + current_date)

        elif "calculate" in command:
            calculate(command)

        elif "open notepad" in command:
            speak("Opening Notepad.")
            os.system("notepad.exe")

        elif "open calculator" in command:
            speak("Opening Calculator.")
            os.system("calc.exe")

        elif "open file explorer" in command or "open explorer" in command:
            speak("Opening File Explorer.")
            os.system("explorer.exe")

        elif "open vs code" in command or "open visual studio code" in command:
            speak("Opening Visual Studio Code.")
            os.system("code")

        elif "exit" in command or "stop" in command or "goodbye" in command:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("Sorry, I don't understand that command.")

    except Exception as e:
        print("Error:", e)
