import os
import sys
import librosa
import numpy as np
import subprocess
import shlex
import shutil
import pandas as pd
import math
import mido
import time

from splitwav import split_one_song
from mergeres import merge_one_song_res

def separate_vocal(wav_file_path) :
    wav_file_name = os.path.basename(wav_file_path).split('.')[0]

    from spleeter.separator import Separator
    import warnings
    separator = Separator('spleeter:2stems')

    mix_path = wav_file_path
    vocal_path = "vocal.wav"

    print("Separating", wav_file_name, "...\n")

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
    print("Segmenting...\n")
    split_one_song(vocal_path, split_dir)

    # predict
    predict_cmd = ("python tools/predict.py -f exps/example/custom/yolox_singing.py -c" 
        "models/musicyolo1.pth --audiodir " + "\"../" + split_dir + "\" --savedir \"../"+ save_dir + "\" "
        "--ext .wav --device cpu")
    args = shlex.split(predict_cmd)
    subprocess.run(args, cwd="MusicYOLO")
    result_path = merge_one_song_res(vocal_path, os.path.join(save_dir, "res"), merged_res_dir)

    return result_path

# convert to midi, taken from assignment 1
def notes2mid(notes):
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    mid.ticks_per_beat = 480
    new_tempo = mido.bpm2tempo(120.0)

    track.append(mido.MetaMessage('set_tempo', tempo=new_tempo))
    track.append(mido.Message('program_change', program=0, time=0))

    cur_total_tick = 0

    for note in notes:
        if note[2] == 0:
            continue
        note[2] = int(round(note[2]))

        ticks_since_previous_onset = int(mido.second2tick(note[0], ticks_per_beat=480, tempo=new_tempo))
        ticks_current_note = int(mido.second2tick(note[1]-0.0001, ticks_per_beat=480, tempo=new_tempo))
        note_on_length = ticks_since_previous_onset - cur_total_tick
        note_off_length = ticks_current_note - note_on_length - cur_total_tick

        track.append(mido.Message('note_on', note=note[2], velocity=100, time=note_on_length))
        track.append(mido.Message('note_off', note=note[2], velocity=100, time=note_off_length))
        cur_total_tick = cur_total_tick + note_on_length + note_off_length

    return mid

def transcribe_one_song(wav_file_path):
    vocal_path = separate_vocal(wav_file_path)
    # vocal_path = "vocal.wav"

    # clear directories
    split_dir = "split"
    if (os.path.exists(split_dir)):
        shutil.rmtree(split_dir)
    os.mkdir(split_dir)

    save_dir = "save"
    if (os.path.exists(save_dir)):
        shutil.rmtree(save_dir)
    os.mkdir(save_dir)

    merged_res_dir = "merged-res"
    if (os.path.exists(merged_res_dir)):
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

    print("Deriving pitch...\n")
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

    return result_df

def get_vocal_midi(song_path):
    startTime = time.time()
    result_df = transcribe_one_song(song_path)
    pd.set_option('display.max_rows', None)

    result = result_df.to_json(orient="values")
    with open("trans.json", "w") as result_file:
        result_file.write(result)

    list_of_rows = result_df.to_numpy().tolist()
    mid = notes2mid(list_of_rows)
    mid.save("trans.mid")
    
    executionTime = (time.time() - startTime)
    print('Transcription time in seconds: ' + str(executionTime))

if __name__=='__main__':
    get_vocal_midi("sample.wav")
