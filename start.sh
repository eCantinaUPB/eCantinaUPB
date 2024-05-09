#!/bin/sh

PYTHON_EXECUTABLE="python3"
VENV_DIR="venv"

if [[ ! -d $VENV_DIR ]]; then
  echo "No venv found, creating one"
  $PYTHON_EXECUTABLE -m venv $VENV_DIR

  echo "Installing dependencies via pip"
  source $VENV_DIR/bin/activate
  $PYTHON_EXECUTABLE -m pip install -r requirements.txt
fi

source $VENV_DIR/bin/activate
$PYTHON_EXECUTABLE eCantinaUPB
