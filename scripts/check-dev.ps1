$backend = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
$frontend = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue

if ($backend) {
  Write-Host 'Backend listening on 8000'
} else {
  Write-Host 'Backend NOT running on 8000'
}

if ($frontend) {
  Write-Host 'Frontend listening on 3000'
} else {
  Write-Host 'Frontend NOT running on 3000'
}
