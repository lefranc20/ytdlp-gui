import tkinter as tk
from tkinter import ttk

def criar_widgets(tela, iniciar_download, selecionar_diretorio, limpar_url, ultimo_diretorio):
    # Frame início
    frame_inicio = tk.Frame(tela)
    frame_inicio.pack()

    tk.Label(frame_inicio, text="URL do Vídeo/Playlist:").grid(column=0, row=0)
    entrada_url = tk.Entry(frame_inicio, width=50)
    entrada_url.grid(column=1, row=0)

    botaoLimpar = tk.Button(frame_inicio, text="Limpar a URL", font=("Helvetica", 10), command=limpar_url)
    botaoLimpar.grid(column=2, row=0, pady=10)

    # Diretório de download
    tk.Label(tela, text="Diretório de Download:").pack()
    entrada_diretorio = tk.Entry(tela, width=50)
    entrada_diretorio.pack()
    entrada_diretorio.insert(0, ultimo_diretorio)

    tk.Button(tela, text="Selecionar", command=lambda: selecionar_diretorio(entrada_diretorio)).pack(pady=10)

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
    # botao_download = tk.Button(tela, text="Iniciar Download", command=iniciar_download)
    # botao_download.pack(pady=20)
    # Novo botão de download:
    tk.Button(tela, text="Baixar", command=lambda: iniciar_download(entrada_url, entrada_resolucao, entrada_diretorio)).pack(pady=10)

    # Barra de progresso
    progresso = ttk.Progressbar(tela, orient="horizontal", length=400, mode="determinate")
    progresso.pack()

    # Área de saída de texto (simulando um terminal, para visualizar a saída dos comandos reais)
    saida_texto = tk.Text(tela, height=10, width=60, bg="black", fg="white", font=("Courier", 9))
    saida_texto.pack(fill=tk.X)

    return entrada_url, entrada_diretorio, opcao_escolhida, formato_audio, progresso, saida_texto