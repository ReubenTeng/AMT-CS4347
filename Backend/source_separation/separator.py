#omnizart: https://pypi.org/project/omnizart/

import os
import subprocess

def separate(file_name):
    # create temp mid file
    # run omnizart
    subprocess.run(["omnizart", "vocal", "transcribe", file_name])
    # os.remove(file_name)

def test_with_taylor():
    audio_file = open("audio_files" + os.sep + "Taylor Swift - Lavender Haze (Official Lyric Video).wav", "rb").read()
    separate(audio_file)