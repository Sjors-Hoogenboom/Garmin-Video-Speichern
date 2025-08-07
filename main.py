import wave

import speech_recognition as sr
import pyaudio
from difflib import get_close_matches
from pydub import AudioSegment

recognizer = sr.Recognizer()

sound = AudioSegment.from_wav("GarminListening.wav").set_channels(1)

OUTPUT_DEVICE_INDEX = 9
MICROPHONE_DEVICE_INDEX = 4
p = pyaudio.PyAudio()

# Uncomment to find out the index of the microphone input you want to use, recommended to use pure microphone and not voicemod/ filtered audio
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Audio {index} name: {name}")

# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(f"{i}: {info['name']} (Output: {info['maxOutputChannels']})")

def play_sound():
    wf = wave.open("GarminListening.wav", "rb")
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

def is_word_close_enough(recognized_text, target_word, cutoff=0.8):
    matches = get_close_matches(target_word.lower(), recognized_text.lower().split(), n=1, cutoff=cutoff)
    return bool(matches)


with sr.Microphone(MICROPHONE_DEVICE_INDEX) as source:
    print("Say something...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="de-DE")
        print("You said:", text)

        if is_word_close_enough(text, "Garmin"):
            play_sound()
            print("Garmin!")
        else:
            print("Try again")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service:", e)
