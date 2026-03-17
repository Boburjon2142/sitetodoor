$root = 'c:\Users\Omen\Desktop\Loyiha'
$appDir = Join-Path $root 'python_html_app'
$venvPython = Join-Path $appDir '.venv\Scripts\python.exe'

Set-Location $appDir

if (-not (Test-Path $venvPython)) {
  python -m venv .venv
}

& $venvPython -m pip install --disable-pip-version-check -r requirements.txt

if (-not (Test-Path '.env')) {
  Copy-Item '.env.example' '.env'
}

Get-Content '.env' | ForEach-Object {
  if ($_ -match '^\s*([^#=]+)=(.*)$') {
    [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim())
  }
}

[System.Environment]::SetEnvironmentVariable('DEBUG', '1')
[System.Environment]::SetEnvironmentVariable('ALLOWED_HOSTS', '127.0.0.1,localhost,testserver')

Write-Host ''
Write-Host 'Loyiha ishga tushmoqda:'
Write-Host '  http://127.0.0.1:5050'
Write-Host 'Oynani yopmang.'
Write-Host ''

& $venvPython manage.py migrate
& $venvPython manage.py seed_marketplace
& $venvPython manage.py runserver 127.0.0.1:5050 --noreload
