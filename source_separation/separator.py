#spleeter: https://github.com/deezer/spleeter

import os
import subprocess

def separate(file):
    """Separate the audio file into vocals and accompaniment"""

    # create temp file
    temp_file = open("temp.wav", "w")
    temp_file.close()
    temp_file = open("temp.wav", "wb")
    temp_file.write(file)
    temp_file.close()

    # run demucs
    subprocess.run(["spleeter", "separate", "-p" , "spleeter:2stems", "-o",  "output", "temp.wav"])

    # read output
    vocals = open("output/temp/vocals.wav", "rb").read()
    # delete temp files
    os.remove("temp.wav")
    os.rmdir("output/temp")

def test_with_taylor():
    audio_file = open("audio_files" + os.sep + "Taylor Swift - Lavender Haze (Official Lyric Video).wav", "rb").read()
    separate(audio_file)