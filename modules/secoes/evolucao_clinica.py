import streamlit as st

def get_campos():
    return {
        'evolucao_notas': ''
    }

def render():
    st.markdown("##### 11. Evolução Clínica (Texto Livre)")
    
    st.text_area("Notas", key="evolucao_notas", height="content", placeholder="Cole neste campo a evolução...", label_visibility="collapsed")