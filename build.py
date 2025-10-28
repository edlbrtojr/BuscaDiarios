import os
import sys
import subprocess
import shutil

def build_executable():
    print("Iniciando build do executável...")
    
    # Nome do executável e pasta de distribuição
    exe_name = "BuscaDiarios"
    dist_folder = "BuscaDiarios-Distribuicao"
    
    try:
        # Limpar builds anteriores
        for path in ['dist', 'build', dist_folder]:
            if os.path.exists(path):
                shutil.rmtree(path)
        if os.path.exists(exe_name + '.spec'):
            os.remove(exe_name + '.spec')
        
        # Criar pasta dist se não existir
        os.makedirs('dist', exist_ok=True)
        
        # Configurar comando do PyInstaller com mais opções para garantir um executável autossuficiente
        cmd = [
            'pyinstaller',
            '--name=' + exe_name,
            '--onefile',
            '--noconsole',
            '--add-data=README.md;.',
            '--add-data=requirements.txt;.',
            '--hidden-import=pdfplumber',
            '--hidden-import=tkinter',
            '--hidden-import=selenium',
            '--clean',  # Limpa cache PyInstaller
            'start.py'
        ]
            
        # Executar PyInstaller
        print("Executando PyInstaller...")
        subprocess.run(cmd, check=True)
        
        # Criar pasta de distribuição
        os.makedirs(dist_folder)
        
        # Copiar arquivos necessários
        shutil.copy(os.path.join('dist', exe_name + '.exe'), os.path.join(dist_folder, exe_name + '.exe'))
        shutil.copy('install_startup.bat', os.path.join(dist_folder, 'install_startup.bat'))
        shutil.copy('README.md', os.path.join(dist_folder, 'Leia-me.txt'))
        
        # Criar pasta Downloads no diretório de distribuição
        downloads_dir = os.path.join(dist_folder, 'Downloads', 'Diários', 'AC')
        os.makedirs(os.path.join(downloads_dir, 'Diários Oficiais do Estado'), exist_ok=True)
        os.makedirs(os.path.join(downloads_dir, 'Diários do Tribunal de Justiça'), exist_ok=True)
        
        # Criar arquivo de instruções rápidas
        with open(os.path.join(dist_folder, 'INSTRUCOES.txt'), 'w', encoding='utf-8') as f:
            f.write("""BUSCA DIÁRIOS - INSTRUÇÕES RÁPIDAS

1. INSTALAÇÃO
   - Extraia esta pasta para o local desejado (ex: C:\\Programas\\BuscaDiarios)
   - Execute BuscaDiarios.exe para iniciar o programa
   - (Opcional) Execute install_startup.bat para iniciar automaticamente com o Windows

2. REQUISITOS
   - Windows 7 ou superior
   - Google Chrome instalado

3. COMO USAR
   - Execute BuscaDiarios.exe
   - Configure os termos de busca na interface
   - Clique em "Iniciar Busca"
   - Os PDFs serão baixados na pasta Downloads

4. SUPORTE
   - Consulte o arquivo Leia-me.txt para mais informações
   - Em caso de problemas, certifique-se de que o Chrome está instalado

5. EXECUÇÃO AUTOMÁTICA
   - Execute install_startup.bat para configurar a inicialização automática
   - O programa iniciará minimizado quando o Windows iniciar
   - Para desativar, remova o atalho da pasta Startup do Windows""")
        
        # Criar arquivo ZIP para distribuição
        shutil.make_archive(dist_folder, 'zip', dist_folder)
        
        print("\nBuild concluído com sucesso!")
        print(f"\nArquivos de distribuição criados em: {dist_folder}")
        print(f"Arquivo ZIP criado: {dist_folder}.zip")
        print("\nPara compartilhar o programa, envie o arquivo ZIP criado.")
        print("\nIMPORTANTE: O executável NÃO requer Python instalado na máquina do usuário.")
        
    except subprocess.CalledProcessError as e:
        print(f"\nErro durante o build: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable() 