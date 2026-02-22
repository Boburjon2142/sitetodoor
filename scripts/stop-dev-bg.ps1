$root = Split-Path -Parent $PSScriptRoot
if (-not $root) { $root = 'c:\Users\Omen\Desktop\Loyiha' }

$pidFile = Join-Path $root '.run\pids.json'
if (Test-Path $pidFile) {
  $pids = Get-Content $pidFile | ConvertFrom-Json
  foreach ($procId in @($pids.backend_pid, $pids.frontend_pid)) {
    if ($procId) {
      Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    }
  }
  Remove-Item $pidFile -Force
}
Write-Host 'Stopped backend/frontend processes.'
