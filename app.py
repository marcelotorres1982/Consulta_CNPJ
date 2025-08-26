import streamlit as st
import requests
import re
import json
from typing import Dict, Optional
import time
from dataclasses import dataclass

# Configuração da página
st.set_page_config(
    page_title="Consulta CNPJ",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="collapsed"
)


@dataclass
class EmpresaInfo:
    """Classe para estruturar informações da empresa"""
    nome_fantasia: str = ""
    razao_social: str = ""
    telefone: str = ""
    email: str = ""
    endereco: str = ""
    situacao: str = ""
    cnae_principal: str = ""
    porte: str = ""
    natureza_juridica: str = ""
    capital_social: str = ""
    data_abertura: str = ""
    fonte: str = ""
    sucesso: bool = True


class CNPJService:
    """Serviço para consulta de CNPJ com múltiplas APIs funcionais"""

    @staticmethod
    def limpar_cnpj(cnpj: str) -> str:
        """Remove pontuação do CNPJ"""
        return re.sub(r'\D', '', cnpj)

    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:
        """Validação básica de CNPJ"""
        cnpj_limpo = CNPJService.limpar_cnpj(cnpj)
        return len(cnpj_limpo) == 14 and cnpj_limpo.isdigit()

    @staticmethod
    def formatar_cnpj(cnpj: str) -> str:
        """Formata CNPJ com pontuação"""
        cnpj_limpo = CNPJService.limpar_cnpj(cnpj)
        return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"

    @staticmethod
    def consultar_cnpja_publica(cnpj: str) -> EmpresaInfo:
        """Consulta na API Pública do CNPJá (5 consultas/minuto, sem cadastro)"""
        cnpj_limpo = CNPJService.limpar_cnpj(cnpj)
        url = f"https://open.cnpja.com/office/{cnpj_limpo}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                data = response.json()

                # Montar endereço
                endereco_parts = []
                if data.get('address'):
                    addr = data['address']
                    if addr.get('street'): endereco_parts.append(addr['street'])
                    if addr.get('number'): endereco_parts.append(addr['number'])
                    if addr.get('district'): endereco_parts.append(addr['district'])
                    if addr.get('city'): endereco_parts.append(addr['city'])
                    if addr.get('state'): endereco_parts.append(addr['state'])
                    if addr.get('zip'): endereco_parts.append(f"CEP: {addr['zip']}")

                endereco = ', '.join(endereco_parts)

                # Status da empresa
                situacao = "Ativa" if data.get('status', {}).get('text') == 'ATIVA' else data.get('status', {}).get(
                    'text', '')

                # CNAE principal
                cnae = ""
                if data.get('mainActivity'):
                    cnae = f"{data['mainActivity'].get('code')} - {data['mainActivity'].get('text')}"

                # Porte da empresa
                porte = data.get('size', {}).get('text', '') if data.get('size') else ''

                # Capital social
                capital = ""
                if data.get('registrations') and len(data['registrations']) > 0:
                    capital_valor = data['registrations'][0].get('equity')
                    if capital_valor:
                        capital = f"R$ {capital_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

                # Data de abertura
                data_abertura = data.get('founded', '')

                # Garantir que temos pelo menos um nome
                nome_fantasia = data.get('alias') or data.get('name', '') or "Empresa encontrada"
                razao_social = data.get('name', '') or nome_fantasia

                return EmpresaInfo(
                    nome_fantasia=nome_fantasia,
                    razao_social=razao_social,
                    telefone=', '.join(
                        [p.get('area', '') + p.get('number', '') for p in data.get('phones', [])]) if data.get(
                        'phones') else '',
                    email=', '.join([e.get('address', '') for e in data.get('emails', [])]) if data.get(
                        'emails') else '',
                    endereco=endereco,
                    situacao=situacao,
                    cnae_principal=cnae,
                    porte=porte,
                    capital_social=capital,
                    data_abertura=data_abertura,
                    fonte="CNPJá API Pública"
                )

            elif response.status_code == 429:
                # Rate limit - tenta próxima API
                return CNPJService.consultar_cnpjws(cnpj)
            else:
                return CNPJService.consultar_cnpjws(cnpj)

        except Exception:
            return CNPJService.consultar_cnpjws(cnpj)

    @staticmethod
    def consultar_cnpjws(cnpj: str) -> EmpresaInfo:
        """Consulta na API do CNPJ.ws (3 consultas/minuto)"""
        cnpj_limpo = CNPJService.limpar_cnpj(cnpj)
        url = f"https://publica.cnpj.ws/cnpj/{cnpj_limpo}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                data = response.json()

                # Montar endereço
                endereco_parts = []
                if data.get('logradouro'): endereco_parts.append(data['logradouro'])
                if data.get('numero'): endereco_parts.append(data['numero'])
                if data.get('bairro'): endereco_parts.append(data['bairro'])
                if data.get('municipio'): endereco_parts.append(data['municipio'])
                if data.get('uf'): endereco_parts.append(data['uf'])
                if data.get('cep'): endereco_parts.append(f"CEP: {data['cep']}")

                endereco = ', '.join(endereco_parts)

                return EmpresaInfo(
                    nome_fantasia=data.get('estabelecimento', {}).get('nome_fantasia') or data.get('razao_social', ''),
                    razao_social=data.get('razao_social', ''),
                    telefone=data.get('estabelecimento', {}).get('ddd1', '') + data.get('estabelecimento', {}).get(
                        'telefone1', ''),
                    email=data.get('estabelecimento', {}).get('correio_eletronico', ''),
                    endereco=endereco,
                    situacao=data.get('estabelecimento', {}).get('situacao_cadastral', ''),
                    cnae_principal=data.get('estabelecimento', {}).get('atividade_principal', {}).get('subclasse', ''),
                    porte=data.get('porte', {}).get('descricao', ''),
                    capital_social=str(data.get('capital_social', '')),
                    data_abertura=data.get('estabelecimento', {}).get('data_inicio_atividade', ''),
                    fonte="CNPJ.ws API Pública"
                )
            else:
                return CNPJService.consultar_receitaws(cnpj)

        except Exception:
            return CNPJService.consultar_receitaws(cnpj)

    @staticmethod
    def consultar_receitaws(cnpj: str) -> EmpresaInfo:
        """Consulta na ReceitaWS (fallback)"""
        cnpj_limpo = CNPJService.limpar_cnpj(cnpj)
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_limpo}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get('status') == 'OK':
                    endereco_parts = []
                    if data.get('logradouro'): endereco_parts.append(data['logradouro'])
                    if data.get('numero'): endereco_parts.append(data['numero'])
                    if data.get('bairro'): endereco_parts.append(data['bairro'])
                    if data.get('municipio'): endereco_parts.append(data['municipio'])
                    if data.get('uf'): endereco_parts.append(data['uf'])
                    if data.get('cep'): endereco_parts.append(f"CEP: {data['cep']}")

                    return EmpresaInfo(
                        nome_fantasia=data.get('fantasia') or data.get('nome', ''),
                        razao_social=data.get('nome', ''),
                        telefone=data.get('telefone', ''),
                        email=data.get('email', ''),
                        endereco=', '.join(endereco_parts),
                        situacao=data.get('situacao', ''),
                        data_abertura=data.get('abertura', ''),
                        fonte="ReceitaWS"
                    )
                else:
                    return CNPJService.consultar_brasilapi(cnpj)
            else:
                return CNPJService.consultar_brasilapi(cnpj)

        except Exception:
            return CNPJService.consultar_brasilapi(cnpj)

    @staticmethod
    def consultar_brasilapi(cnpj: str) -> EmpresaInfo:
        """Consulta na BrasilAPI (última tentativa)"""
        cnpj_limpo = CNPJService.limpar_cnpj(cnpj)
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                endereco = f"{data.get('logradouro', '')}, {data.get('numero', '')}, {data.get('bairro', '')}, {data.get('municipio', '')}, {data.get('uf', '')} - CEP: {data.get('cep', '')}"

                return EmpresaInfo(
                    nome_fantasia=data.get('nome_fantasia') or data.get('razao_social', ''),
                    razao_social=data.get('razao_social', ''),
                    telefone=data.get('ddd_telefone_1', ''),
                    email=data.get('email', ''),
                    endereco=endereco.replace(', , ', ', ').strip(', '),
                    situacao=data.get('descricao_situacao_cadastral', ''),
                    cnae_principal=data.get('cnae_fiscal_descricao', ''),
                    porte=data.get('porte', ''),
                    capital_social=str(data.get('capital_social', '')),
                    data_abertura=data.get('data_inicio_atividade', ''),
                    fonte="BrasilAPI"
                )
            else:
                return EmpresaInfo(
                    nome_fantasia="CNPJ não encontrado em nenhuma fonte",
                    fonte="Todas as APIs falharam",
                    sucesso=False
                )

        except Exception:
            return EmpresaInfo(
                nome_fantasia="Erro de conexão com todas as APIs",
                fonte="Erro de rede",
                sucesso=False
            )


def mostrar_resultado_completo(resultado: EmpresaInfo):
    """Exibe resultado completo com todas as informações"""
    if resultado.sucesso:
        st.success("✅ Consulta realizada com sucesso!")

        # Nome da empresa em destaque
        nome_para_exibir = ""

        # Prioridade: nome_fantasia, depois razao_social
        if resultado.nome_fantasia and resultado.nome_fantasia.strip():
            nome_para_exibir = resultado.nome_fantasia.strip()
        elif resultado.razao_social and resultado.razao_social.strip():
            nome_para_exibir = resultado.razao_social.strip()

        if nome_para_exibir:
            st.markdown(f"# 🏢 {nome_para_exibir}")

            # Se nome fantasia é diferente da razão social, mostrar ambos
            if (resultado.nome_fantasia and resultado.razao_social and
                    resultado.nome_fantasia.strip() != resultado.razao_social.strip() and
                    resultado.razao_social.strip()):
                st.markdown(f"**Razão Social:** {resultado.razao_social.strip()}")
        else:
            st.markdown("# 🏢 Empresa Encontrada")

        st.markdown("---")

        with st.container():
            st.markdown("### 📊 Informações Detalhadas")

            # Cards com informações principais
            col1, col2 = st.columns(2)

            with col1:
                if resultado.situacao:
                    cor = "🟢" if "ativa" in resultado.situacao.lower() else "🟡"
                    st.metric(f"{cor} Situação", resultado.situacao)
                if resultado.porte:
                    st.metric("📊 Porte", resultado.porte)
                if resultado.capital_social:
                    st.metric("💰 Capital Social", resultado.capital_social)

            with col2:
                if resultado.data_abertura:
                    st.metric("📅 Data de Abertura", resultado.data_abertura)
                if resultado.cnae_principal:
                    st.metric("🏭 Atividade Principal", resultado.cnae_principal[:50] + "..." if len(
                        resultado.cnae_principal) > 50 else resultado.cnae_principal)

            # Informações de contato
            if resultado.telefone or resultado.email:
                st.markdown("### 📞 Contatos")
                col1, col2 = st.columns(2)

                with col1:
                    if resultado.telefone:
                        st.info(f"📞 **Telefone:** {resultado.telefone}")
                    else:
                        st.warning("📞 **Telefone:** Não informado")

                with col2:
                    if resultado.email:
                        st.info(f"📧 **Email:** {resultado.email}")
                    else:
                        st.warning("📧 **Email:** Não informado")

            # Endereço
            if resultado.endereco:
                st.markdown("### 📍 Endereço")
                st.info(resultado.endereco)

            # Atividade completa (se for muito grande)
            if resultado.cnae_principal and len(resultado.cnae_principal) > 50:
                st.markdown("### 🏭 Atividade Principal Completa")
                st.info(resultado.cnae_principal)

            # Fonte dos dados
            st.caption(f"*Fonte: {resultado.fonte}*")

    else:
        st.error(f"❌ {resultado.nome_fantasia}")
        st.info("""
        💡 **Possíveis soluções:**
        - Verifique se o CNPJ está correto
        - Aguarde alguns segundos e tente novamente
        - O CNPJ pode estar inativo ou não ter dados públicos disponíveis
        """)


def main():
    """Função principal da aplicação"""

    # Inicializar estado da sessão
    if 'cnpj_input' not in st.session_state:
        st.session_state.cnpj_input = ""
    if 'resultado_busca' not in st.session_state:
        st.session_state.resultado_busca = None

    # Header
    st.title("🏢 Consulta CNPJ Completa")
    st.markdown("**Consulte informações detalhadas de empresas brasileiras**")
    st.markdown("*Múltiplas APIs oficiais e públicas*")
    st.markdown("---")

    # Sidebar com informações
    with st.sidebar:
        st.markdown("### 🎯 APIs Consultadas")
        st.markdown("""
        **Ordem de consulta:**
        1. 🚀 **CNPJá API** - Dados da Receita Federal
        2. 🔍 **CNPJ.ws** - Base pública atualizada  
        3. 🏛️ **ReceitaWS** - Receita Federal
        4. 🇧🇷 **BrasilAPI** - API oficial do governo

        **📋 Dados disponíveis:**
        - ✅ Razão social e nome fantasia
        - 🏢 Situação cadastral e porte
        - 📍 Endereço completo
        - 📞 Telefone e email
        - 🏭 CNAE principal
        - 💰 Capital social
        - 📅 Data de abertura
        """)

        st.markdown("---")
        st.markdown("### ⚡ Limites das APIs")
        st.info("""
        - **CNPJá:** 5 consultas/min
        - **CNPJ.ws:** 3 consultas/min  
        - **ReceitaWS:** 60 consultas/min
        - **BrasilAPI:** Sem limite
        """)

        st.markdown("---")
        st.markdown("### 🔗 Links")
        st.markdown("""
        - [🐙 Código Fonte](https://github.com/marcelotorres1982/PythonProject)
        - [🏛️ Receita Federal](https://www.gov.br/receitafederal)
        """)

        st.markdown("---")
        st.markdown("**Desenvolvido por:** Marcelo Torres")

    # Exemplos de CNPJ para teste
    with st.expander("📝 CNPJs para teste (empresas reais)"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **🛒 Grandes Varejistas:**
            - **Magazine Luiza:** 47.960.950/0001-21
            - **Via (ex-Casas Bahia):** 59.438.907/0001-01
            - **Americanas:** 00.776.574/0001-56
            """)

        with col2:
            st.markdown("""
            **🏭 Grandes Empresas:**
            - **Petrobras:** 33.000.167/0001-01
            - **Vale:** 33.592.510/0001-54
            - **JBS:** 02.916.265/0001-60
            """)

        st.info("💡 **Dica:** Cole qualquer CNPJ acima para testar a aplicação!")

    # Input do CNPJ
    st.markdown("### 🔍 Consultar CNPJ")

    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        cnpj_input = st.text_input(
            "Digite o CNPJ:",
            value=st.session_state.cnpj_input,
            placeholder="00.000.000/0000-00",
            help="Digite o CNPJ com ou sem pontuação",
            key="input_cnpj"
        )
        # Atualizar session_state quando o input muda
        st.session_state.cnpj_input = cnpj_input

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        buscar_clicked = st.button("🔍 Buscar", type="primary", use_container_width=True)

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        limpar_clicked = st.button("🧹 Limpar", use_container_width=True)

    # Funcionalidade do botão limpar
    if limpar_clicked:
        st.session_state.cnpj_input = ""
        st.session_state.resultado_busca = None
        st.rerun()

    # Processamento da busca
    if buscar_clicked and cnpj_input:
        if not CNPJService.validar_cnpj(cnpj_input):
            st.error("❌ CNPJ inválido! Certifique-se de que possui 14 dígitos.")
            return

        # Mostrar CNPJ formatado
        cnpj_formatado = CNPJService.formatar_cnpj(cnpj_input)
        st.info(f"🔍 Consultando CNPJ: **{cnpj_formatado}**")

        # Progress bar com etapas
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("🚀 Consultando CNPJá API...")
            progress_bar.progress(25)
            time.sleep(0.8)

            status_text.text("🔍 Tentando CNPJ.ws...")
            progress_bar.progress(50)
            time.sleep(0.5)

            status_text.text("🏛️ Consultando ReceitaWS...")
            progress_bar.progress(75)
            time.sleep(0.5)

            status_text.text("✅ Finalizando consulta...")
            progress_bar.progress(100)
            time.sleep(0.3)

        # Realizar consulta
        resultado = CNPJService.consultar_cnpja_publica(cnpj_input)
        st.session_state.resultado_busca = resultado

        # Limpar elementos de loading
        progress_container.empty()

    # Exibir resultado se existir
    if st.session_state.resultado_busca:
        mostrar_resultado_completo(st.session_state.resultado_busca)


if __name__ == "__main__":
    main()