$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
if (-not $root) { $root = 'c:\Users\Omen\Desktop\Loyiha' }

$runDir = Join-Path $root '.run'
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

$backendOut = Join-Path $runDir 'backend.out.log'
$backendErr = Join-Path $runDir 'backend.err.log'
$frontendOut = Join-Path $runDir 'frontend.out.log'
$frontendErr = Join-Path $runDir 'frontend.err.log'
$pidFile = Join-Path $runDir 'pids.json'

$stopScript = Join-Path $PSScriptRoot 'stop-dev-bg.ps1'
if (Test-Path $stopScript) {
  & powershell -ExecutionPolicy Bypass -File $stopScript | Out-Null
}

$env:USE_SQLITE = '1'
Set-Location (Join-Path $root 'backend')
python manage.py migrate | Out-Null
python manage.py seed_demo_users | Out-Null
python manage.py seed_catalog | Out-Null

$backend = Start-Process -FilePath python -WorkingDirectory (Join-Path $root 'backend') -ArgumentList 'manage.py','runserver','127.0.0.1:8000' -RedirectStandardOutput $backendOut -RedirectStandardError $backendErr -PassThru
$frontendCmd = "set NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api/v1 && npm run dev"
$frontend = Start-Process -FilePath cmd.exe -WorkingDirectory (Join-Path $root 'frontend') -ArgumentList '/c', $frontendCmd -RedirectStandardOutput $frontendOut -RedirectStandardError $frontendErr -PassThru

$data = @{ backend_pid = $backend.Id; frontend_pid = $frontend.Id } | ConvertTo-Json
Set-Content -Path $pidFile -Value $data

Start-Sleep -Seconds 8
Write-Host "Backend:  http://127.0.0.1:8000/api/docs/"
Write-Host "Frontend: http://127.0.0.1:3000"
Write-Host "Logs:     $runDir"
