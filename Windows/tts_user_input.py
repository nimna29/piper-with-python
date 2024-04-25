import subprocess
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from io import BytesIO

def text_to_speech(user_text):
    output_file = "./audio/tts_output.wav"
    piper_path = "./piper/piper.exe"
    model_path = "./voice_models/en_US-ryan-medium.onnx"
    config_path = "./voice_models/en_en_US_ryan_medium_en_US-ryan-medium.onnx.json"

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

    # Playe Audio: If you don't need remove this block
    play_audio(output_file)


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


if __name__ == "__main__":
    user_text = input("Enter the text for TTS: ")

    text_to_speech(user_text)
