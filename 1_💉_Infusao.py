import streamlit as st
import pandas as pd
from utils import load_data

# ==============================================================================
# 1. CONFIGURAÇÃO VISUAL
# ==============================================================================
st.set_page_config(page_title="Intensiva Calculator Pro", page_icon="⚕️", layout="wide")

COLOR_PRIMARY = "#0F9D58"
COLOR_ACCENT = "#1a73e8"
COLOR_BG = "#FFFFFF"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BG}; }}
    h1, h2, h3 {{ color: {COLOR_PRIMARY}; font-family: 'Roboto', sans-serif; }}
    
    /* ESTILO DOS CARTÕES */
    .result-box {{
        background-color: white; 
        padding: 15px; 
        border-radius: 8px;
        border: 1px solid #ddd; 
        border-left: 5px solid {COLOR_ACCENT}; 
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .result-title {{ font-size: 0.85em; color: #666; font-weight: bold; text-transform: uppercase; margin-bottom: 4px; }}
    .result-value {{ font-size: 1.3em; color: #333; font-weight: bold; }}
    
    .stForm {{ background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #eee; }}
    </style>
""", unsafe_allow_html=True)

# Função auxiliar de formatação
def format_br(valor, casas=1):
    if valor is None: return ""
    if isinstance(valor, (int, float)):
        fmt = f"{{:,.{casas}f}}"
        return fmt.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    return str(valor)

# ==============================================================================
# 2. CARREGAMENTO DE DADOS
# ==============================================================================
st.header("💉 Calculadora de Infusão")

# Tenta carregar do Google Sheets (Aba DB_INFUSAO), se falhar, usa o CSV
df_inf = load_data('DB_INFUSAO', 'banco_dados_infusao.csv')

if df_inf.empty:
    st.error("Erro: Banco de dados não encontrado (Verifique conexão ou arquivos CSV).")
    st.stop()

# ==============================================================================
# 3. INTERFACE DE ENTRADA
# ==============================================================================
col_input_1, col_input_2 = st.columns([1, 2.5])

with col_input_1:
    peso = st.number_input("Peso do Paciente (kg)", value=70.0, step=0.1, format="%.1f")

with col_input_2:
    # Identifica a coluna correta do nome
    col_nome = 'nome_formatado' if 'nome_formatado' in df_inf.columns else 'apresentacao'
    
    if col_nome in df_inf.columns:
        lista_drogas = sorted(df_inf[col_nome].unique())
        
        # --- LÓGICA PARA PADRÃO NOREPINEFRINA ---
        index_padrao = 0
        for i, droga in enumerate(lista_drogas):
            if "noradrenalina" in droga.lower() or "norepinefrina" in droga.lower():
                index_padrao = i
                break
        
        droga_nome = st.selectbox(
            "Selecione a Medicação", 
            lista_drogas, 
            index=index_padrao 
        )
    else:
        st.error("Erro de estrutura: Coluna de nome não encontrada.")
        st.stop()

# ==============================================================================
# 4. CÁLCULOS E LÓGICA
# ==============================================================================
if droga_nome:
    row = df_inf[df_inf[col_nome] == droga_nome].iloc[0]
    info = row.to_dict()

    st.markdown("### Preparo")
    c1, c2, c3 = st.columns(3)
    
    # --- DEFINIÇÃO DE VALORES PADRÃO ---
    is_nora = "noradrenalina" in droga_nome.lower() or "norepinefrina" in droga_nome.lower()
    
    if is_nora:
        def_amp = 4.0
        def_dil = 234
    else:
        # Padrão geral: 1 amp em 98ml (Solução de 100ml)
        def_amp = float(info.get('qtd_amp_padrao', 1.0)) if pd.notna(info.get('qtd_amp_padrao')) and float(info.get('qtd_amp_padrao', 0)) > 0 else 1.0
        def_dil = int(info.get('diluente_padrao', 98)) if pd.notna(info.get('diluente_padrao')) and int(info.get('diluente_padrao', 0)) > 0 else 98
    
    try:
        mg_amp = float(info.get('mg_amp', 0))
        vol_amp = float(info.get('vol_amp', 0))
    except:
        mg_amp = 0
        vol_amp = 0

    with c1: 
        n_ampolas = st.number_input("Número de Ampolas", value=def_amp, step=1.0, format="%.1f")
    with c2: 
        vol_diluente = st.number_input("Volume de Diluente (ml)", value=def_dil, step=1, format="%d")
        
    # --- CÁLCULOS MATEMÁTICOS ---
    qtd_total = n_ampolas * mg_amp
    vol_total = (n_ampolas * vol_amp) + vol_diluente
    if vol_total <= 0: vol_total = 1
    
    conc_principal = qtd_total / vol_total
    conc_secundaria = conc_principal * 1000
    unidade_str = str(info.get('unidade', 'mg'))
    
    if "UI" in unidade_str:
        label_conc_1, label_conc_2 = "UI/ml", "mUI/ml"
    else:
        label_conc_1, label_conc_2 = "mg/ml", "mcg/ml"

    # Função local de conversão
    def converte_dose(dose, unidade_droga):
        try: dose = float(dose)
        except: return 0
        if dose == 0: return 0
        
        if unidade_droga == "mcg/kg/min": return (dose * peso * 60) / conc_secundaria if conc_secundaria else 0
        elif unidade_droga == "mcg/kg/h": return (dose * peso) / conc_secundaria if conc_secundaria else 0
        elif unidade_droga == "mg/kg/h": return (dose * peso) / conc_principal if conc_principal else 0
        elif unidade_droga == "mg/h": return dose / conc_principal if conc_principal else 0
        elif unidade_droga == "mcg/min": return (dose * 60) / conc_secundaria if conc_secundaria else 0
        elif unidade_droga == "mg/min": return (dose * 60) / conc_principal if conc_principal else 0
        elif unidade_droga == "UI/min": return (dose * 60) / conc_principal if conc_principal else 0
        elif unidade_droga == "UI/kg/h": return (dose * peso) / conc_principal if conc_principal else 0
        elif unidade_droga == "mg/kg/min": return (dose * peso * 60) / conc_principal if conc_principal else 0
        return 0

    # Limites
    dose_min = info.get('dose_min', 0)
    dose_max_hab = info.get('dose_max_hab', 0)
    dose_max_tol = info.get('dose_max_tol', 0)

    bomba_min = converte_dose(dose_min, unidade_str)
    bomba_max_hab = converte_dose(dose_max_hab, unidade_str)
    bomba_max_tol = converte_dose(dose_max_tol, unidade_str)

    # --- EXIBIÇÃO ---
    st.markdown("### 1. Dados da Solução")
    col_res1, col_res2, col_res3 = st.columns(3)
    
    # PARTE 1: VERDE (Dados da Solução)
    # Sobrescrevemos o estilo padrão com border-left-color verde
    with col_res1:
        st.markdown(f"""<div class="result-box" style="border-left-color: #28a745;"><div class="result-title">VOLUME FINAL</div><div class="result-value">{int(vol_total)} ml</div></div>""", unsafe_allow_html=True)
    with col_res2:
        st.markdown(f"""<div class="result-box" style="border-left-color: #28a745;"><div class="result-title">CONCENTRAÇÃO ({label_conc_1})</div><div class="result-value">{format_br(conc_principal, 4)} {label_conc_1}</div></div>""", unsafe_allow_html=True)
    with col_res3:
        st.markdown(f"""<div class="result-box" style="border-left-color: #28a745;"><div class="result-title">CONCENTRAÇÃO ({label_conc_2})</div><div class="result-value">{format_br(conc_secundaria, 2)} {label_conc_2}</div></div>""", unsafe_allow_html=True)

    st.markdown(f"### 2. Limites de Velocidade da Bomba ({unidade_str})")
    c_lim1, c_lim2, c_lim3 = st.columns(3)
    
    # PARTE 2: CORES DO SEMÁFORO
    # Alteração feita aqui: Adicionado ', 2' na função format_br para os valores dentro dos parênteses
    with c_lim1:
        # MÍNIMA = AZUL
        st.markdown(f"""<div class="result-box" style="border-left-color: #1a73e8;"><div class="result-title">MÍNIMA<br>({format_br(dose_min, 2)})</div><div class="result-value">{format_br(bomba_min)} ml/h</div></div>""", unsafe_allow_html=True)
    with c_lim2:
        # MÁXIMA HABITUAL = AMARELO
        st.markdown(f"""<div class="result-box" style="border-left-color: #ffc107;"><div class="result-title">MÁXIMA HABITUAL<br>({format_br(dose_max_hab, 2)})</div><div class="result-value">{format_br(bomba_max_hab)} ml/h</div></div>""", unsafe_allow_html=True)
    with c_lim3:
        # MÁXIMA ESTUDADA = VERMELHO
        st.markdown(f"""<div class="result-box" style="border-left-color: #dc3545;"><div class="result-title">MÁXIMA ESTUDADA<br>({format_br(dose_max_tol, 2)})</div><div class="result-value">{format_br(bomba_max_tol)} ml/h</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    
    # --- SIMULADOR ---
    st.subheader("3. Simulador em Tempo Real")
    col_sim1, col_sim2 = st.columns(2)
    
    with col_sim1:
        val_inicial = float(bomba_min) if bomba_min > 0 else 0.0
        ml_h_atual = st.number_input("Velocidade Atual da Bomba (ml/h)", value=val_inicial, step=0.1, format="%.1f")
        
        if ml_h_atual > 0:
            # Cálculo Reverso
            if unidade_str == "mcg/kg/min": dose_real = (ml_h_atual * conc_secundaria) / peso / 60
            elif unidade_str == "mcg/kg/h": dose_real = (ml_h_atual * conc_secundaria) / peso
            elif unidade_str == "mg/kg/h": dose_real = (ml_h_atual * conc_principal) / peso
            elif unidade_str == "mg/h": dose_real = ml_h_atual * conc_principal
            elif unidade_str == "mcg/min": dose_real = (ml_h_atual * conc_secundaria) / 60
            elif unidade_str == "mg/min": dose_real = (ml_h_atual * conc_principal) / 60
            elif unidade_str == "UI/min": dose_real = (ml_h_atual * conc_principal) / 60
            elif unidade_str == "UI/kg/h": dose_real = (ml_h_atual * conc_principal) / peso
            elif unidade_str == "mg/kg/min": dose_real = (ml_h_atual * conc_principal) / peso / 60
            else: dose_real = 0
            
            st.metric(f"Dose Entregue ({unidade_str})", f"{format_br(dose_real, 2)}")
            
            try:
                max_tol = float(dose_max_tol)
                max_hab = float(dose_max_hab)
                if max_tol > 0 and dose_real > max_tol: 
                    st.error("🚨 PERIGO: Dose acima da MÁXIMA ESTUDADA!")
                elif max_hab > 0 and dose_real > max_hab: 
                    st.warning("⚠️ Atenção: Dose acima da máxima habitual.")
                else: 
                    st.success("✅ Dentro da faixa segura.")
            except: pass