import whisper
import os

model = whisper.load_model("base")

def extract_audio_text(file_path):
    result = model.transcribe(file_path)
    return [{
        "text": result["text"],
        "page": "audio",
        "source": os.path.basename(file_path)
    }]
