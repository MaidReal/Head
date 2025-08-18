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
pip install lark-parser
pip install numpy
pip install empy
pip install catkin_pkg
pip install setuptools wheel
pip install pygame
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
Go to `cuda toolkit <cuda_version>` and pick linux, x86_64, wsl-ubuntu, 2.0, local

follow this guide: `https://www.youtube.com/watch?v=R4m8YEixidI`