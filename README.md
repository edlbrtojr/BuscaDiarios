# Busca Diários

Após ser aprovado no cadastro reserva do concurso do Tribunal de Justiça do Acre, criei este script para rodar diariamente e verificar se meu nome apareceu em alguns dos diários, pois tinha medo de ser convocado e não receber nenhum tipo de e-mail.

Utilizando deste medo e dos meus conhecimentos em python, desenvolvi a aplicação para baixar automaticamente e pesquisar termos, como meu nome,  nos Diários Oficiais do Estado do Acre e Diários do Tribunal de Justiça do Acre.

## Funcionalidades

- Download automático dos diários oficiais diretamente dos sites oficiais
- Renomeação dos arquivos com data formatada
- Busca de termos específicos nos PDFs baixados
- Interface gráfica amigável para configuração e visualização dos resultados
- Possibilidade de execução automática na inicialização do Windows

## Requisitos

- Windows 7 ou superior
- Google Chrome instalado

## Instalação

### Versão Executável (Recomendado)

1. Baixe a última versão do executável da seção Releases
2. Execute o arquivo `BuscaDiarios.exe`
3. (Opcional) Execute `install_startup.bat` para configurar a execução automática na inicialização do Windows

### Compilando do Código Fonte

Se você preferir compilar o executável a partir do código fonte:

1. Clone ou baixe este repositório
2. Execute `build.bat` para criar o executável
3. O executável será criado na pasta `dist`
4. (Opcional) Execute `install_startup.bat` para configurar a execução automática

## Como Usar

### Modo Executável

Simplesmente clique duas vezes no arquivo `BuscaDiarios.exe`. A interface gráfica será aberta automaticamente.

Na interface você pode:

- Configurar a pasta de downloads
- Editar os termos de busca
- Selecionar quais diários baixar
- Iniciar a busca e visualizar os resultados

### Execução Automática

Se você configurou a execução automática usando o `install_startup.bat`:

1. O programa iniciará automaticamente quando você ligar o computador
2. Você pode encontrar o ícone na bandeja do sistema (system tray)
3. Para desativar a execução automática, remova o atalho da pasta Startup do Windows

### Modo Desenvolvimento

Para desenvolvedores que queiram modificar o código:

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar em modo desenvolvimento
python start.py

# Criar executável
python build.py
```

## Personalização

Você pode editar os termos de busca:

1. Através da interface gráfica (recomendado)
2. Editando o arquivo `main.py` (modo desenvolvimento)

## Solução de Problemas

- Se os downloads não funcionarem, verifique sua conexão com a internet
- Em caso de erros com o Selenium, certifique-se de que o Chrome está instalado e atualizado
- Problemas com PDFs não encontrados podem ocorrer se o download falhar ou se o site mudar sua estrutura
- Se o programa não iniciar automaticamente, verifique a pasta Startup do Windows

## Licença

Este software é de uso livre.

---

# Diary Search

This script automates the download and search for specific terms in Official Gazettes from selected sources. Currently, it downloads the Official Gazettes of the State of Acre (DOE-AC) and the Court of Justice of Acre (DTJ-AC), renames the downloaded PDF files with the current date, and then searches for a predefined list of terms within these PDFs.

## Features

- Downloads the latest edition of the Official Gazette of the State of Acre.
- Downloads the latest edition of the Diary of the Court of Justice of Acre.
- Renames the downloaded PDF files with a standardized format (`DOE-AC - Diário Oficial do Estado do Acre - DD-MM-YYYY.pdf` and `DTJ-AC - Diário do Tribunal de Justiça do Estado do Acre - DD-MM-YYYY.pdf`).
- Searches for a list of terms (defined in the `infos_buscadas` variable) within the downloaded PDFs.
- Prints the search results to the console, indicating the file, page number, term found, and number of occurrences.

## How to Use

### Prerequisites

- Python 3.x installed.
- Google Chrome installed.
- ChromeDriver compatible with your Google Chrome version. Ensure `chromedriver` is in your system's PATH or specify the path to it in the script if needed.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd BuscaDiarios
    ```
2.  **Install dependencies:**
    ```bash
    pip install selenium pdfplumber
    ```
3.  **Configure the Script:**
    - Open the `main.py` file.
    - **(Important)** Update the `local_de_download` paths within the `Diario_Estado_Acre` and `Diario_TJ_AC` functions to the directories where you want to save the downloaded PDFs. These directories must exist before running the script.
    - Modify the `infos_buscadas` list with the terms you want to search for in the PDFs.

### Execution

Run the script from the terminal:

```bash
python main.py
```

The script will download the PDFs, rename them, and perform the search. The results will be displayed in the console.
