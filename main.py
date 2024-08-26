from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
from datetime import datetime
import pdfplumber
import smtplib
import threading
stime = time.time()

# Variáveis utilizadas
infos_buscadas =['edilberto', 'EDILBERTO DE ARAUJO', 'EDILBERTO DE ARAÚJO', 'LIMA JUNIOR', 'LIMA JÚNIOR'
            ]
novo_nome = None  # Inicializado como None
local_de_download = None
lock = threading.Lock()

# Configurações do Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

prefs = {
    "download.default_directory": local_de_download,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
}

chrome_options.add_experimental_option("prefs", prefs)

def Diario_Estado_Acre():
    url_do_site = 'https://diario.ac.gov.br/'
    local_de_download = r'C:\Users\edlbr\OneDrive\Área de Trabalho\Diários\AC\Diários Oficiais do Estado'
    prefs.update({"download.default_directory": local_de_download})

    def download_DOE_AC():
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url_do_site)
        time.sleep(1)
        download_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/a")
        download_button.click()
        time.sleep(2)
        driver.quit()

    download_DOE_AC()

    def renomeia_pdf_DOE_AC():
        global novo_nome
        data_completa = datetime.now()
        data_simples = data_completa.date()
        data_formatada = data_simples.strftime("%d-%m-%Y")
        arquivos = os.listdir(local_de_download)
        time.sleep(2)
        arquivo_mais_recente = max([os.path.join(local_de_download, f) for f in arquivos], key=os.path.getctime)
        novo_nome = os.path.join(local_de_download, "DOE-AC - Diário Oficial do Estado do Acre - " + data_formatada + ".pdf")
        try:
            os.rename(arquivo_mais_recente, novo_nome)
        except FileExistsError:
            os.replace(arquivo_mais_recente, novo_nome)


        return novo_nome  # Retorna o caminho do PDF renomeado

    return renomeia_pdf_DOE_AC()  # Chama a função e retorna o caminho do PDF

def Diario_TJ_AC():
    url_do_site = 'https://diario.tjac.jus.br/edicoes.php'
    local_de_download = r'C:\Users\edlbr\OneDrive\Área de Trabalho\Diários\AC\Diários do Tribunal de Justiça'
    prefs.update({"download.default_directory": local_de_download})

    def download_TJ_AC():
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url_do_site)
        time.sleep(1)
        download_button = driver.find_element(By.XPATH, 
                                              "/html/body/table/tbody/tr[3]/td/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/a")
        download_button.click()
        time.sleep(2)
        driver.quit()

    download_TJ_AC()

    def renomeia_pdf_TJ_AC():
        global novo_nome
        data_completa = datetime.now()
        data_simples = data_completa.date()
        data_formatada = data_simples.strftime("%d-%m-%Y")
        arquivos = os.listdir(local_de_download)
        time.sleep(2)
        arquivo_mais_recente = max([os.path.join(local_de_download, f) for f in arquivos], key=os.path.getctime)
        novo_nome = os.path.join(local_de_download, "DTJ-AC - Diário do Tribunal de Justiça do Estado do Acre - " + data_formatada + ".pdf")
        try:
            os.rename(arquivo_mais_recente, novo_nome)
        except FileExistsError:
            os.replace(arquivo_mais_recente, novo_nome)

        return novo_nome  # Retorna o caminho do PDF renomeado

    return renomeia_pdf_TJ_AC()  # Chama a função e retorna o caminho do PDF

    
# Função para ler o PDF e buscar o nome
def busca_no_pdf(lista_de_pdfs):
    resultados = []
    for pdf_path in lista_de_pdfs:
        if not os.path.exists(pdf_path):
            print(f"Erro: O arquivo PDF {pdf_path} não foi encontrado.")
            continue
        
        with pdfplumber.open(pdf_path) as diario:
            for numero_pagina, pagina in enumerate(diario.pages, start=1):
                print(f"Lendo página {pagina} do arquivo {os.path.basename(pdf_path)}")
                conteudo = pagina.extract_text()
                if conteudo:
                    for termo in infos_buscadas:
                        ocorrencias = conteudo.lower().count(termo.lower())
                        if ocorrencias > 0:
                            resultados.append({
                                'arquivo': os.path.basename(pdf_path),
                                'pagina': numero_pagina,
                                'termo': termo,
                                'ocorrencias': ocorrencias
                            })

    if resultados:
        return resultados
    else:
        print("Nenhum dos termos foi encontrado nos PDFs.")
        return []

ftime = time.time()

if __name__ == "__main__":
    
    pdfs_baixados = [Diario_Estado_Acre(), Diario_TJ_AC()]
    
    resultados = busca_no_pdf(pdfs_baixados)

    if resultados:
        for resultado in resultados:
            print(f"O termo '{resultado['termo']}' foi encontrado {resultado['ocorrencias']} vez(es) na página {resultado['pagina']} do arquivo {resultado['arquivo']}.")
    else:
        print("Nenhuma ocorrência encontrada nos PDFs.")

    print(stime-ftime)

