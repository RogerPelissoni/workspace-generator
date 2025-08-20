import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
from datetime import datetime
import os

NUM_CONTAINERS = 10
ARQUIVO_CAMINHOS = "caminhos.txt"
ARQUIVO_HISTORICO = "historico.txt"

entradas_caminho = {}
entradas_titulo = {}

def registrar_historico(container, titulo):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"{agora} | {container} | {titulo}\n"
    with open(ARQUIVO_HISTORICO, "a", encoding="utf-8") as f:
        f.write(linha)

def carregar_historico():
    try:
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            conteudo = f.read()
        caixa_historico.config(state="normal")
        caixa_historico.delete(1.0, tk.END)
        caixa_historico.insert(tk.END, conteudo)
        caixa_historico.config(state="disabled")
    except FileNotFoundError:
        caixa_historico.config(state="normal")
        caixa_historico.delete(1.0, tk.END)
        caixa_historico.insert(tk.END, "Nenhum histórico disponível ainda.")
        caixa_historico.config(state="disabled")

def salvar_caminhos():
    with open(ARQUIVO_CAMINHOS, "w", encoding="utf-8") as f:
        for nome in entradas_caminho:
            caminho = entradas_caminho[nome].get().strip()
            titulo = entradas_titulo[nome].get().strip()
            f.write(f"{nome}|{caminho}|{titulo}\n")

def carregar_caminhos():
    if not os.path.exists(ARQUIVO_CAMINHOS):
        return
    with open(ARQUIVO_CAMINHOS, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split("|")
            if len(partes) == 3:
                nome, caminho, titulo = partes
                if nome in entradas_caminho:
                    entradas_caminho[nome].insert(0, caminho)
                if nome in entradas_titulo:
                    entradas_titulo[nome].insert(0, titulo)

def executar_container():
    container_selecionado = var_container.get()
    caminho = entradas_caminho[container_selecionado].get().strip()
    titulo = entradas_titulo[container_selecionado].get().strip()

    if not caminho:
        messagebox.showwarning("Aviso", f"Defina o caminho para o {container_selecionado}.")
        return

    comando = f'start cmd /k "title {titulo} && echo {container_selecionado} aberto && \"{caminho}\""'

    try:
        subprocess.Popen(comando, shell=True)
        registrar_historico(container_selecionado, titulo)
        carregar_historico()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao iniciar:\n{e}")

def ao_fechar():
    salvar_caminhos()
    janela.destroy()

def filtrar_historico():
    termo = entrada_filtro.get().lower()
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            filtradas = [linha for linha in linhas if termo in linha.lower()]
            caixa_historico.config(state="normal")
            caixa_historico.delete(1.0, tk.END)
            caixa_historico.insert(tk.END, "".join(filtradas))
            caixa_historico.config(state="disabled")

# Interface gráfica
janela = tk.Tk()
janela.title("Gerenciador de Containers")
janela.protocol("WM_DELETE_WINDOW", ao_fechar)

tk.Label(janela, text="Escolha o container e defina título e caminho:").pack(pady=5)
var_container = tk.StringVar(value="Container 1")

for i in range(1, NUM_CONTAINERS + 1):
    nome = f"Container {i}"
    frame = tk.Frame(janela)
    frame.pack(fill="x", padx=10, pady=2)

    tk.Radiobutton(frame, text=nome, variable=var_container, value=nome).pack(side="left")

    tk.Label(frame, text="Título:", width=7).pack(side="left")
    entrada_titulo = tk.Entry(frame, width=30)
    entrada_titulo.pack(side="left", padx=5)
    entradas_titulo[nome] = entrada_titulo

    tk.Label(frame, text="Caminho:", width=8).pack(side="left")
    entrada_caminho = tk.Entry(frame, width=50)
    entrada_caminho.pack(side="left", padx=5)
    entradas_caminho[nome] = entrada_caminho

tk.Button(janela, text="Executar", command=executar_container).pack(pady=10)

tk.Label(janela, text="Filtro de histórico:").pack(pady=5)
entrada_filtro = tk.Entry(janela, width=40)
entrada_filtro.pack(pady=5)
entrada_filtro.bind("<KeyRelease>", lambda e: filtrar_historico())

tk.Label(janela, text="Histórico de execuções:").pack(pady=5)
caixa_historico = scrolledtext.ScrolledText(janela, width=100, height=12, state="disabled")
caixa_historico.pack(pady=5)

carregar_caminhos()
carregar_historico()
janela.mainloop()