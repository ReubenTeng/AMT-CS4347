import "./App.css";
import React from "react";
import { Audio } from "react-loader-spinner";
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
            loading: false,
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
                disabled={this.loading}
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
                disabled={this.loading}
            >
                Upload
            </button>,
            document.getElementById("upload-button")
        );
    }

    async uploadFile() {
        this.loading = true;
        ReactDOM.render(
            <Audio
                height="240"
                width="240"
                color="#03a9f4"
                ariaLabel="loading"
                wrapperStyle
                wrapperClass
            />,
            document.getElementById("load-spinner")
        );
        document.getElementById("content").style.display = "none";
        let result = separate(this.sound_src);
        this.readMIDIFile(await result);
        ReactDOM.render(<div />, document.getElementById("load-spinner"));
        document.getElementById("content").style.display = "";
        this.loading = false;
    }

    readMIDIFile(midi_blob) {
        // convert midi_blob to url
        this.midi_src = URL.createObjectURL(midi_blob);

        ReactDOM.render(
            <div>
                <MidiPlayer src={this.midi_src} />
                {/* button to download midi file */}
                <div>
                    <a href={this.midi_src} download="output.mid">
                        <button>Download MIDI</button>
                    </a>
                </div>
            </div>,
            document.getElementById("midi-player")
        );
    }

    async sendYoutubeLink() {
        this.loading = true;
        ReactDOM.render(
            <Audio
                height="240"
                width="240"
                color="#03a9f4"
                ariaLabel="loading"
                wrapperStyle
                wrapperClass
            />,
            document.getElementById("load-spinner")
        );
        document.getElementById("content").style.display = "none";
        let result = await separate_by_youtube(this.youtube_src);
        this.readMIDIFile(await result);
        ReactDOM.render(<div />, document.getElementById("load-spinner"));
        document.getElementById("content").style.display = "";
        this.loading = false;
    }

    render() {
        return (
            <div>
                <div id="content">
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
                                disabled={
                                    this.state.isRecording || this.loading
                                }
                            >
                                Start
                            </button>
                            <button
                                onClick={this.stop}
                                disabled={
                                    !this.state.isRecording || this.loading
                                }
                            >
                                Stop
                            </button>
                            <audio
                                src={this.state.blobURL}
                                controls="controls"
                            />
                        </div>
                        {/* mid column */}
                        <div>
                            <h1>Upload a file</h1>
                            <input
                                type="file"
                                onChange={(event) => {
                                    this.readFile(event);
                                }}
                                accept="audio/mp3"
                                disabled={this.loading}
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
                                disabled={this.loading}
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
                <div
                    style={{
                        margin: "auto",
                        width: "min-content",
                        marginTop: "240px", // non-responsive sizing but should look fine on a 1920 x 1080 screen
                    }}
                    id="load-spinner"
                ></div>
            </div>
        );
    }
}

export default UploadFilePage;
