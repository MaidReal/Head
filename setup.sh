#!/usr/bin/env bash
set -euo pipefail


# -------- configurable defaults --------
PYTHON_VERSION="${PYTHON_VERSION:-3.12.3}"  # override: PYTHON_VERSION=3.11.9 ./setup.sh
VENV_NAME="${VENV_NAME:-ros2_env}"
INSTALL_TORCH_CUDA="${INSTALL_TORCH_CUDA:-1}"  # set to 0 to skip CUDA + Torch CUDA wheels
ROS_DISTRO="${ROS_DISTRO:-jazzy}"             # used for the .bashrc hint
# ---------------------------------------


echo "=== Updating apt ==="
sudo apt-get update -y


echo "=== Installing system deps (audio, dev tools) ==="
sudo apt-get install -y \
  libportaudio2 libportaudiocpp0 portaudio19-dev pulseaudio libpulse-dev pulseaudio-utils ffmpeg \
  make build-essential curl git ca-certificates \
  libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
  libffi-dev liblzma-dev libncursesw5-dev xz-utils tk-dev \
  llvm libxml2-dev libxmlsec1-dev \
  python3-pip python3-venv


echo "=== Installing/Updating pyenv ==="
if [ ! -d "${HOME}/.pyenv" ]; then
  curl -fsSL https://pyenv.run | bash
else
  echo "pyenv already present at ~/.pyenv"
fi


# Make pyenv available in THIS script run
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"


# Idempotently add pyenv init to ~/.bashrc
if ! grep -q 'PYENV_ROOT="$HOME/.pyenv"' "$HOME/.bashrc" 2>/dev/null; then
  {
    echo ''
    echo '# >>> pyenv init >>>'
    echo 'export PYENV_ROOT="$HOME/.pyenv"'
    echo '[[ -d "$PYENV_ROOT/bin" ]] && export PATH="$PYENV_ROOT/bin:$PATH"'
    echo 'eval "$(pyenv init -)"'
    echo '# <<< pyenv init <<<'
  } >> "$HOME/.bashrc"
  echo "Appended pyenv init to ~/.bashrc"
fi


echo "=== Installing Python ${PYTHON_VERSION} via pyenv ==="
pyenv install -s "${PYTHON_VERSION}"
pyenv virtualenv --system-site-packages "${PYTHON_VERSION}" "${VENV_NAME}"


# Activate the virtual environment
pyenv activate "${VENV_NAME}"
python -m pip install --upgrade pip


echo "=== Installing Python requirements ==="
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  echo "WARNING: requirements.txt not found; skipping."
fi


if [ "${INSTALL_TORCH_CUDA}" = "1" ]; then
  echo "=== Installing CUDA Toolkit 12.9 ==="
  wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
  sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
  wget https://developer.download.nvidia.com/compute/cuda/12.9.0/local_installers/cuda-repo-wsl-ubuntu-12-9-local_12.9.0-1_amd64.deb
  sudo dpkg -i cuda-repo-wsl-ubuntu-12-9-local_12.9.0-1_amd64.deb
  sudo cp /var/cuda-repo-wsl-ubuntu-12-9-local/cuda-*-keyring.gpg /usr/share/keyrings/
  sudo apt-get update
  sudo apt-get -y install cuda-toolkit-12-9


  # Add CUDA to PATH if not already in .bashrc
  if ! grep -q '/usr/local/cuda/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH=$PATH:/usr/local/cuda/bin' >> "$HOME/.bashrc"
    echo "Added CUDA bin path to ~/.bashrc"
  fi


  echo "=== Installing PyTorch CUDA 12.9 wheels ==="
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129
else
  echo "Skipping CUDA + Torch install (INSTALL_TORCH_CUDA=${INSTALL_TORCH_CUDA})"
fi


echo "=== Setting up locale for ROS 2 ==="
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
locale


echo "=== Adding ROS 2 apt source ==="
sudo apt install -y software-properties-common
sudo add-apt-repository universe


sudo apt update && sudo apt install -y curl
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb \
  "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb


echo "=== Installing ROS 2 Jazzy Desktop ==="
sudo apt update
sudo apt install -y ros-dev-tools
sudo apt upgrade -y
sudo apt install -y ros-jazzy-desktop


echo "=== Adding ROS 2 sourcing to ~/.bashrc (idempotent) ==="
if [ -f "/opt/ros/${ROS_DISTRO}/setup.bash" ] && ! grep -q "/opt/ros/${ROS_DISTRO}/setup.bash" "$HOME/.bashrc" 2>/dev/null; then
  echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> "$HOME/.bashrc"
  echo "Added: source /opt/ros/${ROS_DISTRO}/setup.bash"
else
  echo "ROS 2 setup not added (either file missing or already present)."
fi


echo "=== Done ✅ ==="
echo "Activate your venv with:  pyenv activate ${VENV_NAME}"
echo "If you just installed CUDA or ROS 2, restart WSL or run:  source ~/.bashrc"