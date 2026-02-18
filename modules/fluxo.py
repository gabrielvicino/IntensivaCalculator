import streamlit as st

# Mapeamento: chave do JSON retornado pela IA → chave do session_state
_MAPA_NOTAS = {
    "identificacao": "identificacao_notas",
    "hd":            "hd_notas",
    "comorbidades":  "comorbidades_notas",
    "muc":           "muc_notas",
    "hmpa":          "hmpa_texto",
    "dispositivos":  "dispositivos_notas",
    "culturas":      "culturas_notas",
    "antibioticos":  "antibioticos_notas",
    "complementares":"complementares_notas",
    "laboratoriais": "laboratoriais_notas",
    "evolucao":      "evolucao_notas",
    "sistemas":      "sistemas_notas",
    "conduta":       "conduta_final_lista",
}

def atualizar_notas_ia(dados: dict):
    """Recebe o JSON do ia_extrator e preenche os campos _notas de cada seção."""
    if not dados:
        return

    erro = dados.get("_erro")
    if erro:
        st.error(f"Erro na extração: {erro}")
        return

    preenchidos = 0
    for chave_json, chave_estado in _MAPA_NOTAS.items():
        valor = dados.get(chave_json, "")
        if valor and valor.strip():
            st.session_state[chave_estado] = valor.strip()
            preenchidos += 1

    if preenchidos:
        st.toast(f"✅ {preenchidos} seções preenchidas com sucesso!", icon="🧬")
    else:
        st.warning("A IA não encontrou dados para preencher. Verifique o texto colado.")

def limpar_tudo():
    """Reseta todos os campos do formulário para o estado inicial."""
    keys_texto = [
        'nome', 'prontuario', 'leito', 'origem', 'equipe', 
        'di_hosp', 'di_uti', 'di_enf', 'hd_principal', 'texto_final_gerado',
        'saps3', 'mrs', 'pps', 'cfs'
    ]
    for k in keys_texto:
        if k in st.session_state: st.session_state[k] = ""
            
    # Resets específicos
    st.session_state['idade'] = 0
    st.session_state['sofa_adm'] = 0
    st.session_state['sofa_atual'] = 0
    st.session_state['paliativo'] = False
    st.session_state['hd_status'] = "Estável"
    st.session_state['sexo'] = "Masculino"
    
    st.toast("Formulário reiniciado.", icon="🔄")

def atualizar_dados_ia(dados):
    """Recebe o JSON da IA e atualiza o session_state com segurança."""
    if not dados: return

    # 1. Identidade
    identidade = dados.get('identidade', {})
    st.session_state.update(identidade)
    
    # 2. Datas (se vierem aninhadas)
    datas = identidade.get('datas', {})
    if datas:
        st.session_state['di_hosp'] = datas.get('hospital', '')
        st.session_state['di_uti'] = datas.get('uti', '')
        st.session_state['di_enf'] = datas.get('enf', '')
    
    # 3. Scores
    scores = dados.get('scores', {})
    if scores:
        st.session_state['saps3'] = scores.get('saps3', '')
        st.session_state['sofa_adm'] = scores.get('sofa_adm', 0)
        st.session_state['sofa_atual'] = scores.get('sofa_atual', 0)
        st.session_state['mrs'] = str(scores.get('mrs', ''))
        st.session_state['pps'] = scores.get('pps', '')
        st.session_state['paliativo'] = scores.get('paliativo', False)
        
    st.toast("Sucesso! Dados preenchidos.", icon="✅")