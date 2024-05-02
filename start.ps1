$PYTHON_EXECUTABLE = "py"
$VENV_DIR = "venv"

if (!(Test-Path $VENV_DIR -PathType Container)) {
  Write-Host "No venv found, creating one"
  & $PYTHON_EXECUTABLE -m venv $VENV_DIR

  Write-Host "Installing dependencies via pip"
  & "$VENV_DIR\Scripts\Activate.ps1"
  & $PYTHON_EXECUTABLE -m pip install -r requirements.txt
}

& "$VENV_DIR\Scripts\Activate.ps1"
& $PYTHON_EXECUTABLE eCantinaUPB
