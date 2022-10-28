from locale import normalize
import librosa
import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import IPython.display as ipd

def get_onsets(file_path):
    y, sr = librosa.load(file_path)

    # get onsets
    onset_strength_by_frame = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.times_like(onset_strength_by_frame, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_strength_by_frame, sr=sr, normalize=True)
    print('onset_frames:')
    print(onset_frames)

    # filter onsets
    temp_onset_frames = []
    temp_onset_strength = np.copy(onset_strength_by_frame)
    for i in range(onset_frames.size):
        if (i == 0 or (i > 0 and temp_onset_strength[onset_frames[i]] >= temp_onset_strength[onset_frames[i - 1]] / 1.5) or temp_onset_strength[onset_frames[i]] > 4):
            temp_onset_frames.append(onset_frames[i])
        else:
            temp_onset_strength[onset_frames[i]] = temp_onset_strength[onset_frames[i - 1]]

    onset_frames = np.array(temp_onset_frames)
    print('updated onset_frames:')
    print(onset_frames)

    # get offsets
    # TODO

    # plot graph for visualisation
    D = np.abs(librosa.stft(y))
    fig, ax = plt.subplots(nrows=2, sharex=True)
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                         x_axis='time', y_axis='log', ax=ax[0])
    ax[0].set(title='Power spectrogram')
    ax[0].label_outer()
    ax[1].plot(times, onset_strength_by_frame, label='Onset strength')
    ax[1].vlines(times[onset_frames], 0, onset_strength_by_frame.max(), color='r', alpha=0.9,
           linestyle='--', label='Onsets')
    ax[1].legend()

    plt.savefig('my_plot.png')

    # get input with click track indicating onsets
    clicks = librosa.clicks(frames=onset_frames, sr=sr, length=len(y))
    audio = ipd.Audio(y + clicks, rate=sr)
    with open('with_click.wav', 'wb') as f:
        f.write(audio.data)

    return librosa.frames_to_time(onset_frames)

file_path = "F66603570-40228097_169333-380081730_1609808501-GB-F-021.wav"
# file_path = "download.wav"
frames = get_onsets(file_path)
print("frames:")
print(frames)
