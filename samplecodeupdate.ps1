<# 
.SYNOPSIS
  Download & extract SampleApps.zip into a local folder with overwrite.

.DESCRIPTION
  - 지정 URL에서 ZIP 파일을 다운로드
  - ZIP을 임시 경로에 저장 후 Unblock
  - 대상 폴더가 없으면 생성
  - Expand-Archive -Force 로 파일을 덮어쓰기 추출
  - 완료 후 임시 ZIP 삭제

.PARAMETER Destination
  압축을 풀 대상 폴더 경로 (기본값: .\SampleApps)

.PARAMETER Url
  ZIP 다운로드 URL (기본값: MicrosoftLearning APL-2007 SampleApps.zip)

.EXAMPLE
  .\Get-SampleApps.ps1
  -> .\SampleApps 폴더로 덮어쓰기 추출

.EXAMPLE
  .\Get-SampleApps.ps1 -Destination "D:\Lab\SampleApps" -Verbose
#>

[CmdletBinding()]
param(
    [string]$Destination = ".\SampleApps",
    [string]$Url = "https://raw.githubusercontent.com/MicrosoftLearning/APL-2007-Accelerate-app-development-by-using-GitHub-Copilot/master/LearnModuleExercises/Downloads/SampleApps.zip"
)

function Set-Tls12 {
    try {
        if ([Net.ServicePointManager]::SecurityProtocol -band [Net.SecurityProtocolType]::Tls12) { return }
        [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
        Write-Verbose "TLS 1.2 활성화."
    } catch {
        Write-Verbose "TLS 설정을 변경하지 못했습니다(무시 가능): $($_.Exception.Message)"
    }
}

function Invoke-DownloadWithRetry {
    param(
        [Parameter(Mandatory=$true)][string]$DownloadUrl,
        [Parameter(Mandatory=$true)][string]$OutFile,
        [int]$MaxRetry = 3,
        [int]$DelaySeconds = 2
    )
    for ($i=1; $i -le $MaxRetry; $i++) {
        try {
            Write-Verbose "다운로드 시도 #$($i): $DownloadUrl"
            # PS5 호환을 위해 -UseBasicParsing 포함 (PS7에서는 무시됨)
            Invoke-WebRequest -Uri $DownloadUrl -OutFile $OutFile -UseBasicParsing -TimeoutSec 120
            if ((Test-Path $OutFile) -and ((Get-Item $OutFile).Length -gt 0)) {
                Write-Verbose "다운로드 성공: $OutFile"
                return $true
            } else {
                throw "다운로드된 파일이 없거나 비어 있습니다."
            }
        } catch {
            Write-Warning "다운로드 실패: $($_.Exception.Message)"
            if ($i -lt $MaxRetry) {
                Start-Sleep -Seconds $DelaySeconds
            } else {
                return $false
            }
        }
    }
}

try {
    Write-Verbose "작업 시작"

    # 1) TLS 1.2 보장 (구형 환경 대비)
    Set-Tls12

    # 2) 임시 경로 및 파일명 준비
    $tempDir = [IO.Path]::GetTempPath()
    $zipPath = Join-Path $tempDir "SampleApps_$([Guid]::NewGuid().ToString('N')).zip"

    # 3) ZIP 다운로드
    $ok = Invoke-DownloadWithRetry -DownloadUrl $Url -OutFile $zipPath
    if (-not $ok) { throw "ZIP 파일 다운로드에 최종 실패했습니다." }

    # 4) Zone Identifier 제거 (차단 해제)
    try {
        Unblock-File -Path $zipPath -ErrorAction Stop
        Write-Verbose "ZIP 파일 차단 해제."
    } catch {
        Write-Verbose "Unblock-File 실패(무시 가능): $($_.Exception.Message)"
    }

    # 5) 대상 폴더 생성
    if (-not (Test-Path $Destination)) {
        New-Item -ItemType Directory -Path $Destination | Out-Null
        Write-Verbose "대상 폴더 생성: $Destination"
    }

    # 6) 압축 해제 (덮어쓰기)
    Write-Verbose "압축 해제 시작 -> $Destination"
    Expand-Archive -Path $zipPath -DestinationPath $Destination -Force
    Write-Host "✅ SampleApps가 '$Destination' 경로로 성공적으로 배포되었습니다." -ForegroundColor Green

    # 7) 압축 해제 후 ZIP 삭제
    if (Test-Path $zipPath) {
        Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
        Write-Verbose "다운받은 ZIP 삭제 완료: $zipPath"
    }

    # 8) python이 들어간 폴더만 남기고 나머지 최상위 폴더 삭제
    $subFolders = Get-ChildItem -Path $Destination -Directory
    foreach ($folder in $subFolders) {
        if ($folder.Name -notmatch '(?i)python') {
            try {
                Remove-Item -Path $folder.FullName -Recurse -Force -ErrorAction Stop
                Write-Verbose "삭제됨: $($folder.FullName)"
            } catch {
                Write-Warning "삭제 실패: $($folder.FullName) - $($_.Exception.Message)"
            }
        }
    }
    Write-Host "✅ 'python'이름이 들어간 폴더만 남기고 나머지 삭제 완료." -ForegroundColor Green


} catch {
    Write-Error "작업 실패: $($_.Exception.Message)"
    exit 1
} finally {
    # 7) 임시 ZIP 정리
    if (Test-Path $zipPath) {
        Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
        Write-Verbose "임시 ZIP 삭제 완료."
    }
}
