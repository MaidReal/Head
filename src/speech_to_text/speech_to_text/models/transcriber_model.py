import whisper

class WhisperModel():
    def __init__(self):
        self.model = whisper.load_model("tiny.en")
    
    def transcribe(self, path):
        result = self.model.transcribe(path)
        return result