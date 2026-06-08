param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Password
)

$dataInDir = Join-Path $PSScriptRoot "data\in"
$files = Get-ChildItem -Path $dataInDir -File

$gitUrls = @()
foreach ($file in $files) {
    $matches = Select-String -Path $file.FullName -Pattern 'https?://(github\.com|gitlab\.com)/\S+' -AllMatches
    foreach ($match in $matches.Matches) {
        $gitUrls += $match.Value
    }
}

$gitUrls = $gitUrls | Sort-Object -Unique

Write-Host "Found $($gitUrls.Count) unique git URLs to mirror."

foreach ($url in $gitUrls) {
    Write-Host "Mirroring: $url"
    $FormParameters = @{
        github_url      = $url
        access_password = $Password
    }
    try {
        Invoke-WebRequest -UseBasicParsing -Uri "https://gitadd.r00ted.ch" -Method Post -Body $FormParameters
        Write-Host "  -> Success"
    } catch {
        Write-Host "  -> Failed: $_"
    }

    Start-Sleep -Seconds 20
}