import tkinter as tk
import threading
from tkinter import messagebox
from config import carregar_config, salvar_config, selecionar_diretorio
from download import executar_comando
from utils import listar_formatos, tem_restricao_de_idade
from widgets import criar_widgets
from PIL import Image, ImageTk
import sys
import os

def main():
    tela = tk.Tk()
    tela.title("ytdlp-GUI")
    tela.geometry("700x450")

    # Icone
    def obter_caminho_recurso(caminho_relativo):
        """Retorna o caminho correto do arquivo, seja rodando como script ou como executável."""
        if getattr(sys, 'frozen', False):  # Verifica se está rodando como executável
            base_path = sys._MEIPASS  # PyInstaller armazena arquivos temporários aqui
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, caminho_relativo)

    # Carregar o ícone corretamente
    icone_path = obter_caminho_recurso('icone.png')
    try:
        ico = Image.open(icone_path)
        photo = ImageTk.PhotoImage(ico)
        tela.wm_iconphoto(False, photo)
    except Exception as e:
        print(f"Erro ao carregar o ícone: {e}")

    def limpar_url():
        entrada_url.delete(0, tk.END)

    def iniciar_download(entrada_url, entrada_resolucao, entrada_diretorio):
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
        
        thread = threading.Thread(target=executar_comando, args=(comando, tipo, progresso, tela, saida_texto))
        thread.start()

    ultimo_diretorio = carregar_config()
    entrada_url, entrada_diretorio, opcao_escolhida, formato_audio, progresso, saida_texto = criar_widgets(
        tela, iniciar_download, selecionar_diretorio, limpar_url, ultimo_diretorio
    )

    tela.mainloop()

if __name__ == "__main__":
    main()