import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, filedialog
import threading
import os
import time
from datetime import datetime
import main

class DiariosBuscaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Busca Diários - AC")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Variáveis
        self.search_terms = main.infos_buscadas
        self.download_folder = os.path.join(os.getcwd(), "Downloads", "Diários")
        self.pdfs_baixados = []
        self.is_running = False
        
        # Criar os componentes da interface
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Busca Diários - Acre", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Frame para configurações
        config_frame = ttk.LabelFrame(main_frame, text="Configurações", padding=10)
        config_frame.pack(fill=tk.X, pady=5)
        
        # Pasta de download
        folder_frame = ttk.Frame(config_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(folder_frame, text="Pasta de Downloads:").pack(side=tk.LEFT, padx=(0, 5))
        self.folder_entry = ttk.Entry(folder_frame)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.folder_entry.insert(0, self.download_folder)
        
        browse_btn = ttk.Button(folder_frame, text="Procurar", command=self.browse_folder)
        browse_btn.pack(side=tk.LEFT)
        
        # Frame para termos de busca
        terms_frame = ttk.LabelFrame(main_frame, text="Termos de Busca", padding=10)
        terms_frame.pack(fill=tk.X, pady=5)
        
        self.terms_text = scrolledtext.ScrolledText(terms_frame, height=5, wrap=tk.WORD)
        self.terms_text.pack(fill=tk.X, expand=True)
        
        # Preencher com os termos existentes
        self.terms_text.insert(tk.END, "\n".join(self.search_terms))
        
        # Frame para ações
        action_frame = ttk.Frame(main_frame, padding=10)
        action_frame.pack(fill=tk.X, pady=5)
        
        # Checkboxes para selecionar os diários
        self.check_frame = ttk.Frame(action_frame)
        self.check_frame.pack(anchor=tk.W, pady=5)
        
        self.doe_var = tk.BooleanVar(value=True)
        self.dtj_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(self.check_frame, text="Diário Oficial do Estado", variable=self.doe_var).pack(anchor=tk.W)
        ttk.Checkbutton(self.check_frame, text="Diário do Tribunal de Justiça", variable=self.dtj_var).pack(anchor=tk.W)
        
        # Botões
        button_frame = ttk.Frame(action_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.run_button = ttk.Button(button_frame, text="Iniciar Busca", command=self.run_search)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Parar", command=self.stop_search, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(action_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill=tk.X, pady=5)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto")
        status_label = ttk.Label(action_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W, pady=5)
        
        # Frame para resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados da Busca", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área de texto para os resultados
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.config(state=tk.DISABLED)
        
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
        self.stop_button.config(state=tk.NORMAL)
        
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
                doe_pdf = main.Diario_Estado_Acre()
                if doe_pdf:
                    self.pdfs_baixados.append(doe_pdf)
                    self.add_result("Download concluído: " + os.path.basename(doe_pdf))
            
            if self.dtj_var.get() and self.is_running:
                self.update_status("Baixando Diário do Tribunal de Justiça...", 50)
                dtj_pdf = main.Diario_TJ_AC()
                if dtj_pdf:
                    self.pdfs_baixados.append(dtj_pdf)
                    self.add_result("Download concluído: " + os.path.basename(dtj_pdf))
            
            if not self.pdfs_baixados:
                self.add_result("Nenhum diário foi baixado.")
                self.update_status("Nenhum diário baixado", 0)
            else:
                # Buscar os termos nos PDFs
                if self.is_running:
                    self.update_status("Buscando termos nos PDFs...", 75)
                    resultados = main.busca_no_pdf(self.pdfs_baixados)
                    
                    if resultados:
                        self.add_result("\n--- RESULTADOS DA BUSCA ---\n")
                        for resultado in resultados:
                            self.add_result(f"O termo '{resultado['termo']}' foi encontrado {resultado['ocorrencias']} vez(es) na página {resultado['pagina']} do arquivo {resultado['arquivo']}.")
                    else:
                        self.add_result("Nenhum dos termos buscados foi encontrado nos PDFs.")
                    
                    self.update_status("Busca concluída com sucesso!", 100)
                
            if not self.is_running:
                self.update_status("Operação interrompida pelo usuário", 0)
            
        except Exception as e:
            self.add_result(f"Erro durante a execução: {str(e)}")
            self.update_status(f"Erro: {str(e)}", 0)
        
        finally:
            # Restaurar UI
            self.is_running = False
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def add_result(self, text):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiariosBuscaApp(root)
    root.mainloop() 