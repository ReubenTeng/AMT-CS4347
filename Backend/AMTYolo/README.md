# Singing Melody Transcriber
This document provides the instructions on how to set up and test the backend's transcription system.

## Set Up MusicYOLO
MusicYOLO must be set up before using the full system (with frontend), using the trascription system in the backend directly from command line, or evaluating the performance of MusicYOLO. Follow these instructions only after downloading the requirements in the main directory.

Step 1. Follow the instructions in the README of the MusicYOLO sub-directory to install YOLOX/use the commands below.
```shell
cd MusicYOLO
pip3 install -U pip && pip3 install -r requirements.txt
pip3 install -v -e .  # or  python3 setup.py develop
```
Step 2. Follow the instructions in the README of the MusicYOLO sub-directory to install pycocotools/use the commands below. (Working directory: MusicYOLO)
```shell
pip3 install cython;
cd cocoapi/PythonAPI && pip3 install -v .
```

## Evaluate MusicYOLO's performance
To evaluate MusicYOLO's performance on the **SSVD** (sight singing) dataset, follow the instructions in the README of the MusicYOLO sub-directory.

To evaluate MusicYOLO's performance on the **MIR-ST500** (pop song) dataset, follow the instructions in the README of the MIR-ST500 sub-directory.

## Transcribe one song

Step 1. Upload the audio file into this directory (AMTYolo).

Step 2. In amtprototype.py, comment out the lines to predict the MIR-ST500 dataset (all lines after line 191).

Step 3. In amtprototype.py, uncomment lines 185-189.

Step 4. In amtprototype.py, replace the path in line 185 to the file path of your uploaded audio file.

Step 5. Run `python amtprototype.py`. Your transcribed midi file will be found at `trans.mid`.

## Evaluate transcriber's performance
To evaluate our transcription system's performance on the MIR-ST500 dataset's test set:

Step 1. Download the MIR-ST500 datasset using the instructions in the README of the MIR-ST500 sub-directory. (May have been done if you have evaluated MusicYOLO's performance using the dataset)

Step 2. Run `python amtprototype.py` without any changes. (Undo changes if you have used it to transcribe 1 song like described in the previous section)

Step 3. Run `python evaluate.py`. You may check that line 166 is correctly pointing to your generated prediction JSON file.

If any errors are faced/the task is aborted due to lack of resources, you may predict the transcriptions in batches (i.e. not on so many songs at once). By default, our code is written to predict on the first 30 songs of the test set.