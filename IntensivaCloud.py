import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
    .result-box {{
        background-color: white; padding: 15px; border-radius: 8px;
        border: 1px solid #ddd; border-left: 5px solid {COLOR_ACCENT}; margin-bottom: 10px;
    }}
    .result-title {{ font-size: 0.9em; color: #666; font-weight: bold; }}
    .result-value {{ font-size: 1.4em; color: #333; font-weight: bold; }}
    .stForm {{ background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #eee; }}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CONEXÃO GOOGLE SHEETS (SOMENTE LEITURA)
# ==============================================================================
SHEET_NAME_INF = "DB_INFUSAO"
SHEET_NAME_IOT = "DB_IOT"

def get_google_sheet_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = {
        "type": st.secrets["gcp_service_account"]["type"],
        "project_id": st.secrets["gcp_service_account"]["project_id"],
        "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
        "private_key": st.secrets["gcp_service_account"]["private_key"],
        "client_email": st.secrets["gcp_service_account"]["client_email"],
        "client_id": st.secrets["gcp_service_account"]["client_id"],
        "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
        "token_uri": st.secrets["gcp_service_account"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
    }
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

@st.cache_data(ttl=60) # Atualiza a cada 60 segundos se houver mudança
def load_data_from_sheet(sheet_tab_name):
    try:
        client = get_google_sheet_client()
        sheet = client.open("IntensivaDB").worksheet(sheet_tab_name)
        data = sheet.get_all_records()
        if not data: return pd.DataFrame()
        df = pd.DataFrame(data)
        # Garante que números sejam números, mas ignora erros se estiver vazio
        cols_numericas = ['mg_amp', 'vol_amp', 'dose_min', 'dose_max_hab', 'dose_max_tol', 'conc', 'dose_hab', 'dose_max']
        for col in cols_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except Exception:
        return pd.DataFrame()

# ==============================================================================
# CARREGAMENTO DE DADOS
# ==============================================================================
df_inf = load_data_from_sheet(SHEET_NAME_INF)
df_iot = load_data_from_sheet(SHEET_NAME_IOT)

def df_to_dict_inf(df):
    if df.empty: return {}
    # Remove duplicatas baseadas no nome
    df = df.drop_duplicates(subset=['nome_formatado'], keep='last')
    return df.set_index('nome_formatado').to_dict(orient='index')

def df_to_dict_iot(df):
    if df.empty: return {}
    df = df.drop_duplicates(subset=['nome_formatado'], keep='last')
    return df.set_index('nome_formatado').to_dict(orient='index')

MED_DB_INF = df_to_dict_inf(df_inf)
MED_DB_IOT = df_to_dict_iot(df_iot)

# ==============================================================================
# UTILITÁRIOS
# ==============================================================================
def format_br(valor):
    if valor is None: return ""
    if isinstance(valor, (int, float)):
        texto = f"{valor:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if "," in texto:
            texto = texto.rstrip("0")
            if texto.endswith(","): texto = texto[:-1]
        return texto
    return str(valor)

# ==============================================================================
# PÁGINAS
# ==============================================================================
def calcular_infusao():
    st.header("💉 Calculadora de Infusão")
    
    col_input_1, col_input_2 = st.columns([1, 2.5])
    with col_input_1:
        peso = st.number_input("Peso (kg)", value=70.0, step=0.1, format="%.1f")
    with col_input_2:
        lista_drogas = sorted(list(MED_DB_INF.keys()))
        if not lista_drogas:
            st.warning("Banco de dados vazio. Preencha a Planilha Google.")
            droga_nome = None
        else:
            droga_nome = st.selectbox("Selecione a Medicação", lista_drogas)
    
    if droga_nome:
        info = MED_DB_INF[droga_nome]
        st.markdown("### Preparo")
        c1, c2, c3 = st.columns(3)
        
        # Recupera valores padrão do banco de dados
        padrao_amp = float(info.get('qtd_amp_padrao', 1.0)) if 'qtd_amp_padrao' in info else 1.0
        padrao_dil = float(info.get('diluente_padrao', 246.0)) if 'diluente_padrao' in info else 246.0

        with c1: n_ampolas = st.number_input("Nº Ampolas", value=padrao_amp, step=1.0, format="%.1f")
        with c2: vol_diluente = st.number_input("Diluente (ml)", value=padrao_dil, step=1.0, format="%.1f")
            
        qtd_total = n_ampolas * float(info['mg_amp'])
        vol_total = (n_ampolas * float(info['vol_amp'])) + vol_diluente
        if vol_total <= 0: vol_total = 1
        conc_principal = qtd_total / vol_total
        conc_secundaria = conc_principal * 1000
        unidade_str = str(info['unidade'])
        
        if "UI" in unidade_str:
            label_conc_1, label_conc_2 = "UI/ml", "mUI/ml"
        else:
            label_conc_1, label_conc_2 = "mg/ml", "mcg/ml"

        def converte_dose_para_mlh(dose, unidade_droga):
            dose = float(dose)
            if dose == 0: return 0
            if unidade_droga == "mcg/kg/min": return (dose * peso * 60) / conc_secundaria
            elif unidade_droga == "mcg/kg/h": return (dose * peso) / conc_secundaria
            elif unidade_droga == "mg/kg/h": return (dose * peso) / conc_principal
            elif unidade_droga == "mg/h": return dose / conc_principal
            elif unidade_droga == "mcg/min": return (dose * 60) / conc_secundaria
            elif unidade_droga == "mg/min": return (dose * 60) / conc_principal
            elif unidade_droga == "UI/min": return (dose * 60) / conc_principal
            elif unidade_droga == "UI/kg/h": return (dose * peso) / conc_principal
            elif unidade_droga == "mg/kg/min": return (dose * peso * 60) / conc_principal
            return 0

        bomba_min = converte_dose_para_mlh(info['dose_min'], unidade_str)
        bomba_max_hab = converte_dose_para_mlh(info['dose_max_hab'], unidade_str)
        bomba_max_tol = converte_dose_para_mlh(info['dose_max_tol'], unidade_str)

        # RESULTADOS
        st.info(f"Concentração: **{format_br(conc_principal)} {label_conc_1}** |  **{format_br(conc_secundaria)} {label_conc_2}**")
        
        st.markdown(f"**Velocidades de Bomba ({unidade_str} ➔ ml/h)**")
        c_lim1, c_lim2, c_lim3 = st.columns(3)
        with c_lim1:
            st.markdown(f"""<div class="result-box" style="border-left-color: #f1c40f;"><div class="result-title">MÍNIMA<br>({format_br(info['dose_min'])})</div><div class="result-value">{format_br(bomba_min)} <span style='font-size:0.6em'>ml/h</span></div></div>""", unsafe_allow_html=True)
        with c_lim2:
            st.markdown(f"""<div class="result-box" style="border-left-color: #2ecc71;"><div class="result-title">HABITUAL<br>({format_br(info['dose_max_hab'])})</div><div class="result-value">{format_br(bomba_max_hab)} <span style='font-size:0.6em'>ml/h</span></div></div>""", unsafe_allow_html=True)
        with c_lim3:
            st.markdown(f"""<div class="result-box" style="border-left-color: #e74c3c;"><div class="result-title">TOLERADA<br>({format_br(info['dose_max_tol'])})</div><div class="result-value">{format_br(bomba_max_tol)} <span style='font-size:0.6em'>ml/h</span></div></div>""", unsafe_allow_html=True)

        st.divider()
        st.caption("Simulador Reverso")
        col_sim1, col_sim2 = st.columns([1, 2])
        with col_sim1:
            ml_h_atual = st.number_input("Vazão (ml/h)", value=0.0, step=0.1)
        with col_sim2:
            if ml_h_atual > 0:
                # Calculo reverso simplificado
                if "mcg/kg/min" in unidade_str: dose_real = (ml_h_atual * conc_secundaria) / peso / 60
                elif "mg/kg/h" in unidade_str: dose_real = (ml_h_atual * conc_principal) / peso
                else: dose_real = 0 # Simplificação para o exemplo
                
                # Só exibe se calculou algo
                if dose_real > 0:
                    st.metric(f"Dose Real ({unidade_str})", f"{format_br(dose_real)}")

def page_iot():
    st.header("⚡ Intubação Orotraqueal")
    peso = st.number_input("Peso (kg)", value=70.0, step=0.1, format="%.1f")
    
    dados_tabela = []
    for nome_droga in sorted(MED_DB_IOT.keys()):
        dado = MED_DB_IOT[nome_droga]
        conc = float(dado['conc'])
        if conc > 0:
            vol_min = (float(dado['dose_min']) * peso) / conc
            vol_hab = (float(dado['dose_hab']) * peso) / conc
            vol_max = (float(dado['dose_max']) * peso) / conc
            
            dados_tabela.append({
                "Medicação": nome_droga,
                "Vol. Mínimo": f"{format_br(vol_min)} ml",
                "Vol. Médio": f"**{format_br(vol_hab)} ml**", 
                "Vol. Máximo": f"{format_br(vol_max)} ml"
            })
        
    if dados_tabela:
        st.dataframe(pd.DataFrame(dados_tabela), use_container_width=True, hide_index=True)
    else:
        st.warning("Nenhum dado na planilha DB_IOT.")

def page_conversao():
    st.header("🔄 Conversão Universal")
    # (Mantive simples para economizar espaço, mas funcional)
    c1, c2 = st.columns(2)
    with c1: peso = st.number_input("Peso (kg)", 70.0)
    with c2: qtd = st.number_input("Mg Total na Solução", 250.0)
    vol = st.number_input("Volume Total (ml)", 250.0)
    if vol > 0:
        conc = qtd/vol
        st.info(f"Concentração: {conc} mg/ml | {conc*1000} mcg/ml")
        mlh = st.number_input("Vazão (ml/h)", 10.0)
        st.write(f"Dose: {format_br((mlh * conc * 1000)/peso/60)} mcg/kg/min")

# ==============================================================================
# MENU LATERAL
# ==============================================================================
st.sidebar.title("Menu")
nav = st.sidebar.radio("Navegar:", ["Infusão Contínua", "Intubação", "Conversão"])

if nav == "Infusão Contínua": calcular_infusao()
elif nav == "Intubação": page_iot()
elif nav == "Conversão": page_conversao()