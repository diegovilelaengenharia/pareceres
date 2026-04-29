@echo off
title Motor SMOSU - Oliveira/MG
color 0A
chcp 65001 > nul

echo ======================================================================
echo           GERADOR DE PARECERES E ALVARAS - SMOSU OLIVEIRA/MG
echo ======================================================================
echo.
echo  Escolha o modo de geracao:
echo.
echo    [1] MODO MOTOR  — JSON estruturado -^> compilador padrao
echo        (O JSON precisa ter: considerandos[], fundamentacao_legal[], etc.)
echo.
echo    [2] MODO LIVRE  — Texto narrativo da IA -^> mesmo layout visual
echo        (O JSON precisa ter: texto_livre com o parecer escrito livremente)
echo.
echo ======================================================================
set /p MODO="  Digite 1 ou 2 e pressione ENTER: "

echo.
if "%MODO%"=="1" goto MOTOR
if "%MODO%"=="2" goto LIVRE
echo [!] Opcao invalida. Encerrando.
pause
exit /b 1

:MOTOR
echo [>] MODO MOTOR — Compilando JSONs da pasta [1_Colar_JSON_Aqui]...
echo.
python "_Sistema_Interno\01_Motor_Python\compilador.py"
goto FIM

:LIVRE
echo [>] MODO LIVRE — Compilando com texto narrativo...
echo.
python "_Sistema_Interno\01_Motor_Python\compilador_livre.py"
goto FIM

:FIM
echo.
echo Processo concluido! Verifique a pasta [2_Documentos_Prontos].
echo.
pause
