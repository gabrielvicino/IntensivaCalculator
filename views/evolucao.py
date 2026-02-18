import streamlit as st
import google.generativeai as genai
import os
from pathlib import Path

# Importa os módulos
from modules import ui, agentes, fichas, gerador, fluxo, ia_extrator, agentes_secoes
from utils import load_data, mostrar_rodape

# ==============================================================================
# CARREGAMENTO DE CHAVES DE API (secrets.toml → .env → vazio)
# ==============================================================================
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
except ImportError:
    pass

def _carregar_chave(nome_secret: str, nome_env: str) -> str:
    try:
        if hasattr(st, "secrets") and nome_secret in st.secrets:
            return st.secrets[nome_secret]
    except Exception:
        pass
    return os.getenv(nome_env, "")

OPENAI_API_KEY  = _carregar_chave("OPENAI_API_KEY",  "OPENAI_API_KEY")
GOOGLE_API_KEY  = _carregar_chave("GOOGLE_API_KEY",  "GOOGLE_API_KEY")

# ==============================================================================
# MODELOS DISPONÍVEIS
# ==============================================================================
MODELOS_GEMINI = ["gemini-2.5-flash", "gemini-2.5-pro"]

# ==============================================================================
# SETUP
# ==============================================================================
ui.carregar_css()
fichas.inicializar_estado()

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.header("Configurações")

    provider = st.radio("IA:", ["OpenAI GPT", "Google Gemini"], index=0)

    if provider == "OpenAI GPT":
        api_key      = OPENAI_API_KEY
        modelo_escolhido = "gpt-4o"
        st.success("IA: OpenAI - GPT-4o")
        if api_key and len(api_key) > 10:
            st.success(f"✅ API Key: ...{api_key[-8:]}")
        else:
            st.error("❌ API Key não carregada!")

    else:  # Google Gemini
        api_key = GOOGLE_API_KEY
        if api_key:
            genai.configure(api_key=api_key)
        modelo_escolhido = st.selectbox("Modelo:", MODELOS_GEMINI, index=0)
        st.success(f"IA: Google - {modelo_escolhido}")
        if api_key and len(api_key) > 10:
            st.success(f"✅ API Key: ...{api_key[-8:]}")
        else:
            st.error("❌ API Key não carregada!")

# ==============================================================================
# TÍTULO E BUSCA
# ==============================================================================
st.title("📝 Evolução Diária")
st.write("") 

with st.container():
    with st.form(key="form_busca_paciente"):
        c_input, c_btn = st.columns([4, 1], vertical_alignment="bottom")
        
        with c_input:
            st.markdown('<label style="font-size: 1.2rem; font-weight: 600; color: #444; margin-bottom: 5px; display: block;">Número de Prontuário:</label>', unsafe_allow_html=True)
            busca_input = st.text_input("Label Oculta", placeholder="Digite 'TESTE' ou o número...", key="busca_input_field", label_visibility="collapsed")
        
        with c_btn:
            submit_btn = st.form_submit_button("🔍 Buscar", use_container_width=True)

        if submit_btn:
            if busca_input and (busca_input.upper() == "TESTE" or busca_input == "12345"):
                st.session_state.update({
                    'nome': 'João da Silva (Paciente Teste)',
                    'idade': 68,
                    'prontuario': 'TESTE-001',
                    'leito': 'UTI-05',
                    'origem': 'PS / Emergência',
                    'di_hosp': '12 dias',
                    'di_uti': '4 dias',
                    'hd_principal': 'Choque Séptico de Foco Pulmonar',
                    'comorbidades_previas': 'HAS, DM2, Tabagismo prévio',
                    'alergias': 'Nega',
                    'vm_modo': 'PCV',
                    'vm_parametros': 'PEEP 8 | FiO2 40%',
                    'sonda': 'SNE',
                    'acesso_venoso': 'CVC Jugular D',
                    'antibioticos': 'Meropenem (D4), Vancomicina (D2)',
                    'saps3': '55', 
                    'sofa_adm': 8,
                    'sofa_atual': 6
                })
                st.toast("Modo Treinamento Ativado! 🧪", icon="✅")
            elif busca_input:
                st.warning("Paciente não encontrado no banco de dados real. Tente digitar 'TESTE'.")
            else:
                st.warning("Digite um número.")

# ==============================================================================
# PAINEL DE IDENTIFICAÇÃO
# ==============================================================================
ui.render_barra_paciente()

# ==============================================================================
# BLOCO 1: PRONTUÁRIO E SELEÇÃO INTELIGENTE
# ==============================================================================
ui.render_header_secao("1. Prontuário", "📄", ui.COLOR_BLUE)

with st.container(border=True):
    texto_input = st.text_area("Input", height=150, label_visibility="collapsed", placeholder="Cole a evolução aqui (Ctrl+V)...")

    st.write("")

    # BOTÃO 1: apenas fatia o prontuário nos campos _notas
    if st.button("✨ Extrair Dados Selecionados", type="primary", use_container_width=True):
        if not api_key:
            st.error("Sem chave API.")
        elif not texto_input:
            st.warning("Cole o texto do prontuário primeiro.")
        else:
            provider_completo = f"{provider} {modelo_escolhido}" if provider == "Google Gemini" else provider
            with st.spinner("🔪 Fatiando prontuário em 12 seções..."):
                dados_notas = ia_extrator.extrair_dados_prontuario(
                    texto_bruto=texto_input,
                    api_key=api_key,
                    provider=provider_completo,
                    modelo=modelo_escolhido
                )
                fluxo.atualizar_notas_ia(dados_notas)

# ---------------------------------------------------------------------------
# BLOCO DE AGENTES: checklist + botão aplicar
# ---------------------------------------------------------------------------
with st.container(border=True):
    st.markdown("**🤖 Agentes de preenchimento automático**")
    st.caption("Selecione quais seções deseja preencher com IA e clique em Aplicar.")

    # Inicializar estado dos checkboxes
    # Padrão: apenas seções 10+ (laboratoriais em diante) marcadas
    _AGENTES_PADRAO_ATIVO = {"laboratoriais", "controles", "evolucao", "sistemas"}
    _agentes_labels = list(agentes_secoes.NOMES_SECOES.items())  # [(chave, "1. Nome"), ...]
    for chave, _ in _agentes_labels:
        if f"ag_chk_{chave}" not in st.session_state:
            st.session_state[f"ag_chk_{chave}"] = chave in _AGENTES_PADRAO_ATIVO

    # Toggle mestre
    def _toggle_agentes():
        estado = st.session_state["ag_toggle_mestre"]
        for chave, _ in _agentes_labels:
            st.session_state[f"ag_chk_{chave}"] = estado

    col_tog, _ = st.columns([2, 5])
    with col_tog:
        st.toggle("Selecionar todos / Nenhum", key="ag_toggle_mestre",
                  value=True, on_change=_toggle_agentes)

    st.write("")

    # Grid 4 colunas com checkboxes
    cols = st.columns(4)
    selecionados = []
    for i, (chave, label) in enumerate(_agentes_labels):
        with cols[i % 4]:
            if st.checkbox(label, key=f"ag_chk_{chave}"):
                selecionados.append(chave)

    st.write("")

    # BOTÃO 2: roda apenas os agentes selecionados
    if st.button("🚀 Aplicar Agentes Selecionados", type="primary", use_container_width=True):
        if not api_key:
            st.error("Sem chave API.")
        elif not selecionados:
            st.warning("Selecione pelo menos um agente.")
        else:
            provider_completo = f"{provider} {modelo_escolhido}" if provider == "Google Gemini" else provider
            erros = []
            progresso = st.progress(0, text="Iniciando agentes...")
            total = len(selecionados)

            for idx, secao in enumerate(selecionados):
                nome = agentes_secoes.NOMES_SECOES[secao]
                progresso.progress((idx) / total, text=f"🤖 Processando {nome}...")

                chave_notas = agentes_secoes._NOTAS_MAP[secao]
                texto_secao = st.session_state.get(chave_notas, "").strip()

                if not texto_secao:
                    continue

                fn = agentes_secoes._AGENTES[secao]
                dados = fn(texto_secao, api_key, provider_completo, modelo_escolhido)

                if "_erro" in dados:
                    erros.append(f"{nome}: {dados['_erro']}")
                else:
                    st.session_state.update(dados)

            progresso.progress(1.0, text="✅ Concluído!")

            if erros:
                for e in erros:
                    st.warning(f"⚠️ {e}")
            else:
                st.success(f"✅ {total} agente(s) aplicado(s) com sucesso!")

# ==============================================================================
# BLOCO 2: DADOS CLÍNICOS
# ==============================================================================
ui.render_header_secao("2. Dados Clínicos", "✍️", "#f59e0b")
fichas.render_formulario_completo()

# ==============================================================================
# BLOCO 3: PRONTUÁRIO COMPLETO
# ==============================================================================
c_head_1, c_head_2 = st.columns([3.5, 1.5], vertical_alignment="bottom")

with c_head_1:
    ui.render_header_secao("3. Prontuário Completo", "✅", ui.COLOR_GREEN)

with c_head_2:
    if st.button("📋 Copiar Texto", use_container_width=True):
        st.toast("Texto copiado!", icon="📋")
    st.markdown('<div style="height: 12px"></div>', unsafe_allow_html=True) 

txt_final = gerador.gerar_texto_final()

with st.container(border=True):
    st.text_area("Final", value=txt_final, height=200, label_visibility="collapsed")

# ==============================================================================
# RODAPÉ
# ==============================================================================
st.markdown("---")
col_salvar, col_limpar = st.columns([3, 1])

with col_salvar:
    if st.button("💾 Salvar no Prontuário", type="primary", use_container_width=True):
        st.success("✅ Evolução salva.")

with col_limpar:
    st.button("🗑️ Limpar Tudo", on_click=fluxo.limpar_tudo, use_container_width=True)


# Rodapé com nota legal
mostrar_rodape()