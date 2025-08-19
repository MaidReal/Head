import whisper

model = whisper.load_model("turbo")
result = model.transcribe("recorded_audio.wav")
# print(result["text"])
print(result)