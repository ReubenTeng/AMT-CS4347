import shutil
import os

# moves vocal wav files (extracted using spleeter) into another directory
if __name__=='__main__':
    dataset_dir = "test"
    vocal_dir = "vocal"
    os.makedirs(dataset_dir) 
    os.makedirs(vocal_dir) 

    for test_dir in os.listdir(dataset_dir):
        vocalpath = os.path.join(dataset_dir, test_dir, "Vocal.wav")
        if not os.path.exists(vocalpath): continue # for songs that cannot be download from youtube

        shutil.copy(vocalpath, os.path.join(vocal_dir, test_dir + ".wav"))
