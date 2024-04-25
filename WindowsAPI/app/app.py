from fastapi import FastAPI


app = FastAPI(
    title="FastAPI for TTS",
    description="FastAPI for Text-to-Speech (TTS) using Piper",
    version="0.0.0"
)


# Root rount
@app.get("/", tags=['Root'])
def home():
    return {'message': 'Welcome to FastAPI for TTS'}