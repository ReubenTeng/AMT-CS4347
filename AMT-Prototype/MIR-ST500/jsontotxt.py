import os
import json

# converts annotation into a format usable by MusicYOLO
if __name__=='__main__':
    annotationFilePath = "MIR-ST500_corrected.json"
    json_file = open(annotationFilePath, "r")
    data = json.load(json_file)
    annotation_dir = "annotation" 
    os.makedirs(annotation_dir) 

    for song_num in range(1, 500):
        annt_file_path = os.path.join(annotation_dir, str(song_num) + ".txt")
        annt_file = open(annt_file_path, "w")
        annt_file.write("") # empty file
        annt_file.close()

        annt_file = open(annt_file_path, "a")
        arr = data[str(song_num)]
        for sub_arr in arr:
            line = str(sub_arr[0]) + "\t" + str(sub_arr[1]) + "\t" +str(sub_arr[2]) + "\n"
            annt_file.write(line)
        annt_file.close()

    json_file.close()