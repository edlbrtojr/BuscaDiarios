#!/usr/bin/env python
import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Busca Diários - Download e busca de termos em diários oficiais')
    parser.add_argument('--cli', action='store_true', help='Executar no modo linha de comando (sem interface gráfica)')
    parser.add_argument('--terms', nargs='+', help='Termos para buscar (apenas no modo CLI)')
    args = parser.parse_args()

    if args.cli:
        # Modo linha de comando
        import main
        if args.terms:
            # Substituir os termos de busca pelos argumentos passados
            main.infos_buscadas = args.terms
        
        # Executar o script principal
        import main
        if __name__ == "__main__":
            main_module_name = os.path.splitext(os.path.basename(main.__file__))[0]
            main_spec = __import__(main_module_name)
    else:
        # Modo gráfico
        import gui
        import tkinter as tk
        
        def center_window(window, width=900, height=700):
            # Get screen dimensions
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            
            # Calculate position coordinates
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            
            # Set the window position
            window.geometry(f"{width}x{height}+{x}+{y}")
            
        if __name__ == "__main__":
            root = tk.Tk()
            app = gui.DiariosBuscaApp(root)
            center_window(root)
            root.mainloop()

if __name__ == "__main__":
    main() 