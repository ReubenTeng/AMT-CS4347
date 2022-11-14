from fastapi import FastAPI, File
from separator import separate
from amtprototype import transcribe_one_song
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from pydantic import BaseModel
import youtube_dl

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class YoutubeLink(BaseModel):
    url: str

@app.get("/")
def test_root():
    return {"message": "Hello World"}

# receive file bytestream and pass to separator, and return results
@app.post("/separate")
def separate_file(file: bytes = File(...)):
    open("temp.mp3", "wb").write(file)
    transcribe_one_song("temp.mp3", "temp.mid", "temp.json")
    return FileResponse("temp.mid", media_type="audio/midi")
    
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

    # separate audio
    transcribe_one_song("temp.mp3", "temp.mid", "temp.json")
    return FileResponse("temp.mid", media_type="audio/midi")

