import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO GERAL (Aplicada a todas as páginas)
# ==============================================================================
# Esta linha substitui todos os 'st.set_page_config' que comentamos nas views
st.set_page_config(
    page_title="Intensiva Calculator Pro",
    page_icon="⚕️",
    layout="wide"
)

# ==============================================================================
# SISTEMA DE NAVEGAÇÃO (ROUTER)
# ==============================================================================
# Define a estrutura do menu lateral
pg = st.navigation({
    "Principal": [
        st.Page("views/home.py", title="Home", icon="⚕️", default=True),
    ],
    "Ferramentas Clínicas": [
        st.Page("views/infusao.py", title="Infusão Contínua", icon="💉"),
        st.Page("views/intubacao.py", title="Intubação (IOT)", icon="⚡"),
        st.Page("views/conversao.py", title="Conversão Universal", icon="🔄"),
    ],
})

# ==============================================================================
# EXECUÇÃO
# ==============================================================================
pg.run()