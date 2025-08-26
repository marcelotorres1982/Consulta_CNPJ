# 🏢 Consulta CNPJ Completa - Streamlit

Uma aplicação web moderna e robusta para consulta completa de informações empresariais através do CNPJ, utilizando múltiplas APIs oficiais brasileiras.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen?style=for-the-badge)

## 🚀 Características Principais

- ✅ **Múltiplas APIs**: Sistema inteligente com 4 fontes de dados diferentes
- 🔍 **Busca Robusta**: Fallback automático entre APIs
- 📊 **Dados Completos**: Informações detalhadas da Receita Federal
- 🎨 **Interface Moderna**: Design responsivo com Streamlit
- ⚡ **Performance**: Consultas rápidas e eficientes
- 🧹 **UX Aprimorada**: Botão limpar e nome destacado
- 📱 **Mobile Friendly**: Funciona perfeitamente em dispositivos móveis

## 🎯 APIs Consultadas (em ordem de prioridade)

1. **🚀 CNPJá API Pública** - Dados atualizados da Receita Federal (5 consultas/min)
2. **🔍 CNPJ.ws API** - Base pública especializada (3 consultas/min) 
3. **🏛️ ReceitaWS** - API consolidada da Receita Federal (60 consultas/min)
4. **🇧🇷 BrasilAPI** - API oficial do governo brasileiro (sem limite)

## 📋 Informações Disponíveis

### 📊 Dados Básicos
- 🏢 **Razão Social** e Nome Fantasia
- 🟢 **Situação Cadastral** (Ativa/Inativa)
- 📊 **Porte da Empresa** (MEI, Pequena, Média, Grande)
- 📅 **Data de Abertura**
- 💰 **Capital Social**

### 📞 Contatos
- 📞 **Telefones** (quando disponível publicamente)
- 📧 **Emails** (quando disponível publicamente)

### 📍 Localização
- 🏠 **Endereço Completo** (Logradouro, número, bairro, cidade, UF, CEP)

### 🏭 Atividades
- 📋 **CNAE Principal** (Código e descrição da atividade)

## 🖥️ Demo

### Interface Principal
```
🏢 Consulta CNPJ Completa
Consulte informações detalhadas de empresas brasileiras
Múltiplas APIs oficiais e públicas

🔍 Consultar CNPJ
[Campo de entrada] [🔍 Buscar] [🧹 Limpar]
```

### Resultado da Consulta
```
✅ Consulta realizada com sucesso!

# 🏢 MAGAZINE LUIZA S.A.
Razão Social: MAGAZINE LUIZA S.A.

📊 Informações Detalhadas
🟢 Situação: ATIVA
📊 Porte: SOCIEDADE EMPRESÁRIA DE GRANDE PORTE
📅 Data de Abertura: 16/11/1992
💰 Capital Social: R$ 878.956.000,17

📞 Contatos
📞 Telefone: (11) 4003-6000
📧 Email: Não informado

📍 Endereço
AV PRESIDENTE JUSCELINO KUBITSCHEK DE OLIVEIRA, 1455, 
VILA NOVA, FRANCA, SP - CEP: 14401-135
```

## 🏃‍♂️ Como Executar Localmente

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/marcelotorres1982/cnpj-consulta-streamlit.git
   cd cnpj-consulta-streamlit
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

4. **Acesse no navegador:**
   ```
   http://localhost:8501
   ```

## 🌐 Deploy no Streamlit Cloud

### Opção 1: Deploy Automático (Recomendado)

1. **Fork este repositório** para sua conta GitHub
2. **Acesse** [share.streamlit.io](https://share.streamlit.io)
3. **Faça login** com sua conta GitHub
4. **Clique em "New app"**
5. **Selecione:**
   - Repository: `seu-usuario/cnpj-consulta-streamlit`
   - Branch: `main`
   - Main file path: `app.py`
6. **Clique em "Deploy!"**
7. **Aguarde** alguns minutos - sua aplicação estará online!

### Opção 2: Deploy Manual

```bash
# 1. Prepare os arquivos
git add .
git commit -m "Deploy inicial"
git push origin main

# 2. Configure no Streamlit Cloud seguindo os passos acima
```

## 📁 Estrutura do Projeto

```
cnpj-consulta-streamlit/
├── app.py              # 🐍 Aplicação principal Streamlit
├── requirements.txt    # 📦 Dependências Python
├── README.md          # 📚 Documentação
└── .gitignore         # 🚫 Arquivos ignorados pelo Git
```

## 🧪 CNPJs para Teste

### 🛒 Grandes Varejistas
- **Magazine Luiza:** `47.960.950/0001-21`
- **Via (ex-Casas Bahia):** `59.438.907/0001-01`
- **Americanas:** `00.776.574/0001-56`

### 🏭 Grandes Empresas
- **Petrobras:** `33.000.167/0001-01`
- **Vale:** `33.592.510/0001-54`
- **JBS:** `02.916.265/0001-60`

### 🏦 Bancos
- **Banco do Brasil:** `00.000.000/0001-91`
- **Itaú:** `60.701.190/0001-04`
- **Bradesco:** `60.746.948/0001-12`

## ⚡ Melhorias vs Versão Original

| Aspecto | Versão Original (CustomTkinter) | Nova Versão (Streamlit) |
|---------|--------------------------------|--------------------------|
| **Plataforma** | 🖥️ Desktop apenas | 🌐 Web + Mobile |
| **APIs** | 1 fonte (cnpj.biz) | 4 fontes oficiais |
| **Scraping** | Selenium (pesado) | APIs REST (leve) |
| **Deploy** | ❌ Difícil | ✅ Automático |
| **Dados** | Básicos | Completos da RF |
| **UX** | Simples | Moderna + Progress bar |
| **Manutenção** | Complexa | Simples |
| **Performance** | Lenta | Rápida |
| **Recursos** | Alto consumo | Baixo consumo |

## 🔧 Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** - Framework para apps web em Python
- **[Requests](https://requests.readthedocs.io/)** - Biblioteca HTTP para Python
- **[Python 3.8+](https://python.org/)** - Linguagem de programação

## 📊 Limites das APIs

| API | Limite | Observações |
|-----|--------|-------------|
| CNPJá | 5/min | Dados mais completos |
| CNPJ.ws | 3/min | Boa cobertura |
| ReceitaWS | 60/min | Mais permissiva |
| BrasilAPI | Ilimitado | Oficial do governo |

## ⚠️ Limitações e Considerações

### 📋 Dados Disponíveis
- **Telefone/Email**: Nem sempre disponíveis (dependem da empresa tornar público)
- **Atualizações**: Dados podem ter defasagem em relação à fonte original
- **CNPJs Inativos**: Podem não retornar informações completas

### 🔐 Uso Responsável
- **Rate Limiting**: Respeite os limites das APIs
- **Dados Públicos**: Use apenas para fins legítimos
- **Legislação**: Observe as leis de proteção de dados (LGPD)

### 🚀 Para Uso Comercial
- **High Volume**: Considere APIs pagas especializadas
- **SLA Garantido**: APIs gratuitas não oferecem garantias
- **Dados Sensíveis**: Consulte advogado especializado

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. **Fork** o projeto
2. **Crie** sua feature branch (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. **Abra** um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🔗 Links Úteis

- **🚀 [Demo Online](https://cnpj-consulta.streamlit.app)** *(substitua pela URL real)*
- **🐙 [Repositório GitHub](https://github.com/marcelotorres1982/PythonProject)**
- **📚 [Documentação Streamlit](https://docs.streamlit.io)**
- **🏛️ [Receita Federal](https://www.gov.br/receitafederal)**
- **🇧🇷 [BrasilAPI](https://brasilapi.com.br)**

## 👨‍💻 Autor

**Marcelo Torres**
- GitHub: [@marcelotorres1982](https://github.com/marcelotorres1982)
- LinkedIn: [Conecte-se comigo]([https://linkedin.com/in/marcelotorres1982](https://www.linkedin.com/in/marcelo-t-554b8045/)) *(ajuste conforme necessário)*

---

## 📈 Changelog

### v2.0.0 - Versão Streamlit (Atual)
- ✅ Migração completa para Streamlit
- ✅ 4 APIs integradas com fallback automático
- ✅ Interface moderna e responsiva
- ✅ Botão limpar funcional
- ✅ Nome da empresa destacado
- ✅ Deploy automático no cloud

### v1.0.0 - Versão Original
- ✅ Interface desktop com CustomTkinter
- ✅ Integração básica com cnpj.biz
- ✅ Funcionalidade core de consulta

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no repositório!**

🔄 **Encontrou algum problema ou tem sugestões? Abra uma [issue](https://github.com/marcelotorres1982/PythonProject/issues)!**
