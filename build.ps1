$ErrorActionPreference = "Stop"
if (-not (Test-Path ".venv")) { py -3.12 -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
& .\.venv\Scripts\python.exe -m pytest
& .\.venv\Scripts\pyinstaller.exe --noconfirm --clean --onefile --windowed --collect-all customtkinter --name "RAEV-Shield" --paths src src\raev_shield\__main__.py
if (Get-Command iscc -ErrorAction SilentlyContinue) {
  iscc installer.iss
  Write-Host "Instalador creado en installer-output\RAEV-Shield-Setup.exe"
} else {
  Write-Host "Ejecutable portable creado en dist\RAEV-Shield.exe (Inno Setup no está instalado)."
}
