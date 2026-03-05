import streamlit as st

# Sufixos dos campos lab_{i}_{suf} para deslocamento (Evolução Hoje)
_LAB_SUFIXOS = [
    "data", "hb", "ht", "vcm", "hcm", "rdw", "leuco", "plaq",
    "cr", "ur", "na", "k", "mg", "pi", "cat", "cai",
    "tgp", "tgo", "fal", "ggt", "bt", "bd", "prot_tot", "alb", "amil", "lipas",
    "cpk", "cpk_mb", "bnp", "trop", "pcr", "vhs", "tp", "ttpa",
    "ur_dens", "ur_le", "ur_nit", "ur_leu", "ur_hm", "ur_prot", "ur_cet", "ur_glic",
    # Gasometria 1
    "gas_tipo", "gas_hora",
    "gas_ph", "gas_pco2", "gas_po2", "gas_hco3", "gas_be", "gas_sat",
    "gas_lac", "gas_ag", "gas_cl", "gas_na", "gas_k", "gas_cai",
    "gasv_pco2", "svo2",
    # Gasometria 2
    "gas2_tipo", "gas2_hora",
    "gas2_ph", "gas2_pco2", "gas2_po2", "gas2_hco3", "gas2_be", "gas2_sat",
    "gas2_lac", "gas2_ag", "gas2_cl", "gas2_na", "gas2_k", "gas2_cai",
    "gas2v_pco2", "gas2_svo2",
    # Gasometria 3
    "gas3_tipo", "gas3_hora",
    "gas3_ph", "gas3_pco2", "gas3_po2", "gas3_hco3", "gas3_be", "gas3_sat",
    "gas3_lac", "gas3_ag", "gas3_cl", "gas3_na", "gas3_k", "gas3_cai",
    "gas3v_pco2", "gas3_svo2",
    "outros", "conduta",
]

# Sufixos que armazenam o tipo de gasometria (precisam de tratamento especial no deslocamento)
_GAS_TIPO_SUFIXOS = {"gas_tipo", "gas2_tipo", "gas3_tipo"}


def _deslocar_laboratoriais():
    """
    Desloca os resultados por data: Hoje→vazio, Ontem→Hoje, Anteontem→Ontem, Anteontem→4 dias atrás.
    Slot 4 (Laboratoriais Admissão / Externo) é FIXO — nunca é deslocado.
    """
    def _copiar(orig: int, dest: int):
        for suf in _LAB_SUFIXOS:
            key_orig = f"lab_{orig}_{suf}"
            key_dest = f"lab_{dest}_{suf}"
            val = st.session_state.get(key_orig)
            if suf in _GAS_TIPO_SUFIXOS:
                st.session_state[key_dest] = val if val in (None, "Arterial", "Venosa", "Pareada") else None
            else:
                st.session_state[key_dest] = val if val is not None else ""

    def _limpar(slot: int):
        for suf in _LAB_SUFIXOS:
            key = f"lab_{slot}_{suf}"
            if suf in _GAS_TIPO_SUFIXOS:
                st.session_state[key] = None
            else:
                st.session_state[key] = ""

    # Ordem reversa para não sobrescrever antes de ler
    # 9→10, 8→9, 7→8, 6→7, 5→6 (demais exames)
    for i in range(9, 4, -1):
        _copiar(i, i + 1)
    # 3→5 (anteontem vira 4 dias atrás; pula slot 4)
    _copiar(3, 5)
    # 2→3, 1→2 (ontem→anteontem, hoje→ontem)
    _copiar(2, 3)
    _copiar(1, 2)
    # Slot 1 fica vazio; slot 4 permanece inalterado
    _limpar(1)


# 1. Definição das Variáveis (10 Slots de Data)
def get_campos():
    campos = {'laboratoriais_notas': ''}
    
    for i in range(1, 11):
        campos.update({
            f'lab_{i}_data': '',
            
            # Linha 1: Hemato
            f'lab_{i}_hb': '', f'lab_{i}_ht': '', f'lab_{i}_vcm': '', f'lab_{i}_hcm': '', 
            f'lab_{i}_rdw': '', f'lab_{i}_leuco': '', f'lab_{i}_plaq': '',
            
            # Linha 2: Renal/Eletrolitos
            f'lab_{i}_cr': '', f'lab_{i}_ur': '', f'lab_{i}_na': '', f'lab_{i}_k': '', 
            f'lab_{i}_mg': '', f'lab_{i}_pi': '', f'lab_{i}_cat': '', f'lab_{i}_cai': '',
            
            # Linha 3: Hepático/Panc
            f'lab_{i}_tgp': '', f'lab_{i}_tgo': '', f'lab_{i}_fal': '', f'lab_{i}_ggt': '',
            f'lab_{i}_bt': '', f'lab_{i}_bd': '', f'lab_{i}_prot_tot': '',
            f'lab_{i}_alb': '', f'lab_{i}_amil': '', f'lab_{i}_lipas': '',
            
            # Linha 4: Cardio/Coag/Inflam
            f'lab_{i}_cpk': '', f'lab_{i}_cpk_mb': '', f'lab_{i}_bnp': '',
            f'lab_{i}_trop': '', f'lab_{i}_pcr': '', f'lab_{i}_vhs': '',
            f'lab_{i}_tp': '', f'lab_{i}_ttpa': '',
            
            # Linha 5: Urina
            f'lab_{i}_ur_dens': '', f'lab_{i}_ur_le': '', f'lab_{i}_ur_nit': '', f'lab_{i}_ur_leu': '',
            f'lab_{i}_ur_hm': '', f'lab_{i}_ur_prot': '', f'lab_{i}_ur_cet': '', f'lab_{i}_ur_glic': '',
            
            # Gasometria 1
            f'lab_{i}_gas_tipo': None, f'lab_{i}_gas_hora': '',
            f'lab_{i}_gas_ph': '', f'lab_{i}_gas_pco2': '', f'lab_{i}_gas_po2': '', f'lab_{i}_gas_hco3': '',
            f'lab_{i}_gas_be': '', f'lab_{i}_gas_sat': '', f'lab_{i}_gas_lac': '', f'lab_{i}_gas_ag': '',
            f'lab_{i}_gas_cl': '', f'lab_{i}_gas_na': '', f'lab_{i}_gas_k': '', f'lab_{i}_gas_cai': '',
            f'lab_{i}_gasv_pco2': '', f'lab_{i}_svo2': '',

            # Gasometria 2
            f'lab_{i}_gas2_tipo': None, f'lab_{i}_gas2_hora': '',
            f'lab_{i}_gas2_ph': '', f'lab_{i}_gas2_pco2': '', f'lab_{i}_gas2_po2': '', f'lab_{i}_gas2_hco3': '',
            f'lab_{i}_gas2_be': '', f'lab_{i}_gas2_sat': '', f'lab_{i}_gas2_lac': '', f'lab_{i}_gas2_ag': '',
            f'lab_{i}_gas2_cl': '', f'lab_{i}_gas2_na': '', f'lab_{i}_gas2_k': '', f'lab_{i}_gas2_cai': '',
            f'lab_{i}_gas2v_pco2': '', f'lab_{i}_gas2_svo2': '',

            # Gasometria 3
            f'lab_{i}_gas3_tipo': None, f'lab_{i}_gas3_hora': '',
            f'lab_{i}_gas3_ph': '', f'lab_{i}_gas3_pco2': '', f'lab_{i}_gas3_po2': '', f'lab_{i}_gas3_hco3': '',
            f'lab_{i}_gas3_be': '', f'lab_{i}_gas3_sat': '', f'lab_{i}_gas3_lac': '', f'lab_{i}_gas3_ag': '',
            f'lab_{i}_gas3_cl': '', f'lab_{i}_gas3_na': '', f'lab_{i}_gas3_k': '', f'lab_{i}_gas3_cai': '',
            f'lab_{i}_gas3v_pco2': '', f'lab_{i}_gas3_svo2': '',

            # Linha 8: Outros
            f'lab_{i}_outros': '',
            
            # Linha 9: Conduta Específica desta data
            f'lab_{i}_conduta': ''
        })
    return campos

# Títulos dos slots: 1=Hoje, 2=Ontem, 3=Anteontem, 4=Lab Admissão/Externo, 5+=Anteriores
_SLOT_TITULOS = {
    1: "Hoje",
    2: "Ontem",
    3: "Anteontem",
    4: "Laboratoriais Admissão / Externo",
}


def _render_slot(i):
    titulo = _SLOT_TITULOS.get(i) or f"Resultado Anterior #{i}"
    
    with st.container(border=True):
        # Cabeçalho: Data
        c_tit, c_date = st.columns([2, 1], vertical_alignment="center")
        c_tit.markdown(f"**{titulo}**")
        c_date.text_input(f"Data #{i}", key=f'lab_{i}_data', placeholder="DD/MM/AAAA", label_visibility="collapsed")
        
        # LINHA 1: Hemato
        cols1 = st.columns([1, 1, 1, 1, 1, 2.5, 1.2])
        with cols1[0]: st.text_input("Hb", key=f'lab_{i}_hb')
        with cols1[1]: st.text_input("Ht", key=f'lab_{i}_ht')
        with cols1[2]: st.text_input("VCM", key=f'lab_{i}_vcm')
        with cols1[3]: st.text_input("HCM", key=f'lab_{i}_hcm')
        with cols1[4]: st.text_input("RDW", key=f'lab_{i}_rdw')
        with cols1[5]: st.text_input("Leuco (Dif)", key=f'lab_{i}_leuco', placeholder="Total (Seg/Bast)")
        with cols1[6]: st.text_input("Plaq", key=f'lab_{i}_plaq')
        
        # LINHA 2: Renal
        cols2 = st.columns(8)
        with cols2[0]: st.text_input("Cr", key=f'lab_{i}_cr')
        with cols2[1]: st.text_input("Ur", key=f'lab_{i}_ur')
        with cols2[2]: st.text_input("Na", key=f'lab_{i}_na')
        with cols2[3]: st.text_input("K", key=f'lab_{i}_k')
        with cols2[4]: st.text_input("Mg", key=f'lab_{i}_mg')
        with cols2[5]: st.text_input("Pi", key=f'lab_{i}_pi')
        with cols2[6]: st.text_input("CaT", key=f'lab_{i}_cat')
        with cols2[7]: st.text_input("CaI", key=f'lab_{i}_cai')

        # LINHA 3: Hepático
        cols3 = st.columns(10)
        with cols3[0]: st.text_input("TGP", key=f'lab_{i}_tgp')
        with cols3[1]: st.text_input("TGO", key=f'lab_{i}_tgo')
        with cols3[2]: st.text_input("FAL", key=f'lab_{i}_fal')
        with cols3[3]: st.text_input("GGT", key=f'lab_{i}_ggt')
        with cols3[4]: st.text_input("BT", key=f'lab_{i}_bt')
        with cols3[5]: st.text_input("BD", key=f'lab_{i}_bd')
        with cols3[6]: st.text_input("Prot Tot", key=f'lab_{i}_prot_tot')
        with cols3[7]: st.text_input("Alb", key=f'lab_{i}_alb')
        with cols3[8]: st.text_input("Amil", key=f'lab_{i}_amil')
        with cols3[9]: st.text_input("Lipas", key=f'lab_{i}_lipas')

        # LINHA 4: Cardio/Coag
        cols4 = st.columns(8)
        with cols4[0]: st.text_input("CPK", key=f'lab_{i}_cpk')
        with cols4[1]: st.text_input("CPK-MB", key=f'lab_{i}_cpk_mb')
        with cols4[2]: st.text_input("BNP", key=f'lab_{i}_bnp')
        with cols4[3]: st.text_input("Trop", key=f'lab_{i}_trop')
        with cols4[4]: st.text_input("PCR", key=f'lab_{i}_pcr')
        with cols4[5]: st.text_input("VHS", key=f'lab_{i}_vhs')
        with cols4[6]: st.text_input("TP", key=f'lab_{i}_tp')
        with cols4[7]: st.text_input("TTPa", key=f'lab_{i}_ttpa')

        # LINHA 5: Urina (Sem separador visual, apenas label discreto)
        st.caption("Urina (EAS)")
        u1, u2, u3, u4, u5, u6, u7, u8 = st.columns(8)
        with u1: st.text_input("Dens", key=f'lab_{i}_ur_dens')
        with u2: st.text_input("L.Est", key=f'lab_{i}_ur_le')
        with u3: st.text_input("Nit", key=f'lab_{i}_ur_nit')
        with u4: st.text_input("Leuco", key=f'lab_{i}_ur_leu')
        with u5: st.text_input("Hm", key=f'lab_{i}_ur_hm')
        with u6: st.text_input("Prot", key=f'lab_{i}_ur_prot')
        with u7: st.text_input("Cet", key=f'lab_{i}_ur_cet')
        with u8: st.text_input("Glic", key=f'lab_{i}_ur_glic')

        # GASOMETRIA — expander com até 3 gasometrias
        def _render_gas_block(slot, gn):
            """Renderiza um bloco de gasometria. gn=1 usa prefixo 'gas', gn=2 'gas2', gn=3 'gas3'."""
            p  = "gas" if gn == 1 else f"gas{gn}"
            kv = f"lab_{slot}_{p}v_pco2"
            ks = f"lab_{slot}_svo2"       if gn == 1 else f"lab_{slot}_{p}_svo2"

            _tipo_key = f"lab_{slot}_{p}_tipo"
            if st.session_state.get(_tipo_key) not in (None, "Arterial", "Venosa", "Pareada"):
                st.session_state[_tipo_key] = None

            _c_hora, _c_pills, _c_esp = st.columns([1, 3, 4])
            with _c_hora:
                st.text_input("Hora", key=f"lab_{slot}_{p}_hora", placeholder="16h", label_visibility="collapsed")
            with _c_pills:
                st.pills(f"Gaso {gn} #{slot}", ["Arterial", "Venosa", "Pareada"], key=_tipo_key, label_visibility="collapsed")

            ga = st.columns(6)
            with ga[0]: st.text_input("pH",    key=f"lab_{slot}_{p}_ph")
            with ga[1]: st.text_input("pCO2",  key=f"lab_{slot}_{p}_pco2")
            with ga[2]: st.text_input("pO2",   key=f"lab_{slot}_{p}_po2")
            with ga[3]: st.text_input("HCO3",  key=f"lab_{slot}_{p}_hco3")
            with ga[4]: st.text_input("BE",    key=f"lab_{slot}_{p}_be")
            with ga[5]: st.text_input("SatO2", key=f"lab_{slot}_{p}_sat")

            gb = st.columns(6)
            with gb[0]: st.text_input("Lac",  key=f"lab_{slot}_{p}_lac")
            with gb[1]: st.text_input("AG",   key=f"lab_{slot}_{p}_ag")
            with gb[2]: st.text_input("Cl",   key=f"lab_{slot}_{p}_cl")
            with gb[3]: st.text_input("Na",   key=f"lab_{slot}_{p}_na")
            with gb[4]: st.text_input("K",    key=f"lab_{slot}_{p}_k")
            with gb[5]: st.text_input("Cai",  key=f"lab_{slot}_{p}_cai")

            gc1, gc2, gc3 = st.columns([1, 1, 4])
            with gc1: st.text_input("pCO2(v)", key=kv)
            with gc2: st.text_input("SvO2",    key=ks)

        st.caption("Gasometria")
        _render_gas_block(i, 1)

        with st.expander("+ Gasometrias anteriores", expanded=False):
            _render_gas_block(i, 2)
            st.divider()
            _render_gas_block(i, 3)

        # LINHA 8: Outros
        st.text_input(
            "Outros", 
            key=f'lab_{i}_outros', 
            placeholder="Ex: Culturas parciais, Níveis séricos, etc."
        )

        # LINHA 9: Conduta (EM LINHA, dentro do bloco)
        st.text_input(
                "Conduta Laboratorial",
                key=f"lab_{i}_conduta",
                label_visibility="collapsed",
                placeholder="Escreva a conduta aqui..."
            )

# 2. Renderização Principal
def render(_agent_btn_callback=None):
    st.markdown('<span id="sec-10"></span>', unsafe_allow_html=True)
    st.markdown("##### 10. Exames Laboratoriais")

    st.text_area("Notas", key="laboratoriais_notas", height="content", placeholder="Cole neste campo a evolução...", label_visibility="collapsed")
    st.write("")

    # Botões: Evolução Hoje | Parsing Exames | Completar Campos | Extrair Exames | Comparar
    _bcol1, _bcol2, _bcol3, _bcol4, _bcol5 = st.columns([1, 1, 1, 1, 1])
    with _bcol1:
        evo_clicked = st.form_submit_button(
            "Evolução Hoje",
            key="btn_evolucao_hoje_lab",
            use_container_width=True,
            help="Último Resultado vira Anterior #2, Anterior #2 vira #3, etc. Slot 1 fica vazio para novos exames.",
        )
        if evo_clicked:
            _deslocar_laboratoriais()
            st.toast("✅ Resultados deslocados. Último → Anterior #2, etc. Slot 1 pronto para preenchimento.", icon="✅")
    with _bcol2:
        if st.form_submit_button(
            "Parsing Exames",
            key="_fsbtn_lab_deterministico",
            use_container_width=True,
            help="Preenche deterministicamente (DD/MM – Hb x | Ht x | ...). Não perde dados já preenchidos.",
        ):
            st.session_state["_lab_deterministico_pendente"] = True
    with _bcol3:
        if _agent_btn_callback:
            _agent_btn_callback()
    with _bcol4:
        if st.form_submit_button(
            "Extrair Exames",
            key="_fsbtn_extrair_lab",
            use_container_width=True,
            help="Formata os exames com IA (PACER) e aplica o agente automaticamente",
        ):
            st.session_state["_lab_extrair_pendente"] = True
    with _bcol5:
        if st.form_submit_button(
            "Comparar",
            key="_fsbtn_comparar_lab",
            use_container_width=True,
            help="Abre tabela comparativa com todos os campos (hemato, bioquímica, gasometria, urina)",
        ):
            st.session_state["_comparar_lab_pendente"] = True

    # --- 4 Slots VISÍVEIS (Hoje, Ontem, Anteontem, Lab Externos) ---
    for i in range(1, 5):
        _render_slot(i)
        st.write("")
    
    # --- Demais exames (fechado por padrão) ---
    with st.expander("Demais exames", expanded=False):
        for i in range(5, 11):
            _render_slot(i)
            st.write("")