import torch
import torchaudio
import sounddevice as sd
import numpy as np
from pathlib import Path
import wave

# Load Silero VAD model
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True)
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

# Parameters
SAMPLE_RATE = 16000  # Silero VAD requires 16 kHz
CHUNK_DURATION = 1  # seconds, shorter chunk times didn't work as well
CHANNELS = 1
WAV_OUTPUT_PATH = 'recorded_audio.wav'

# Buffer for recorded audio
recorded_audio = []

def audio_callback(indata, frames, time, status):
    """This callback runs for each audio chunk from the microphone"""
    if status:
        print(status)
    # Flatten the data to 1D and convert to float32
    audio_chunk = indata[:, 0].astype(np.float32)
    
    # Convert to torch tensor
    audio_tensor = torch.from_numpy(audio_chunk)
    # Get speech timestamps
    speech_timestamps = get_speech_timestamps(audio_tensor, model, sampling_rate=SAMPLE_RATE)
    if speech_timestamps:
        print("Speaking...")
        recorded_audio.extend(audio_chunk)
    else:
        print("Silent...")

# Start recording
print("Recording... Press Ctrl+C to stop.")
try:
    with sd.InputStream(channels=CHANNELS, samplerate=SAMPLE_RATE, callback=audio_callback, blocksize=int(SAMPLE_RATE*CHUNK_DURATION)):
        while True:
            sd.sleep(500)
            # pass
except KeyboardInterrupt:
    print("Recording stopped.")

# Save the recorded audio to WAV
recorded_audio_np = np.array(recorded_audio)
recorded_audio_np = (recorded_audio_np * 32767).astype(np.int16)  # convert to 16-bit PCM

with wave.open(WAV_OUTPUT_PATH, 'w') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 16-bit
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(recorded_audio_np.tobytes())

print(f"Audio saved to {WAV_OUTPUT_PATH}")