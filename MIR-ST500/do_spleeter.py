import os
import sys
import librosa
import numpy as np

# this file is adapted from the MusicYOLO repository
# we have commented out the extraction of the instrumental as it is not necessary for the project
if __name__ == '__main__':

    yt_id = []
    data_id = []
    offset_list = []

    dataset_dir = sys.argv[1]

    from spleeter.separator import Separator
    import warnings
    separator = Separator('spleeter:2stems')

    for the_dir in os.listdir(dataset_dir):
        # if int(the_dir) < 470 or int(the_dir) > 470: continue # in case of out of memory error, edit this line to run in smaller groups
        mix_path = os.path.join(dataset_dir, the_dir, "Mixture.mp3")
        vocalpath = os.path.join(dataset_dir, the_dir, "Vocal.wav")
        # instpath = os.path.join(dataset_dir, the_dir, "Inst.wav")
        # if os.path.exists(vocalpath) and os.path.exists(instpath): continue # for already split songs
        if os.path.exists(vocalpath): continue # for already split songs
        if not os.path.exists(mix_path): continue # for songs that cannot be download from youtube
        print("Splitting ", the_dir, "\n")
    
        y, sr = librosa.core.load(mix_path, sr=None, mono=True)
        if sr != 44100:
            y = librosa.core.resample(y=y, orig_sr=sr, target_sr=44100)

        waveform = np.expand_dims(y, axis=1)

        prediction = separator.separate(waveform)
        voc = librosa.core.to_mono(prediction["vocals"].T)
        voc = np.clip(voc, -1.0, 1.0)

        # acc = librosa.core.to_mono(prediction["accompaniment"].T)
        # acc = np.clip(acc, -1.0, 1.0)

        import soundfile
        soundfile.write(os.path.join(dataset_dir, the_dir, "Vocal.wav"), voc, 44100, subtype='PCM_16')
        # soundfile.write(os.path.join(dataset_dir, the_dir, "Inst.wav"), acc, 44100, subtype='PCM_16')
