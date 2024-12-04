#! /usr/bin/env bash

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y direnv libusb-1.0-0-dev python3-venv
sudo apt install -y zsh mosh tio tmux

if [ ! -d ~/.oh-my-zsh ]; then
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  cat <<'EOF' >> ~/.zshrc

### needs to be the last thing in the .bashrc file ###
### adds direnv ###
if [ -x "$(command -v direnv)" ]; then
  eval "$(direnv hook $SHELL)"
fi

EOF

else
  echo '-----------------------------------------'
  echo 'Oh My Zsh and direnv already installed'
  echo '-----------------------------------------'
fi

