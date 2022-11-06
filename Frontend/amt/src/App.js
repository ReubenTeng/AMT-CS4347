import "./App.css";
import React, { useRef } from "react";
import MicRecorder from "mic-recorder-to-mp3";
import PianoRoll from "react-piano-roll";
import ReactDOM from "react-dom";
import MidiPlayer from "react-midi-player";

// const defaultMidi =
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
    constructor(props) {
        super(props);
        this.state = {
            isRecording: false,
            blobURL: "",
            isBlocked: false,
            isFileUploaded: false,
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
                const blobURL = URL.createObjectURL(blob);
                this.setState({
                    blobURL,
                    isRecording: false,
                    isFileUploaded: false,
                });
            })
            .catch((e) => console.log(e));
    };

    readMIDIFile(event) {
        this.midi_src = URL.createObjectURL(event.target.files[0]);
        ReactDOM.render(
            <MidiPlayer src={this.midi_src} />,
            document.getElementById("midi-player")
        );
    }

    log(thing) {
        console.log(thing);
    }

    render() {
        if (!this.state.isFileUploaded) {
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
                            <audio
                                src={this.state.blobURL}
                                controls="controls"
                            />
                        </div>
                        {/* right column */}
                        <div>
                            <h1>Upload a file</h1>
                            <input
                                type="file"
                                onChange={(event) => {
                                    this.readMIDIFile(event);
                                }}
                            />
                            {/* accept="audio/*" /> */}
                            <button
                                onClick={(event) => {
                                    this.setState({ isFileUploaded: true });
                                }}
                            >
                                Upload
                            </button>
                        </div>
                    </div>
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
        } else {
            return (
                //display piano roll
                <PianoRoll
                    width={1200}
                    height={660}
                    zoom={6}
                    resolution={2}
                    gridLineColor={0x333333}
                    blackGridBgColor={0x1e1e1e}
                    whiteGridBgColor={0x282828}
                    noteData={[
                        ["0:0:0", "F5", ""],
                        ["0:0:0", "C4", "2n"],
                        ["0:0:0", "D4", "2n"],
                        ["0:0:0", "E4", "2n"],
                        ["0:2:0", "B4", "4n"],
                        ["0:3:0", "A#4", "4n"],
                        ["0:0:0", "F2", ""],
                    ]}
                    ref={this.playbackRef}
                />
            );
        }
    }
}

export default UploadFilePage;
