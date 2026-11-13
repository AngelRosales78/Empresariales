$ErrorActionPreference = 'Stop'

function Invoke-LabCommand {
    param([string]$Program, [string[]]$Arguments)

    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Falló $Program $($Arguments -join ' ')"
    }
}

Push-Location (Join-Path $PSScriptRoot 'api')
try {
    Invoke-LabCommand python @('-m', 'pip', 'install', '-r', 'requirements.txt')
    Invoke-LabCommand python @('manage.py', 'migrate', '--noinput')

    $hasExams = Invoke-LabCommand python @('manage.py', 'shell', '--verbosity', '0', '-c', 'from quiz.models import Exam; print(int(Exam.objects.exists()))')
    if ($hasExams -eq '0' -and -not (Test-Path '..\react\.env.local')) {
        Invoke-LabCommand python @('manage.py', 'seed_quiz', '--verbosity', '0')
    }
    $token = Invoke-LabCommand python @('manage.py', 'shell', '--verbosity', '0', '-c', 'from quiz.management.commands.seed_quiz import ensure_users; print(ensure_users()[0])')
    if ($token -notmatch '^[a-f0-9]{40}$') {
        throw 'No se pudo obtener el token local del laboratorio.'
    }
    Set-Content -LiteralPath '..\react\.env.local' -Value "VITE_QUIZ_TOKEN=$token" -Encoding utf8
} finally {
    Pop-Location
}

Push-Location (Join-Path $PSScriptRoot 'react')
try {
    Invoke-LabCommand npm.cmd @('ci')
} finally {
    Pop-Location
}
