@echo off
echo Iniciando Arkanoid...
echo.
echo Versiones disponibles:
echo 1. Arkanoid Básico
echo 2. Arkanoid Mejorado
echo.
set /p choice="Selecciona una versión (1 o 2): "

if "%choice%"=="1" (
    echo Ejecutando Arkanoid Básico...
    C:/Users/joser/source/repos/arkanoid/.venv/Scripts/python.exe arkanoid.py
) else if "%choice%"=="2" (
    echo Ejecutando Arkanoid Mejorado...
    C:/Users/joser/source/repos/arkanoid/.venv/Scripts/python.exe arkanoid_enhanced.py
) else (
    echo Opción no válida. Ejecutando versión básica...
    C:/Users/joser/source/repos/arkanoid/.venv/Scripts/python.exe arkanoid.py
)

pause
