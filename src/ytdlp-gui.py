import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import json
import os
import sys
from PIL import Image, ImageTk

CONFIG_FILE = "config.json"  # Nome do arquivo de configuração, para o local do diretório

def salvar_config(diretorio):
    # Salva o diretório escolhido no arquivo config.json
    with open(CONFIG_FILE, "w") as f:
        json.dump({"diretorio": diretorio}, f)

def carregar_config():
    # Carrega o diretório salvo no arquivo config.json
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("diretorio", "")  # Retorna o diretório salvo
    return ""  # Retorna vazio se o arquivo não existir

def selecionar_diretorio():
    # Abre o seletor de diretórios e salva a escolha
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

def extrair_metadados(nome_arquivo):
    # Extrai metadados do arquivo JSON gerado pelo yt-dlp
    info_json = f"{nome_arquivo}.info.json"
    if os.path.exists(info_json):
        with open(info_json, "r") as f:
            metadata = json.load(f)
            return metadata
    return None

def embutir_metadados(nome_arquivo, metadata):
    # Embutir metadados no arquivo de vídeo/áudio usando ffmpeg
    if metadata:
        # Converte todo o conteúdo do JSON em uma string formatada
        comentario = json.dumps(metadata, indent=4, ensure_ascii=False)

        # Comando ffmpeg para embutir os metadados no arquivo
        comando = [
            "ffmpeg",
            "-i", nome_arquivo,  # Arquivo de entrada
            "-c", "copy",  # Copia o vídeo/áudio sem re-encodar
            "-metadata", f"comment={comentario}",  # Embutir todo o JSON no campo "comment"
            "-map_metadata", "0",  # Mapeia os metadados para o arquivo de saída
            f"{nome_arquivo}_com_metadados.{nome_arquivo.split('.')[-1]}"  # Arquivo de saída
        ]

        # Executa o comando ffmpeg
        subprocess.run(comando, check=True)

        # Substitui o arquivo original pelo arquivo com metadados
        os.replace(f"{nome_arquivo}_com_metadados.{nome_arquivo.split('.')[-1]}", nome_arquivo)
        os.remove(f"{nome_arquivo}.info.json")  # Remove o arquivo JSON de metadados

def executar_comando(comando, tipo):
    try:
        progresso['value'] = 0
        process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        saida_texto.delete(1.0, tk.END)
        for linha in process.stdout:
            saida_texto.insert(tk.END, linha)
            saida_texto.see(tk.END)
            atualizar_progresso(linha)
        process.wait()

        if tipo in ["audio", "melhor_video", "resolucao"]:
            # Extrai o nome do arquivo baixado
            nome_arquivo = None
            for linha in saida_texto.get("1.0", tk.END).splitlines():
                if "Destination: " in linha:
                    nome_arquivo = linha.split("Destination: ")[-1].strip()
                    break

            if nome_arquivo and os.path.exists(nome_arquivo):
                metadata = extrair_metadados(nome_arquivo.split('.')[0])
                if metadata:
                    embutir_metadados(nome_arquivo, metadata)

        messagebox.showinfo("Sucesso", "Download concluído!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {e}")

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

def iniciar_download():
    url = entrada_url.get()
    diretorio = entrada_diretorio.get()
    
    if not url or not diretorio or not opcao_escolhida.get():
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return
    
    # Verifica se o vídeo tem restrição de idade
    if tem_restricao_de_idade(url):
        # Se tiver restrição, não baixa miniatura (não dando problemas no download do video)
        miniatura = "--no-thumbnail"
    else:
        # Se não tiver restrição, baixa a miniatura
        miniatura = "--embed-thumbnail"

    tipo = opcao_escolhida.get() 
    if tipo == "audio":
        formato = formato_audio.get()
        comando = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "bestaudio",
            "-x",
            "--audio-format", formato,
            "-o", f"{diretorio}/%(title)s [%(upload_date)s] [%(id)s].%(ext)s",
            "--embed-metadata",
            miniatura,
            url
        ]
    elif tipo == "melhor_video":
        comando = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "bestvideo+bestaudio", "--merge-output-format", "mp4",
            "-o", f"{diretorio}/%(title)s [%(upload_date)s] [%(id)s].%(ext)s",
            "--embed-metadata",
            miniatura,
            url
        ]
    elif tipo == "resolucao":
        resolucao = entrada_resolucao.get()
        comando = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", f"bestvideo[height<={resolucao}]+bestaudio/best[height<={resolucao}]",
            "--merge-output-format", "mp4",
            "-o", f"{diretorio}/%(title)s [%(upload_date)s] [%(id)s].%(ext)s",
            "--embed-metadata",
            miniatura,
            url
        ]
    elif tipo == "playlist":
        comando = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-o", f"{diretorio}/%(playlist_title)s/%(playlist_index)s-%(title)s [%(upload_date)s] [%(id)s].%(ext)s",
            "--embed-metadata",
            miniatura,
            url
        ]
    elif tipo == "listar_formatos":
        listar_formatos(url)
        return
    
    thread = threading.Thread(target=executar_comando, args=(comando, tipo))
    thread.start()

# Criando a interface
tela = tk.Tk()
tela.title("ytdlp-GUI")
tela.geometry("700x450")

# Frame para a URL e local de Download
frame_inicio = tk.Frame(tela)
frame_inicio.pack()

# Entrada da URL
tk.Label(frame_inicio, text="URL do Vídeo/Playlist:").grid(column=0, row=0)
entrada_url = tk.Entry(frame_inicio, width=50)
entrada_url.grid(column=1, row=0)

# Botão para limpar a URL
botaoLimpar = tk.Button(frame_inicio, text="Limpar a URL", font=("Helvetica", 10))
botaoLimpar.grid(column=2, row=0, pady=10)
botaoLimpar.config(command=lambda: entrada_url.delete(0, tk.END))

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

radio_listar_formatos = tk.Radiobutton(frame_opcoes, text="Listar Formatos Disponíveis", variable=opcao_escolhida, value="listar_formatos")
radio_listar_formatos.grid(row=4, column=0, sticky='w')

# Botão de download
btn_download = tk.Button(tela, text="Baixar", command=iniciar_download)
btn_download.pack()

# Barra de progresso
progresso = ttk.Progressbar(tela, mode='determinate', length=400)
progresso.pack(fill=tk.X, padx=5, pady=5)

# Área de saída de texto (simulando um terminal, para visualizar a saída dos comandos reais)
saida_texto = tk.Text(tela, height=10, width=60, bg="black", fg="white", font=("Courier", 9))
saida_texto.pack(fill=tk.X)

# Icone (NOVO)
def obter_caminho_recurso(caminho_relativo):
    """Retorna o caminho correto do arquivo, seja rodando como script ou como executável."""
    if getattr(sys, 'frozen', False):  # Verifica se está rodando como executável
        base_path = sys._MEIPASS  # PyInstaller armazena arquivos temporários aqui
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, caminho_relativo)

# Carregar o ícone corretamente
icone_path = obter_caminho_recurso('src/icone.png')
try:
    ico = Image.open(icone_path)
    photo = ImageTk.PhotoImage(ico)
    tela.wm_iconphoto(False, photo)
except Exception as e:
    print(f"Erro ao carregar o ícone: {e}")


# Rodando a interface
tela.mainloop()