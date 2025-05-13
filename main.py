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
infos_buscadas = ['edilberto', 'EDILBERTO DE ARAUJO', 'EDILBERTO DE ARAÚJO', 'LIMA JUNIOR', 'LIMA JÚNIOR']
local_de_download = os.path.join(os.getcwd(), "Downloads", "Diários")
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
    local_dir = os.path.join(local_de_download, 'AC', 'Diários Oficiais do Estado')
    os.makedirs(local_dir, exist_ok=True)
    
    # Atualizar as preferências de download
    updated_prefs = prefs.copy()
    updated_prefs["download.default_directory"] = local_dir
    
    # Atualizar opções do Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("prefs", updated_prefs)

    def download_DOE_AC():
        driver = webdriver.Chrome(options=options)
        driver.get(url_do_site)
        time.sleep(1)
        download_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/a")
        download_button.click()
        time.sleep(2)
        driver.quit()

    download_DOE_AC()

    def renomeia_pdf_DOE_AC():
        data_completa = datetime.now()
        data_simples = data_completa.date()
        data_formatada = data_simples.strftime("%d-%m-%Y")
        
        arquivos = os.listdir(local_dir)
        if not arquivos:
            return None
            
        time.sleep(2)
        arquivo_mais_recente = max([os.path.join(local_dir, f) for f in arquivos], key=os.path.getctime)
        novo_nome = os.path.join(local_dir, "DOE-AC - Diário Oficial do Estado do Acre - " + data_formatada + ".pdf")
        try:
            os.rename(arquivo_mais_recente, novo_nome)
        except FileExistsError:
            os.replace(arquivo_mais_recente, novo_nome)

        return novo_nome  # Retorna o caminho do PDF renomeado

    return renomeia_pdf_DOE_AC()  # Chama a função e retorna o caminho do PDF

def Diario_TJ_AC():
    url_do_site = 'https://diario.tjac.jus.br/edicoes.php'
    local_dir = os.path.join(local_de_download, 'AC', 'Diários do Tribunal de Justiça')
    os.makedirs(local_dir, exist_ok=True)
    
    # Atualizar as preferências de download
    updated_prefs = prefs.copy()
    updated_prefs["download.default_directory"] = local_dir
    
    # Atualizar opções do Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("prefs", updated_prefs)

    def download_TJ_AC():
        driver = webdriver.Chrome(options=options)
        driver.get(url_do_site)
        time.sleep(1)
        download_button = driver.find_element(By.XPATH, 
                                              "/html/body/table/tbody/tr[3]/td/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/a")
        download_button.click()
        time.sleep(2)
        driver.quit()

    download_TJ_AC()

    def renomeia_pdf_TJ_AC():
        data_completa = datetime.now()
        data_simples = data_completa.date()
        data_formatada = data_simples.strftime("%d-%m-%Y")
        
        arquivos = os.listdir(local_dir)
        if not arquivos:
            return None
            
        time.sleep(2)
        arquivo_mais_recente = max([os.path.join(local_dir, f) for f in arquivos], key=os.path.getctime)
        novo_nome = os.path.join(local_dir, "DTJ-AC - Diário do Tribunal de Justiça do Estado do Acre - " + data_formatada + ".pdf")
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
        if not pdf_path or not os.path.exists(pdf_path):
            print(f"Erro: O arquivo PDF {pdf_path} não foi encontrado.")
            continue
        
        try:
            with pdfplumber.open(pdf_path) as diario:
                for numero_pagina, pagina in enumerate(diario.pages, start=1):
                    print(f"Lendo página {numero_pagina} do arquivo {os.path.basename(pdf_path)}")
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
        except Exception as e:
            print(f"Erro ao processar o PDF {pdf_path}: {str(e)}")

    if resultados:
        return resultados
    else:
        print("Nenhum dos termos foi encontrado nos PDFs.")
        return []

ftime = time.time()

if __name__ == "__main__":
    # Criar diretórios de download se não existirem
    os.makedirs(os.path.join(local_de_download, 'AC', 'Diários Oficiais do Estado'), exist_ok=True)
    os.makedirs(os.path.join(local_de_download, 'AC', 'Diários do Tribunal de Justiça'), exist_ok=True)
    
    pdfs_baixados = []
    
    # Download do Diário Oficial do Estado
    pdf_doe = Diario_Estado_Acre()
    if pdf_doe:
        pdfs_baixados.append(pdf_doe)
    
    # Download do Diário do Tribunal de Justiça
    pdf_tj = Diario_TJ_AC()
    if pdf_tj:
        pdfs_baixados.append(pdf_tj)
    
    resultados = busca_no_pdf(pdfs_baixados)

    if resultados:
        for resultado in resultados:
            print(f"O termo '{resultado['termo']}' foi encontrado {resultado['ocorrencias']} vez(es) na página {resultado['pagina']} do arquivo {resultado['arquivo']}.")
    else:
        print("Nenhuma ocorrência encontrada nos PDFs.")

    print(f"Tempo de execução: {ftime-stime} segundos")

