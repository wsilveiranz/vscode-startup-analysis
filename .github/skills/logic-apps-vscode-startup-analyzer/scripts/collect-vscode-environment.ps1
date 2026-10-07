param(
  [string]$OutputDirectory = ".\vscode-startup-evidence"
)
$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$root = Join-Path $OutputDirectory $stamp
New-Item -ItemType Directory -Force -Path $root | Out-Null

function Save-CommandOutput([string]$Name, [scriptblock]$Command) {
  try { & $Command 2>&1 | Out-File -Encoding utf8 (Join-Path $root $Name) }
  catch { $_ | Out-File -Encoding utf8 (Join-Path $root $Name) }
}

Save-CommandOutput "code-version.txt" { code --version }
Save-CommandOutput "code-status.txt" { code --status }
Save-CommandOutput "extensions.txt" { code --list-extensions --show-versions }
Save-CommandOutput "powershell-version.txt" { $PSVersionTable | Format-List * }
Save-CommandOutput "computer-info.txt" {
  Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,OSArchitecture,TotalVisibleMemorySize,FreePhysicalMemory
  Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed
  Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID,Size,FreeSpace,FileSystem
}
@"
Manual evidence still required:
1. Developer: Startup Performance report saved as text.
2. Developer: Show Running Extensions screenshot.
3. Readiness milestone and observed elapsed time.
4. Cold or warm run classification.
Review all files before sharing with another organization.
"@ | Out-File -Encoding utf8 (Join-Path $root "README.txt")
Write-Output $root
