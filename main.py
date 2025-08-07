import wave
from difflib import get_close_matches

import pyaudio
import pyautogui
import speech_recognition as sr

recognizer = sr.Recognizer()

# The original meme is German, change to en-US for English speech recognition
LANGUAGE = "de-DE"

# These are the words that the application will look for
FIRST_TARGET_WORDS = ["Garmin"]
SECOND_TARGET_WORDS = ["Video speichern"]

# Words that also match the target for if it can't recognize what you're saying
SECONDARY_MATCHES = ["gar"]

# Files of the audio, have to be .wav
FILENAME_ONE = "GarminListening.wav"
FILENAME_TWO = "GarminConfirmed.wav"

OUTPUT_DEVICE_INDEX = [9]
MICROPHONE_DEVICE_INDEX = 4
p = pyaudio.PyAudio()

# Uncomment to find the index of the microphone input you want to use, recommended to use pure microphone and not voicemod/ filtered audio
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Audio {index} name: {name}")

# Uncomment to find the index of the output you want to use
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(f"{i}: {info['name']} (Output: {info['maxOutputChannels']})")

def play_sound(filename, output_device_indices):
    wf = wave.open(filename, "rb")
    streams = []

    for device_index in output_device_indices:
        stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                output_device_index=device_index
        )
        streams.append(stream)

    wf.rewind()
    data = wf.readframes(1024)
    while data:
        for stream in streams:
            stream.write(data)
        data = wf.readframes(1024)

    for stream in streams:
        stream.stop_stream()
        stream.close()

    wf.close()

def listen_and_recognize(prompt, target_words, fallback_matches=None):
    if fallback_matches is None:
        fallback_matches = []

    with sr.Microphone(device_index=MICROPHONE_DEVICE_INDEX) as source:
        print(prompt)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=LANGUAGE)
            print("You said:", text)
            text_lower = text.lower()

            if any(target.lower() in text_lower for target in target_words):
                return True

            if any(fallback.lower() in text_lower for fallback in fallback_matches):
                return True

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results:", e)

    return False

with sr.Microphone(device_index=MICROPHONE_DEVICE_INDEX) as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.5)

try:
    while True:
        if listen_and_recognize("\nSay Garmin", FIRST_TARGET_WORDS, fallback_matches=SECONDARY_MATCHES):
            play_sound(FILENAME_ONE, OUTPUT_DEVICE_INDEX)
            print(", ".join(FIRST_TARGET_WORDS) + "!")
            if listen_and_recognize("\nSay video speichern", SECOND_TARGET_WORDS):
                print(", ".join(SECOND_TARGET_WORDS) + "!")
                pyautogui.hotkey('ctrl', ',')
                play_sound(FILENAME_TWO, OUTPUT_DEVICE_INDEX)
            else:
                print("Video not detected")
        else:
            print("Garmin not detected")

finally:
    p.terminate()