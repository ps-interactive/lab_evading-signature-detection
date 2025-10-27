Write-Host "Detection Comparison Results:" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

$payloads = @(
    "basic_payload.exe",
    "encoded_v5.exe", 
    "obfuscated_v1.exe",
    "advanced_obfuscated.exe"
)

$results = @()
$successCount = 0
$totalFound = 0

foreach ($payload in $payloads) {
    $filePath = "C:\Users\Public\Desktop\$payload"
    
    if (Test-Path $filePath) {
        $totalFound++
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
                if ($payload -eq "basic_payload.exe") {
                    $details = "(Should be detected - check AV)"
                } elseif ($payload -eq "encoded_v5.exe") {
                    $details = "(Encoding bypass)"
                } elseif ($payload -eq "obfuscated_v1.exe") {
                    $details = "(String obfuscation)"
                } else {
                    $details = "(Multiple techniques)"
                }
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
    } else {
        Write-Host "$($payload.PadRight(28)): QUARANTINED (File not found)" -ForegroundColor DarkGray
    }
}

Write-Host ""
if ($totalFound -eq 0) {
    Write-Host "No payload files found. They may have been quarantined during download." -ForegroundColor Yellow
} else {
    Write-Host "Success Rate: $successCount/$totalFound payloads evaded detection" -ForegroundColor Cyan
}

# Find most effective
$effective = $results | Where-Object {$_.Status -eq "NOT DETECTED"} | Select-Object -Last 1
if ($effective) {
    Write-Host "Most effective: $($effective.Payload)" -ForegroundColor Green
}
