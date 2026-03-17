$listeners = Get-NetTCPConnection -LocalPort 5050 -State Listen -ErrorAction SilentlyContinue

foreach ($listener in $listeners) {
  Stop-Process -Id $listener.OwningProcess -Force -ErrorAction SilentlyContinue
}

Write-Host 'Stopped app on port 5050 (if it was running).'
