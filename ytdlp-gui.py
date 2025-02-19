import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import json
import os
from PIL import Image, ImageTk

CONFIG_FILE = "config.json"  # Nome do arquivo de configuração, para o local do diretório

def salvar_config(diretorio):
    """Salva o diretório escolhido no arquivo config.json"""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"diretorio": diretorio}, f)

def carregar_config():
    """Carrega o diretório salvo no arquivo config.json"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("diretorio", "")  # Retorna o diretório salvo
    return ""  # Retorna vazio se o arquivo não existir

def selecionar_diretorio():
    """Abre o seletor de diretórios e salva a escolha"""
    diretorio = filedialog.askdirectory()
    if diretorio:
        entrada_diretorio.delete(0, tk.END)
        entrada_diretorio.insert(0, diretorio)
        salvar_config(diretorio)  # Salva a escolha do usuário

def atualizar_progresso(linha):
    if "[download]" in linha and "%" in linha:
        try:
            progresso_percentual = float(linha.split('%')[0].split()[-1])
            progresso['value'] = progresso_percentual
            tela.update_idletasks()
        except ValueError:
            pass

def executar_comando(comando):
    try:
        progresso['value'] = 0
        process = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        saida_texto.delete(1.0, tk.END)
        for linha in process.stdout:
            saida_texto.insert(tk.END, linha)
            saida_texto.see(tk.END)
            atualizar_progresso(linha)
        process.wait()
        messagebox.showinfo("Sucesso", "Download concluído!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Ocorreu um erro durante o download!")

def iniciar_download():
    url = entrada_url.get()
    diretorio = entrada_diretorio.get()
    if not url or not diretorio or not opcao_escolhida.get():
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return
    
    tipo = opcao_escolhida.get()
    if tipo == "audio":
        formato = formato_audio.get()
        comando = f'yt-dlp -f bestaudio -x --audio-format {formato} -o "{diretorio}/%(title)s [%(upload_date)s] [%(id)s].%(ext)s" "{url}"'
    elif tipo == "melhor_video":
        comando = f'yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 -o "{diretorio}/%(title)s [%(upload_date)s] [%(id)s].%(ext)s" "{url}"'
    elif tipo == "resolucao":
        resolucao = entrada_resolucao.get()
        comando = f'yt-dlp -f "bestvideo[height<={resolucao}]+bestaudio/best[height<={resolucao}]" --merge-output-format mp4 -o "{diretorio}/%(title)s [%(upload_date)s] [%(id)s].%(ext)s" "{url}"'
    elif tipo == "playlist":
        comando = f'yt-dlp -o "{diretorio}/%(playlist_title)s/%(playlist_index)s-%(title)s [%(upload_date)s] [%(id)s].%(ext)s" "{url}"'
    
    thread = threading.Thread(target=executar_comando, args=(comando,))
    thread.start()

# Criando a interface
tela = tk.Tk()
tela.title("ytdlp-GUI")
tela.geometry("500x400")

# Entrada da URL
tk.Label(tela, text="URL do Vídeo/Playlist:").pack()
entrada_url = tk.Entry(tela, width=50)
entrada_url.pack()

# Escolha do diretório
tk.Label(tela, text="Diretório de Download:").pack()
entrada_diretorio = tk.Entry(tela, width=50)
entrada_diretorio.pack()

# Carregar o último diretório salvo
ultimo_diretorio = carregar_config()
entrada_diretorio.insert(0, ultimo_diretorio)  # Preenche o campo com o diretório salvo

tk.Button(tela, text="Selecionar", command=selecionar_diretorio).pack(pady=10)

# Opções de download
opcao_escolhida = tk.StringVar()

frame_opcoes = tk.Frame(tela)
frame_opcoes.pack()

radio_audio = tk.Radiobutton(frame_opcoes, text="Baixar Áudio", variable=opcao_escolhida, value="audio")
radio_audio.grid(row=0, column=0, sticky='w')
formato_audio = tk.StringVar(value="mp3")
ttk.Combobox(frame_opcoes, textvariable=formato_audio, values=["mp3", "m4a"]).grid(row=0, column=1)

radio_video_melhor = tk.Radiobutton(frame_opcoes, text="Melhor Qualidade ('Best')", variable=opcao_escolhida, value="melhor_video")
radio_video_melhor.grid(row=1, column=0, sticky='w')

radio_video_resolucao = tk.Radiobutton(frame_opcoes, text="Resolução Específica (Exemplo: 720)", variable=opcao_escolhida, value="resolucao")
radio_video_resolucao.grid(row=2, column=0, sticky='w')
entrada_resolucao = tk.Entry(frame_opcoes, width=10)
entrada_resolucao.grid(row=2, column=1)

radio_playlist = tk.Radiobutton(frame_opcoes, text="Baixar Playlist", variable=opcao_escolhida, value="playlist")
radio_playlist.grid(row=3, column=0, sticky='w')

# Botão de download
btn_download = tk.Button(tela, text="Baixar", command=iniciar_download)
btn_download.pack()

# Barra de progresso
progresso = ttk.Progressbar(tela, mode='determinate', length=400)
progresso.pack(fill=tk.X, padx=5, pady=5)

# Área de saída de texto (simulando um terminal, para visualizar a saída dos comandos reais)
saida_texto = tk.Text(tela, height=10, width=60, bg="black", fg="white", font=("Courier", 9))
saida_texto.pack(fill=tk.X)

# Icone (de teste meuy)
ico = Image.open('icone.png')
photo = ImageTk.PhotoImage(ico)
tela.wm_iconphoto(False, photo)

# Rodando a interface
tela.mainloop()