# Script de PowerShell para ejecutar Arkanoid
Write-Host "=== ARKANOID - JUEGO EN PYTHON ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Versiones disponibles:" -ForegroundColor Yellow
Write-Host "1. Arkanoid Básico" -ForegroundColor White
Write-Host "2. Arkanoid Mejorado (con efectos especiales)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Selecciona una versión (1 o 2)"

$pythonExe = "$PSScriptRoot\.venv\Scripts\python.exe"

switch ($choice) {
    "1" {
        Write-Host "Ejecutando Arkanoid Básico..." -ForegroundColor Green
        & $pythonExe "arkanoid.py"
    }
    "2" {
        Write-Host "Ejecutando Arkanoid Mejorado..." -ForegroundColor Green
        & $pythonExe "arkanoid_enhanced.py"
    }
    default {
        Write-Host "Opción no válida. Ejecutando versión básica..." -ForegroundColor Yellow
        & $pythonExe "arkanoid.py"
    }
}

Write-Host ""
Write-Host "¡Gracias por jugar!" -ForegroundColor Cyan
Read-Host "Presiona Enter para salir"
