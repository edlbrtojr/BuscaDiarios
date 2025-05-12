# Busca Diários

Este script automatiza o download e a busca por termos específicos em Diários Oficiais de fontes selecionadas. Atualmente, ele baixa os Diários Oficiais do Estado do Acre (DOE-AC) e do Tribunal de Justiça do Acre (DTJ-AC), renomeia os arquivos PDF baixados com a data atual e, em seguida, procura por uma lista pré-definida de termos nesses PDFs.

## Funcionalidades

- Baixa a edição mais recente do Diário Oficial do Estado do Acre.
- Baixa a edição mais recente do Diário do Tribunal de Justiça do Acre.
- Renomeia os arquivos PDF baixados com um formato padronizado (`DOE-AC - Diário Oficial do Estado do Acre - DD-MM-AAAA.pdf` e `DTJ-AC - Diário do Tribunal de Justiça do Estado do Acre - DD-MM-AAAA.pdf`).
- Busca por uma lista de termos (definida na variável `infos_buscadas`) dentro dos PDFs baixados.
- Imprime no console os resultados da busca, indicando o arquivo, a página, o termo encontrado e o número de ocorrências.

## Como Usar

### Pré-requisitos

- Python 3.x instalado.
- Google Chrome instalado.
- ChromeDriver compatível com a sua versão do Google Chrome. Certifique-se de que o `chromedriver` esteja no seu PATH do sistema ou especifique o caminho para ele no script.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd BuscaDiarios
    ```
2.  **Instale as dependências:**
    ```bash
    pip install selenium pdfplumber
    ```
3.  **Configure o Script:**
    - Abra o arquivo `main.py`.
    - **(Importante)** Atualize os caminhos em `local_de_download` dentro das funções `Diario_Estado_Acre` e `Diario_TJ_AC` para os diretórios onde você deseja salvar os PDFs baixados. Os diretórios precisam existir antes de executar o script.
    - Modifique a lista `infos_buscadas` com os termos que você deseja procurar nos PDFs.

### Execução

Execute o script a partir do terminal:

```bash
python main.py
```

O script irá baixar os PDFs, renomeá-los e realizar a busca. Os resultados serão exibidos no console.

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
