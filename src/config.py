import json
import os
import tkinter as tk
from tkinter import filedialog

CONFIG_FILE = "config.json"

def salvar_config(diretorio):
    # Salva o diretório escolhido no arquivo config.json
    with open(CONFIG_FILE, "w") as f:
        json.dump({"diretorio": diretorio}, f)

def carregar_config():
    # Carrega o diretório salvo no arquivo config.json
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("diretorio", "") # Retorna o diretório salvo
    return "" # Retorna vazio se o arquivo não existir

def selecionar_diretorio(entrada_diretorio):
    # Abre o seletor de diretórios e salva a escolha
    diretorio = filedialog.askdirectory()
    if diretorio:
        entrada_diretorio.delete(0, tk.END)
        entrada_diretorio.insert(0, diretorio)
        salvar_config(diretorio)  # Salva a escolha do usuário