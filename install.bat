@echo off
echo ========================================
echo    Instalador do BuscaDiarios
echo ========================================
echo.

set "DEFAULT_INSTALL_DIR=C:\Programas\BuscaDiarios"
set "EXE_NAME=BuscaDiarios.exe"
set "SOURCE_DIR=%~dp0"

if not exist "%SOURCE_DIR%%EXE_NAME%" (
    echo ERRO: O arquivo %EXE_NAME% nao foi encontrado!
    echo Execute primeiro o script build.bat para gerar o executavel.
    goto :end
)

:ask_install_dir
echo Por favor, escolha o diretorio de instalacao:
echo [1] Padrao (%DEFAULT_INSTALL_DIR%)
echo [2] Escolher outro diretorio
echo [3] Usar o diretorio atual (%SOURCE_DIR%)
set /p choice="Escolha uma opcao [1-3]: "

if "%choice%"=="1" (
    set "INSTALL_DIR=%DEFAULT_INSTALL_DIR%"
) else if "%choice%"=="2" (
    echo Por favor, digite o caminho completo para instalacao:
    set /p INSTALL_DIR="Caminho: "
) else if "%choice%"=="3" (
    set "INSTALL_DIR=%SOURCE_DIR%"
) else (
    echo Opcao invalida!
    goto :ask_install_dir
)

echo.
echo Instalando em: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    if errorlevel 1 (
        echo ERRO: Nao foi possivel criar o diretorio %INSTALL_DIR%.
        echo Verifique as permissoes ou escolha outro diretorio.
        goto :ask_install_dir
    )
)

REM Criar estrutura de diretórios
mkdir "%INSTALL_DIR%\Downloads\Diários\AC\Diários Oficiais do Estado" 2>nul
mkdir "%INSTALL_DIR%\Downloads\Diários\AC\Diários do Tribunal de Justiça" 2>nul

REM Copiar arquivos
echo Copiando arquivos...
copy "%SOURCE_DIR%%EXE_NAME%" "%INSTALL_DIR%\" >nul
copy "%SOURCE_DIR%README.md" "%INSTALL_DIR%\Leia-me.txt" >nul
copy "%SOURCE_DIR%install_startup.bat" "%INSTALL_DIR%\" >nul

echo Instalacao concluida com sucesso!
echo.

:ask_shortcuts
echo Deseja criar atalhos?
echo [1] Criar atalho na Area de Trabalho
echo [2] Adicionar ao Menu Iniciar
echo [3] Configurar para iniciar com o Windows
echo [4] Pular esta etapa
set /p shortcut_choice="Escolha uma opcao [1-4]: "

if "%shortcut_choice%"=="1" (
    echo Criando atalho na Area de Trabalho...
    powershell -Command "$WS = New-Object -ComObject WScript.Shell; $Shortcut = $WS.CreateShortcut([System.Environment]::GetFolderPath('Desktop') + '\BuscaDiarios.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\%EXE_NAME%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"
    echo Atalho criado na Area de Trabalho.
) else if "%shortcut_choice%"=="2" (
    echo Adicionando ao Menu Iniciar...
    powershell -Command "$WS = New-Object -ComObject WScript.Shell; $Shortcut = $WS.CreateShortcut([System.Environment]::GetFolderPath('StartMenu') + '\Programs\BuscaDiarios.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\%EXE_NAME%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"
    echo Programa adicionado ao Menu Iniciar.
) else if "%shortcut_choice%"=="3" (
    echo Configurando para iniciar com o Windows...
    powershell -Command "$WS = New-Object -ComObject WScript.Shell; $Shortcut = $WS.CreateShortcut([System.Environment]::GetFolderPath('Startup') + '\BuscaDiarios.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\%EXE_NAME%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Save()"
    echo Programa configurado para iniciar com o Windows.
) else if "%shortcut_choice%"=="4" (
    echo Pulando a criacao de atalhos.
) else (
    echo Opcao invalida!
    goto :ask_shortcuts
)

echo.
echo ========================================
echo    Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para executar o programa, vá até:
echo %INSTALL_DIR%\%EXE_NAME%
echo.

:end
pause 