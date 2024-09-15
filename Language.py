import speech_recognition as sr
from gtts import gTTS
import os
import pronouncing

# Initialize the recognizer
r = sr.Recognizer()

def record_text():  # Input via microphone
    while True:  # For error handling
        try:
            with sr.Microphone() as source:  # Using the device microphone
                print('Listening...')  # Waiting for input
                r.adjust_for_ambient_noise(source, duration=0.2)  # Adjust for ambient noise
                audio = r.listen(source)  # Listen to the audio input
                mytext = r.recognize_google(audio)  # Using Google Speech-to-Text API
                print(f'You said: {mytext}')
                return mytext
        except sr.RequestError as e:
            print(f'Could not request results: {e}')
        except sr.UnknownValueError:
            print('Unknown error occurred, please repeat.')

def input_text():  # Input via console
    return input("Please enter text: ")

def output_text(text):  # Output to file
    with open('output.txt', 'a') as f:
        f.write(text + '\n')

# Converting text to speech using gTTS
def speak_text(mytext):  
    tts = gTTS(text=mytext, lang='en')
    tts.save('temp_audio.mp3')
    os.system('start temp_audio.mp3')  # This works on Windows

# Getting phonetic pronunciation
def get_pronunciation(word):
    phonics = pronouncing.phones_for_word(word)
    if phonics:
        return phonics[0]
    else:
        return None

# Display of phonetic pronunciation
def provide_pronunciation_feedback(phrase):
    common_errors = {
        'data': "Try pronouncing 'data' as day-ta",
        'school': "Try pronouncing 'school' as 's-kool'.",
        'politics': "Try pronouncing 'politics' as 'po-lee-ticks'",
        'heavy': "Try pronouncing 'heavy' as 'hair-vee'",
        'schedule': "Try pronouncing 'schedule' as 'ske-jool'"
    }
    
    pronunciation = get_pronunciation(phrase)
    if pronunciation:
        phonetic_representation = pronunciation.replace(" ", "-")  
        print(f"The word '{phrase}' is pronounced like: {phonetic_representation}")
    else:
        print(f"Phonetic pronunciation for '{phrase}' isn't found.")
    
    feedback = common_errors.get(phrase.lower())
    if feedback:
        print(feedback)

# Stopping the code after usage
def confirm_exit():
    print('Do you really want to stop? (yes/no)')
    response = input().strip().lower()
    return response == 'yes'

# Main loop
while True:
    choice = input("Type 's' for speech input or 't' for text input: ").strip().lower()

    if choice == 's':
        text = record_text()
    elif choice == 't':
        text = input_text()
    else:
        print("Invalid choice. Please try again.")
        continue

    # Loop to stop the code if the user is done using it
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
    for word in words:
        provide_pronunciation_feedback(word)
