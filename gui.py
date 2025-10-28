import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, filedialog
import threading
import os
import time
from datetime import datetime
import main
import pdfplumber
from tkinter.font import Font
import sys

class ModernUI:
    def __init__(self, root):
        # Configure colors - Light modern theme
        self.colors = {
            "bg_light": "#ffffff",        # White background
            "bg_off": "#f8fafc",          # Slightly off-white background (slate-50)
            "primary": "#3b82f6",         # Primary blue (blue-500)
            "primary_hover": "#2563eb",   # Primary hover (blue-600)
            "secondary": "#8b5cf6",       # Secondary purple (violet-500)
            "accent": "#f97316",          # Accent orange (orange-500)
            "success": "#10b981",         # Success color (emerald-500)
            "danger": "#ef4444",          # Danger/error color (red-500)
            "text_dark": "#1e293b",       # Dark text (slate-800)
            "text_muted": "#64748b",      # Muted text (slate-500)
            "border": "#e2e8f0",          # Border color (slate-200)
            "card_bg": "#ffffff",         # Card background (white)
            "card_shadow": "#f1f5f9",     # Card shadow color (slate-100)
            "input_bg": "#f8fafc"         # Input background (slate-50)
        }
        
        # Configure fonts
        self.fonts = {
            "title": Font(family="Segoe UI", size=16, weight="bold"),
            "subtitle": Font(family="Segoe UI", size=12, weight="bold"),
            "body": Font(family="Segoe UI", size=10),
            "small": Font(family="Segoe UI", size=9),
            "button": Font(family="Segoe UI", size=10, weight="bold")
        }
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        
        # Frame styles
        style.configure("Modern.TFrame", background=self.colors["bg_light"])
        style.configure("Card.TFrame", background=self.colors["card_bg"], relief="flat")
        
        # Label styles
        style.configure("Modern.TLabel", 
                        background=self.colors["bg_light"], 
                        foreground=self.colors["text_dark"])
        
        style.configure("Card.TLabel", 
                        background=self.colors["card_bg"], 
                        foreground=self.colors["text_dark"])
                        
        style.configure("Title.TLabel", 
                        background=self.colors["bg_light"], 
                        foreground=self.colors["primary"],
                        font=self.fonts["title"])
                        
        style.configure("Subtitle.TLabel", 
                        background=self.colors["card_bg"], 
                        foreground=self.colors["text_dark"],
                        font=self.fonts["subtitle"])
        
        # Button styles - Ensure button text is visible
        style.configure("Primary.TButton", 
                        font=self.fonts["button"])
        
        style.map("Primary.TButton",
                 background=[("active", self.colors["primary_hover"]), ("!disabled", self.colors["primary"])],
                 foreground=[("active", "#ffffff"), ("!disabled", "#ffffff")])
        
        style.configure("Danger.TButton", 
                        font=self.fonts["button"])
        
        style.map("Danger.TButton",
                 background=[("active", "#b91c1c"), ("!disabled", self.colors["danger"])],
                 foreground=[("active", "#ffffff"), ("!disabled", "#ffffff")])
        
        # Progressbar style
        style.configure("Modern.Horizontal.TProgressbar", 
                        background=self.colors["primary"],
                        troughcolor=self.colors["bg_off"])
        
        # Entry style
        style.configure("Modern.TEntry", 
                        fieldbackground=self.colors["input_bg"],
                        foreground=self.colors["text_dark"],
                        insertcolor=self.colors["text_dark"],
                        borderwidth=1)
        
        # Checkbutton style
        style.configure("Modern.TCheckbutton", 
                        background=self.colors["card_bg"],
                        foreground=self.colors["text_dark"])
        
        style.map("Modern.TCheckbutton",
                 background=[("active", self.colors["card_bg"])],
                 foreground=[("active", self.colors["text_dark"])])
        
        # LabelFrame style
        style.configure("Card.TLabelframe", 
                        background=self.colors["card_bg"],
                        foreground=self.colors["text_dark"],
                        borderwidth=1,
                        relief="solid")
        
        style.configure("Card.TLabelframe.Label", 
                        background=self.colors["card_bg"],
                        foreground=self.colors["primary"],
                        font=self.fonts["subtitle"])

class DiariosBuscaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Busca Diários - Acre")
        self.root.geometry("900x700")
        self.root.minsize(900, 700)
        
        # Apply modern theme
        self.ui = ModernUI(root)
        self.root.configure(bg=self.ui.colors["bg_light"])
        
        # Variáveis
        self.search_terms = main.infos_buscadas
        self.download_folder = os.path.join(os.getcwd(), "Downloads", "Diários")
        self.pdfs_baixados = []
        self.is_running = False
        
        # Ícones (emojis)
        self.icons = {
            "doc": "📄",
            "search": "🔍",
            "download": "📥",
            "settings": "⚙️",
            "check": "✅",
            "error": "❌",
            "warning": "⚠️",
            "star": "⭐",
            "loading": "🔄",
            "result": "📋",
            "sparkles": "✨",
            "folder": "📁"
        }
        
        # Criar os componentes da interface
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, style="Modern.TFrame", padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho com ícone e título
        header_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Logo placeholder (emoji como um ícone simples)
        logo_label = ttk.Label(header_frame, text=f"{self.icons['doc']}", font=Font(size=24), style="Modern.TLabel")
        logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Container para título e subtítulo
        title_container = ttk.Frame(header_frame, style="Modern.TFrame")
        title_container.pack(side=tk.LEFT, fill=tk.X)
        
        # Título principal
        title_label = ttk.Label(title_container, text="Busca Diários", style="Title.TLabel")
        title_label.pack(anchor=tk.W)
        
        # Subtítulo
        subtitle_label = ttk.Label(title_container, 
                                   text="Busca e processamento de diários oficiais do Acre",
                                   style="Modern.TLabel",
                                   font=self.ui.fonts["body"],
                                   foreground=self.ui.colors["text_muted"])
        subtitle_label.pack(anchor=tk.W)
        
        # Container principal com duas colunas
        content_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna da esquerda (configurações)
        left_column = ttk.Frame(content_frame, style="Modern.TFrame")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        # Coluna da direita (resultados)
        right_column = ttk.Frame(content_frame, style="Modern.TFrame")
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))
        
        # === COLUNA ESQUERDA (CONFIGURAÇÕES) ===
        
        # Card para configurações
        config_card = ttk.LabelFrame(left_column, text=f"{self.icons['settings']} Configurações", 
                                    style="Card.TLabelframe", padding=15)
        config_card.pack(fill=tk.X, pady=5)
        
        # Pasta de download
        folder_frame = ttk.Frame(config_card, style="Card.TFrame")
        folder_frame.pack(fill=tk.X, pady=10)
        
        folder_label = ttk.Label(folder_frame, text=f"{self.icons['folder']} Pasta de Downloads:", style="Card.TLabel")
        folder_label.pack(anchor=tk.W, pady=(0, 5))
        
        folder_input_frame = ttk.Frame(folder_frame, style="Card.TFrame")
        folder_input_frame.pack(fill=tk.X)
        
        self.folder_entry = ttk.Entry(folder_input_frame, style="Modern.TEntry")
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.folder_entry.insert(0, self.download_folder)
        
        # Use tk.Button instead of ttk.Button for better control of colors
        self.browse_btn = tk.Button(folder_input_frame, text="Procurar", 
                               bg=self.ui.colors["primary"],
                               fg="white",
                               font=self.ui.fonts["button"],
                               activebackground=self.ui.colors["primary_hover"],
                               activeforeground="white",
                               relief=tk.FLAT,
                               padx=10,
                               command=self.browse_folder)
        self.browse_btn.pack(side=tk.RIGHT)
        
        # Card para termos de busca
        terms_card = ttk.LabelFrame(left_column, text=f"{self.icons['search']} Termos de Busca", 
                                  style="Card.TLabelframe", padding=15)
        terms_card.pack(fill=tk.BOTH, expand=True, pady=10)
        
        terms_info = ttk.Label(terms_card, 
                              text="Digite os termos de busca, um por linha:",
                              style="Card.TLabel")
        terms_info.pack(anchor=tk.W, pady=(0, 5))
        
        # Estilizar o ScrolledText
        self.terms_text = scrolledtext.ScrolledText(terms_card, height=8, width=0,
                                                   wrap=tk.WORD, font=self.ui.fonts["body"],
                                                   bg=self.ui.colors["input_bg"],
                                                   fg=self.ui.colors["text_dark"],
                                                   insertbackground=self.ui.colors["text_dark"])
        self.terms_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Preencher com os termos existentes
        self.terms_text.insert(tk.END, "\n".join(self.search_terms))
        
        # Card para ações
        action_card = ttk.LabelFrame(left_column, text="Ações", 
                                   style="Card.TLabelframe", padding=15)
        action_card.pack(fill=tk.X, pady=5)
        
        # Checkboxes para selecionar os diários
        self.check_frame = ttk.Frame(action_card, style="Card.TFrame")
        self.check_frame.pack(fill=tk.X, pady=5)
        
        check_title = ttk.Label(self.check_frame, text="Selecione os diários para busca:",
                               style="Card.TLabel")
        check_title.pack(anchor=tk.W, pady=(0, 5))
        
        self.doe_var = tk.BooleanVar(value=True)
        self.dtj_var = tk.BooleanVar(value=True)
        
        doe_check = ttk.Checkbutton(self.check_frame, text="Diário Oficial do Estado", 
                                  variable=self.doe_var, style="Modern.TCheckbutton")
        doe_check.pack(anchor=tk.W, padx=(10, 0), pady=2)
        
        dtj_check = ttk.Checkbutton(self.check_frame, text="Diário do Tribunal de Justiça", 
                                  variable=self.dtj_var, style="Modern.TCheckbutton")
        dtj_check.pack(anchor=tk.W, padx=(10, 0), pady=2)
        
        # Botões
        button_frame = ttk.Frame(action_card, style="Card.TFrame")
        button_frame.pack(fill=tk.X, pady=(15, 5))
        
        # Use tk.Button instead of ttk.Button for better control of colors
        self.run_button = tk.Button(button_frame, 
                                  text=f"{self.icons['search']} Iniciar Busca", 
                                  bg=self.ui.colors["primary"],
                                  fg="white",
                                  font=self.ui.fonts["button"],
                                  activebackground=self.ui.colors["primary_hover"],
                                  activeforeground="white",
                                  relief=tk.FLAT,
                                  padx=10,
                                  command=self.run_search)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, 
                                   text=f"{self.icons['error']} Parar", 
                                   bg=self.ui.colors["danger"],
                                   fg="white",
                                   font=self.ui.fonts["button"],
                                   activebackground="#b91c1c",  # darker red
                                   activeforeground="white",
                                   relief=tk.FLAT,
                                   padx=10,
                                   state=tk.DISABLED,
                                   disabledforeground="#f1f5f9",
                                   command=self.stop_search)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # === COLUNA DIREITA (RESULTADOS) ===
        
        # Card para progresso
        progress_card = ttk.LabelFrame(right_column, text=f"{self.icons['loading']} Status", 
                                     style="Card.TLabelframe", padding=15)
        progress_card.pack(fill=tk.X, pady=5)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para iniciar")
        status_label = ttk.Label(progress_card, textvariable=self.status_var, style="Card.TLabel")
        status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Barra de progresso
        progress_label = ttk.Label(progress_card, text="Progresso:", style="Card.TLabel")
        progress_label.pack(anchor=tk.W, pady=(5, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_card, variable=self.progress_var, 
                                      maximum=100, length=200, mode='determinate',
                                      style="Modern.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        # Card para resultados
        results_card = ttk.LabelFrame(right_column, text=f"{self.icons['result']} Resultados da Busca", 
                                    style="Card.TLabelframe", padding=15)
        results_card.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Área de texto para os resultados
        self.results_text = scrolledtext.ScrolledText(results_card, wrap=tk.WORD, 
                                                    bg=self.ui.colors["input_bg"],
                                                    fg=self.ui.colors["text_dark"],
                                                    font=self.ui.fonts["body"])
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.config(state=tk.DISABLED)
        
        # Rodapé
        footer_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        footer_frame.pack(fill=tk.X, pady=(15, 0))
        
        footer_text = ttk.Label(footer_frame, 
                              text="© 2025 • Busca Diários • v1.0",
                              style="Modern.TLabel",
                              font=self.ui.fonts["small"],
                              foreground=self.ui.colors["text_muted"])
        footer_text.pack(side=tk.RIGHT)
        
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
    
    def update_status(self, message, progress=None):
        self.status_var.set(message)
        if progress is not None:
            self.progress_var.set(progress)
        self.root.update_idletasks()
    
    def run_search(self):
        if self.is_running:
            return
        
        # Atualizar termos de busca
        terms = self.terms_text.get("1.0", tk.END).strip().split("\n")
        if not terms or all(term.strip() == "" for term in terms):
            messagebox.showerror("Erro", "Por favor, insira pelo menos um termo de busca.")
            return
        
        # Atualizar configurações
        main.infos_buscadas = [term.strip() for term in terms if term.strip()]
        download_dir = self.folder_entry.get().strip()
        
        # Verificar se o diretório existe, se não, tentar criar
        if not os.path.exists(download_dir):
            try:
                os.makedirs(download_dir)
            except:
                messagebox.showerror("Erro", f"Não foi possível criar o diretório: {download_dir}")
                return
        
        # Atualizar o diretório de download
        self.download_folder = download_dir
        
        # Limpar resultados anteriores
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        # Configurar UI para execução
        self.is_running = True
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL, bg=self.ui.colors["danger"])
        
        # Iniciar a busca em uma thread
        threading.Thread(target=self.execute_search, daemon=True).start()
    
    def stop_search(self):
        self.is_running = False
        self.update_status("Operação interrompida pelo usuário", 0)
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def execute_search(self):
        try:
            self.pdfs_baixados = []
            
            # Definir os diretórios de download
            doe_dir = os.path.join(self.download_folder, "AC", "Diários Oficiais do Estado")
            dtj_dir = os.path.join(self.download_folder, "AC", "Diários do Tribunal de Justiça")
            
            # Garantir que os diretórios existam
            os.makedirs(doe_dir, exist_ok=True)
            os.makedirs(dtj_dir, exist_ok=True)
            
            # Configurar diretórios no script principal
            main.local_de_download = self.download_folder
            
            # Baixar e processar os diários selecionados
            if self.doe_var.get():
                self.update_status("Baixando Diário Oficial do Estado...", 25)
                self.add_result(f"{self.icons['download']} Iniciando download do Diário Oficial do Estado...")
                doe_pdf = main.Diario_Estado_Acre()
                if doe_pdf:
                    self.pdfs_baixados.append(doe_pdf)
                    self.add_result(f"{self.icons['check']} Download concluído: " + os.path.basename(doe_pdf))
            
            if self.dtj_var.get() and self.is_running:
                self.update_status("Baixando Diário do Tribunal de Justiça...", 50)
                self.add_result(f"{self.icons['download']} Iniciando download do Diário do Tribunal de Justiça...")
                dtj_pdf = main.Diario_TJ_AC()
                if dtj_pdf:
                    self.pdfs_baixados.append(dtj_pdf)
                    self.add_result(f"{self.icons['check']} Download concluído: " + os.path.basename(dtj_pdf))
            
            if not self.pdfs_baixados:
                self.add_result(f"{self.icons['error']} Nenhum diário foi baixado.")
                self.update_status("Nenhum diário baixado", 0)
            else:
                # Buscar os termos nos PDFs
                if self.is_running:
                    self.update_status("Buscando termos nos PDFs...", 75)
                    self.add_result(f"\n{self.icons['search']} INICIANDO BUSCA NOS PDFs {self.icons['search']}\n")
                    resultados = self.busca_no_pdf(self.pdfs_baixados)
                    
                    if resultados:
                        self.add_result(f"\n{self.icons['result']} RESULTADOS DA BUSCA {self.icons['result']}\n")
                        for resultado in resultados:
                            self.add_result(f"{self.icons['star']} O termo '{resultado['termo']}' foi encontrado {resultado['ocorrencias']} vez(es) na página {resultado['pagina']} do arquivo {resultado['arquivo']}.")
                    else:
                        self.add_result(f"{self.icons['search']} Nenhum dos termos buscados foi encontrado nos PDFs.")
                    
                    self.update_status("Busca concluída com sucesso!", 100)
                
            if not self.is_running:
                self.update_status("Operação interrompida pelo usuário", 0)
            
        except Exception as e:
            self.add_result(f"{self.icons['error']} Erro durante a execução: {str(e)}")
            self.update_status(f"Erro: {str(e)}", 0)
        
        finally:
            # Restaurar UI
            self.is_running = False
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    # Versão modificada da função busca_no_pdf para mostrar o progresso na GUI
    def busca_no_pdf(self, lista_de_pdfs):
        resultados = []
        total_pdfs = len(lista_de_pdfs)
        
        for pdf_index, pdf_path in enumerate(lista_de_pdfs):
            if not pdf_path or not os.path.exists(pdf_path):
                self.add_result(f"{self.icons['error']} Erro: O arquivo PDF {pdf_path} não foi encontrado.")
                continue
            
            try:
                with pdfplumber.open(pdf_path) as diario:
                    total_paginas = len(diario.pages)
                    self.add_result(f"{self.icons['doc']} Processando arquivo {os.path.basename(pdf_path)} ({pdf_index + 1}/{total_pdfs}) - {total_paginas} páginas")
                    
                    for numero_pagina, pagina in enumerate(diario.pages, start=1):
                        # Verificar se a busca foi interrompida
                        if not self.is_running:
                            return resultados
                            
                        # Calcular progresso
                        pdf_progress = 75 + (25 * ((pdf_index / total_pdfs) + (numero_pagina / (total_paginas * total_pdfs))))
                        
                        # Atualizar status
                        msg = f"Lendo página {numero_pagina}/{total_paginas} do arquivo {os.path.basename(pdf_path)}"
                        self.update_status(msg, min(99, pdf_progress))
                        self.add_result(msg, replace_last=True)
                        
                        # Processar o conteúdo
                        conteudo = pagina.extract_text()
                        if conteudo:
                            for termo in main.infos_buscadas:
                                ocorrencias = conteudo.lower().count(termo.lower())
                                if ocorrencias > 0:
                                    resultados.append({
                                        'arquivo': os.path.basename(pdf_path),
                                        'pagina': numero_pagina,
                                        'termo': termo,
                                        'ocorrencias': ocorrencias
                                    })
                                    self.add_result(f"{self.icons['sparkles']} Encontrado: '{termo}' ({ocorrencias}x) na página {numero_pagina}")
            except Exception as e:
                self.add_result(f"{self.icons['error']} Erro ao processar o PDF {pdf_path}: {str(e)}")

        return resultados
    
    def add_result(self, text, replace_last=False):
        self.results_text.config(state=tk.NORMAL)
        
        if replace_last:
            # Remover a última linha
            last_line_start = self.results_text.index("end-1c linestart")
            self.results_text.delete(last_line_start, tk.END)
        
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiariosBuscaApp(root)
    root.mainloop() 