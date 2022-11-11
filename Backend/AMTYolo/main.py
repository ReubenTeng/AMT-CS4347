from fastapi import FastAPI, File, UploadFile
from separator import separate
from amtprototype import get_vocal_midi
# from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import youtube_dl
import os

app = FastAPI();


origins = [
    "http://localhost:3000",
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

class YoutubeLink(BaseModel):
    url: str

@app.get("/")
def test_root():
    return {"message": "Hello World"}

# receive file bytestream and pass to separator, and return results
@app.post("/separate")
def separate_file(file: bytes = File(default="")):
    open("temp.mp3", "wb").write(file)
    get_vocal_midi("temp.mp3")

# receive youtube url, convert to wav file, pass to separator, and return results
@app.post("/separate-youtube")
def separate_youtube(link: YoutubeLink):
    url = link.url
    # download youtube video
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # read file
    file = open("temp.mp3", "rb").read()


    # separate audio
    get_vocal_midi("temp.mp3")
