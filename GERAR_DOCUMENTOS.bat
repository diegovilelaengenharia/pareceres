@echo off
title Painel GEM - SMOSU Oliveira/MG
color 0A
chcp 65001 > nul

echo.
echo ======================================================================
echo           INICIANDO PAINEL WEB DO GERADOR DE DOCUMENTOS
echo ======================================================================
echo.
echo  O painel sera aberto no seu navegador padrao.
echo  (Mantenha esta janela preta aberta enquanto usa o sistema)
echo  (Para desligar, basta fechar esta janela)
echo.

python "_Sistema_Interno\01_Motor_Python\painel_gem.py"

pause
