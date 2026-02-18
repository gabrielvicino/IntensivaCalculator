import streamlit as st
import google.generativeai as genai
import os
from pathlib import Path

# Importa os módulos
from modules import ui, agentes, fichas, gerador, fluxo, ia_extrator
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
MODELOS_OPENAI = ["gpt-4o", "gpt-4o-mini"]
MODELOS_GEMINI = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-thinking",
    "gemini-2.0-flash",
    "gemini-1.5-pro-002",
    "gemini-1.5-flash-002",
]

def verificar_modelos_ativos(api_key):
    """Testa quais modelos Gemini estão ativos para a chave fornecida."""
    validos = []
    genai.configure(api_key=api_key)
    msg = st.empty()
    for m in MODELOS_GEMINI:
        msg.text(f"Testando: {m}...")
        try:
            genai.GenerativeModel(m).generate_content("Oi")
            validos.append(m)
        except Exception:
            pass
    msg.empty()
    return validos or MODELOS_GEMINI

# ==============================================================================
# SETUP
# ==============================================================================
ui.carregar_css()
fichas.inicializar_estado()

if "evolucao_lista_gemini" not in st.session_state:
    st.session_state.evolucao_lista_gemini = MODELOS_GEMINI

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Configuração de IA")

    provider = st.radio("Provedor:", ["OpenAI GPT", "Google Gemini"], index=0)

    if provider == "OpenAI GPT":
        modelo_escolhido = st.selectbox("Modelo:", MODELOS_OPENAI, index=0)

        # Chave carregada automaticamente; permite sobrescrever se necessário
        chave_input = st.text_input(
            "OpenAI API Key",
            value=OPENAI_API_KEY,
            type="password",
            help="Pré-carregada do arquivo de configuração. Altere aqui se necessário."
        )
        api_key = chave_input or OPENAI_API_KEY

        if api_key and len(api_key) > 10:
            st.success(f"✅ OpenAI: ...{api_key[-6:]}")
        else:
            st.error("❌ API Key OpenAI não carregada")

    else:  # Google Gemini
        # Chave carregada automaticamente
        chave_input = st.text_input(
            "Google API Key",
            value=GOOGLE_API_KEY,
            type="password",
            help="Pré-carregada do arquivo de configuração. Altere aqui se necessário."
        )
        api_key = chave_input or GOOGLE_API_KEY

        if api_key:
            genai.configure(api_key=api_key)

        if st.button("🔄 Verificar Modelos"):
            if api_key:
                st.session_state.evolucao_lista_gemini = verificar_modelos_ativos(api_key)
                st.success(f"✅ {len(st.session_state.evolucao_lista_gemini)} modelos ativos")
            else:
                st.warning("Configure a API Key primeiro")

        modelo_escolhido = st.selectbox("Modelo:", st.session_state.evolucao_lista_gemini, index=0)

        if api_key and len(api_key) > 10:
            st.success(f"✅ Google: ...{api_key[-6:]}")
        else:
            st.error("❌ API Key Google não carregada")

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
    # 1. Área de Texto
    texto_input = st.text_area("Input", height=150, label_visibility="collapsed", placeholder="Cole a evolução aqui (Ctrl+V)...")
    
    st.markdown("---")
    
    # --- RÓTULO ELEGANTE ---
    st.markdown("""
    <div style="font-size: 1.1rem; font-weight: 600; color: #444; margin-bottom: 10px;">
        🤖 Selecione os itens para extração:
    </div>
    """, unsafe_allow_html=True)
    
    # --- DEFINIÇÃO DOS AGENTES ---
    agentes_map = {
        "1. Identificação": "identidade",
        "2. HD e Motivo": "hd",
        "3. Comorbidades": "comorbidades",
        "4. MUC / Alergias": "muc",
        "5. HMPA / Neuro": "hmpa",
        "6. Dispositivos": "dispositivos",
        "7. Culturas": "culturas",
        "8. Antibióticos": "antibioticos",
        "9. Complementares": "complementares",
        "10. Laboratoriais": "laboratoriais",
        "11. Evolução Clínica": "evolucao_clinica",
        "12. Sistemas": "sistemas"
    }
    
    chaves_agentes = list(agentes_map.values())

    # --- LÓGICA DE PRÉ-SELEÇÃO (Defaults: 6 ao 12) ---
    defaults_ativos = [
        "dispositivos", "culturas", "antibioticos", "complementares", 
        "laboratoriais", "evolucao_clinica", "sistemas"
    ]

    for chave in chaves_agentes:
        key_widget = f"chk_{chave}"
        if key_widget not in st.session_state:
            st.session_state[key_widget] = (chave in defaults_ativos)

    # --- CALLBACK PARA O BOTÃO MESTRE ---
    def alternar_todos():
        estado_novo = st.session_state.toggle_mestre
        for chave in chaves_agentes:
            st.session_state[f"chk_{chave}"] = estado_novo

    # --- RENDERIZAÇÃO VISUAL ---
    col_mestre, col_info = st.columns([2, 5], vertical_alignment="center")
    with col_mestre:
        st.toggle(
            "Selecionar Todos / Nenhum", 
            key="toggle_mestre", 
            on_change=alternar_todos,
            value=False 
        )
    
    st.markdown("") # Espaço

    # Grid de Checkboxes
    cols = st.columns(4)
    selecionados_para_ia = []

    for i, (label, chave) in enumerate(agentes_map.items()):
        col = cols[i % 4]
        is_checked = col.checkbox(label, key=f"chk_{chave}")
        
        if is_checked:
            selecionados_para_ia.append(chave)

    st.write("") # Espaço

    # 3. BOTÕES DE AÇÃO
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("✨ Extrair Dados Selecionados", type="primary", use_container_width=True):
            if not api_key:
                st.error("Sem chave API.")
            elif not texto_input:
                st.warning("Cole o texto do prontuário primeiro.")
            elif not selecionados_para_ia:
                st.warning("Selecione pelo menos um item para extrair.")
            else:
                with st.spinner(f"Processando com {len(selecionados_para_ia)} agentes de IA..."):
                    provider_completo = f"{provider} {modelo_escolhido}" if provider == "Google Gemini" else provider
                    dados = agentes.agente_admissao(texto_input, provider_completo, api_key, escopos=selecionados_para_ia)
                    fluxo.atualizar_dados_ia(dados)
                    st.success("Dados extraídos com sucesso!")

    with col_btn2:
        if st.button("🧬 Preencher Seções 1–12 com IA", type="secondary", use_container_width=True):
            if not api_key:
                st.error("Sem chave API.")
            elif not texto_input:
                st.warning("Cole o texto do prontuário primeiro.")
            else:
                provider_completo = f"{provider} {modelo_escolhido}" if provider == "Google Gemini" else provider
                with st.spinner("Fatiando prontuário em 12 seções..."):
                    dados = ia_extrator.extrair_dados_prontuario(
                        texto_bruto=texto_input,
                        api_key=api_key,
                        provider=provider_completo,
                        modelo=modelo_escolhido
                    )
                    fluxo.atualizar_notas_ia(dados)

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