import speech_recognition as sr
import pyttsx3
import pronouncing

# Initialize the recognizer
r = sr.Recognizer()

# Initialize a text-to-speech engine
t = pyttsx3.init()

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

def speak_text(mytext):  # Convert text to speech
    t.say(mytext)
    t.runAndWait()

def get_pronunciation(phrase):
    phonics = pronouncing.phones_for_word(phrase)
    if phonics:
        return phonics[0]  # Return the first pronunciation found
    else:
        return None  # No pronunciation found

def provide_pronunciation_feedback(phrase):
    pronunciation = get_pronunciation(phrase)
    if pronunciation:
        phonetic_representation = pronunciation.replace(" ", "-")  # Better display for phonetic representation
        print(f"The word '{phrase}' is pronounced like: {phonetic_representation}")

        # Add specific feedback based on the word
        if phrase.lower() == "schedule":
            print("Try pronouncing 'schedule' as 'sked-jool'.")
        elif phrase.lower() == "data":
            print("You can pronounce 'data' as 'day-ta' or 'da-ta'. Both are correct.")
        # Add more custom feedback here as needed
    else:
        print(f"Pronunciation for '{phrase}' isn't found.")

def confirm_exit():
    print('Do you really want to stop? (yes/no)')
    response = input().strip().lower()
    return response == 'yes'

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
    for phrase in words:
        provide_pronunciation_feedback(phrase)
