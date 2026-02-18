import streamlit as st

def get_campos():
    campos = {}
    
    # Lista de prefixos para facilitar a criação
    sistemas = [
        'neuro', 'resp', 'cardio', 'renal', 'metab', 
        'infec', 'gastro', 'nutri', 'hemato', 'pele'
    ]
    
    # Campo livre abaixo do título
    campos['sistemas_notas'] = ''
    
    # Cria campos genéricos para Obs e Conduta de cada sistema
    for s in sistemas:
        campos[f'sis_{s}_obs'] = ''
        campos[f'sis_{s}_conduta'] = ''

    # --- CAMPOS ESPECÍFICOS ---
    
    # 1. Neuro
    campos.update({
        'sis_neuro_ecg': 15,      # GCS 3-15
        'sis_neuro_ecg_p': 15,    # ECG-P 1-15
        'sis_neuro_rass': 0,      # RASS -5 a +5
        'sis_neuro_delirium': None,
        'sis_neuro_cam_icu': None,
        'sis_neuro_pupilas_tam': None,
        'sis_neuro_pupilas_simetria': None,
        'sis_neuro_pupilas_foto': None,
        'sis_neuro_analgesico_adequado': None,
        'sis_neuro_deficits_focais': '',
        'sis_neuro_analgesia_1_tipo': None,
        'sis_neuro_analgesia_1_drogas': '',
        'sis_neuro_analgesia_1_dose': '',
        'sis_neuro_analgesia_1_freq': '',
        'sis_neuro_analgesia_2_tipo': None,
        'sis_neuro_analgesia_2_drogas': '',
        'sis_neuro_analgesia_2_dose': '',
        'sis_neuro_analgesia_2_freq': '',
        'sis_neuro_analgesia_3_tipo': None,
        'sis_neuro_analgesia_3_drogas': '',
        'sis_neuro_analgesia_3_dose': '',
        'sis_neuro_analgesia_3_freq': '',
        'sis_neuro_sedacao_1_drogas': '',
        'sis_neuro_sedacao_1_dose': '',
        'sis_neuro_sedacao_1_meta': '',
        'sis_neuro_sedacao_2_drogas': '',
        'sis_neuro_sedacao_2_dose': '',
        'sis_neuro_sedacao_2_meta': '',
        'sis_neuro_sedacao_3_drogas': '',
        'sis_neuro_sedacao_3_dose': '',
        'sis_neuro_sedacao_3_meta': '',
        'sis_neuro_bloqueador_dose': '',
        'sis_neuro_vigilancia': ''
    })

    # 2. Respiratório
    campos.update({
        'sis_resp_ausculta': '',
        'sis_resp_modo': None,
        'sis_resp_pressao': '',
        'sis_resp_volume': '',
        'sis_resp_fio2': '',
        'sis_resp_peep': '',
        'sis_resp_freq': '',
        'sis_resp_vent_protetora': None,
        'sis_resp_sincronico': None,
        'sis_resp_assincronia': '',
        'sis_resp_complacencia': '',
        'sis_resp_resistencia': '',
        'sis_resp_dp': '',
        'sis_resp_plato': '',
        'sis_resp_pico': '',
        'sis_resp_disturbio_resp': None,
        'sis_resp_dreno_1': '',
        'sis_resp_dreno_1_debito': '',
        'sis_resp_dreno_2': '',
        'sis_resp_dreno_2_debito': '',
        'sis_resp_dreno_3': '',
        'sis_resp_dreno_3_debito': '',
    })

    # 3. Cardio
    campos.update({
        'sis_cardio_fc': '',
        'sis_cardio_cardioscopia': '',
        'sis_cardio_pam': '',
        'sis_cardio_perfusao': None,
        'sis_cardio_fluido_responsivo': None,
        'sis_cardio_fluido_tolerante': None,
        'sis_cardio_dva_1_med': '',
        'sis_cardio_dva_1_dose': '',
        'sis_cardio_dva_2_med': '',
        'sis_cardio_dva_2_dose': '',
        'sis_cardio_dva_3_med': '',
        'sis_cardio_dva_3_dose': '',
        'sis_cardio_dva_4_med': '',
        'sis_cardio_dva_4_dose': '',
    })

    # 4. Renal
    campos.update({
        'sis_renal_diurese': '',
        'sis_renal_balanco': '',
        'sis_renal_balanco_acum': '',
        'sis_renal_volemia': None,
        'sis_renal_cr_hoje': '',
        'sis_renal_ur_hoje': '',
        'sis_renal_cr_ontem': '',
        'sis_renal_ur_ontem': '',
        'sis_renal_sodio': None,
        'sis_renal_potassio': None,
        'sis_renal_magnesio': None,
        'sis_renal_fosforo': None,
        'sis_renal_calcio': None,
        'sis_renal_trs': None,
        'sis_renal_trs_via': '',
        'sis_renal_trs_ultima': '',
        'sis_renal_trs_proxima': '',
    })

    # 5. Infeccioso
    campos.update({
        'sis_infec_febre': None,
        'sis_infec_febre_vezes': '',
        'sis_infec_febre_ultima': '',
        'sis_infec_atb': None,
        'sis_infec_atb_1': '',
        'sis_infec_atb_2': '',
        'sis_infec_atb_3': '',
        'sis_infec_atb_guiado': None,
        'sis_infec_culturas_and': None,
        'sis_infec_cult_1_sitio': '',
        'sis_infec_cult_1_data': '',
        'sis_infec_cult_2_sitio': '',
        'sis_infec_cult_2_data': '',
        'sis_infec_cult_3_sitio': '',
        'sis_infec_cult_3_data': '',
        'sis_infec_cult_4_sitio': '',
        'sis_infec_cult_4_data': '',
        'sis_infec_pcr_hoje': '',
        'sis_infec_pcr_ult': '',
        'sis_infec_pcr_antepen': '',
        'sis_infec_pct': '',
        'sis_infec_isolamento': None,
        'sis_infec_isolamento_tipo': '',
        'sis_infec_isolamento_motivo': '',
        'sis_infec_patogenos': '',
    })

    # 7. Gastro
    campos.update({
        'sis_gastro_exame_fisico': '',
        'sis_gastro_dieta_oral': '',
        'sis_gastro_dieta_enteral': '',
        'sis_gastro_dieta_enteral_vol': '',
        'sis_gastro_dieta_parenteral': '',
        'sis_gastro_dieta_parenteral_vol': '',
        'sis_gastro_meta_calorica': '',
        'sis_gastro_na_meta': None,
        'sis_gastro_ingestao_quanto': '',
        'sis_gastro_escape_glicemico': None,
        'sis_gastro_escape_vezes': '',
        'sis_gastro_escape_manha': False,
        'sis_gastro_escape_tarde': False,
        'sis_gastro_escape_noite': False,
        'sis_gastro_insulino': None,
        'sis_gastro_insulino_dose': '',
        'sis_gastro_evacuacao': None,
        'sis_gastro_evacuacao_data': '',
        'sis_gastro_laxativo': '',
    })

    # 8. Hemato
    campos.update({
        'sis_hemato_anticoag': None,
        'sis_hemato_anticoag_motivo': '',
        'sis_hemato_anticoag_tipo': None,
        'sis_hemato_sangramento': None,
        'sis_hemato_sangramento_via': '',
        'sis_hemato_sangramento_data': '',
        'sis_hemato_transf_data': '',
        'sis_hemato_transf_1_comp': '',
        'sis_hemato_transf_1_bolsas': '',
        'sis_hemato_transf_2_comp': '',
        'sis_hemato_transf_2_bolsas': '',
        'sis_hemato_transf_3_comp': '',
        'sis_hemato_transf_3_bolsas': '',
        'sis_hemato_hb_hoje': '',
        'sis_hemato_hb_ult': '',
        'sis_hemato_plaq_hoje': '',
        'sis_hemato_plaq_ult': '',
    })

    # 10. Músculo-Esquelético / Pele
    campos.update({
        'sis_pele_lpp': None,
        'sis_pele_lpp_local_1': '',
        'sis_pele_lpp_grau_1': '',
        'sis_pele_lpp_local_2': '',
        'sis_pele_lpp_grau_2': '',
        'sis_pele_lpp_local_3': '',
        'sis_pele_lpp_grau_3': '',
        'sis_pele_polineuropatia': None,
    })

    return campos

# --- FUNÇÃO DE RENDERIZAÇÃO ---
def render():
    st.markdown("##### 13. Evolução Detalhada por Sistemas")
    
    st.text_area("Notas", key="sistemas_notas", height="content", placeholder="Cole neste campo a evolução...", label_visibility="collapsed")
    st.write("")
    
    # NEUROLÓGICO
    with st.container(border=True):
        st.markdown("**Neurológico**")
        
        # Linha 1: ECG (GCS 3-15), ECG-P (1-15), RASS - títulos acima dos campos
        ecg_col, ecgp_col, rass_col = st.columns(3)
        with ecg_col:
            st.markdown("**ECG (Escala de Coma de Glasgow 3-15)**")
            st.number_input("ECG", key="sis_neuro_ecg", min_value=3, max_value=15, label_visibility="collapsed")
        with ecgp_col:
            st.markdown("**ECG-P (1-15)**")
            st.number_input("ECG-P", key="sis_neuro_ecg_p", min_value=1, max_value=15, label_visibility="collapsed")
        with rass_col:
            st.markdown("**RASS (-5 a +5)**")
            st.number_input("RASS", key="sis_neuro_rass", min_value=-5, max_value=5, label_visibility="collapsed")
        
        # Linha 2: Delirium e CAM-ICU lado a lado
        d1, d2 = st.columns(2)
        with d1:
            st.markdown("**Delirium**")
            st.radio("Delirium", ["Sim", "Não"], key="sis_neuro_delirium", horizontal=True, index=None, label_visibility="collapsed")
        with d2:
            st.markdown("**CAM-ICU**")
            st.radio("CAM-ICU", ["Positivo", "Negativo"], key="sis_neuro_cam_icu", horizontal=True, index=None, label_visibility="collapsed")
        
        # Linha 3: Pupilas, Simetria e Fotoreatividade lado a lado
        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown("**Pupilas**")
            st.radio("Pupilas", ["Miótica", "Normal", "Midríase"], key="sis_neuro_pupilas_tam", horizontal=True, index=None, label_visibility="collapsed")
        with p2:
            st.markdown("**Simetria**")
            st.radio("Simetria", ["Simétricas", "Anisocoria"], key="sis_neuro_pupilas_simetria", horizontal=True, index=None, label_visibility="collapsed")
        with p3:
            st.markdown("**Fotoreatividade**")
            st.radio("Fotoreatividade", ["Fotoreagente", "Não fotoreagente"], key="sis_neuro_pupilas_foto", horizontal=True, index=None, label_visibility="collapsed")
        
        # Linha 4: Déficits focais (acima), Controle analgésico adequado (abaixo)
        st.markdown("**Déficits focais**")
        st.text_input("Déficits focais", key="sis_neuro_deficits_focais", placeholder="Ex: Hemiparesia D, afasia...", label_visibility="collapsed")
        st.markdown("**Controle analgésico adequado**")
        st.radio("Analgésico", ["Sim", "Não"], key="sis_neuro_analgesico_adequado", horizontal=True, index=None, label_visibility="collapsed")
        
        # Linha 5: Analgesia - 3 conjuntos (Fixa/Se necessário + Drogas, Dose, Frequência)
        st.markdown("**Analgesia**")
        for i in range(1, 4):
            an_tipo, an1, an2, an3 = st.columns([1, 1, 1, 1])
            with an_tipo:
                st.radio("Fixa / Se necessário", ["Fixa", "Se necessário"], key=f"sis_neuro_analgesia_{i}_tipo", horizontal=True, index=None, label_visibility="collapsed")
            with an1:
                st.text_input("Drogas", key=f"sis_neuro_analgesia_{i}_drogas", placeholder="Drogas", label_visibility="collapsed")
            with an2:
                st.text_input("Dose", key=f"sis_neuro_analgesia_{i}_dose", placeholder="Dose", label_visibility="collapsed")
            with an3:
                st.text_input("Frequência", key=f"sis_neuro_analgesia_{i}_freq", placeholder="Frequência", label_visibility="collapsed")
        
        # Linha 6: Sedação - 3 conjuntos (Drogas, Dose, Meta)
        st.markdown("**Sedação**")
        for i in range(1, 4):
            s1, s2, s3 = st.columns(3)
            with s1:
                st.text_input("Drogas", key=f"sis_neuro_sedacao_{i}_drogas", placeholder="Drogas", label_visibility="collapsed")
            with s2:
                st.text_input("Dose", key=f"sis_neuro_sedacao_{i}_dose", placeholder="Dose", label_visibility="collapsed")
            with s3:
                st.text_input("Meta", key=f"sis_neuro_sedacao_{i}_meta", placeholder="Meta", label_visibility="collapsed")
        
        # Bloqueador neuromuscular
        st.markdown("**Bloqueador neuromuscular**")
        st.text_input("Dose", key="sis_neuro_bloqueador_dose", placeholder="Ex: Cisatracúrio 0.1 mg/kg/h", label_visibility="collapsed")
        
        # Demais neurologia
        st.markdown("**Demais neurologia**")
        st.text_input("Demais neurologia", key="sis_neuro_obs", placeholder="Outros achados...", label_visibility="collapsed")
        
        # Vigilância
        st.markdown("**Vigilância**")
        st.text_input("Vigilância", key="sis_neuro_vigilancia", placeholder="Ex: AVC prévio / Risco de abstinência", label_visibility="collapsed")
        
        # Conduta (por último)
        with st.success("Condutas neurológicas"):
            st.text_input("Conduta", key="sis_neuro_conduta", placeholder="Ex: Desligar sedação, TC crânio...", label_visibility="collapsed")

    # RESPIRATÓRIO
    with st.container(border=True):
        st.markdown("**Respiratório**")
        
        # Ausculta
        st.markdown("**Ausculta**")
        st.text_input("Ausculta", key="sis_resp_ausculta", placeholder="Ex: MV+ bilateral, sem sibilos...", label_visibility="collapsed")
        
        # Modo ventilatório
        st.markdown("**Modo ventilatório**")
        st.radio("Modo", ["Ar Ambiente", "Oxigenoterapia", "VNI", "Cateter de Alto Fluxo", "Ventilação Mecânica"], key="sis_resp_modo", horizontal=True, index=None, label_visibility="collapsed")
        
        # Parâmetros
        st.markdown("**Parâmetros**")
        p1, p2, p3, p4, p5 = st.columns(5)
        with p1:
            st.text_input("Pressão", key="sis_resp_pressao", placeholder="Pressão", label_visibility="collapsed")
        with p2:
            st.text_input("Volume", key="sis_resp_volume", placeholder="Volume", label_visibility="collapsed")
        with p3:
            st.text_input("FiO2", key="sis_resp_fio2", placeholder="FiO2", label_visibility="collapsed")
        with p4:
            st.text_input("PEEP", key="sis_resp_peep", placeholder="PEEP", label_visibility="collapsed")
        with p5:
            st.text_input("Frequência Respiratória", key="sis_resp_freq", placeholder="Frequência Respiratória", label_visibility="collapsed")
        
        # Ventilação protetora, Sincrônico, Assincronia (no lugar de desmame)
        v1, v2, v3 = st.columns(3)
        with v1:
            st.markdown("**Ventilação protetora**")
            st.radio("Vent protetora", ["Sim", "Não"], key="sis_resp_vent_protetora", horizontal=True, index=None, label_visibility="collapsed")
        with v2:
            st.markdown("**Sincrônico**")
            st.radio("Sincrônico", ["Sim", "Não"], key="sis_resp_sincronico", horizontal=True, index=None, label_visibility="collapsed")
        with v3:
            st.markdown("**Assincronia**")
            st.text_input("Assincronia", key="sis_resp_assincronia", placeholder="Ex: Double trigger, esforço ineficaz...", label_visibility="collapsed")
        
        # Mecânica respiratória
        st.markdown("**Mecânica respiratória**")
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.text_input("Complacência", key="sis_resp_complacencia", placeholder="Complacência", label_visibility="collapsed")
        with m2:
            st.text_input("Resistência", key="sis_resp_resistencia", placeholder="Resistência", label_visibility="collapsed")
        with m3:
            st.text_input("Driving Pressure", key="sis_resp_dp", placeholder="Driving Pressure", label_visibility="collapsed")
        with m4:
            st.text_input("Pressão de Platô", key="sis_resp_plato", placeholder="Pressão de Platô", label_visibility="collapsed")
        with m5:
            st.text_input("Pressão de Pico", key="sis_resp_pico", placeholder="Pressão de Pico", label_visibility="collapsed")
        
        # Distúrbio respiratório (sim/não)
        st.markdown("**Distúrbio respiratório**")
        st.radio("Distúrbio resp", ["Sim", "Não"], key="sis_resp_disturbio_resp", horizontal=True, index=None, label_visibility="collapsed")
        
        # Drenos: 3 pares (campo + débito)
        st.markdown("**Drenos**")
        for i in range(1, 4):
            d1, d2 = st.columns([2, 1])
            with d1:
                st.text_input(f"Dreno {i}", key=f"sis_resp_dreno_{i}", placeholder="Ex: Pleural D, mediastinal...", label_visibility="collapsed")
            with d2:
                st.text_input(f"Débito {i}", key=f"sis_resp_dreno_{i}_debito", placeholder="mL/dia", label_visibility="collapsed")
        
        # Demais respiratório
        st.markdown("**Demais respiratório**")
        st.text_input("Demais respiratório", key="sis_resp_obs", placeholder="Outros achados...", label_visibility="collapsed")

        # Conduta
        with st.success("Condutas respiratórias"):
            st.text_input("Conduta", key="sis_resp_conduta", placeholder="Ex: TRE amanhã, Aspirar SN...", label_visibility="collapsed")

    # CARDIOVASCULAR
    with st.container(border=True):
        st.markdown("**Cardiovascular**")

        # Frequência, Cardioscopia, PAM
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown("**Frequência**")
            st.text_input("FC", key="sis_cardio_fc", placeholder="Frequência", label_visibility="collapsed")
        with r2:
            st.markdown("**Cardioscopia**")
            st.text_input("Cardioscopia", key="sis_cardio_cardioscopia", placeholder="Sinusal, Fibrilação Atrial...", label_visibility="collapsed")
        with r3:
            st.markdown("**PAM**")
            st.text_input("PAM", key="sis_cardio_pam", placeholder="PAM", label_visibility="collapsed")

        # Perfusão periférica
        st.markdown("**Perfusão periférica**")
        st.radio("Perfusão", ["Normal", "Lentificada", "Flush", "Tempo de enchimento capilar"], key="sis_cardio_perfusao", horizontal=True, index=None, label_visibility="collapsed")

        # Fluido responsivo / Fluido tolerante
        f1, f2 = st.columns(2)
        with f1:
            st.markdown("**Fluido responsivo**")
            st.radio("Fluido responsivo", ["Sim", "Não"], key="sis_cardio_fluido_responsivo", horizontal=True, index=None, label_visibility="collapsed")
        with f2:
            st.markdown("**Fluido tolerante**")
            st.radio("Fluido tolerante", ["Sim", "Não"], key="sis_cardio_fluido_tolerante", horizontal=True, index=None, label_visibility="collapsed")

        # Drogas Vasoativas: 4 pares Medicamento / Dose
        st.markdown("**Drogas Vasoativas**")
        for i in range(1, 5):
            d1, d2 = st.columns(2)
            with d1:
                st.text_input(f"Medicamento {i}", key=f"sis_cardio_dva_{i}_med", placeholder="Medicamento", label_visibility="collapsed")
            with d2:
                st.text_input(f"Dose {i}", key=f"sis_cardio_dva_{i}_dose", placeholder="Dose", label_visibility="collapsed")

        # Demais cardio e Conduta
        st.markdown("**Demais cardiovascular**")
        st.text_input("Demais cardiovascular", key="sis_cardio_obs", placeholder="Outros achados...", label_visibility="collapsed")
        with st.success("Condutas cardiovasculares"):
            st.text_input("Conduta", key="sis_cardio_conduta", placeholder="Ex: Desmame de DVA, EcoTT...", label_visibility="collapsed")

    # GASTROINTESTINAL
    with st.container(border=True):
        st.markdown("**Trato Gastrointestinal**")

        # Exame Físico
        st.markdown("**Exame Físico**")
        st.text_input("Exame Físico", key="sis_gastro_exame_fisico", placeholder="Ruído Hidroaéreo, palpação...", label_visibility="collapsed")

        # Dieta
        st.markdown("**Dieta**")
        d1, d2, d3, d4, d5, d6 = st.columns(6)
        with d1:
            st.text_input("Oral", key="sis_gastro_dieta_oral", placeholder="Oral", label_visibility="collapsed")
        with d2:
            st.text_input("Enteral", key="sis_gastro_dieta_enteral", placeholder="Enteral", label_visibility="collapsed")
        with d3:
            st.text_input("Volume enteral", key="sis_gastro_dieta_enteral_vol", placeholder="Volume enteral", label_visibility="collapsed")
        with d4:
            st.text_input("Parenteral", key="sis_gastro_dieta_parenteral", placeholder="Parenteral", label_visibility="collapsed")
        with d5:
            st.text_input("Volume parenteral", key="sis_gastro_dieta_parenteral_vol", placeholder="Volume parenteral", label_visibility="collapsed")
        with d6:
            st.text_input("Meta Calórica", key="sis_gastro_meta_calorica", placeholder="Meta Calórica", label_visibility="collapsed")

        m1, m2 = st.columns([1, 2])
        with m1:
            st.markdown("**Ingestão na Meta**")
            st.radio("Na meta", ["Sim", "Não"], key="sis_gastro_na_meta", horizontal=True, index=None, label_visibility="collapsed")
        with m2:
            st.markdown("**Quanto**")
            st.text_input("Quanto", key="sis_gastro_ingestao_quanto", placeholder="Ex: 1200 kcal", label_visibility="collapsed")

        # Glicemia
        st.markdown("**Escape glicêmico**")
        g1, g2, g3, g4, g5, g6, g7 = st.columns([2, 1, 1, 1, 1, 2, 1])
        with g1:
            st.radio("Escape", ["Sim", "Não"], key="sis_gastro_escape_glicemico", horizontal=True, index=None, label_visibility="collapsed")
        with g2:
            st.text_input("Nº de vezes", key="sis_gastro_escape_vezes", placeholder="Nº vezes", label_visibility="collapsed")
        with g3:
            st.checkbox("Manhã", key="sis_gastro_escape_manha")
        with g4:
            st.checkbox("Tarde", key="sis_gastro_escape_tarde")
        with g5:
            st.checkbox("Noite", key="sis_gastro_escape_noite")
        with g6:
            st.markdown("**Insulinoterapia**")
            st.radio("Insulino", ["Sim", "Não"], key="sis_gastro_insulino", horizontal=True, index=None, label_visibility="collapsed")
        with g7:
            st.markdown("**Dose**")
            st.text_input("Dose insulina", key="sis_gastro_insulino_dose", placeholder="Dose", label_visibility="collapsed")

        # Evacuação
        st.markdown("**Evacuação**")
        e1, e2, e3 = st.columns(3)
        with e1:
            st.radio("Evacuação", ["Sim", "Não"], key="sis_gastro_evacuacao", horizontal=True, index=None, label_visibility="collapsed")
        with e2:
            st.text_input("Última evacuação", key="sis_gastro_evacuacao_data", placeholder="Data da última", label_visibility="collapsed")
        with e3:
            st.text_input("Laxativo", key="sis_gastro_laxativo", placeholder="Laxativo", label_visibility="collapsed")

        # Demais gastro e Conduta
        st.markdown("**Demais gastrointestinal**")
        st.text_input("Demais gastrointestinal", key="sis_gastro_obs", placeholder="Outros achados...", label_visibility="collapsed")
        with st.success("Condutas gastrointestinais"):
            st.text_input("Conduta", key="sis_gastro_conduta", placeholder="Ex: Procinético, Laxante...", label_visibility="collapsed")

    # RENAL
    with st.container(border=True):
        st.markdown("**Renal**")

        # Diurese, Balanço, Balanço Acumulado
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown("**Diurese**")
            st.text_input("Diurese", key="sis_renal_diurese", placeholder="Diurese", label_visibility="collapsed")
        with r2:
            st.markdown("**Balanço Hídrico**")
            st.text_input("Balanço", key="sis_renal_balanco", placeholder="Balanço Hídrico", label_visibility="collapsed")
        with r3:
            st.markdown("**Balanço Acumulado**")
            st.text_input("Balanço Acumulado", key="sis_renal_balanco_acum", placeholder="Balanço Acumulado", label_visibility="collapsed")

        # Volemia
        st.markdown("**Volemia**")
        st.radio("Volemia", ["Hipovolêmico", "Euvolêmico", "Hipervolêmico"], key="sis_renal_volemia", horizontal=True, index=None, label_visibility="collapsed")

        # Creatinina e Ureia
        st.markdown("**Função Renal**")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            st.text_input("Creatinina hoje", key="sis_renal_cr_hoje", placeholder="Creatinina hoje", label_visibility="collapsed")
        with f2:
            st.text_input("Ureia hoje", key="sis_renal_ur_hoje", placeholder="Ureia hoje", label_visibility="collapsed")
        with f3:
            st.text_input("Creatinina ontem", key="sis_renal_cr_ontem", placeholder="Creatinina ontem", label_visibility="collapsed")
        with f4:
            st.text_input("Ureia ontem", key="sis_renal_ur_ontem", placeholder="Ureia ontem", label_visibility="collapsed")

        # Distúrbios hidroeletrolíticos
        st.markdown("**Distúrbio hidroeletrolítico**")
        e1, e2, e3, e4, e5 = st.columns(5)
        with e1:
            st.markdown("**Sódio**")
            st.radio("Sódio", ["Normal", "Hiponatremia", "Hipernatremia"], key="sis_renal_sodio", index=None, label_visibility="collapsed")
        with e2:
            st.markdown("**Potássio**")
            st.radio("Potássio", ["Normal", "Hipocalemia", "Hipercalemia"], key="sis_renal_potassio", index=None, label_visibility="collapsed")
        with e3:
            st.markdown("**Magnésio**")
            st.radio("Magnésio", ["Normal", "Hipomagnesemia", "Hipermagnesemia"], key="sis_renal_magnesio", index=None, label_visibility="collapsed")
        with e4:
            st.markdown("**Fósforo**")
            st.radio("Fósforo", ["Normal", "Hipofosfatemia", "Hiperfosfatemia"], key="sis_renal_fosforo", index=None, label_visibility="collapsed")
        with e5:
            st.markdown("**Cálcio**")
            st.radio("Cálcio", ["Normal", "Hipocalcemia", "Hipercalcemia"], key="sis_renal_calcio", index=None, label_visibility="collapsed")

        # TRS
        st.markdown("**Terapia de Substituição Renal (TRS)**")
        t1, t2, t3, t4 = st.columns(4)
        with t1:
            st.radio("TRS", ["Sim", "Não"], key="sis_renal_trs", horizontal=True, index=None, label_visibility="collapsed")
        with t2:
            st.text_input("Via", key="sis_renal_trs_via", placeholder="Via", label_visibility="collapsed")
        with t3:
            st.text_input("Última diálise", key="sis_renal_trs_ultima", placeholder="Data última diálise", label_visibility="collapsed")
        with t4:
            st.text_input("Próxima TRS", key="sis_renal_trs_proxima", placeholder="Programação próxima TRS", label_visibility="collapsed")

        # Demais renal e Conduta
        st.markdown("**Demais renal**")
        st.text_input("Demais renal", key="sis_renal_obs", placeholder="Outros achados...", label_visibility="collapsed")
        with st.success("Condutas renais"):
            st.text_input("Conduta", key="sis_renal_conduta", placeholder="Ex: Ajustar dose ATB, Repor K...", label_visibility="collapsed")

    # INFECCIOSO
    with st.container(border=True):
        st.markdown("**Infeccioso**")

        # Febre 24h
        st.markdown("**Febre nas últimas 24h**")
        f1, f2, f3 = st.columns(3)
        with f1:
            st.radio("Febre", ["Sim", "Não"], key="sis_infec_febre", horizontal=True, index=None, label_visibility="collapsed")
        with f2:
            st.text_input("Quantas vezes", key="sis_infec_febre_vezes", placeholder="Quantas vezes", label_visibility="collapsed")
        with f3:
            st.text_input("Data da última febre", key="sis_infec_febre_ultima", placeholder="Data da última febre", label_visibility="collapsed")

        # Antibioticoterapia
        st.markdown("**Uso de Antibioticoterapia**")
        a1, a2 = st.columns([1, 2])
        with a1:
            st.markdown("**Em uso**")
            st.radio("ATB", ["Sim", "Não"], key="sis_infec_atb", horizontal=True, index=None, label_visibility="collapsed")
        with a2:
            st.markdown("**Guiado por cultura**")
            st.radio("Guiado", ["Sim", "Não"], key="sis_infec_atb_guiado", horizontal=True, index=None, label_visibility="collapsed")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.text_input("Medicamento 1", key="sis_infec_atb_1", placeholder="Medicamento 1", label_visibility="collapsed")
        with m2:
            st.text_input("Medicamento 2", key="sis_infec_atb_2", placeholder="Medicamento 2", label_visibility="collapsed")
        with m3:
            st.text_input("Medicamento 3", key="sis_infec_atb_3", placeholder="Medicamento 3", label_visibility="collapsed")

        # Culturas em andamento
        st.markdown("**Culturas em andamento**")
        st.radio("Culturas", ["Sim", "Não"], key="sis_infec_culturas_and", horizontal=True, index=None, label_visibility="collapsed")
        for i in range(1, 5):
            cs1, cs2 = st.columns([3, 1])
            with cs1:
                st.text_input(f"Sítio {i}", key=f"sis_infec_cult_{i}_sitio", placeholder=f"Sítio {i}", label_visibility="collapsed")
            with cs2:
                st.text_input(f"Coleta {i}", key=f"sis_infec_cult_{i}_data", placeholder="Data coleta", label_visibility="collapsed")

        # PCR e Procalcitonina
        st.markdown("**Marcadores inflamatórios**")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.text_input("PCR hoje", key="sis_infec_pcr_hoje", placeholder="PCR hoje", label_visibility="collapsed")
        with m2:
            st.text_input("Último PCR", key="sis_infec_pcr_ult", placeholder="Último PCR", label_visibility="collapsed")
        with m3:
            st.text_input("PCR antepenúltimo", key="sis_infec_pcr_antepen", placeholder="PCR antepenúltimo", label_visibility="collapsed")
        with m4:
            st.text_input("Procalcitonina", key="sis_infec_pct", placeholder="Procalcitonina", label_visibility="collapsed")

        # Isolamento
        st.markdown("**Isolamento**")
        i1, i2, i3 = st.columns(3)
        with i1:
            st.radio("Isolamento", ["Sim", "Não"], key="sis_infec_isolamento", horizontal=True, index=None, label_visibility="collapsed")
        with i2:
            st.text_input("Tipo", key="sis_infec_isolamento_tipo", placeholder="Tipo", label_visibility="collapsed")
        with i3:
            st.text_input("Motivo", key="sis_infec_isolamento_motivo", placeholder="Motivo", label_visibility="collapsed")

        # Patógenos isolados
        st.markdown("**Patógenos isolados**")
        st.text_input("Patógenos", key="sis_infec_patogenos", placeholder="Ex: K. pneumoniae KPC+, MRSA...", label_visibility="collapsed")

        # Demais infeccioso e Conduta
        st.markdown("**Demais infeccioso**")
        st.text_input("Demais infeccioso", key="sis_infec_obs", placeholder="Outros achados...", label_visibility="collapsed")
        with st.success("Condutas infecciosas"):
            st.text_input("Conduta", key="sis_infec_conduta", placeholder="Ex: Escalonar, manter ou suspender...", label_visibility="collapsed")

    # HEMATOLÓGICO
    with st.container(border=True):
        st.markdown("**Hematológico**")

        # Anticoagulação
        st.markdown("**Anticoagulação**")
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            st.radio("Anticoag", ["Sim", "Não"], key="sis_hemato_anticoag", horizontal=True, index=None, label_visibility="collapsed")
        with ac2:
            st.radio("Tipo", ["Profilática", "Plena"], key="sis_hemato_anticoag_tipo", horizontal=True, index=None, label_visibility="collapsed")
        with ac3:
            st.text_input("Motivo", key="sis_hemato_anticoag_motivo", placeholder="Motivo", label_visibility="collapsed")

        # Sangramento
        st.markdown("**Sangramento**")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.radio("Sangramento", ["Sim", "Não"], key="sis_hemato_sangramento", horizontal=True, index=None, label_visibility="collapsed")
        with s2:
            st.text_input("Via", key="sis_hemato_sangramento_via", placeholder="Via", label_visibility="collapsed")
        with s3:
            st.text_input("Data último sangramento", key="sis_hemato_sangramento_data", placeholder="Data último sangramento", label_visibility="collapsed")

        # Transfusão
        st.markdown("**Transfusão sanguínea**")
        st.text_input("Data última transfusão", key="sis_hemato_transf_data", placeholder="Data última transfusão", label_visibility="collapsed")
        for i in range(1, 4):
            t1, t2 = st.columns([3, 1])
            with t1:
                st.text_input(f"Componente {i}", key=f"sis_hemato_transf_{i}_comp", placeholder=f"Componente {i}", label_visibility="collapsed")
            with t2:
                st.text_input(f"Nº bolsas {i}", key=f"sis_hemato_transf_{i}_bolsas", placeholder="Nº bolsas", label_visibility="collapsed")

        # Hb e Plaquetas
        st.markdown("**Hemograma**")
        h1, h2, h3, h4 = st.columns(4)
        with h1:
            st.text_input("Hb hoje", key="sis_hemato_hb_hoje", placeholder="Hb hoje", label_visibility="collapsed")
        with h2:
            st.text_input("Hb último", key="sis_hemato_hb_ult", placeholder="Hb último", label_visibility="collapsed")
        with h3:
            st.text_input("Plaquetas hoje", key="sis_hemato_plaq_hoje", placeholder="Plaquetas hoje", label_visibility="collapsed")
        with h4:
            st.text_input("Plaquetas último", key="sis_hemato_plaq_ult", placeholder="Plaquetas último", label_visibility="collapsed")

        # Demais hemato e Conduta
        st.markdown("**Demais hematológico**")
        st.text_input("Demais hemato", key="sis_hemato_obs", placeholder="Outros achados...", label_visibility="collapsed")
        with st.success("Condutas hematológicas"):
            st.text_input("Conduta", key="sis_hemato_conduta", placeholder="Ex: Transfundir, Suspender Enoxa...", label_visibility="collapsed")

    # MÚSCULO-ESQUELÉTICO / PELE
    with st.container(border=True):
        st.markdown("**Músculo-Esquelético / Pele**")

        # Lesão por Pressão
        st.markdown("**Lesão por Pressão**")
        lpp_cols = st.columns([1, 2, 1])
        with lpp_cols[0]:
            st.radio("LPP", ["Sim", "Não"], key="sis_pele_lpp", horizontal=True, index=None, label_visibility="collapsed")
        for i in range(1, 4):
            l1, l2 = st.columns([3, 1])
            with l1:
                st.text_input(f"Local {i}", key=f"sis_pele_lpp_local_{i}", placeholder=f"Local {i}", label_visibility="collapsed")
            with l2:
                st.text_input(f"Grau {i}", key=f"sis_pele_lpp_grau_{i}", placeholder=f"Grau {i}", label_visibility="collapsed")

        # Polineuropatia
        st.markdown("**Polineuropatia**")
        st.radio("Polineuropatia", ["Sim", "Não"], key="sis_pele_polineuropatia", horizontal=True, index=None, label_visibility="collapsed")

        # Demais e Conduta
        st.markdown("**Demais músculo-esquelético / pele**")
        st.text_input("Demais", key="sis_pele_obs", placeholder="Outros achados...", label_visibility="collapsed")
        with st.success("Condutas músculo-esqueléticas / pele"):
            st.text_input("Conduta", key="sis_pele_conduta", placeholder="Ex: Curativo, Mudança de decúbito...", label_visibility="collapsed")