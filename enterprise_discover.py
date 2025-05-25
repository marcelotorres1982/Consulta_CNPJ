import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import re

def limpar_cnpj(cnpj):
    return re.sub(r'\D', '', cnpj)

def consulta_speedio(cnpj):
    url = f"https://api-publica.speedio.com.br/buscarcnpj?cnpj={cnpj}"
    try:
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            telefone = data.get("TELEFONE")
            email = data.get("EMAIL")
            if telefone or email:
                return {
                    "fonte": "Speedio",
                    "nome_fantasia": data.get("NOME_FANTASIA"),
                    "telefone": telefone,
                    "email": email
                }
    except Exception as e:
        print("Erro na API Speedio:", e)
    return None

def consulta_publica_cnpj_ws(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    try:
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            est = data.get("estabelecimento", {})
            telefone = f'{est.get("ddd", "")}{est.get("telefone", "")}'.strip()
            email = est.get("email")
            if telefone or email:
                return {
                    "fonte": "publica.cnpj.ws",
                    "nome_fantasia": est.get("nome_fantasia"),
                    "telefone": telefone if telefone else None,
                    "email": email
                }
    except Exception as e:
        print("Erro na API publica.cnpj.ws:", e)
    return None

def scraping_cnpj_biz(cnpj):
    url = f"https://cnpj.biz/{cnpj}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            dados = {}

            email_tag = soup.find("a", href=lambda h: h and "mailto:" in h)
            telefone_tag = soup.find("a", href=lambda h: h and "tel:" in h)

            dados["email"] = email_tag.text.strip() if email_tag else None
            dados["telefone"] = telefone_tag.text.strip() if telefone_tag else None

            nome_fantasia = soup.find("h1")
            dados["nome_fantasia"] = nome_fantasia.text.strip() if nome_fantasia else None

            if dados["email"] or dados["telefone"]:
                dados["fonte"] = "scraping.cnpj.biz"
                return dados
    except Exception as e:
        print("Erro ao acessar cnpj.biz:", e)
    return None

def buscar_dados_empresa(cnpj):
    resultado = consulta_speedio(cnpj)
    if resultado:
        return resultado

    resultado = consulta_publica_cnpj_ws(cnpj)
    if resultado:
        return resultado

    resultado = scraping_cnpj_biz(cnpj)
    if resultado:
        return resultado

    return {
        "erro": "Não foi possível encontrar telefone e email nas fontes disponíveis.",
        "fonte": None,
        "telefone": None,
        "email": None
    }

def buscar():
    cnpj_raw = entry.get()
    cnpj = limpar_cnpj(cnpj_raw)
    if len(cnpj) != 14:
        messagebox.showerror("Erro", "Digite um CNPJ válido com 14 dígitos numéricos.")
        return

    resultado = buscar_dados_empresa(cnpj)

    nome_var.set(resultado.get("nome_fantasia", "N/A"))
    fonte_var.set(resultado.get("fonte", "N/A"))

    telefone = resultado.get("telefone") or ""
    email = resultado.get("email") or ""

    telefone_entry.config(state="normal")
    telefone_entry.delete(0, tk.END)
    telefone_entry.insert(0, telefone)
    telefone_entry.config(state="readonly")

    email_entry.config(state="normal")
    email_entry.delete(0, tk.END)
    email_entry.insert(0, email)
    email_entry.config(state="readonly")

root = tk.Tk()
root.title("Consulta de CNPJ")
root.geometry("400x280")
root.resizable(False, False)

tk.Label(root, text="Digite o CNPJ (com ou sem pontos, barras e traços):").pack(pady=5)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

botao = tk.Button(root, text="Buscar", command=buscar)
botao.pack(pady=10)

frame_result = tk.Frame(root)
frame_result.pack(pady=10, fill="x", padx=20)

tk.Label(frame_result, text="Nome fantasia:").grid(row=0, column=0, sticky="w")
nome_var = tk.StringVar(value="")
nome_label = tk.Label(frame_result, textvariable=nome_var, wraplength=350)
nome_label.grid(row=0, column=1, sticky="w")

tk.Label(frame_result, text="Fonte dos dados:").grid(row=1, column=0, sticky="w")
fonte_var = tk.StringVar(value="")
fonte_label = tk.Label(frame_result, textvariable=fonte_var)
fonte_label.grid(row=1, column=1, sticky="w")

tk.Label(frame_result, text="Telefone:").grid(row=2, column=0, sticky="w")
telefone_entry = tk.Entry(frame_result, width=30, state="readonly")
telefone_entry.grid(row=2, column=1, sticky="w")

tk.Label(frame_result, text="Email:").grid(row=3, column=0, sticky="w")
email_entry = tk.Entry(frame_result, width=30, state="readonly")
email_entry.grid(row=3, column=1, sticky="w")

root.mainloop()
