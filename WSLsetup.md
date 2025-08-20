# Running WSL

In windows powershell:
```bash
wsl --install
```

then run `code .` to have vs code running

Follow the ros2 installation guidelines

## Terminator:


```bash
# Sudo apt update first
sudo apt update
sudo apt install terminator
```

then just type `terminator` in the terminal
 
color font: #380C2A


## Ros2
Install video: https://www.youtube.com/watch?v=cLpVG51EImQ

to avoid having to source ros2 everytime you open a new terminal:
```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

> [!tip]
> `colcon build --symlink-install` reflects the changes automatically, so you dont have to rebuild it everytime you change something


## Pyenv

```bash

# download all dependencies
sudo apt install -y make build-essential libssl-dev zlib1g-dev   libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm   libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev   libffi-dev liblzma-dev git

# install pyenv
curl https://pyenv.run | bash


# go into bash
nano ~/.bashrc

#add this to it
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

#source the new bash
source ~/.bashrc

# Get the current python version
python3 --version

# Install current python version
pyenv install <version>

# Enable system site-pa+-++-+--+------------------------------------+--++ckages in venv
pyenv virtualenv --system-site-packages <version> ros2_env

# source ros2 if not yet
source /opt/ros/jazzy/setup.bash

pyenv activate ros2_env
```

### Python packages needed:
```bash
python -m pip install --upgrade pip

# for sounddevice
sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt install -y python3-pip portaudio19-dev pulseaudio libpulse-dev


pip install lark-parser numpy empy catkin_pkg setuptools wheel pygame pyyaml sounddevice
```


List of commands for pyenv
```bash
#List of commands for pyenv
deactivate

pyenv activate myenv # name of env
pyenv install 3.10.7
pyenv activate spinup-env

#list all python versions installed by pyenv
pyenv versions

#Creating a virtual environment based on a specific version
pyenv virtualenv <version> <name_of_env>
pyenv virtualenv 3.10.7 rl-env

#list all virtual environments
pyenv virtualenvs
```

## Cuda with WSL
follow this guide: `https://www.youtube.com/watch?v=R4m8YEixidI`

Go to `cuda toolkit <cuda_version>` and pick linux, x86_64, wsl-ubuntu, 2.0, local

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin

sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600

wget https://developer.download.nvidia.com/compute/cuda/12.9.0/local_installers/cuda-repo-wsl-ubuntu-12-9-local_12.9.0-1_amd64.deb

sudo dpkg -i cuda-repo-wsl-ubuntu-12-9-local_12.9.0-1_amd64.deb

sudo cp /var/cuda-repo-wsl-ubuntu-12-9-local/cuda-*-keyring.gpg /usr/share/keyrings/

sudo apt-get update

sudo apt-get -y install cuda-toolkit-12-9
```

### Adding cuda to the PATH:

```bash

#go into bashrc
nano ~/.bashrc

#add 
export PATH=$PATH:/usr/local/cuda/bin

```
restart wsl for it to take effect **or** `source ~/.bashrc`

check with

```bash
echo $PATH
```
at the end it should say **/usr/local/cuda/bin**


## Downloading PyTorch 
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129
```

## Virtual environment debugging

I got no clue how it worked but


```bash
# After you colcon build, check install/package_name/lib/package_name/name_of_the_executable or run
head -1 /home/jeff06/Head/install/text_to_speech/lib/text_to_speech/service
```

If head returns something like `#!/usr/bin/python3` then it's using the systems python, not the virtual environment. 

> [!Note]
> `colcon build` works fine, it properly searches through `setup.cfg` and looks at the `build_scripts`. However, `colcon build --symlink-install` is a dummy and ignores (?) the `build_scripts`. 

## Audio in WSL

### Troubleshooting PulseAudio
Trying to get pulseaudio working on wsl however all of the old and even some of the new resources on google are terrible. 

`WSLg` comes with pulse audio installed as a package (Windows 11 perk). Therefore if you run:
```bash
wsl --version
```
you should get something with WSLg

then inside of your WSL, just run 
```bash
export PULSE_SERVER=unix:/mnt/wslg/PulseServer
```

To test it run:
```bash
paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga 

# or 
paplay /usr/share/sounds/alsa/Front_Center.wav 
```

you should hear sounds coming from the desktop speaker.

### Installing Pulseaudio
```bash
sudo apt install -y pulseaudio-utils
```

test recording audio with:
```bash
parecord --device=2 test.wav

# to find the device, (RDPSource is the mic). SUSPENDED means it will be turned on when you start recording
pactl list short sources
```

Listen to it:
```bash
paplay test.wav
```

## VAD (Silero)
No need to install it if you alread have pytorch installed

## Transcriber (Whisper OpenAI)

```bash
pip install -U openai-whisper
```

```bash
sudo apt update && sudo apt install ffmpeg
```

> [!Note]
> So easy to setup omg i love OpenAI