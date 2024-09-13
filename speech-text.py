import speech_recognition as sr
import pyttsx3
import pronouncing
import sys

r = sr.Recognizer()  # Initialize the recognizer
t = pyttsx3.init()  # Initialize a text to speech engine

#using the microphone directly to record input
def record_text():  # Input
    while True:  # For error handling
        try:
            with sr.Microphone() as source:  # Using the device microphone
                print('Listening...') #to show that it is waiting for the input
                r.adjust_for_ambient_noise(source, duration=0.2)  # Adjust for ambient noise
                audio = r.listen(source)  # Listen to the audio input
                mytext = r.recognize_google(audio)  # Using Google Speech-to-Text API
                print(f'You said: {mytext}')
                return mytext
            
        except sr.RequestError as e:
            print(f'Could not request results: {e}')
        except sr.UnknownValueError:
            print('Unknown error occurred, please repeat.')

def output_text(text):  # Output
    with open('output.txt', 'a') as f:
        f.write(text + '\n')

def speak_text(mytext):
    t.say(mytext)  # Converting text to speech
    t.runAndWait()  # Wait until the speaker is finished
   

#getting the pronunciation using CMU dictionary and phonics
def get_pronunciation(phrase): 
    phonics = pronouncing.phones_for_word(phrase)
    if phonics:
        return phonics[0]  # Return the first pronunciation found
    else:
        return None  # No pronunciation found

def provide_pronunciation_feedback(phrase):
    pronunciation = get_pronunciation(phrase)
    if pronunciation:
        # provide feedback
        phonetic_representation = pronunciation.replace(" ", "-")  # Better display for phonetic representation
        print(f"The word '{phrase}' is pronounced like: {phonetic_representation}")

#function to stop the program from running
def confirm_exit():
    print('Do you really want to stop? (yes/no)')
    response = input().strip().lower()
    return response == 'yes'

while True:
    text = record_text()

#loop to stop the code if the user is done using it
    if text.lower() == 'stop':
        if confirm_exit():
            break
        else:
            print('Continuing...')

    print(f"Said Text: {text}")
    output_text(text)
    print('Text written')
    speak_text(text)

    words = text.split()
    for phrase in words:
        provide_pronunciation_feedback(phrase)
