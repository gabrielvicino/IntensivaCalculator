import streamlit as st

# Funções para gerenciar ordem dos exames complementares
def _inicializar_ordem():
    """Inicializa a ordem dos exames complementares se não existir"""
    if 'comp_ordem' not in st.session_state:
        st.session_state.comp_ordem = list(range(1, 9))

def _trocar_ordem(idx1, idx2):
    """Troca a ordem de exibição de dois exames"""
    _inicializar_ordem()
    ordem = st.session_state.comp_ordem
    ordem[idx1], ordem[idx2] = ordem[idx2], ordem[idx1]
    st.session_state.comp_ordem = ordem

# 1. Definição das Variáveis (8 Slots Total)
def get_campos():
    campos = {'complementares_notas': ''}
    for i in range(1, 9):
        campos.update({
            f'comp_{i}_laudo': '',
            f'comp_{i}_conduta': ''
        })
    return campos

# Função auxiliar para desenhar UM card de exame complementar
def _render_linha(idx_display, id_real):
    """
    Renderiza um card de exame complementar.
    idx_display: posição de exibição (1-8)
    id_real: ID real do exame nos dados (1-8)
    """
    with st.container(border=True):
        col_titulo, col_up, col_down = st.columns([10, 1, 1])
        with col_titulo:
            st.markdown(f"**Exame Complementar {idx_display}**")
        with col_up:
            if idx_display > 1:
                if st.button("↑", key=f"comp_up_pos_{idx_display}", help="Mover para cima"):
                    _trocar_ordem(idx_display-1, idx_display-2)
                    st.rerun()
        with col_down:
            if idx_display < 8:
                if st.button("↓", key=f"comp_down_pos_{idx_display}", help="Mover para baixo"):
                    _trocar_ordem(idx_display-1, idx_display)
                    st.rerun()
        st.text_area(
            f"Laudos {idx_display}",
            key=f"comp_{id_real}_laudo",
            placeholder="Exemplo: TC de tórax sem contraste - Consolidação em lobo superior direito...",
            height=120
        )
        with st.success("Conduta"):
            st.text_input(
                f"Conduta {idx_display}",
                key=f"comp_{id_real}_conduta",
                placeholder="Exemplo: Solicitar TC com contraste, Aguardar reavaliação...",
                label_visibility="collapsed"
            )

# 2. Renderização Principal
def render():
    st.markdown("##### 9. Exames Complementares")
    
    st.text_area("Notas", key="complementares_notas", height="content", placeholder="Cole neste campo a evolução...", label_visibility="collapsed")
    st.write("")
    
    # Inicializa ordem
    _inicializar_ordem()
    ordem = st.session_state.comp_ordem
    
    # --- 3 Itens VISÍVEIS ---
    for i in range(1, 4):
        _render_linha(i, ordem[i-1])
        st.write("")
        
    # --- 5 Itens OCULTOS (abre automaticamente se houver conteúdo) ---
    st.write("")
    
    # Verifica se há conteúdo nos exames 4 a 8
    tem_conteudo = False
    for i in range(4, 9):
        id_real = ordem[i-1]
        if (st.session_state.get(f"comp_{id_real}_laudo", "") or 
            st.session_state.get(f"comp_{id_real}_conduta", "")):
            tem_conteudo = True
            break
    
    with st.expander("Demais Exames Complementares", expanded=tem_conteudo):
        for i in range(4, 9):
            _render_linha(i, ordem[i-1])
            st.write("")
