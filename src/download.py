import subprocess
import os
import json
from tkinter import messagebox
from utils import atualizar_progresso, extrair_metadados, embutir_metadados

def executar_comando(comando, tipo, progresso, tela, saida_texto):
    try:
        progresso['value'] = 0
        process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        saida_texto.delete(1.0, "end")
        for linha in process.stdout:
            saida_texto.insert("end", linha)
            saida_texto.see("end")
            atualizar_progresso(linha, progresso, tela)
        process.wait()

        if tipo in ["audio", "melhor_video", "resolucao"]:
            nome_arquivo = None
            for linha in saida_texto.get("1.0", "end").splitlines():
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