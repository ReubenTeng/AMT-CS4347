import os
import sys
import librosa
import numpy as np
import subprocess
import shlex
import shutil
import pandas as pd
import math
from decimal import Decimal

from splitwav import split_one_song
from mergeres import merge_one_song_res

def separate_vocal(wav_file_path) :
    wav_file_name = os.path.basename(wav_file_path).split('.')[0]

    from spleeter.separator import Separator
    import warnings
    separator = Separator('spleeter:2stems')

    mix_path = wav_file_path
    vocal_path = "vocal.wav"

    print("Separating ", wav_file_name, "\n")

    y, sr = librosa.core.load(mix_path, sr=None, mono=True)
    if sr != 44100:
        y = librosa.core.resample(y=y, orig_sr=sr, target_sr=44100)

    waveform = np.expand_dims(y, axis=1)

    prediction = separator.separate(waveform)
    voc = librosa.core.to_mono(prediction["vocals"].T)
    voc = np.clip(voc, -1.0, 1.0)

    import soundfile
    soundfile.write(vocal_path, voc, 44100, subtype='PCM_16')

    return vocal_path

def segment_one_song(vocal_path, split_dir, save_dir, merged_res_dir):
    split_one_song(vocal_path, split_dir)

    # predict
    predict_cmd = ("python tools/predict.py -f exps/example/custom/yolox_singing.py -c" 
        "models/musicyolo1.pth --audiodir " + "\"../" + split_dir + "\" --savedir \"../"+ save_dir + "\" "
        "--ext .wav --device gpu")
    args = shlex.split(predict_cmd)
    subprocess.run(args, cwd="MusicYOLO")

    result_path = merge_one_song_res(vocal_path, os.path.join(save_dir, "res"), merged_res_dir)

    return result_path

def transcribe_one_song(wav_file_path):
    vocal_path = separate_vocal(wav_file_path)
    # vocal_path = "vocal.wav"

    # clear directories
    split_dir = "split"
    shutil.rmtree(split_dir)
    os.mkdir(split_dir)

    save_dir = "save"
    shutil.rmtree(save_dir)
    os.mkdir(save_dir)

    merged_res_dir = "merged-res"
    shutil.rmtree(merged_res_dir)
    os.mkdir(merged_res_dir)

    note_segmentation_path = segment_one_song(vocal_path, split_dir, save_dir, merged_res_dir)
    # note_segmentation_path = "merged-res/vocal.txt"

    onsets = []
    offsets = []
    note_file = open(note_segmentation_path, "r")
    for line in note_file:
        split_line = line.split("\t", 3)
        onset = float(split_line[0])
        offset = float(split_line[1])
        
        onsets.append(onset)
        offsets.append(offset)
    note_file.close()

    # pitch contour
    y, sr = librosa.load(vocal_path)
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C0'), fmax=librosa.note_to_hz('B8'))
    times = librosa.times_like(f0)

    onset_frames = []
    offset_frames = []

    frame_counter = 0
    onset_counter = 0
    offset_counter = 0
    while(frame_counter < len(times) and (onset_counter < len(onsets) or offset_counter < len(offsets))):
        if (onset_counter < len(onsets) and times[frame_counter] < onsets[onset_counter] and times[frame_counter + 1] > onsets[onset_counter]) :
            onset_frames.append(frame_counter)
            onset_counter += 1
        if (offset_counter < len(offsets) and times[frame_counter] < offsets[offset_counter] and times[frame_counter + 1] > offsets[offset_counter]) :
            offset_frames.append(frame_counter)
            offset_counter += 1
        frame_counter += 1

    notes = []
    for i in range(len(offset_frames)):
        end = offset_frames[i] + 1
        if (end >= len(f0)) :
            end = len(offset_frames) - 1
        
        freqs = f0[onset_frames[i]:end]
        freqs = freqs[~np.isnan(freqs)]
        median_freq = np.median(freqs)

        if (math.isnan(median_freq) or len(freqs) <= 0):
            notes.append(median_freq)
        else:
            notes.append(librosa.hz_to_midi(median_freq))

    result_df = pd.DataFrame(list(zip(onsets, offsets, notes)), columns=["Onset", "Offset", "Note"])
    pd.set_option('display.max_rows', None)
    print(result_df)

    return result_df

if __name__=='__main__':
    result_df = transcribe_one_song("sample.wav")
    arr = result_df.to_numpy()
    print(arr)