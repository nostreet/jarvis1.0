import calendar

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia  # for wikipedia search
import smtplib  # for email sending
import webbrowser  # for chrome search

engine = pyttsx3.init()

"""VOICE"""
voices = engine.getProperty('voices')  # getting details of current voice
engine.setProperty('voice', voices[7].id)  # changing index, changes voices. 1 for female


# Enables jarvis to speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Gives back current time
def time():
    time_current = datetime.datetime.now().strftime("%I:%Mpm")
    speak("The current time is")
    speak(time_current)


# Gives today's date
def date():
    # year = str(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = str(datetime.datetime.now().day)
    speak("Todays date is: ")
    speak(date)
    speak(calendar.month_name[month])  # for the full name


# Jarvis initial greeting depending on the time of the day
def greeting():
    hour = datetime.datetime.now().hour
    if 6 < hour < 12:
        speak("Good morning sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir!")
    elif 12 <= hour < 18:
        speak("Good evening sir!")
    else:
        speak("Good night sir!")


# Followup of Jarvis for next command
def wishme():
    greeting()
    speak("Jarvis at your service. Please tell me how can I help you?")


# Function for taking in next users voice command
def takeCommand():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening...")
        speak("I'm listening.")

        # after starting prog it will wait for one sec until listening to our commands
        recognizer.pause_threshold = 1

        # phrase time limit set when there is background noise, not tested if listening
        # process works without background noise
        # audio = recognizer.listen(source, phrase_time_limit=5)   #microphone is source
        audio = recognizer.listen(source)  # microphone is source

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(query)
    except Exception as e:
        print(e)
        speak("Sorry, say that again please.")
        return "None"

    return query


# Connects to webmail server and sends out email
def sendEmail(to, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('email@gmail.com', 'xYZ')
    server.sendmail('fromemail@gmail.com', to, message)
    server.close()


# Searching input 'query' directly on wikipedia
def wiki(query):
    speak("Searching..")
    query = query.replace("wikipedia", "")
    result = wikipedia.summary(query, sentences=2)
    print(result)
    speak(result)


if __name__ == "__main__":
    #Jarvis asking for input
    wishme()

    # until 'quit' command from user
    while True:
        query = takeCommand().lower()

        # if the word time is in the query, start time funtion
        if 'time' in query:
            time()
        elif 'date' in query:
            date()
        elif "wikipedia" in query:
            wiki(query)
        elif "send email" in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = 'info@thebaughmansbees.co.nz'
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Unable to send the email")

        elif 'search in chrome' in query:
            speak("What should I search")
            chromepath = '/Applications/Google Chrome.app %s'
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search + '.com')

        elif 'offline' in query:
            quit()
