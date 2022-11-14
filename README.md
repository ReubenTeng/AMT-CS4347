# ALT-AMT-CS4347
Automatic lyrics and melody trascriber for CS4347
This project is divided into two components, a back-end served by FastAPI and uvicorn, and a front-end built on React. 

## Front-end
Due to dependency issues, this can only be run on Python 3.7. The front-end can be run through the following steps.
1) From within this directory, run `pip install -r requirements.txt`
2) `cd AMTYolo`
3) Follow the instructions within the README file in the AMTYolo directory to set up MusicYolo
4) From within the AMTYolo directory, run `uvicorn main:app --host 0.0.0.0 --port 80`

## Back-end
The back-end is built on React and runs on Node 14.15.3
1) From this directory, run the command `cd ./Frontend/amt`
2) Run `npm install` to install the project dependencies
3) Run `npm start` to start running the front-end open the web-app on your browser

## Using the web-app
### Voice recording
You can start recording your voice by clicking start, then end by clicking stop. Clicking the play button in the left column will let you hear your recording.

### Upload a file
Clicking browse will allow you to choose any mp3 file to upload to the system.

### Download from Youtube
Alternatively, you can also directly copy-paste a Youtube link here. Do note that this is the slowest option by far, since it requires downloading the audio before processing it. Clicking download automatically starts the vocal AMT process.

### Passing to Back-end
After audio is collected from recording or uploading, the "Upload" button will appear at the bottom. Clicking it sends the most recently collected audio to the Back-end for AMT processing.

## Additional Notes
Due to how the back-end handles small audio files (e.g. less than 1 second), such audio samples being sent to the back-end might break the application.