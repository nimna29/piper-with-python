from fastapi import FastAPI, File, UploadFile, Response, HTTPException
import shutil
import os
from .tts import text_to_speech

app = FastAPI(
    title="FastAPI for TTS",
    description="FastAPI for Text-to-Speech (TTS) using Piper",
    version="0.0.0"
)

# Project path
project_path = os.path.dirname(os.path.abspath(__file__))
audio_folder = os.path.join(project_path, "audio")


# Root route
@app.get("/", tags=['Root'])
def home():
    return {'message': 'Welcome to FastAPI for TTS'}


# Route to handle file upload and text-to-speech conversion
@app.post("/tts/", tags=["Text-to-Speech"])
async def text_file_to_speech(
    file_name: str, 
    file: UploadFile = File(...)
    ):
    
    try:
        # Create a directory to store uploaded files if it doesn't exist
        upload_folder = os.path.join(project_path, "upload")
        os.makedirs(upload_folder, exist_ok=True)

        # Save the uploaded file
        upload_file_path = os.path.join(upload_folder, file.filename)
        with open(upload_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read the content of the uploaded file
        with open(upload_file_path, "r") as uploaded_file:
            user_text = uploaded_file.read()

        # Call the text_to_speech function with the extracted text and file name
        output_file_path = text_to_speech(user_text, file_name)

        # Delete the uploaded file after processing
        os.remove(upload_file_path)

        # Return a response with a download link to the generated audio file
        audio_file_name = os.path.basename(output_file_path)
        return Response(
            content=output_file_path, 
            headers={"Content-Disposition": f"attachment; filename={audio_file_name}"},
            )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Uploaded file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to view all audio files with download option
@app.get("/view-audio/", tags=["View All Audio Files"])
async def view_all_audio_files():
    try:
        # Get all files in the audio folder
        audio_files = os.listdir(audio_folder)
        # Return the list of audio files
        return {"audio_files": audio_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to delete specific file inside the audio folder
@app.delete("/delete-audio/{file_name}", tags=["Delete Specific Audio File"])
async def delete_audio_file(file_name: str):
    try:
        # Check if the file exists in the audio folder
        file_name = f"{file_name}.wav"
        file_path = os.path.join(audio_folder, file_name)
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            return {"message": f"File {file_name} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route to delete all files inside the audio folder
@app.delete("/delete-all/", tags=["Delete All Audio Files"])
async def delete_all_audio_files():
    try:
        # Iterate over all files in the audio folder and delete them
        for filename in os.listdir(audio_folder):
            file_path = os.path.join(audio_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return {"message": "All audio files deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))