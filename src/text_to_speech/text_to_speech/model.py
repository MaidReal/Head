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

# model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-hybrid", device="cuda")
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device="cuda")

wav, sampling_rate = torchaudio.load(audio_path)
speaker = model.make_speaker_embedding(wav, sampling_rate)

cond_dict = make_cond_dict(text="Hello, world!", speaker=speaker, language="en-us")
conditioning = model.prepare_conditioning(cond_dict)

codes = model.generate(conditioning)

wavs = model.autoencoder.decode(codes).cpu()
torchaudio.save("sample.wav", wavs[0], model.autoencoder.sampling_rate)