This directory is related to the MIR-ST500 dataset. Files are adapted from the original project's repository. We use this dataset to evaluate both our singing transcription system as well as MusicYOLO.

To download requirements, use:
> pip install -r requirements.txt

Note: This step can be skipped when using MusicYOLO since the requirements should have already been downloaded. Do note that 
Spleeter's version of tensorflow and numpy may be incompatible with other parts of the project. If errors arise, use spleeter in 
a different environment/uninstall numpy and tensorflow before installing spleeter.

## Downloading the dataset
To download the dataset, use:
> python get_youtube.py MIR-ST500_link.json train test

This will download 500 songs from Youtube automatically. Song id #1~#400 (training set) will be saved to "train/", #401~#500(test set) will be saved to "test/". <br>

## Evaluating MusicYOLO on MIR-ST500
The following steps are for evaluating **MusicYOLO** on the MIR-ST500 test set. We evaluate MusicYolo only on the "test" set since the train set was used to train the model musicyolo1.pth.

We use an SVS program to extract vocal, and write the vocal file to "Vocal.wav". Here, do_spleeter.py uses Spleeter to do the job.

> python do_spleeter.py test/

To get the correct format and directories for prediction and evaluation, we do the inference with the following commands:

Step1. Move the extracted vocal files into their own directory "vocal" (Working directory: MIR-ST500)
> python movefiles.py

Step2. Split the audio into 35 second chunks (Working directory: AMTYolo)
> python splitwav.py MIR-ST500/vocal MIR-ST500/split

Step3. Onset/offset detection (use musicyolo1.pth) (Working directory: MusicYOLO) (Create "save" directory in MIR-ST500 first)
```shell
python3 tools/predict.py -f exps/example/custom/yolox_singing.py -c models/musicyolo1.pth --audiodir "../MIR-ST500/split" --savedir "../MIR-ST500/save"  --ext .wav --device gpu
```
Step4. Merge results (Working directory: AMTYolo)
> python mergeres.py MIR-ST500/vocal MIR-ST500/save MIR-ST500/merged-res

Step4. Get correct label files (Working directory: MusicYOLO)
> python jsontotxt.py

Step6. Evaluate (From MusicYOLO directory) 
```shell
python3 tools/note_eval.py --label "../MIR-ST500/annotation" --result "../MIR-ST500/merged-res" --offset
```

Original README:
MIR-ST500 dataset

Version: 2021.02.06

Description
MIR-ST500 dataset is a dataset created by NTU MIRLAB for the task of "automatic singing transcription".
This dataset contains 500 pop songs and the corresponding annotations of VOCAL parts.
For more information, please refer to the paper "On the Preparation and Validation of a Large-scale Dataset" (ICASSP2021).

Data Format
"MIR-ST500_link.json" contains Youtube links of these 500 songs (in dictionary structure of {id:link}). You can download corresponding audio from Youtube using these links.
"MIR-ST500_corrected.json" contains annotations of these 500 songs. It is a dictionary of {id:gt}. Here, "gt" is a list of ground truth notes (in ascending order of the onset). Each note is denoted by [onset, offset, score pitch].
"metadata.csv" contains labeler id (1~14) and verifier id (1~6) of each song in the dataset.

Each song has its own id numbering from 1 to 500. We separate these 500 songs into training set (#1 to #400) and test set (#401 to #500).
If some of the Youtube links do not work, please contact us (especially for those songs in test set !!!).

Contact us
If there is any wrong about the dataset (e.g. note label is incorrect, Youtube link does not work, etc), please contact Jyh-Shing "Roger" Jang (roger.jang@gmail.com) or Jun-You Wang (b06902046@ntu.edu.tw).
If some of the notes are incorrect, we will try our best to correct those labels and release newer version as soon as possible.