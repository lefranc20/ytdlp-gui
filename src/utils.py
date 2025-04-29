import subprocess
import json
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

def atualizar_progresso(linha, progresso, tela):
    if "[download]" in linha and "%" in linha:
        try:
            progresso_percentual = float(linha.split('%')[0].split()[-1])
            progresso['value'] = progresso_percentual
            tela.update_idletasks()
        except ValueError:
            pass

def extrair_metadados(nome_arquivo):
    info_json = f"{nome_arquivo}.info.json"
    if os.path.exists(info_json):
        with open(info_json, "r") as f:
            return json.load(f)
    return None

def embutir_metadados(nome_arquivo, metadata):
    if metadata:
        comentario = json.dumps(metadata, indent=4, ensure_ascii=False)
        comando = [
            "ffmpeg",
            "-i", nome_arquivo,
            "-c", "copy",
            "-metadata", f"comment={comentario}",
            "-map_metadata", "0",
            f"{nome_arquivo}_com_metadados.{nome_arquivo.split('.')[-1]}"
        ]
        subprocess.run(comando, check=True)
        os.replace(f"{nome_arquivo}_com_metadados.{nome_arquivo.split('.')[-1]}", nome_arquivo)
        os.remove(f"{nome_arquivo}.info.json")

def tem_restricao_de_idade(url):
    # Função para verificar se o vídeo tem restrição de idade (o download de thumbnails SEMPRE sofrem esse problema)
    comando = ["yt-dlp", "-j", url]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    if resultado.returncode != 0:
        print(f"Erro ao tentar obter informações sobre o vídeo: {resultado.stderr}")
        return False
    
    info_video = json.loads(resultado.stdout)
    
    # Verifica se o vídeo tem restrição de idade
    if info_video.get('age_limit', 0) > 0:
        return True  # Vídeo tem restrição de idade
    return False  # Vídeo não tem restrição de idade

def listar_formatos(url):
    # Lista os formatos disponíveis para o vídeo usando yt-dlp -F
    try:
        comando = f'yt-dlp -F "{url}"'
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if resultado.returncode == 0:
            # Exibe o resultado no terminal
            print(resultado.stdout)
            
            # Exibe o resultado em um popup
            popup = tk.Toplevel(tela)
            popup.title("Formatos Disponíveis ('yt-dlp -F')")
            popup.geometry("800x600")  # Aumentei a geometria para acomodar mais texto
            
            # Criando o widget ScrolledText sem quebra de linha
            texto_formatos = scrolledtext.ScrolledText(popup, wrap=tk.NONE, font=("Courier", 8))  # Sem wrap
            texto_formatos.insert(tk.END, resultado.stdout)
            texto_formatos.config(state=tk.DISABLED)  # Impede edição

            # Criando a barra de rolagem  horizontal
            scrollbar_horizontal = tk.Scrollbar(popup, orient=tk.HORIZONTAL, command=texto_formatos.xview)
            texto_formatos.config(xscrollcommand=scrollbar_horizontal.set)
            
            texto_formatos.pack(fill=tk.BOTH, expand=True)  # Expande para o tamanho disponível
            scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

            btn_fechar = tk.Button(popup, text="Fechar", command=popup.destroy)
            btn_fechar.pack(pady=10)
        else:
            messagebox.showerror("Erro", f"Erro ao listar formatos: {resultado.stderr}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")