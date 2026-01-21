import streamlit as st
import pandas as pd
from datetime import datetime
from utils import load_data, save_data_append

# ==============================================================================
# 1. CONFIGURAÇÕES E PARSER DE EXAMES
# ==============================================================================
def smart_parser_exames(texto):
    """Tenta extrair valores numéricos de um texto colado (Hb 12 Leuc 10000...)"""
    dados = {}
    if not texto: return dados
    
    # Normaliza: tudo minúsculo e troca : por espaço
    t = texto.lower().replace(":", " ").replace("/", " ")
    tokens = t.split()
    
    # Dicionário de sinônimos para busca
    mapa = {
        'hb': ['hb', 'hemoglobina'],
        'ht': ['ht', 'hematocrito'],
        'leuc': ['leuco', 'leucocitos', 'leucócitos', 'gb'],
        'plaq': ['plaq', 'plaquetas'],
        'cr': ['cr', 'creatinina', 'creat'],
        'ur': ['ur', 'ureia'],
        'na': ['na', 'sodio', 'sódio', 'natremia'],
        'k': ['k', 'potassio', 'potássio', 'calemia'],
        'pcr': ['pcr'],
        'lact': ['lact', 'lactato']
    }
    
    for chave, sinonimos in mapa.items():
        for sin in sinonimos:
            if sin in tokens:
                try:
                    idx = tokens.index(sin)
                    # Tenta pegar o próximo item como valor
                    if idx + 1 < len(tokens):
                        val_str = tokens[idx+1]
                        # Limpa caracteres estranhos mas mantem ponto e virgula
                        val_limpo = ''.join(c for c in val_str if c.isdigit() or c in '.,')
                        dados[chave] = val_limpo
                        break
                except:
                    pass
    return dados

# ==============================================================================
# 2. INTERFACE PRINCIPAL
# ==============================================================================
st.header("📝 Evolução Diária Inteligente")

# --- BARRA SUPERIOR: IDENTIFICAÇÃO ---
with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    id_paciente = c1.text_input("🆔 ID / Leito", placeholder="Ex: 105")
    
    # Botão de carregar (Simulação por enquanto)
    if c2.button("🔄 Carregar Anterior"):
        st.info("Funcionalidade de busca será ativada na próxima etapa.")
    
    data_hoje = c3.date_input("Data", datetime.now())

# ==============================================================================
# 3. FORMULÁRIO ÚNICO (Para fluidez)
# ==============================================================================
with st.form("form_evolucao"):
    
    # --- BLOCO 1: IDENTIDADE & ESCORES (Grid 4 colunas) ---
    st.markdown("### 1. Identificação & Escores")
    b1_c1, b1_c2, b1_c3, b1_c4 = st.columns(4)
    with b1_c1:
        nome = st.text_input("Nome", placeholder="Iniciais ou Primeiro Nome")
        idade = st.text_input("Idade")
    with b1_c2:
        cidade = st.text_input("Cidade")
        origem = st.text_input("Origem", placeholder="Ex: PS, CC") # <--- CAMPO NOVO AQUI
        equipe = st.text_input("Equipe Resp.")
    with b1_c3:
        dih = st.text_input("DIH (Dias)")
        di_uti = st.text_input("DI-UTI")
    with b1_c4:
        apache = st.text_input("APACHE II")
        sofa = st.text_input("SOFA Atual")
    
    st.divider()

    # --- BLOCO 2: CLÍNICA (2 Colunas Largas) ---
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.markdown("#### 🏥 Diagnósticos (HDs)")
        hd_atual = st.text_area("HD Atual (Lista)", height=100, help="1. Sepse Foco Pulmonar\n2. IRA KDIGO 3")
        hd_previo = st.text_area("HDs Prévios / Resolvidos", height=68)
        
    with c_right:
        st.markdown("#### ⚠️ Antecedentes")
        comorbidades = st.text_area("Comorbidades", height=100, placeholder="DM2, HAS, DRC...")
        hmpa = st.text_area("HMPA / Internação Atual", height=68)

    st.divider()

    # --- BLOCO 3: INFECTO & DISPOSITIVOS ---
    st.markdown("#### 🦠 Infecto & Invasões")
    col_inf1, col_inf2 = st.columns(2)
    
    with col_inf1:
        atb_atual = st.text_input("💊 ATB Atual (Droga - Dia - Início)", placeholder="Meropenem D3 (Início 15/01)")
        culturas = st.text_area("🧫 Culturas (Em andamento/Resultado)", height=80)
    
    with col_inf2:
        tot = st.text_input("Tubo Orotraqueal (Data)", placeholder="Data Intubação")
        cvc = st.text_input("Acesso Central (Data/Sítio)")
        svd = st.text_input("Sonda Vesical (Data)")

    st.divider()

    # --- BLOCO 4: EXAMES & PARSER (A Mágica) ---
    st.markdown("#### 🧪 Laboratório & Imagem")
    
    # O Campo "Colar" que preenche os outros
    texto_paste = st.text_area("📋 Cole a linha de exames aqui para preencher auto:", placeholder="Hb: 12.0 Leuc: 14.500 Plaq: 150.000 Cr: 1.2")
    
    # Grid de Exames Manuais
    l1, l2, l3, l4, l5 = st.columns(5)
    gas1, gas2, gas3, gas4 = st.columns(4)
    
    # Usando keys para recuperar depois, se necessário
    l1.text_input("Hb", key="lab_hb")
    l2.text_input("Leuco", key="lab_leuco")
    l3.text_input("Plaq", key="lab_plaq")
    l4.text_input("Cr", key="lab_cr")
    l5.text_input("PCR", key="lab_pcr")
    
    gas1.text_input("pH")
    gas2.text_input("pCO2")
    gas3.text_input("HCO3")
    gas4.text_input("Lactato")

    st.text_area("Imagens / Complementares (TC, RX...)", height=70)

    st.divider()

    # --- BLOCO 5: SISTEMAS (Grid Visual) ---
    st.markdown("#### 🧠 Análise por Sistemas")
    
    # Linha 1
    s1, s2 = st.columns(2)
    with s1: 
        st.caption("Neurológico")
        neuro = st.text_area("Neuro", height=80, label_visibility="collapsed", placeholder="RASS, Sedação, Pupilas...")
    with s2:
        st.caption("Respiratório")
        resp = st.text_area("Resp", height=80, label_visibility="collapsed", placeholder="VM, Modos, Trocas...")

    # Linha 2
    s3, s4 = st.columns(2)
    with s3:
        st.caption("Cardiovascular")
        cardio = st.text_area("Cardio", height=80, label_visibility="collapsed", placeholder="Drogas, PA, Perfusão...")
    with s4:
        st.caption("Renal / Metabólico")
        renal = st.text_area("Renal", height=80, label_visibility="collapsed", placeholder="Diurese, Balanço, Dextros...")

    # Linha 3
    s5, s6 = st.columns(2)
    with s5:
        st.caption("Gastro / Nutri")
        gastro = st.text_area("Gastro", height=80, label_visibility="collapsed", placeholder="Dieta, Evacuações...")
    with s6:
        st.caption("Hemato / Infecto")
        hemato = st.text_area("Hemato", height=80, label_visibility="collapsed", placeholder="Sangramentos, Curva térmica...")

    st.divider()
    
    # --- FINALIZAÇÃO ---
    condutas = st.text_area("🎯 Plano Terapêutico / Condutas", height=100)

    # BOTÃO FINAL
    submit = st.form_submit_button("💾 Salvar & Gerar Resumo", type="primary")

# ==============================================================================
# 4. LÓGICA DE SALVAMENTO (PÓS-CLICK)
# ==============================================================================
if submit:
    if not id_paciente:
        st.error("⚠️ Obrigatório: Preencha o ID do Paciente (Prontuário/Leito) para salvar.")
    else:
        # Prepara a lista de dados EXATAMENTE na ordem das colunas do Sheets
        
        # Formatando datas para string
        data_reg_str = data_hoje.strftime("%d/%m/%Y")
        
        # Recuperando valores dos labs manuais
        lab_hb = st.session_state.get("lab_hb", "")
        lab_leuco = st.session_state.get("lab_leuco", "")
        lab_plaq = st.session_state.get("lab_plaq", "")
        lab_cr = st.session_state.get("lab_cr", "")
        lab_pcr = st.session_state.get("lab_pcr", "")
        
        # Resumo dos labs
        labs_resumo = f"Hb {lab_hb} / Leuco {lab_leuco} / Plaq {lab_plaq} / Cr {lab_cr} / PCR {lab_pcr}"

        # LISTA MESTRA (Ordem das colunas A -> BN)
        # ATENÇÃO: Se mudar no Sheets, tem que mudar aqui!
        dados_paciente = [
            id_paciente,        # A: id_paciente
            data_reg_str,       # B: data_registro
            nome,               # C: nome_paciente
            idade,              # D: idade
            cidade,             # E: cidade
            origem,             # F: origem <--- AGORA ELA ESTÁ AQUI DEFINIDA!
            dih,                # G: dih
            di_uti,             # H: di_uti
            equipe,             # I: equipe
            
            apache,             # J: apache_ii
            "",                 # K: apache_iv
            "",                 # L: saps_ii
            "",                 # M: saps_3
            sofa,               # N: sofa
            "",                 # O: qsofa
            "",                 # P: mrs_barthel
            "",                 # Q: frailty
            "",                 # R: ecog_pps
            
            hd_atual,           # S: hd_atual
            hd_previo,          # T: hd_previo
            comorbidades,       # U: comorbidades
            "",                 # V: mucs
            hmpa,               # W: hmpa
            
            tot,                # X: tot_data
            svd,                # Y: svd_data
            cvc,                # Z: cvc_data
            "",                 # AA: dispositivos_previos
            
            culturas,           # AB: culturas_andamento
            "",                 # AC: culturas_previas
            atb_atual,          # AD: atb_atual
            "",                 # AE: atb_previo
            
            "",                 # AF: tc_laudo
            "",                 # AG: rnm_laudo
            labs_resumo,        # AH: labs_texto_livre
            "",                 # AI: gaso_ph
            "",                 # AJ: gaso_pco2
            "",                 # AK: gaso_hco3
            "",                 # AL: gaso_be
            "",                 # AM: gaso_lactato
            texto_paste,        # AN: laboratorio_smart
            
            "",                 # AO: pas
            "",                 # AP: pad
            "",                 # AQ: pam
            "",                 # AR: fc
            "",                 # AS: fr
            "",                 # AT: dextro
            "",                 # AU: temp
            "",                 # AV: bh_24h
            "",                 # AW: diurese
            "",                 # AX: evacuacao
            "",                 # AY: bh_acumulado
            
            neuro,              # AZ: sis_neuro
            resp,               # BA: sis_resp
            cardio,             # BB: sis_cardio
            renal,              # BC: sis_renal
            gastro,             # BD: sis_gastro
            "",                 # BE: sis_hepatico
            hemato,             # BF: sis_hemato
            "",                 # BG: sis_infecto
            "",                 # BH: sis_endocrino
            "",                 # BI: sis_pele
            "",                 # BJ: sis_dispositivos_analise
            "",                 # BK: sis_profilaxias
            "",                 # BL: sis_planejamento
            
            condutas,           # BM: condutas_finais
            ""                  # BN: resumo_gerado
        ]

        # Resumo visual (para copiar)
        resumo_visual = f"""
        *EVOLUÇÃO UTI - {data_reg_str}*
        **ID:** {id_paciente} | **Nome:** {nome} | **Origem:** {origem}
        
        **# HDs:** {hd_atual}
        **# INFECTO:** ATB: {atb_atual} | Culturas: {culturas}
        
        **# SISTEMAS:**
        - Neuro: {neuro}
        - Resp: {resp}
        - Cardio: {cardio}
        - Renal: {renal}
        
        **# CONDUTAS:**
        {condutas}
        """
        
        # Tenta Salvar
        with st.spinner("Salvando na nuvem..."):
            sucesso = save_data_append("DB_EVOLUCAO", dados_paciente)
            
        if sucesso:
            st.success("✅ Evolução Salva no Google Sheets!")
            st.markdown("### 📋 Copie para o Prontuário:")
            st.code(resumo_visual, language="markdown")
        else:
            st.error("Erro ao salvar. Verifique se a planilha está com as colunas corretas.")