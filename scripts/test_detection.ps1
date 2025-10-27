param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

Write-Host "Testing file: $(Split-Path $FilePath -Leaf)" -ForegroundColor Yellow
Write-Host ""

# Test 1: Windows Defender scan
try {
    $scanResult = Start-MpScan -ScanPath $FilePath -ScanType QuickScan -ErrorAction Stop
    $threats = Get-MpThreatDetection -ErrorAction SilentlyContinue | Where-Object {$_.Resources -like "*$FilePath*"}
    
    if ($threats) {
        Write-Host "Windows Defender scan: FAILED (Detected)" -ForegroundColor Red
        Write-Host "Threat name: $($threats[0].ThreatName)" -ForegroundColor Red
    } else {
        Write-Host "Windows Defender scan: PASSED (Not detected)" -ForegroundColor Green
    }
} catch {
    Write-Host "Windows Defender scan: PASSED (Not detected)" -ForegroundColor Green
}

# Test 2: String analysis
$strings = & {
    $bytes = [System.IO.File]::ReadAllBytes($FilePath)
    $text = [System.Text.Encoding]::ASCII.GetString($bytes)
    $pattern = 'kernel32|ntdll|VirtualAlloc|CreateProcess|meterpreter'
    [regex]::Matches($text, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
}

if ($strings.Count -gt 0) {
    Write-Host "String analysis: Suspicious strings found" -ForegroundColor Yellow
    Write-Host "Found: $($strings.Count) suspicious strings" -ForegroundColor Yellow
} else {
    Write-Host "String analysis: No suspicious strings found" -ForegroundColor Green
}

# Test 3: Entropy check
$bytes = [System.IO.File]::ReadAllBytes($FilePath)
$entropy = 0
$freq = @{}

foreach ($byte in $bytes) {
    if ($freq.ContainsKey($byte)) {
        $freq[$byte]++
    } else {
        $freq[$byte] = 1
    }
}

foreach ($count in $freq.Values) {
    $p = $count / $bytes.Length
    if ($p -gt 0) {
        $entropy -= $p * [Math]::Log($p, 2)
    }
}

Write-Host "Entropy check: $([Math]::Round($entropy, 1)) " -NoNewline
if ($entropy -gt 7.5) {
    Write-Host "(High - Possibly packed/encrypted)" -ForegroundColor Yellow
} elseif ($entropy -gt 6.0) {
    Write-Host "(Moderate)" -ForegroundColor Green
} else {
    Write-Host "(Low)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Overall result: " -NoNewline
if (-not $threats -and $strings.Count -eq 0 -and $entropy -lt 7.5) {
    Write-Host "Likely to evade signature detection" -ForegroundColor Green
} else {
    Write-Host "May be detected by antivirus" -ForegroundColor Yellow
}
