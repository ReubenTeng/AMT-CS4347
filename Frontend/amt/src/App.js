import "./App.css";
import React from "react";
import MicRecorder from "mic-recorder-to-mp3";
import ReactDOM from "react-dom";
import MidiPlayer from "react-midi-player";
import { separate, separate_by_youtube } from "./APIService";

const Mp3Recorder = new MicRecorder({ bitRate: 128 });

const browserSupportsMedia = () => {
    return (
        navigator.mediaDevices.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.mzGetUserMedia
    );
};

class UploadFilePage extends React.Component {
    midi_src;
    sound_src = "";
    youtube_src;
    constructor(props) {
        super(props);
        this.state = {
            isRecording: false,
            blobURL: "",
            isBlocked: false,
        };
        this.myRef = React.createRef();
        this.playbackRef = this.myRef;
        window.addEventListener("keydown", ({ key }) => {
            if (key === " ") {
                this.playbackRef.current.toggle();
            } else if (key === "Enter") {
                this.playbackRef.current.seek("0:0:0");
            }
        });
    }

    readRecording(blob) {
        this.sound_src = new File([blob], "recording.mp3");

        ReactDOM.render(
            <button
                onClick={(event) => {
                    this.uploadFile();
                }}
            >
                Upload
            </button>,
            document.getElementById("upload-button")
        );
    }

    componentDidMount() {
        browserSupportsMedia(
            { audio: true },
            () => {
                console.log("Permission Granted");
                this.setState({ isBlocked: false });
            },
            () => {
                console.log("Permission Denied");
                this.setState({ isBlocked: true });
            }
        );
    }

    start = () => {
        if (this.state.isBlocked) {
            console.log("Permission Denied");
        } else {
            Mp3Recorder.start()
                .then(() => {
                    this.setState({ isRecording: true });
                })
                .catch((e) => console.error(e));
        }
    };

    stop = () => {
        Mp3Recorder.stop()
            .getMp3()
            .then(([buffer, blob]) => {
                // read blob as bytes
                this.readRecording(blob);
                const blobURL = URL.createObjectURL(blob);
                this.setState({
                    blobURL,
                    isRecording: false,
                });
            })
            .catch((e) => console.log(e));
    };

    readFile(event) {
        this.sound_src = event.target.files[0];
        ReactDOM.render(
            <button
                onClick={(event) => {
                    this.uploadFile();
                }}
            >
                Upload
            </button>,
            document.getElementById("upload-button")
        );
    }

    uploadFile() {
        this.midi_src = separate(this.sound_src);
    }

    readMIDIFile(event) {
        this.midi_src = URL.createObjectURL(event.target.files[0]);
        ReactDOM.render(
            <MidiPlayer src={this.midi_src} />,
            document.getElementById("midi-player")
        );
    }

    sendYoutubeLink() {
        this.midi_src = separate_by_youtube(this.youtube_src);
    }

    render() {
        return (
            <div>
                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-evenly",
                    }}
                >
                    {/* left column */}
                    <div>
                        <h1>Record your own voice</h1>
                        <button
                            onClick={this.start}
                            disabled={this.state.isRecording}
                        >
                            Start
                        </button>
                        <button
                            onClick={this.stop}
                            disabled={!this.state.isRecording}
                        >
                            Stop
                        </button>
                        <audio src={this.state.blobURL} controls="controls" />
                    </div>
                    {/* mid column */}
                    <div>
                        <h1>Upload a file</h1>
                        <input
                            type="file"
                            onChange={(event) => {
                                this.readFile(event);
                            }}
                            accept="audio/*"
                        />
                    </div>
                    {/* right column - download audio from youtube*/}
                    <div>
                        <h1>Download audio from youtube</h1>
                        <input
                            type="text"
                            placeholder="Enter youtube link"
                            onChange={(event) => {
                                this.youtube_src = event.target.value;
                            }}
                        />
                        <button
                            onClick={() => {
                                this.sendYoutubeLink();
                            }}
                        >
                            Download
                        </button>
                    </div>
                </div>
                <div
                    style={{
                        margin: "auto",
                        textAlign: "center",
                        marginTop: "40px",
                    }}
                    id="upload-button"
                ></div>
                <div
                    id="midi-player"
                    style={{
                        margin: "auto",
                        textAlign: "center",
                        marginTop: "40px",
                    }}
                ></div>
            </div>
        );
    }
}

export default UploadFilePage;
