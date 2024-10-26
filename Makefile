UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
  VENV_DIR=.venv-linux
else
  VENV_DIR=.venv-osx
endif

init: $(VENV_DIR) nvm
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install --upgrade -r requirements.txt

$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

nvm: ~/.nvm
	. ${HOME}/.nvm/nvm.sh && nvm install v16 && nvm use v16

~/.nvm:
	$(shell curl \
          https://raw.githubusercontent.com/creationix/nvm/master/install.sh \
          | bash)
	$(shell cat nvm.txt >> ~/.zshrc)
	$(error You need to log out and log back in or source .zshrc)

local:
	jupyter-lab --ip 0.0.0.0

clean:
	rm -rf .venv
