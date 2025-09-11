# Project Description
This project provides a wrapper for large language models (LLMs) and related audio processing tools. It is designed for Ubuntu and WSL2, supporting GPU acceleration and audio workflows for speech-to-text, text-to-speech, and model conversion.

---

## Dependencies
- Ubuntu 24 or WSL2 (Windows Subsystem for Linux)
- Python (recommended: pyenv)
- CUDA toolkit (for GPU support)
- PulseAudio (for audio in WSL)
- PyTorch
- Required Python packages: lark-parser, numpy, empy, catkin_pkg, setuptools, wheel, pygame, pyyaml, sounddevice
- FFmpeg
- Terminator

---

## Quick Setup
### Option A: Automated (only tested with wsl)
Make `setup.sh` executable and run:
```bash
chmod +x setup.sh
./setup.sh
```

### Option B: Manual
#### 1. WSL & Python Environment
- Install WSL in Windows Powershell:
  ```bash
  wsl --install
  ```
- Install pyenv dependencies:
  ```bash
  sudo apt update
  sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git
  ```
- Install pyenv:
  ```bash
  curl https://pyenv.run | bash
  ```
- Add to `~/.bashrc`:
  ```bash
  export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
  source ~/.bashrc
  ```
- Install and activate Python:
  ```bash
  pyenv install <version>
  pyenv virtualenv <version> <env_name>
  pyenv activate <env_name>
  ```

## Submodules setup
To grab all of the submodules just run:
```bash
git submodule update --init
```

#### 2. Python Packages
Upgrade pip and install requirements:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt --upgrade
pip install --user -U nltk

python src/lip_sync/misc/download_nltk.py
```

#### 3. Audio in WSL
- For PulseAudio (WSLg):
  ```bash
  export PULSE_SERVER=unix:/mnt/wslg/PulseServer
  paplay /usr/share/sounds/alsa/Front_Center.wav
  ```
- Install PulseAudio utilities:
  ```bash
  sudo apt install -y pulseaudio-utils
  ```

#### 4. CUDA Toolkit (12.9 Example)
Follow official instructions or:
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.9.0/local_installers/cuda-repo-wsl-ubuntu-12-9-local_12.9.0-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-12-9-local_12.9.0-1_amd64.deb
sudo cp /var/cuda-repo-wsl-ubuntu-12-9-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-9
```
- Add CUDA to PATH:
  ```bash
  nano ~/.bashrc
  export PATH=$PATH:/usr/local/cuda/bin
  source ~/.bashrc
  ```

#### 5. PyTorch
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129
```

#### 6. Additional Tools 
- Terminator: `sudo apt install terminator` (optional)
- FFmpeg: `sudo apt update && sudo apt install ffmpeg`
---

## Run files
Export workspace root for zonos:
```bash
export WORKSPACE_ROOT=/ # Add path to your ros2_ws here
```

in root directory (Head) run:
```bash
colcon build
```

source install:
```bash
source install/setup.bash
```
### Gaze tracking
```bash
ros2 run gaze_tracking head_tracker
```

### Lip Sync
```bash
ros2 run lip_sync lip_sync_sub
```

### Brain

Server:
```bash
llama-server -m models/gpt-oss-20b.gguf --jinja -ngl 99 -fa --n-cpu-moe
```

Bridge:
```bash
ros2 launch brain llama_bridge.launch.py
```

### Text to Speech 
```bash
ros2 run text_to_speech service
```

### Speech to Text

Listen through microphone:
```bash
ros2 run speech_to_text listener
```

Running the model:
```bash
ros2 run speech_to_text stt_model
```


## Notes
- For ROS2 setup, see official documentation and consider adding `source /opt/ros/jazzy/setup.bash` to your `~/.bashrc`.
- For troubleshooting audio, use `parecord` and `paplay`.
- For model conversion and usage, refer to the scripts and documentation in the repository.
