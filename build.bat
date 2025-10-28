@echo off
echo ========================================
echo    Compilando BuscaDiarios
echo ========================================
echo.

echo Verificando ambiente Python...
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Python nao encontrado! Necessario para compilacao.
    echo Por favor, instale o Python antes de continuar.
    goto :end
)

echo Instalando dependencias...
python -m pip install --upgrade pip > nul
pip install -r requirements.txt
pip install pyinstaller > nul

echo.
echo Criando executavel...
python build.py

if exist "dist\BuscaDiarios.exe" (
    echo.
    echo ========================================
    echo    Compilacao concluida com sucesso!
    echo ========================================
    echo.
    echo O executavel foi criado em: dist\BuscaDiarios.exe
    echo.
    echo IMPORTANTE: O executavel NAO requer Python na maquina do usuario final.
    echo             Ele contem tudo necessario para executar o programa.
    echo.
    
    echo Deseja executar o instalador agora?
    echo [1] Sim, instalar o programa
    echo [2] Nao, apenas sair
    set /p install_choice="Escolha uma opcao [1-2]: "
    
    if "%install_choice%"=="1" (
        call install.bat
    ) else (
        echo.
        echo Para instalar posteriormente, execute install.bat
    )
) else (
    echo.
    echo ERRO: A compilacao falhou! Verifique as mensagens acima.
)

:end
echo.
echo Pressione qualquer tecla para sair...
pause > nul 