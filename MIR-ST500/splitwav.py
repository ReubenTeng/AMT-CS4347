import math
import os
from pydub import AudioSegment

def split_one_song(source_file_path, dest_folder):
    chunk_size = 35000 # 35s
    old_wav = AudioSegment.from_wav(source_file_path)
    num_of_splits = math.ceil(len(old_wav) / chunk_size) 
    source_file_name = os.path.basename(source_file_path).split('.')[0]
    for i in range(num_of_splits):
        t1 = i * chunk_size
        t2 = t1 + chunk_size - 1
        if t2 > len(old_wav):
            t2 = len(old_wav) - 1
        new_wav = old_wav[t1:t2]

        new_file_path = os.path.join(dest_folder, source_file_name + "_" + str(i) + ".wav")
        new_wav.export(new_file_path, format="wav")

if __name__=='__main__':
    vox_dir = sys.argv[1] # vocals already separated from song
    split_dir = sys.argv[2]
    os.makedirs(split_dir) 
    for vox_wav in os.listdir(vox_dir):
        split_one_song(os.path.join(vox_dir, vox_wav), split_dir)