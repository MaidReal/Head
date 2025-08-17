import torch
import torchaudio
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
zonos_path = os.path.join(parent_dir, 'resources/Zonos')
audio_path = os.path.join(zonos_path, 'assets/exampleaudio.mp3')
sys.path.insert(0, zonos_path)

from zonos.model import Zonos
from zonos.conditioning import make_cond_dict

class ZonosModel():
    def __init__():
        self.model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device="cuda")
        wav, sampling_rate = torchaudio.load(audio_path)
        self.speaker = self.model.make_speaker_embedding(wav, sampling_rate)

    def generate_audio(text):
        cond_dict = make_cond_dict(text=text, speaker=self.speaker, language="en-us")
        conditioning = self.model.prepare_conditioning(cond_dict)
        codes = self.model.generate(conditioning)
        wavs = self.model.autoencoder.decode(codes).cpu()

        torchaudio.save("/src/text_to_speech/text_to_speech/sample.wav", wavs[0], self.model.autoencoder.sampling_rate)
        