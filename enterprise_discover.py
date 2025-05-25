import re
import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import webbrowser

# Configurações da interface
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Limpa pontuação do CNPJ
def limpar_cnpj(cnpj):
    return re.sub(r'\D', '', cnpj)

# Busca telefone e email usando Selenium com melhorias
def scraping_cnpj_biz_selenium(cnpj):
    url = f"https://cnpj.biz/{cnpj}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Espera até que o nome da empresa ou links estejam presentes
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, 'html.parser')
        telefone_tag = soup.find("a", href=lambda h: h and "tel:" in h)
        telefone = telefone_tag['href'].replace("tel:", "") if telefone_tag else ""

        email_tag = soup.find("a", href=lambda h: h and "mailto:" in h)
        email = email_tag['href'].replace("mailto:", "") if email_tag else ""

        nome_fantasia = soup.find("h1")

        return {
            "nome_fantasia": nome_fantasia.text.strip() if nome_fantasia else "N/A",
            "telefone": telefone,
            "email": email,
            "fonte": "cnpj.biz (Selenium)"
        }


    except Exception as e:
        print("Erro ao buscar dados:", e)
        return {
            "nome_fantasia": "Erro ao buscar",
            "telefone": "",
            "email": "",
            "fonte": "Erro"
        }

# Função chamada ao clicar em "Buscar"
def buscar():
    cnpj = limpar_cnpj(entry_cnpj.get())
    if len(cnpj) != 14:
        resultado_nome.configure(text="CNPJ inválido!")
        return

    resultado = scraping_cnpj_biz_selenium(cnpj)
    resultado_nome.configure(text=resultado["nome_fantasia"])
    resultado_fonte.configure(text=f"Fonte: {resultado['fonte']}")

    entry_telefone.configure(state="normal")
    entry_telefone.delete(0, "end")
    entry_telefone.insert(0, resultado["telefone"])
    entry_telefone.configure(state="readonly")

    entry_email.configure(state="normal")
    entry_email.delete(0, "end")
    entry_email.insert(0, resultado["email"])
    entry_email.configure(state="readonly")

# Interface com customtkinter
app = ctk.CTk()
app.title("Consulta CNPJ - by Marcelo Torres")
app.geometry("500x350")
app.resizable(False, False)

ctk.CTkLabel(app, text="Digite o CNPJ (com ou sem pontuação):", font=("Arial", 14)).pack(pady=10)
entry_cnpj = ctk.CTkEntry(app, width=250, font=("Arial", 14))
entry_cnpj.pack(pady=5)

ctk.CTkButton(app, text="Buscar", command=buscar, width=150).pack(pady=10)

resultado_nome = ctk.CTkLabel(app, text="", font=("Arial", 16, "bold"))
resultado_nome.pack(pady=5)

resultado_fonte = ctk.CTkLabel(app, text="", font=("Arial", 12))
resultado_fonte.pack(pady=2)

frame_resultados = ctk.CTkFrame(app)
frame_resultados.pack(pady=15, fill="x", padx=40)

ctk.CTkLabel(frame_resultados, text="Telefone:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_telefone = ctk.CTkEntry(frame_resultados, width=300, font=("Arial", 12), state="readonly")
entry_telefone.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(frame_resultados, text="Email:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_email = ctk.CTkEntry(frame_resultados, width=300, font=("Arial", 12), state="readonly")
entry_email.grid(row=1, column=1, padx=10, pady=5)

def abrir_github():
    webbrowser.open("https://github.com/marcelotorres1982/PythonProject")

link_github = ctk.CTkLabel(app, text="🔗 Projeto no GitHub", text_color="white", cursor="hand2")
link_github.pack(pady=5)
link_github.bind("<Button-1>", lambda e: abrir_github())

app.mainloop()
