@echo off
title Painel GEM - SMOSU Oliveira/MG
color 0A
chcp 65001 > nul

:: Garante que o script rode a partir da pasta raiz do projeto
cd /d "%~dp0"

echo [>] Iniciando Motor de Inteligência...
python "Sistema\motor\ui\painel_gem.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Ocorreu um erro ao iniciar o Painel GEM.
    echo [!] Verifique se o Python está instalado e se as dependências estão em 'Sistema/motor/requirements.txt'.
    pause
)
