@echo off
echo ========================================
echo   Configurar Inicialização Automática
echo ========================================
echo.

:: Obter o diretório atual
set "CURRENT_DIR=%~dp0"
set "EXE_PATH=%CURRENT_DIR%BuscaDiarios.exe"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

:: Verificar se o executável existe
if not exist "%EXE_PATH%" (
    echo Erro: Executavel nao encontrado em %EXE_PATH%
    echo Verifique se você está executando este script do diretório correto.
    goto :end
)

:: Criar atalho no startup
echo Criando atalho na pasta de inicialização...
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $Shortcut = $WS.CreateShortcut('%STARTUP_DIR%\BuscaDiarios.lnk'); $Shortcut.TargetPath = '%EXE_PATH%'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Save()"

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo      Configuração concluída!
    echo ========================================
    echo.
    echo BuscaDiarios foi configurado para iniciar com o Windows.
    echo O atalho foi criado em: %STARTUP_DIR%\BuscaDiarios.lnk
    echo.
    echo Para desativar a inicialização automática, exclua o atalho:
    echo %STARTUP_DIR%\BuscaDiarios.lnk
) else (
    echo Erro ao criar o atalho de inicializacao.
)

:end
echo.
echo Pressione qualquer tecla para sair...
pause > nul 