# Próximos Passos - BuscaDiários

Este documento explica como expandir a aplicação BuscaDiários para incluir mais diários oficiais de diferentes estados e tribunais.

## Como Adicionar Novos Diários à Busca

Para adicionar novos diários à busca, siga os passos abaixo:

### 1. Adicionar uma Nova Função no `main.py`

Abra o arquivo `main.py` e adicione uma nova função seguindo o padrão das funções existentes (`Diario_Estado_Acre` e `Diario_TJ_AC`).

**Exemplo para adicionar o Diário Oficial do Estado do Amazonas:**

```python
def Diario_Estado_Amazonas():
    url_do_site = 'https://diario.am.gov.br/'  # Substitua pela URL correta
    local_dir = os.path.join(local_de_download, 'AM', 'Diários Oficiais do Estado')
    os.makedirs(local_dir, exist_ok=True)

    # Configurar opções do Chrome
    updated_prefs = prefs.copy()
    updated_prefs["download.default_directory"] = local_dir

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("prefs", updated_prefs)

    def download_DOE_AM():
        driver = webdriver.Chrome(options=options)
        driver.get(url_do_site)
        time.sleep(1)
        # Atualize o XPath conforme necessário para o botão de download
        download_button = driver.find_element(By.XPATH, "/xpath/para/o/botao")
        download_button.click()
        time.sleep(2)
        driver.quit()

    download_DOE_AM()

    def renomeia_pdf_DOE_AM():
        data_completa = datetime.now()
        data_simples = data_completa.date()
        data_formatada = data_simples.strftime("%d-%m-%Y")

        arquivos = os.listdir(local_dir)
        if not arquivos:
            return None

        time.sleep(2)
        arquivo_mais_recente = max([os.path.join(local_dir, f) for f in arquivos], key=os.path.getctime)
        novo_nome = os.path.join(local_dir, "DOE-AM - Diário Oficial do Estado do Amazonas - " + data_formatada + ".pdf")
        try:
            os.rename(arquivo_mais_recente, novo_nome)
        except FileExistsError:
            os.replace(arquivo_mais_recente, novo_nome)

        return novo_nome

    return renomeia_pdf_DOE_AM()
```

### 2. Atualizar a Interface Gráfica no `gui.py`

Após adicionar a função no `main.py`, você precisa atualizar a interface gráfica para incluir os novos diários:

1. **Adicione variáveis BooleanVar para os novos diários:**

```python
# Na função __init__ da classe DiariosBuscaApp
self.doe_am_var = tk.BooleanVar(value=True)
```

2. **Adicione novos checkboxes na interface:**

```python
# Na função create_widgets da classe DiariosBuscaApp
am_check = ttk.Checkbutton(self.check_frame, text="Diário Oficial do Estado do Amazonas",
                          variable=self.doe_am_var, style="Modern.TCheckbutton")
am_check.pack(anchor=tk.W, padx=(10, 0), pady=2)
```

3. **Atualize o método execute_search para incluir os novos diários:**

```python
# No método execute_search da classe DiariosBuscaApp
if self.doe_am_var.get() and self.is_running:
    self.update_status("Baixando Diário Oficial do Estado do Amazonas...", 60)
    self.add_result(f"{self.icons['download']} Iniciando download do Diário Oficial do Estado do Amazonas...")
    am_pdf = main.Diario_Estado_Amazonas()
    if am_pdf:
        self.pdfs_baixados.append(am_pdf)
        self.add_result(f"{self.icons['check']} Download concluído: " + os.path.basename(am_pdf))
```

### 3. Criar Diretórios para Novos Estados no `build.py`

Para garantir que os diretórios corretos sejam criados ao gerar a distribuição, atualize o arquivo `build.py`:

```python
# Na seção que cria pastas de downloads
downloads_dir_am = os.path.join(dist_folder, 'Downloads', 'Diários', 'AM')
os.makedirs(os.path.join(downloads_dir_am, 'Diários Oficiais do Estado'), exist_ok=True)
os.makedirs(os.path.join(downloads_dir_am, 'Diários do Tribunal de Justiça'), exist_ok=True)
```

### 4. Reconstruir a Aplicação

Após fazer todas as alterações, execute o script `build.py` para reconstruir a aplicação:

```
python build.py
```

Este processo irá:

1. Empacotar seu código atualizado em um executável
2. Criar a estrutura de diretórios necessária
3. Gerar os arquivos de distribuição atualizados

## Dicas para Adicionar Novos Diários

1. **Pesquise a URL correta:** Encontre a URL oficial do diário que deseja adicionar.
2. **Identifique o XPath do botão de download:** Use ferramentas como o DevTools do Chrome para identificar o XPath do botão de download.
3. **Teste a função separadamente:** Antes de integrar à aplicação, teste a nova função separadamente para garantir que funciona corretamente.
4. **Ajuste os tempos de espera (`time.sleep`):** Dependendo da velocidade de carregamento do site, pode ser necessário ajustar os tempos de espera.
5. **Considere tratamento de erros:** Adicione tratamento de exceções para lidar com problemas de conexão ou alterações no site.

## Estrutura de Pastas Recomendada

Para manter a organização, siga esta estrutura de pastas:

```
Downloads/
  └── Diários/
      ├── AC/
      │   ├── Diários Oficiais do Estado/
      │   └── Diários do Tribunal de Justiça/
      ├── AM/
      │   ├── Diários Oficiais do Estado/
      │   └── Diários do Tribunal de Justiça/
      └── [Outros Estados]/
          ├── Diários Oficiais do Estado/
          └── Diários do Tribunal de Justiça/
```

## Considerações Finais

- Para cada novo estado ou tipo de diário que você deseja adicionar, repita este processo, criando funções apropriadas no `main.py` e atualizando a GUI de acordo.
- Considere implementar um sistema de configuração mais dinâmico no futuro, que permita adicionar diários sem precisar modificar o código-fonte.
- Lembre-se de que os sites dos diários oficiais podem mudar com o tempo, exigindo atualizações nas funções de download.
