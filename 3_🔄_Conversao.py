import streamlit as st

# ==============================================================================
# 1. CONFIGURAÇÃO VISUAL E ESTILO
# ==============================================================================
st.set_page_config(page_title="Conversão Universal", page_icon="🔄", layout="wide")

COLOR_PRIMARY = "#0F9D58"
COLOR_ACCENT = "#1a73e8"
COLOR_BG = "#FFFFFF"

# CSS Personalizado
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BG}; }}
    h1, h2, h3 {{ color: {COLOR_PRIMARY}; font-family: 'Roboto', sans-serif; }}
    
    /* ESTILO DOS CARTÕES DE RESULTADO */
    .result-box {{
        background-color: white; 
        padding: 15px; 
        border-radius: 8px;
        border: 1px solid #ddd; 
        border-left: 5px solid {COLOR_ACCENT}; 
        margin-bottom: 10px;
        box_shadow: 0 2px 4px rgba(0,0,0,0.05);
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
# 2. LÓGICA DA PÁGINA
# ==============================================================================
st.header("🔄 Conversão Universal")

# --- 1. CONFIGURAÇÃO DA SOLUÇÃO ---
st.markdown("##### 1. Configurar Solução")
c1, c2, c3, c4 = st.columns(4)

with c1: 
    peso = st.number_input("Peso (kg)", value=70.0, step=0.1, key="conv_peso", format="%.1f")
with c2: 
    qtd = st.number_input("Qtd. Total", value=250.0, step=0.1, key="conv_qtd", format="%.1f")
with c3: 
    unid = st.selectbox("Unidade", ["mg", "mcg", "g", "UI"], key="conv_unid")
with c4: 
    vol = st.number_input("Volume Total (ml)", value=250, step=1, key="conv_vol", format="%d")

if vol <= 0: vol = 1
conc_base = qtd / vol

# Define fatores de conversão
fator_c1 = 1
lbl_c1 = ""
fator_c2 = None
lbl_c2 = "-"

if unid == "g":
    fator_c1 = 1000        # g -> mg
    lbl_c1 = "mg"
    fator_c2 = 1000000     # g -> mcg
    lbl_c2 = "mcg"
elif unid == "mg":
    fator_c1 = 1           # mg -> mg
    lbl_c1 = "mg"
    fator_c2 = 1000        # mg -> mcg
    lbl_c2 = "mcg"
elif unid == "mcg":
    fator_c1 = 1
    lbl_c1 = "mcg"
    fator_c2 = None
    lbl_c2 = "-"
elif unid == "UI":
    fator_c1 = 1
    lbl_c1 = "UI"
    fator_c2 = 1000
    lbl_c2 = "mUI"

conc_c1 = conc_base * fator_c1
conc_c2 = conc_base * fator_c2 if fator_c2 else 0

st.info(f"Concentração: **{format_br(conc_c1)} {lbl_c1}/ml**" + (f" | **{format_br(conc_c2)} {lbl_c2}/ml**" if fator_c2 else ""))

# --- 2. INPUT DE VELOCIDADE ---
st.markdown("##### 2. Velocidade de Infusão")
ml_h = st.number_input("Vazão da Bomba (ml/h)", value=10.0, step=0.1, key="c_mlh", format="%.1f")

# --- 3. CÁLCULOS E EXIBIÇÃO ---
st.markdown("##### 3. Resultados Detalhados")

# Cálculos Coluna 1
dose_h_c1 = ml_h * conc_c1
dose_min_c1 = dose_h_c1 / 60
dose_kg_h_c1 = dose_h_c1 / peso
dose_kg_min_c1 = dose_kg_h_c1 / 60

# Cálculos Coluna 2
if fator_c2:
    dose_h_c2 = ml_h * conc_c2
    dose_min_c2 = dose_h_c2 / 60
    dose_kg_h_c2 = dose_h_c2 / peso
    dose_kg_min_c2 = dose_kg_h_c2 / 60

col_res_a, col_res_b = st.columns(2)

# --- Renderização Segura do HTML ---
with col_res_a:
    st.markdown(f"**Unidade Principal ({lbl_c1})**")
    
    html_content_a = f"""
    <div class="result-box" style="border-left-color: #2ecc71;">
        <div class="result-title">DOSE / HORA</div>
        <div class="result-value">{format_br(dose_h_c1)} {lbl_c1}/h</div>
        <div class="result-title" style="margin-top:10px;">DOSE / MINUTO</div>
        <div class="result-value">{format_br(dose_min_c1)} {lbl_c1}/min</div>
    </div>
    <div class="result-box" style="border-left-color: #2ecc71;">
        <div class="result-title">DOSE / KG / HORA</div>
        <div class="result-value">{format_br(dose_kg_h_c1)} {lbl_c1}/kg/h</div>
        <div class="result-title" style="margin-top:10px;">DOSE / KG / MINUTO</div>
        <div class="result-value">{format_br(dose_kg_min_c1)} {lbl_c1}/kg/min</div>
    </div>
    """
    st.markdown(html_content_a, unsafe_allow_html=True)

if fator_c2:
    with col_res_b:
        st.markdown(f"**Unidade Secundária ({lbl_c2})**")
        
        html_content_b = f"""
        <div class="result-box" style="border-left-color: #3498db;">
            <div class="result-title">DOSE / HORA</div>
            <div class="result-value">{format_br(dose_h_c2)} {lbl_c2}/h</div>
            <div class="result-title" style="margin-top:10px;">DOSE / MINUTO</div>
            <div class="result-value">{format_br(dose_min_c2)} {lbl_c2}/min</div>
        </div>
        <div class="result-box" style="border-left-color: #3498db;">
            <div class="result-title">DOSE / KG / HORA</div>
            <div class="result-value">{format_br(dose_kg_h_c2)} {lbl_c2}/kg/h</div>
            <div class="result-title" style="margin-top:10px;">DOSE / KG / MINUTO</div>
            <div class="result-value">{format_br(dose_kg_min_c2)} {lbl_c2}/kg/min</div>
        </div>
        """
        st.markdown(html_content_b, unsafe_allow_html=True)