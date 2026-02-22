param(
  [switch]$UseSQLite = $true,
  [switch]$Bootstrap
)

$root = Split-Path -Parent $PSScriptRoot
if (-not $root) { $root = 'c:\Users\Omen\Desktop\Loyiha' }

$backendCmd = "cd /d $root\backend && " + ($(if($UseSQLite){"set USE_SQLITE=1 && "}else{""})) + ($(if($Bootstrap){"python manage.py migrate && python manage.py seed_demo_users && python manage.py seed_catalog && "}else{""})) + "python manage.py runserver 127.0.0.1:8000"
$frontendCmd = "cd /d $root\frontend && set NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api/v1 && npm run dev"

Start-Process cmd.exe -ArgumentList '/k', $backendCmd
Start-Process cmd.exe -ArgumentList '/k', $frontendCmd

Write-Host 'Backend:  http://127.0.0.1:8000/api/docs/'
Write-Host 'Frontend: http://127.0.0.1:3000'
