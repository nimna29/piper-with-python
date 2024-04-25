import subprocess
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from io import BytesIO

# Project path
project_path = os.path.dirname(os.path.abspath(__file__))

def text_to_speech(user_text, file_name):
    output_file_dir = os.path.join(project_path, "audio")
    output_file = os.path.join(output_file_dir, f"{file_name}.wav")
    
    piper_dir = os.path.join(project_path, "piper")
    piper_path = os.path.join(piper_dir, "piper.exe")
    
    voice_models_dir = os.path.join(project_path, "voice_models")
    model_path = os.path.join(voice_models_dir, "en_US-ryan-medium.onnx") # Change the model path if you are using a different model
    config_path = os.path.join(voice_models_dir, "en_en_US_ryan_medium_en_US-ryan-medium.onnx.json") # Change the config path if you are using a different model

    command = [
        piper_path,
        "-m", model_path,
        "-c", config_path,
        "-f", output_file
    ]

    try:
        # Use subprocess.PIPE to pass user_text to Piper's stdin
        with subprocess.Popen(command, stdin=subprocess.PIPE, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            p.communicate(input=user_text)
            p.wait()
    except subprocess.CalledProcessError as e:
        print(f"Error running Piper TTS: {e}")
    else:
        print(f"\nTTS: {user_text}")
        
        return output_file


# Function to play audio from the file
def play_audio(output_file):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the generated audio file into a BytesIO object
    with open(output_file, "rb") as audio_file:
        audio_data = BytesIO(audio_file.read())

    # Load the audio data into pygame mixer
    pygame.mixer.music.load(audio_data)
    
    # Play the audio
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

