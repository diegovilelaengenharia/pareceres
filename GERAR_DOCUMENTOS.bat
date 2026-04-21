@echo off
title Motor SMOSU - Oliveira/MG
color 0A
echo ======================================================================
echo           GERADOR DE PARECERES E ALVARAS - SMOSU OLIVEIRA/MG
echo ======================================================================
echo.
echo Lendo arquivos da pasta [1_Colar_JSON_Aqui]...
echo.
python "_Sistema_Interno\01_Motor_Python\compilador.py"
echo.
echo Processo concluido! Verifique a pasta [2_Documentos_Prontos].
echo.
pause
