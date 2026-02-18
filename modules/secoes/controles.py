import streamlit as st

# Parâmetros: (chave, label, tem_min_max)
_PARAMS = [
    ("pas",     "Pressão Arterial Sistólica (mmHg)",   True),
    ("pad",     "Pressão Arterial Diastólica (mmHg)",  True),
    ("pam",     "Pressão Arterial Média (mmHg)",       True),
    ("fc",      "Frequência Cardíaca (bpm)",           True),
    ("fr",      "Frequência Respiratória (irpm)",      True),
    ("sato2",   "Saturação de O₂ (%)",                 True),
    ("temp",    "Temperatura (°C)",                    True),
    ("glic",    "Glicemia (mg/dL)",                    True),
    ("diurese", "Diurese",                             False),
    ("balanco", "Balanço Hídrico",                     False),
]

_DIAS = ["anteontem", "ontem", "hoje"]

# Cabeçalho: cada dia ocupa uma coluna de largura 2 (= min 1 + max 1)
_COLS_HEADER = [2.2, 0.08, 2, 0.08, 2, 0.08, 2]
# Dados: cada dia ocupa duas colunas de largura 1
_COLS_DATA   = [2.2, 0.08, 1, 1, 0.08, 1, 1, 0.08, 1, 1]


def get_campos():
    campos = {"controles_notas": ""}
    for dia in _DIAS:
        campos[f"ctrl_{dia}_data"] = ""
        for chave, _, min_max in _PARAMS:
            if min_max:
                campos[f"ctrl_{dia}_{chave}_min"] = ""
                campos[f"ctrl_{dia}_{chave}_max"] = ""
            else:
                campos[f"ctrl_{dia}_{chave}"] = ""
    return campos


def render():
    st.markdown("##### 11. Controles & Balanço Hídrico")

    # Campo notas para extração da IA
    st.text_area(
        "controles_notas",
        key="controles_notas",
        height=None,
        placeholder="Cole neste campo os controles do prontuário...",
        label_visibility="collapsed",
    )

    st.markdown("""
    <style>
        input[id*="ctrl_anteontem_data"],
        input[id*="ctrl_ontem_data"],
        input[id*="ctrl_hoje_data"] {
            text-align: center;
        }
        input[id*="ctrl_anteontem_data"]::placeholder,
        input[id*="ctrl_ontem_data"]::placeholder,
        input[id*="ctrl_hoje_data"]::placeholder {
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):

        # ── Cabeçalho: dia + data (largura = min + max combinados) ────────────
        h = st.columns(_COLS_HEADER)
        # h[0]=label, h[1]=sep, h[2]=anteontem, h[3]=sep, h[4]=ontem, h[5]=sep, h[6]=hoje
        for col_idx, dia in zip([2, 4, 6], _DIAS):
            with h[col_idx]:
                st.markdown(f"**{dia.capitalize()}**")
                st.text_input(f"data_{dia}", key=f"ctrl_{dia}_data",
                              placeholder="dd/mm/aaaa", label_visibility="collapsed")

        # ── Linhas de parâmetros ──────────────────────────────────────────────
        for chave, label, min_max in _PARAMS:
            r = st.columns(_COLS_DATA)
            # r[0]=label, r[1]=sep, r[2]=ant_min, r[3]=ant_max,
            # r[4]=sep, r[5]=ont_min, r[6]=ont_max, r[7]=sep, r[8]=hj_min, r[9]=hj_max

            with r[0]:
                st.markdown(f"**{label}**")

            if min_max:
                with r[2]:
                    st.text_input(f"ant_{chave}_min", key=f"ctrl_anteontem_{chave}_min",
                                  placeholder="Mín", label_visibility="collapsed")
                with r[3]:
                    st.text_input(f"ant_{chave}_max", key=f"ctrl_anteontem_{chave}_max",
                                  placeholder="Máx", label_visibility="collapsed")
                with r[5]:
                    st.text_input(f"ont_{chave}_min", key=f"ctrl_ontem_{chave}_min",
                                  placeholder="Mín", label_visibility="collapsed")
                with r[6]:
                    st.text_input(f"ont_{chave}_max", key=f"ctrl_ontem_{chave}_max",
                                  placeholder="Máx", label_visibility="collapsed")
                with r[8]:
                    st.text_input(f"hj_{chave}_min", key=f"ctrl_hoje_{chave}_min",
                                  placeholder="Mín", label_visibility="collapsed")
                with r[9]:
                    st.text_input(f"hj_{chave}_max", key=f"ctrl_hoje_{chave}_max",
                                  placeholder="Máx", label_visibility="collapsed")
            else:
                with r[2]:
                    st.text_input(f"ant_{chave}", key=f"ctrl_anteontem_{chave}",
                                  placeholder="Valor", label_visibility="collapsed")
                with r[5]:
                    st.text_input(f"ont_{chave}", key=f"ctrl_ontem_{chave}",
                                  placeholder="Valor", label_visibility="collapsed")
                with r[8]:
                    st.text_input(f"hj_{chave}", key=f"ctrl_hoje_{chave}",
                                  placeholder="Valor", label_visibility="collapsed")
