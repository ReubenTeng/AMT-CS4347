from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI();

@app.get("/")
def test_root():
    return {"message": "Hello World"}

@app.get("/default-midi")
def default_midi():
    return FileResponse("sample-midi/MaryHadALittleLamb.mid")