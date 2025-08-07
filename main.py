import wave
from difflib import get_close_matches

import pyaudio
import pyautogui
import speech_recognition as sr

recognizer = sr.Recognizer()

# The original meme is German, change to en-US for English speech recognition
LANGUAGE = "de-DE"

# These are the words that the application will look for
FIRST_TARGET_WORD = "Garmin"
SECOND_TARGET_WORD = "Video speichern"

# Files of the audio, have to be .wav
FILENAME_ONE = "GarminListening.wav"
FILENAME_TWO = "GarminConfirmed.wav"

OUTPUT_DEVICE_INDEX = 9
MICROPHONE_DEVICE_INDEX = 4
p = pyaudio.PyAudio()

# Uncomment to find the index of the microphone input you want to use, recommended to use pure microphone and not voicemod/ filtered audio
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Audio {index} name: {name}")

# Uncomment to find the index of the output you want to use
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(f"{i}: {info['name']} (Output: {info['maxOutputChannels']})")

def play_sound(filename):
    wf = wave.open(filename, "rb")
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=OUTPUT_DEVICE_INDEX)
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    wf.close()

def is_word_close_enough(recognized_text, target_phrase, cutoff=0.8):
    matches = get_close_matches(target_phrase.lower(), [recognized_text.lower()], n=1, cutoff=cutoff)
    return bool(matches)

def listen_and_recognize(prompt, target_word):
    with sr.Microphone(device_index=MICROPHONE_DEVICE_INDEX) as source:
        print(prompt)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=LANGUAGE)
            print("You said:", text)
            return is_word_close_enough(text, target_word)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results:", e)

    return False

with sr.Microphone(device_index=MICROPHONE_DEVICE_INDEX) as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.5)

try:
    while True:
        if listen_and_recognize("\nSay Garmin", FIRST_TARGET_WORD):
            play_sound(FILENAME_ONE)
            print(FIRST_TARGET_WORD + "!")
            if listen_and_recognize("\nSay video speichern", SECOND_TARGET_WORD):
                print(SECOND_TARGET_WORD + "!")
                pyautogui.hotkey('ctrl', ',')
                play_sound(FILENAME_TWO)
            else:
                print("Video not detected")
        else:
            print("Garmin not detected")

finally:
    p.terminate()