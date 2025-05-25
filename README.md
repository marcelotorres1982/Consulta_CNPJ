🔍 Consulta de CNPJ

Este projeto permite consultar informações públicas de empresas brasileiras (CNPJ), extraindo telefone e email diretamente do site https://cnpj.biz, 
utilizando web scraping com Selenium, e exibe os dados em uma interface moderna com CustomTkinter.

🚀 Funcionalidades
Consulta de CNPJ com ou sem pontuação (ex: 00.000.000/0000-00 ou 00000000000000)

Extração automática de:

Nome Fantasia

Telefone (via href="tel:")

Email (via href="mailto:")

Interface gráfica moderna com campos de cópia fácil de telefone e email

Processamento automático com Selenium Headless (sem abrir o navegador)

🛠 Tecnologias Utilizadas
Ferramenta	Função
Python	Linguagem principal
CustomTkinter	Interface gráfica moderna baseada no Tkinter
Selenium	Automação e scraping do conteúdo da web
BeautifulSoup	Extração e parsing de HTML
re (Regex)	Limpeza de caracteres do CNPJ
ChromeDriver	Navegador automatizado (requer instalação separada)

📦 Requisitos
Python 3.8+

Google Chrome instalado

ChromeDriver compatível com sua versão do Chrome

Instale as dependências com:

bash
Copiar
Editar
pip install customtkinter selenium beautifulsoup4
⚙️ Execução
Clone este repositório:

bash
Copiar
Editar
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
Execute o script:

bash
Copiar
Editar
python nome_do_arquivo.py
Digite um CNPJ válido na interface e clique em Buscar.

📌 Observações
A fonte de dados utilizada (cnpj.biz) é pública, mas o site não fornece API oficial. O scraping respeita limites razoáveis (até ~30 consultas diárias).

Este projeto é para fins educacionais e uso pessoal.

📷 Exemplo

![image](https://github.com/user-attachments/assets/c2f874c7-4a86-4a14-8aa4-8be6e791acfe)


🧑‍💻 Desenvolvido por Marcelo Torres
