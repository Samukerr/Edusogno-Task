import speech_recognition as sr
import pyttsx3
import pronouncing

# Initialize the recognizer
r = sr.Recognizer()

# Initialize a text-to-speech engine
t = pyttsx3.init()

#initializing the Microphone to listin to audio input and utilize Google API
def record_text():  
    while True: 
        try:
            with sr.Microphone() as source:
                print('Listening...') 
                r.adjust_for_ambient_noise(source, duration=0.2)  
                audio = r.listen(source) 
                mytext = r.recognize_google(audio) 
                print(f'You said: {mytext}')
                return mytext
        except sr.RequestError as e:
            print(f'Could not request results: {e}')
        except sr.UnknownValueError:
            print('Unknown error occurred, please repeat.')

# Input via terminal
def input_text():  
    return input("Please enter text: ")
    
# Output stored in text file
def output_text(text):  
    with open('output.txt', 'a') as f:
        f.write(text + '\n')
        
# Convert text to speech and speech-text from audio input
def speak_text(mytext): 
    t.say(mytext)
    t.runAndWait()
    
# getting pronunciation from CMU dictionary
def get_pronunciation(phrase):
    phonics = pronouncing.phones_for_word(phrase)
    if phonics:
        return phonics[0]  
    else:
        return None
#return the pronunciation in terminal
def provide_pronunciation_feedback(phrase):
    pronunciation = get_pronunciation(phrase)
    if pronunciation:
        phonetic_representation = pronunciation.replace(" ", "-")  # for Better display of phonetic representation
        print(f"The word '{phrase}' is pronounced like: {phonetic_representation}")
    else:
        print(f"Pronunciation for '{phrase}' isn't found.")
        
#stopping the modle from running
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
#output displayed on terminal
    print(f"Said Text: {text}")
    output_text(text)
    print('Text written')
    speak_text(text)

    words = text.split()
    for phrase in words:
        provide_pronunciation_feedback(phrase)
