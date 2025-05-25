import requests
from pprint import pprint

# Define o CNPJ
cnpj = "09811654000170"
url = f"https://publica.cnpj.ws/cnpj/{cnpj}"

# Faz a requisição GET
response = requests.get(url)

# Verifica se a requisição deu certo (código 200)
if response.status_code == 200:
    data = response.json()
    estabelecimento = data.get("estabelecimento", {})

    # Usa valores padrão caso algum campo seja None
    ddd = estabelecimento.get("ddd") or ""
    telefone_numero = estabelecimento.get("telefone") or ""
    telefone = f"{ddd}{telefone_numero}"

    email = estabelecimento.get("email") or "Não informado"

    print("Telefone:", telefone if telefone else "Não informado")
    print("Email:", email)
else:
    print(f"Erro: {response.status_code}")
