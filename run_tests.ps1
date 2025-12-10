# PowerShell helper to run tests in a fresh venv
$venvPath = "./.venv"
if (-Not (Test-Path $venvPath)) {
    python -m venv $venvPath
}
$activate = "$venvPath\Scripts\Activate.ps1"
if (Test-Path $activate) {
    & $activate
} else {
    Write-Host "Activation script not found. Activate your venv manually."
}

pip install -r requirements.txt
pip install pytest
pytest -q
