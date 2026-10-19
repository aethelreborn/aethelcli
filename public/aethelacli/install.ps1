# aethelcli Windows installer
# irm https://darkie.dpdns.org/aethelacli/install.ps1 | iex

$ErrorActionPreference = "Stop"
$Repo      = "https://github.com/aethelreborn/aethelcli.git"
$InstallDir = "$env:LOCALAPPDATA\aethelcli"
$BinDir     = "$env:LOCALAPPDATA\aethelcli\bin"

function Write-Banner {
@"
    ___         __  __         __     ___   ____
   /   |  ___  / /_/ /_  ___  / /    /   | /  _/
  / /| | / _ \/ __/ __ \/ _ \/ /    / /| | / /  
 / ___ |/  __/ /_/ / / /  __/ /    / ___ |_/ /   
/_/  |_|\___/\__/_/ /_/\___/_/    /_/  |_/___/   
                                                 
          aethelcli · darkie.dpdns.org
"@
}

Write-Banner
Write-Host ""
Write-Host "[*] installing aethelcli → $InstallDir" -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[-] python not found. install Python 3.11+ and re-run." -ForegroundColor Red
    exit 1
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[-] git not found. install Git for Windows and re-run." -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Force -Path $InstallDir, $BinDir | Out-Null
$tmp = Join-Path $env:TEMP ("aethelcli-" + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Force -Path $tmp | Out-Null

Write-Host "[*] cloning source" -ForegroundColor Cyan
git clone --depth 1 $Repo "$tmp\src"
if (-not $?) { Write-Host "[-] clone failed" -ForegroundColor Red; exit 1 }

if (Test-Path "$InstallDir\aethelcli") { Remove-Item -Recurse -Force "$InstallDir\aethelcli" }
Copy-Item -Recurse -Force "$tmp\src\aethelcli" "$InstallDir\"
Copy-Item -Force "$tmp\src\requirements.txt" "$InstallDir\" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force $tmp

Write-Host "[*] creating virtualenv" -ForegroundColor Cyan
python -m venv "$InstallDir\venv"
& "$InstallDir\venv\Scripts\python.exe" -m pip install --upgrade pip -q
& "$InstallDir\venv\Scripts\python.exe" -m pip install rich requests customtkinter pillow psutil -q

$launcher = @"
@echo off
set PYTHONPATH=$InstallDir;%PYTHONPATH%
"$InstallDir\venv\Scripts\python.exe" -m aethelcli %*
"@
Set-Content -Path "$BinDir\aethelcli.bat" -Value $launcher -Encoding ASCII

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$BinDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$BinDir", "User")
    $env:Path += ";$BinDir"
}

Write-Host "[*] sending install telemetry" -ForegroundColor Cyan
$env:PYTHONPATH = $InstallDir
& "$InstallDir\venv\Scripts\python.exe" -c @"
import sys
sys.path.insert(0, r'$InstallDir')
try:
    from aethelcli.webhook import report_install
    report_install()
except Exception as e:
    print('[!] webhook skipped:', e)
"@

Write-Host "[+] installed" -ForegroundColor Green
Write-Host ""
Write-Host "  run:  aethelcli"
Write-Host "  gui:  aethelcli --gui"
Write-Host ""
& "$BinDir\aethelcli.bat"
