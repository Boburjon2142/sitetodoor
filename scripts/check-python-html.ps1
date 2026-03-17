$listener = Get-NetTCPConnection -LocalPort 5050 -State Listen -ErrorAction SilentlyContinue

if ($listener) {
  Write-Host 'Loyiha 5050 portda ishlayapti'
} else {
  Write-Host 'Loyiha 5050 portda ishlamayapti'
}
