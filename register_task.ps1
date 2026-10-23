<#
Registers a Windows Scheduled Task that runs the pipeline every day at 05:00.
Run this ONCE, from an elevated PowerShell prompt, from inside the project folder.

Usage:
    .\register_task.ps1
#>

$ProjectRoot = $PSScriptRoot
$Python = "C:\Users\deipt\AppData\Local\Programs\Python\Python313\python.exe"
$Script = Join-Path $ProjectRoot "src\run_pipeline.py"

if (-not (Test-Path $Python)) {
    Write-Error "Python not found at $Python. Update the `$Python path in this script."
    exit 1
}

$Action = New-ScheduledTaskAction -Execute $Python -Argument "`"$Script`"" -WorkingDirectory $ProjectRoot
$Trigger = New-ScheduledTaskTrigger -Daily -At 5:00AM
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5)

try {
    Register-ScheduledTask `
        -TaskName "ZomatoBIPipeline" `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Description "Regenerates synthetic data, reloads Postgres, and rebuilds mart_performance for the Zomato BI dashboard." `
        -RunLevel Highest `
        -ErrorAction Stop | Out-Null
} catch {
    Write-Error "Failed to register task: $_"
    Write-Host "Make sure this PowerShell window's title bar says 'Administrator: Windows PowerShell'."
    exit 1
}

Write-Host "Scheduled task 'ZomatoBIPipeline' registered. It will run daily at 05:00."
Write-Host "Test it immediately with: Start-ScheduledTask -TaskName 'ZomatoBIPipeline'"
