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

# Get the current python version
python3 --version

# Install current python version
pyenv install <version>

# Enable system site-packages in venv
pyenv virtualenv --system-site-packages <version> ros2env

# source ros2 if not yet
source /opt/ros/jazzy/setup.bash

pyenv activate ros2env
```

### Python packages needed:
```bash
python -m pip install --upgrade pip

pip install lark-parser numpy empy catkin_pkg setuptools wheel pygame
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
restart wsl for it to take effect


## Downloading PyTorch 
```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu129
```