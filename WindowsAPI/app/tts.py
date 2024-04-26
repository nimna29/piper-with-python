import subprocess
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pydub import AudioSegment

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
        
        # Call convert_to_pcm function after TTS conversion
        output_file_converted = convert_to_pcm(output_file)
        
        return output_file_converted


# Function to convert audio to PCM format
def convert_to_pcm(output_file):
    # Load the WAV audio file
    audio = AudioSegment.from_file(output_file)

    # Set parameters for PCM WAV format
    audio = audio.set_sample_width(2)  # 16-bit PCM
    audio = audio.set_frame_rate(44100)  # 44.1 kHz sample rate

    # Define the new file name with "converted" suffix
    output_file_converted = os.path.splitext(output_file)[0] + "_converted.wav"

    # Export the audio as PCM WAV
    audio.export(output_file_converted, format="wav")
    print("\nAudio saved successfully as PCM WAV format!")

    # Delete the original WAV file
    os.remove(output_file)
    
    return output_file_converted