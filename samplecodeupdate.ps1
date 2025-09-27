<#
.SYNOPSIS
  Download all ZIP files containing 'python' (case-insensitive) from a GitHub repo path,
  extract them into a "samples" subfolder, and remove the ZIP files afterward.

.PARAMETER OutDir
  Base local path where the "samples" folder will be created (default: current directory).

.PARAMETER Owner
  GitHub organization/owner (default: MicrosoftLearning).

.PARAMETER Repo
  GitHub repository name (default: mslearn-github-copilot-dev).

.PARAMETER RepoPath
  Path inside the repository (default: DownloadableCodeProjects/Downloads).
#>

[CmdletBinding()]
param(
  [string]$OutDir   = (Get-Location).Path,
  [string]$Owner    = "MicrosoftLearning",
  [string]$Repo     = "mslearn-github-copilot-dev",
  [string]$RepoPath = "DownloadableCodeProjects/Downloads"
)

# Force TLS 1.2 for compatibility
try {
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
} catch { }

# GitHub API endpoint
$apiUrl  = "https://api.github.com/repos/$Owner/$Repo/contents/$RepoPath"
$headers = @{
  "User-Agent" = "PowerShell"
  "Accept"     = "application/vnd.github+json"
}

Write-Host "Fetching file list from GitHub... ($apiUrl)"
try {
  $items = Invoke-RestMethod -Uri $apiUrl -Headers $headers -ErrorAction Stop
} catch {
  Write-Error "Failed to call GitHub API: $($_.Exception.Message)"
  exit 1
}

if (-not $items) {
  Write-Warning "No items found at path: $RepoPath"
  exit 0
}

# Filter ZIP files with "python" in the name
$pythonZips = $items | Where-Object {
  $_.type -eq 'file' -and $_.name -match '\.zip$' -and $_.name -imatch 'python'
}

if (-not $pythonZips) {
  Write-Warning "No ZIP files containing 'python' were found."
  exit 0
}

# Create "samples" directory under output base
$samplesDir = Join-Path $OutDir "samples"
$null = New-Item -ItemType Directory -Path $samplesDir -Force -ErrorAction SilentlyContinue

foreach ($file in $pythonZips) {
  $zipName     = $file.name
  $downloadUrl = $file.download_url
  if (-not $downloadUrl) {
    $downloadUrl = "https://raw.githubusercontent.com/$Owner/$Repo/main/$RepoPath/$zipName"
  }

  $localZip   = Join-Path $samplesDir $zipName
  $destFolder = Join-Path $samplesDir ([IO.Path]::GetFileNameWithoutExtension($zipName))

  Write-Host "`nDownloading: $zipName"
  try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $localZip -Headers $headers -UseBasicParsing -ErrorAction Stop
  } catch {
    Write-Warning "Failed to download $zipName - $($_.Exception.Message)"
    continue
  }

  Write-Host "Extracting to: $destFolder"
  try {
    $null = New-Item -ItemType Directory -Path $destFolder -Force -ErrorAction SilentlyContinue
    Expand-Archive -Path $localZip -DestinationPath $destFolder -Force
  } catch {
    Write-Warning "Failed to extract $zipName - $($_.Exception.Message)"
    continue
  }

  Write-Host "Removing ZIP file: $zipName"
  try {
    Remove-Item -LiteralPath $localZip -Force -ErrorAction SilentlyContinue
  } catch {
    Write-Warning "Failed to delete $zipName - $($_.Exception.Message)"
  }
}

Write-Host "`nAll tasks completed! Extracted projects are under: $samplesDir"
