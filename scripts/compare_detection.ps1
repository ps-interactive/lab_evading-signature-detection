Write-Host "Detection Comparison Results:" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

$payloads = @(
    "basic_payload.exe",
    "encoded_v1.exe",
    "encoded_v5.exe",
    "obfuscated_v1.exe",
    "advanced_obfuscated.exe"
)

$results = @()
$successCount = 0

foreach ($payload in $payloads) {
    $filePath = "C:\Users\Public\Desktop\$payload"
    
    if (Test-Path $filePath) {
        try {
            # Quick scan
            $null = Start-MpScan -ScanPath $filePath -ScanType QuickScan -ErrorAction Stop
            $threats = Get-MpThreatDetection -ErrorAction SilentlyContinue | Where-Object {$_.Resources -like "*$payload*"}
            
            if ($threats) {
                $status = "DETECTED"
                $details = "($($threats[0].ThreatName))"
                $color = "Red"
            } else {
                $status = "NOT DETECTED"
                $details = "(Signature bypass)"
                $color = "Green"
                $successCount++
            }
        } catch {
            $status = "NOT DETECTED"
            $details = "(Clean)"
            $color = "Green"
            $successCount++
        }
        
        $result = [PSCustomObject]@{
            Payload = $payload
            Status = $status
            Details = $details
        }
        $results += $result
        
        Write-Host "$($payload.PadRight(28)): $status $details" -ForegroundColor $color
    }
}

Write-Host ""
Write-Host "Success Rate: $successCount/$($payloads.Count) payloads evaded detection" -ForegroundColor Cyan

# Find most effective
$effective = $results | Where-Object {$_.Status -eq "NOT DETECTED"} | Select-Object -Last 1
if ($effective) {
    Write-Host "Most effective: $($effective.Payload)" -ForegroundColor Green
}
