import streamlit as st
import pandas as pd
from utils import load_data

# ==============================================================================
# 1. CONFIGURAÇÃO VISUAL E ESTILO
# ==============================================================================
# [BLOQUEADO] Gerenciado pelo app.py para evitar erro de DuplicateConfig
# st.set_page_config(page_title="Intubação Orotraqueal", page_icon="⚡", layout="wide")

COLOR_PRIMARY = "#0F9D58"
COLOR_BG = "#FFFFFF"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BG}; }}
    h1, h2, h3 {{ color: {COLOR_PRIMARY}; font-family: 'Roboto', sans-serif; }}
    
    /* Aumentar um pouco a fonte da tabela para ficar mais legível */
    .stDataFrame {{ font-size: 1.1rem; }}
    
    /* Remover padding excessivo do topo */
    .block-container {{ padding-top: 2rem; }}
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
st.header("⚡ Intubação Orotraqueal")

# --- CARREGAMENTO HÍBRIDO ---
df_iot = load_data('DB_IOT', 'banco_dados_iot.csv')

if df_iot.empty:
    st.error("Erro: Banco de dados não encontrado.")
    st.stop()

# --- INPUT DE DADOS ---
col_p, col_void = st.columns([1, 3])
with col_p:
    peso = st.number_input("Peso do Paciente (kg)", value=70.0, step=0.5, format="%.1f")

# --- PROCESSAMENTO DA TABELA ---
dados_tabela = []

# Identifica coluna de nome
col_nome = None
possiveis_nomes = ['nome_formatado', 'medicacao', 'apresentacao', 'droga']
for c in possiveis_nomes:
    if c in df_iot.columns:
        col_nome = c
        break

if col_nome:
    for index, row in df_iot.iterrows():
        try:
            nome = row[col_nome]
            
            # Garante float
            conc = float(row.get('conc', 0))
            dose_min = float(row.get('dose_min', 0))
            # Tratamento para coluna habitual/média
            dose_hab = float(row.get('dose_hab', 0)) if 'dose_hab' in row else float(row.get('dose_media', 0))
            dose_max = float(row.get('dose_max', 0))
            
            if conc > 0:
                # Cálculo (Dose * Peso) / Conc
                vol_min = (dose_min * peso) / conc
                vol_hab = (dose_hab * peso) / conc
                vol_max = (dose_max * peso) / conc
                
                # Monta dicionário (já formatado para string com 'ml', mas vamos estilizar depois)
                dados_tabela.append({
                    "Medicação": nome,
                    "Vol. Mínimo": f"{format_br(vol_min)} ml",
                    "Vol. Habitual": f"{format_br(vol_hab)} ml",  # Nome alterado aqui
                    "Vol. Máximo": f"{format_br(vol_max)} ml"
                })
        except Exception:
            continue

    # --- EXIBIÇÃO ---
    if dados_tabela:
        st.markdown("---")
        df_display = pd.DataFrame(dados_tabela)
        
        # --- ESTILIZAÇÃO DA TABELA (Pandas Styler) ---
        # Aqui definimos as cores de texto e pesos de fonte
        def highlight_cols(x):
            df_styler = x.copy()
            # Define Dataframe vazio de estilos
            df_styler.loc[:, :] = '' 
            return df_styler

        # Criação do Styler object
        styler = df_display.style\
            .map(lambda v: 'color: #1565C0; font-weight: bold;', subset=['Vol. Mínimo'])\
            .map(lambda v: 'color: #2E7D32; font-weight: bold;', subset=['Vol. Habitual'])\
            .map(lambda v: 'color: #C62828; font-weight: bold;', subset=['Vol. Máximo'])\
            .map(lambda v: 'font-weight: 600; color: #333;', subset=['Medicação'])

        # Exibe com column_config para ajustar larguras se necessário, mas o styler cuida das cores
        st.dataframe(
            styler, 
            use_container_width=True, 
            hide_index=True,
            height=(len(df_display) + 1) * 35 + 3 # Altura dinâmica baseada nas linhas
        )
    else:
        st.warning("Não foi possível calcular as doses.")

else:
    st.error("Erro de Estrutura: Coluna de nome da medicação não encontrada.")