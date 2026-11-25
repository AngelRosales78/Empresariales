$ErrorActionPreference = 'Stop'

function Invoke-LabCommand {
    param([string]$Program, [string[]]$Arguments)

    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: $Program $($Arguments -join ' ')"
    }
}

Push-Location (Join-Path $PSScriptRoot 'api')
try {
    if (-not (Test-Path '.venv')) {
        Invoke-LabCommand python @('-m', 'venv', '.venv')
    }
    $python = Join-Path (Get-Location) '.venv\Scripts\python.exe'
    Invoke-LabCommand $python @('-m', 'pip', 'install', '--quiet', '-r', 'requirements.txt')
    Invoke-LabCommand $python @('manage.py', 'migrate', '--noinput')

    # Seed only a brand new database, so deleted records do not come back.
    if (-not (Test-Path '..\react\.env.local')) {
        Invoke-LabCommand $python @('manage.py', 'seed_quiz', '--verbosity', '0')
        Invoke-LabCommand $python @('manage.py', 'seed_catalog')
    }
    $token = Invoke-LabCommand $python @('manage.py', 'shell', '--verbosity', '0', '-c', 'from quiz.management.commands.seed_quiz import ensure_users; print(ensure_users()[0])')
    if ($token -notmatch '^[a-f0-9]{40}$') {
        throw 'Could not read the local lab token.'
    }
    Set-Content -LiteralPath '..\react\.env.local' -Value "VITE_QUIZ_TOKEN=$token" -Encoding ascii
} finally {
    Pop-Location
}

Push-Location (Join-Path $PSScriptRoot 'react')
try {
    Invoke-LabCommand npm.cmd @('ci')
} finally {
    Pop-Location
}
