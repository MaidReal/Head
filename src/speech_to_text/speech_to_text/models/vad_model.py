import torch
import torchaudio
import sounddevice as sd
import numpy as np
from pathlib import Path
import wave

class SileroModel():
    # Buffer for recorded audio
    recorded_audio = [] #class instance
    def __init__(self):        
        # Load Silero VAD model
        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True)
        (self.get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

        # Parameters
        self.SAMPLE_RATE = 16000  # Silero VAD requires 16 kHz
        self.CHUNK_DURATION = 1  # seconds, shorter chunk times didn't work as well
        self.CHANNELS = 1
        
        self.speaking = False
        
        self.stream = sd.InputStream(
            channels=self.CHANNELS,
            samplerate=self.SAMPLE_RATE,
            blocksize=int(self.SAMPLE_RATE * self.CHUNK_DURATION),
            callback=self.audio_callback
        )
        
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        """This callback runs for each audio chunk from the microphone"""
        if status:
            print(status)
        # Flatten the data to 1D and convert to float32
        audio_chunk = indata[:, 0].astype(np.float32)
        
        # Convert to torch tensor
        audio_tensor = torch.from_numpy(audio_chunk)
        # Get speech timestamps
        speech_timestamps = self.get_speech_timestamps(audio_tensor, self.model, sampling_rate=self.SAMPLE_RATE)
        if speech_timestamps:
            SileroModel.recorded_audio.extend(audio_chunk)
            self.speaking = True            
        else:
            self.speaking = False
           
    def get_is_speaking(self):
        return self.speaking
        
    def save_recording(self, path):
        # Save the recorded audio to WAV
        recorded_audio_np = np.array(SileroModel.recorded_audio)
        recorded_audio_np = (recorded_audio_np * 32767).astype(np.int16)  # convert to 16-bit PCM

        with wave.open(path, 'w') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.SAMPLE_RATE)
            wf.writeframes(recorded_audio_np.tobytes())
        
        SileroModel.recorded_audio = [] # erase all previous conversation