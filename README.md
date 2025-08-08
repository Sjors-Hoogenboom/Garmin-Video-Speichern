# Garmin, Video speichern

A simple python project that listens to a trigger word/ phrase which plays the Garmin beep.   
After that, it will listen to a second phrase which in turn plays the "video saved" sound from Garmin, just like the original meme

Also does a key combination after the two phrases are said, which should be set to a clipping software's own keybind, so it actually saves a video just like how Garmin dashcams work

## How to setup

1. Change the following variables:

    1. **HOTKEY_COMBINATION = ('ctrl', 'comma')**, which should be the same as the keybind on your clipping software
   2. **OUTPUT_DEVICE_INDEX = [9]**, This is the output device where the sound will be played.  
       To get the correct output index, uncomment in main.py the following code to see all available output devices:
        ```python
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print(f"{i}: {info['name']} (Output: {info['maxOutputChannels']})")
        ```
   3. **MICROPHONE_DEVICE_INDEX = 4**, This is the input device the application listens to.  
      To find your microphone input index, uncomment and run:
      ```python
      for index, name in enumerate(sr.Microphone.list_microphone_names()):
          print(f"Audio {index} name: {name}")
      ```
   4. **SECONDARY_MATCHES = ["gar"]**, A list of backup words if it can't interpret what you are saying correctly (for example, contains "gar" at the moment, since saying "okay Garmin" would result in it thinking I said "ok Gar" every so often)


2. #### optional: change language

   1. If you want to change language/ use the other languages versions of the meme, change **LANGUAGE = "de-DE"** into "en-US" for English or "fr-FR" for French
   2. Change the target words to the appropriate language