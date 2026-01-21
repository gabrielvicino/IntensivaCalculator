import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Link da sua planilha
SHEET_URL = "https://docs.google.com/spreadsheets/d/15Rxc1tYYmgG7Sikn2UOvz-GFN6jvneMHnA-l-O8keNs/edit?gid=0#gid=0"

def load_data(worksheet_name, csv_fallback=None):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # ttl=0 obriga a ler os dados novos AGORA, ignorando o cache antigo
        df = conn.read(spreadsheet=SHEET_URL, worksheet=worksheet_name, ttl=0)
        return df
    except Exception as e:
        return pd.DataFrame()

def save_data_append(worksheet_name, new_data_row):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Lê a planilha REAL agora (sem cache)
        existing_data = conn.read(spreadsheet=SHEET_URL, worksheet=worksheet_name, ttl=0)
        
        # --- DIAGNÓSTICO DE ERRO (Para sabermos o que acontece) ---
        qtd_planilha = len(existing_data.columns)
        qtd_codigo = len(new_data_row)
        
        # Se os números não baterem, ele vai te contar exatamente o porquê
        if qtd_codigo != qtd_planilha:
            st.error(f"❌ ERRO DE CONTAGEM: O código está enviando {qtd_codigo} dados, mas o Python achou {qtd_planilha} colunas na planilha.")
            st.error("Motivo provável: O cache do Streamlit está lendo a versão antiga da planilha.")
            return False
            
        # Se passou no teste, salva
        new_df = pd.DataFrame([new_data_row], columns=existing_data.columns)
        updated_df = pd.concat([existing_data, new_df], ignore_index=True)
        conn.update(spreadsheet=SHEET_URL, worksheet=worksheet_name, data=updated_df)
        return True
        
    except Exception as e:
        st.error(f"Erro detalhado do Google: {e}")
        return False