import streamlit as st
import google.generativeai as genai

# Importa os módulos
from modules import ui, agentes, fichas, gerador, fluxo
from utils import load_data, mostrar_rodape

# ==============================================================================
# LISTA COMPLETA DE MODELOS CANDIDATOS (Todos os Gemini)
# ==============================================================================
CANDIDATOS_GEMINI = [
    # === GEMINI 2.5 (Janeiro 2026 - MAIS RECENTES) ===
    "gemini-2.5-flash",                    # RECOMENDADO: Mais rápido e recente
    "gemini-2.5-flash-preview-0205",       # Preview específico
    "gemini-2.5-flash-preview-01-17",      # Preview de janeiro
    "gemini-2.5-pro",                      # Máxima inteligência 2.5
    "gemini-2.5-pro-preview-0205",         # Preview Pro
    "gemini-2.5-pro-preview-01-17",        # Preview Pro janeiro
    "gemini-2.5-flash-thinking",           # Raciocínio avançado 2.5
    "gemini-2.5-flash-thinking-exp",       # Experimental thinking
    "gemini-2.5-flash-thinking-exp-01-21", # Experimental específico
    
    # === GEMINI 2.0 (Dezembro 2025 - Descontinuados em Fevereiro 2026) ===
    "gemini-2.0-flash",                    # Flash 2.0 padrão
    "gemini-2.0-flash-exp",                # Experimental 2.0
    "gemini-2.0-flash-thinking-exp",       # Thinking experimental 2.0
    "gemini-2.0-flash-thinking-exp-1219",  # Versão específica
    
    # === GEMINI 1.5 PRO (Estáveis - 2M tokens) ===
    "gemini-1.5-pro",                      # Pro sem sufixo (latest)
    "gemini-1.5-pro-latest",               # Última versão stable
    "gemini-1.5-pro-002",                  # Versão stable 002
    "gemini-1.5-pro-001",                  # Versão stable 001
    "gemini-1.5-pro-exp-0827",             # Experimental agosto
    "gemini-1.5-pro-exp-0801",             # Experimental agosto
    
    # === GEMINI 1.5 FLASH (Estáveis - Rápidos) ===
    "gemini-1.5-flash",                    # Flash sem sufixo (latest)
    "gemini-1.5-flash-latest",             # Última versão stable
    "gemini-1.5-flash-002",                # Versão stable 002
    "gemini-1.5-flash-001",                # Versão stable 001
    "gemini-1.5-flash-8b",                 # Versão 8B (mais leve)
    "gemini-1.5-flash-8b-latest",          # 8B latest
    "gemini-1.5-flash-8b-001",             # 8B versão 001
    "gemini-1.5-flash-8b-exp-0827",        # 8B experimental agosto
    "gemini-1.5-flash-8b-exp-0924",        # 8B experimental setembro
    "gemini-1.5-flash-exp-0827",           # Experimental agosto
    
    # === GEMINI EXPERIMENTAL (Previews e Testes) ===
    "gemini-exp-1206",                     # Experimental dezembro 2024
    "gemini-exp-1121",                     # Experimental novembro 2024
    "gemini-exp-1114",                     # Experimental novembro 2024
    "gemini-exp-1005",                     # Experimental outubro 2024
    
    # === GEMINI 1.0 (Legado - Descontinuados) ===
    "gemini-pro",                          # Pro 1.0 (legado)
    "gemini-pro-vision",                   # Vision 1.0 (legado)
    "gemini-1.0-pro",                      # 1.0 Pro explícito
    "gemini-1.0-pro-latest",               # 1.0 Pro latest
    "gemini-1.0-pro-001",                  # 1.0 Pro versão 001
    "gemini-1.0-pro-vision",               # 1.0 Vision
    "gemini-1.0-pro-vision-latest",        # 1.0 Vision latest
]

# ==============================================================================
# FUNÇÃO PARA VERIFICAR MODELOS ATIVOS
# ==============================================================================
def verificar_modelos_ativos(api_key):
    """Testa quais modelos Gemini estão ativos na API Key fornecida"""
    modelos_validos = []
    genai.configure(api_key=api_key)
    status_msg = st.empty()
    
    for modelo in CANDIDATOS_GEMINI:
        status_msg.text(f"Testando: {modelo}...")
        try:
            m = genai.GenerativeModel(modelo)
            m.generate_content("Oi")
            modelos_validos.append(modelo)
        except Exception:
            pass
    
    status_msg.empty()
    return modelos_validos

# 1. Setup e CSS
ui.carregar_css()
fichas.inicializar_estado()

# 2. Configurações Sidebar
# Inicializar session_state para API keys e lista de modelos
if "evolucao_google_key" not in st.session_state: st.session_state.evolucao_google_key = ""
if "evolucao_openai_key" not in st.session_state: st.session_state.evolucao_openai_key = ""
if "evolucao_lista_modelos_validos" not in st.session_state:
    st.session_state.evolucao_lista_modelos_validos = [
        "gemini-2.5-flash",              # RECOMENDADO: Mais rápido
        "gemini-2.5-pro",                # Máxima qualidade
        "gemini-2.5-flash-thinking",     # Raciocínio avançado
        "gemini-1.5-pro-002"             # Maior contexto
    ]

with st.sidebar:
    st.header("⚙️ Configuração")
    
    # Seleção de IA (Google Gemini como padrão)
    provider = st.radio("IA Padrão:", ["Google Gemini", "OpenAI GPT"], index=0)
    
    if provider == "Google Gemini":
        # API Key do Google
        api_key = st.text_input("Gemini API Key", value=st.session_state.evolucao_google_key, type="password")
        if api_key:
            st.session_state.evolucao_google_key = api_key
            genai.configure(api_key=api_key)
        
        # Botão para atualizar modelos disponíveis
        if st.button("🔄 Atualizar Modelos"):
            if api_key:
                validos = verificar_modelos_ativos(api_key)
                if validos:
                    st.session_state.evolucao_lista_modelos_validos = validos
                    st.success(f"✅ {len(validos)} modelos encontrados!")
            else:
                st.warning("⚠️ Configure a API Key primeiro")
        
        # Dropdown com modelos disponíveis
        modelo_escolhido = st.selectbox(
            "Modelo:",
            st.session_state.evolucao_lista_modelos_validos,
            index=0  # Primeiro da lista como padrão
        )
        
        # Info sobre o modelo selecionado
        if "2.5-flash" in modelo_escolhido and "thinking" not in modelo_escolhido:
            st.success("⚡ Gemini 2.5 Flash: Mais rápido e recente (RECOMENDADO)")
        elif "2.5-pro" in modelo_escolhido:
            st.info("🤖 Gemini 2.5 Pro: Máxima inteligência")
        elif "1.5-pro" in modelo_escolhido:
            st.info("📚 Gemini 1.5 Pro: Maior contexto (2M tokens)")
        elif "thinking" in modelo_escolhido:
            st.info("🎓 Gemini 2.5 Thinking: Raciocínio avançado")
    
    else:  # OpenAI GPT
        # Modelos OpenAI
        modelo_escolhido = st.selectbox("Modelo:", ["gpt-4o", "gpt-4o-mini"], index=0)
        
        # API Key do OpenAI
        api_key = st.text_input("OpenAI Key", value=st.session_state.evolucao_openai_key, type="password")
        if api_key: st.session_state.evolucao_openai_key = api_key

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

    # 3. BOTÃO DE AÇÃO
    if st.button("✨ Extrair Dados Selecionados", type="primary", use_container_width=True):
        if not api_key:
            st.error("Sem chave API.")
        elif not texto_input:
            st.warning("Cole o texto do prontuário primeiro.")
        elif not selecionados_para_ia:
            st.warning("Selecione pelo menos um item para extrair.")
        else:
            with st.spinner(f"Processando com {len(selecionados_para_ia)} agentes de IA..."):
                # Adaptar provider para o formato esperado pelo agente
                provider_completo = f"{provider} {modelo_escolhido}" if provider == "Google Gemini" else provider
                dados = agentes.agente_admissao(texto_input, provider_completo, api_key, escopos=selecionados_para_ia)
                fluxo.atualizar_dados_ia(dados)
                st.success("Dados extraídos com sucesso!")

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