export PATH=$PATH:$PWD/bin:$PWD/test
export CSPY_PATH=$PWD

if [[ "$OSTYPE" == "linux-gnu" ]]; then
  source .venv-linux/bin/activate
else
  source .venv-osx/bin/activate
fi
