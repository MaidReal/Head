import torch
import torchaudio
import sys
import os


workspace_root = '/home/jeff06/Head'
if workspace_root is None:
    raise RuntimeError("Environment variable WORKSPACE_ROOT not set")
zonos_path = os.path.join(workspace_root, 'src', 'resources', 'Zonos')
audio_path = os.path.join(zonos_path, 'assets/exampleaudio.mp3')
sys.path.insert(0, zonos_path)

from zonos.model import Zonos
from zonos.conditioning import make_cond_dict

class ZonosModel():
    def __init__(self):
        self.model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device="cuda")
        wav, sampling_rate = torchaudio.load(audio_path)
        self.speaker = self.model.make_speaker_embedding(wav, sampling_rate)

    def generate_audio(self, text):
        cond_dict = make_cond_dict(text=text, speaker=self.speaker, language="en-us")
        conditioning = self.model.prepare_conditioning(cond_dict)
        codes = self.model.generate(conditioning)
        wavs = self.model.autoencoder.decode(codes).cpu()
        
        save_dir = os.path.expanduser("~/Head/src/text_to_speech/text_to_speech")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, "sample.wav")


        torchaudio.save(save_path, wavs[0], self.model.autoencoder.sampling_rate)