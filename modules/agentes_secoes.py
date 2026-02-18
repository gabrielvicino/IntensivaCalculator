"""
12 agentes de IA para preencher os campos estruturados de cada seção
a partir do texto já fatiado pelo ia_extrator.
"""
import json
import streamlit as st
from openai import OpenAI
import google.generativeai as genai


def _chamar_ia(prompt_system: str, texto: str, api_key: str, provider: str, modelo: str) -> dict:
    """Helper: envia texto para a IA e retorna JSON parseado."""
    try:
        if "OpenAI" in provider or "GPT" in provider:
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=modelo if modelo.startswith("gpt") else "gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user",   "content": f"TEXTO DA SEÇÃO:\n\n{texto}"}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(resp.choices[0].message.content)
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name=modelo if modelo.startswith("gemini") else "gemini-2.5-flash",
                system_instruction=prompt_system
            )
            resp = model.generate_content(f"TEXTO DA SEÇÃO:\n\n{texto}")
            txt = resp.text.replace("```json", "").replace("```", "").strip()
            return json.loads(txt)
    except json.JSONDecodeError as e:
        return {"_erro": f"JSON inválido: {e}"}
    except Exception as e:
        return {"_erro": str(e)}


# ==============================================================================
# AGENTE 1: IDENTIFICAÇÃO
# ==============================================================================
_PROMPT_IDENTIFICACAO = """Você é um extrator de dados médicos. Leia o texto clínico e preencha os campos de identificação do paciente.
REGRAS:
- Extraia APENAS o que está explicitamente no texto. Dados ausentes = string vazia "".
- sexo: EXATAMENTE "Masculino" ou "Feminino"
- idade: número inteiro (ex: 65), não string
- sofa_adm, sofa_atual: números inteiros
- saps3: string numérica (ex: "55")
- paliativo: true ou false
- Datas no formato DD/MM/AAAA
- Retorne APENAS JSON válido.

{
  "nome": "Nome completo do paciente",
  "idade": 0,
  "sexo": "Masculino",
  "prontuario": "número do prontuário/HC",
  "leito": "número ou nome do leito",
  "origem": "procedência (PS, UPA, Enfermaria, Transferência, etc.)",
  "equipe": "equipe médica responsável",
  "di_hosp": "data internação hospitalar DD/MM/AAAA",
  "di_uti": "data entrada UTI DD/MM/AAAA",
  "di_enf": "data entrada enfermaria DD/MM/AAAA",
  "saps3": "valor SAPS3",
  "sofa_adm": 0,
  "sofa_atual": 0,
  "mrs": "valor mRS",
  "pps": "valor PPS",
  "cfs": "valor CFS",
  "paliativo": false
}"""

def preencher_identificacao(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_IDENTIFICACAO, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    for k in ["sofa_adm", "sofa_atual"]:
        if k in r:
            try: r[k] = int(r[k]) if r[k] != "" else 0
            except: r[k] = 0
    if "idade" in r:
        try: r["idade"] = int(r["idade"]) if r["idade"] != "" else 0
        except: r["idade"] = 0
    if "paliativo" in r and isinstance(r["paliativo"], str):
        r["paliativo"] = r["paliativo"].lower() in ("true", "sim", "yes", "1")
    return r


# ==============================================================================
# AGENTE 2: HD - DIAGNÓSTICOS ATUAIS E PRÉVIOS
# ==============================================================================
_PROMPT_HD = """Você é um extrator de dados médicos. Extraia hipóteses diagnósticas ativas e prévias.
REGRAS:
- Máximo 4 diagnósticos atuais (ativos/em andamento) e 4 prévios (resolvidos/histórico).
- Dados ausentes = string vazia "".
- class: estadiamento/gravidade (ex: "KDIGO 3", "Killip II", "Estágio 2").
- Datas: DD/MM/AAAA.
- NÃO preencha campos de conduta.
- Retorne APENAS JSON válido.

{
  "hd_atual_1_nome": "", "hd_atual_1_class": "", "hd_atual_1_data": "", "hd_atual_1_obs": "",
  "hd_atual_2_nome": "", "hd_atual_2_class": "", "hd_atual_2_data": "", "hd_atual_2_obs": "",
  "hd_atual_3_nome": "", "hd_atual_3_class": "", "hd_atual_3_data": "", "hd_atual_3_obs": "",
  "hd_atual_4_nome": "", "hd_atual_4_class": "", "hd_atual_4_data": "", "hd_atual_4_obs": "",
  "hd_prev_1_nome": "", "hd_prev_1_class": "", "hd_prev_1_data_ini": "", "hd_prev_1_data_fim": "", "hd_prev_1_obs": "",
  "hd_prev_2_nome": "", "hd_prev_2_class": "", "hd_prev_2_data_ini": "", "hd_prev_2_data_fim": "", "hd_prev_2_obs": "",
  "hd_prev_3_nome": "", "hd_prev_3_class": "", "hd_prev_3_data_ini": "", "hd_prev_3_data_fim": "", "hd_prev_3_obs": "",
  "hd_prev_4_nome": "", "hd_prev_4_class": "", "hd_prev_4_data_ini": "", "hd_prev_4_data_fim": "", "hd_prev_4_obs": ""
}"""

def preencher_hd(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_HD, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    return r


# ==============================================================================
# AGENTE 3: COMORBIDADES
# ==============================================================================
_PROMPT_COMORBIDADES = """Você é um extrator de dados médicos. Extraia comorbidades do paciente.
REGRAS:
- Máximo 10 comorbidades.
- Dados ausentes = string vazia "".
- class: estadiamento ou controle (ex: "Controlada", "Estágio 3", "Descompensada").
- NÃO preencha conduta.
- Retorne APENAS JSON válido.

{
  "cmd_1_nome": "", "cmd_1_class": "",
  "cmd_2_nome": "", "cmd_2_class": "",
  "cmd_3_nome": "", "cmd_3_class": "",
  "cmd_4_nome": "", "cmd_4_class": "",
  "cmd_5_nome": "", "cmd_5_class": "",
  "cmd_6_nome": "", "cmd_6_class": "",
  "cmd_7_nome": "", "cmd_7_class": "",
  "cmd_8_nome": "", "cmd_8_class": "",
  "cmd_9_nome": "", "cmd_9_class": "",
  "cmd_10_nome": "", "cmd_10_class": ""
}"""

def preencher_comorbidades(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_COMORBIDADES, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    return r


# ==============================================================================
# AGENTE 4: MUC - MEDICAÇÕES DE USO CONTÍNUO
# ==============================================================================
_PROMPT_MUC = """Você é um extrator de dados médicos. Extraia medicações de uso contínuo (domiciliar/prévio ao internamento).
REGRAS:
- Máximo 10 medicações.
- Dados ausentes = string vazia "".
- muc_adesao_global: EXATAMENTE "Uso Regular", "Uso Irregular" ou "Não usa".
- NÃO preencha conduta.
- Retorne APENAS JSON válido.

{
  "muc_adesao_global": "Uso Regular",
  "muc_1_nome": "", "muc_1_dose": "", "muc_1_freq": "",
  "muc_2_nome": "", "muc_2_dose": "", "muc_2_freq": "",
  "muc_3_nome": "", "muc_3_dose": "", "muc_3_freq": "",
  "muc_4_nome": "", "muc_4_dose": "", "muc_4_freq": "",
  "muc_5_nome": "", "muc_5_dose": "", "muc_5_freq": "",
  "muc_6_nome": "", "muc_6_dose": "", "muc_6_freq": "",
  "muc_7_nome": "", "muc_7_dose": "", "muc_7_freq": "",
  "muc_8_nome": "", "muc_8_dose": "", "muc_8_freq": "",
  "muc_9_nome": "", "muc_9_dose": "", "muc_9_freq": "",
  "muc_10_nome": "", "muc_10_dose": "", "muc_10_freq": ""
}"""

def preencher_muc(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_MUC, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    return r


# ==============================================================================
# AGENTE 5: HMPA — reescreve a HMA/HMP mantendo fidelidade absoluta
# ==============================================================================
_PROMPT_HMPA = """Você é um Especialista em Redação Médica e Comunicação Clínica de Alta Complexidade.
Sua tarefa é reescrever a História da Moléstia Atual (HMA) e Pregressa (HMP) fornecida, otimizando a clareza e o fluxo lógico para leitura por outro médico intensivista.

### ⛔ REGRAS DE OURO (INVIOLÁVEIS):
1.  **FIDELIDADE ABSOLUTA:** Você está PROIBIDO de adicionar, inferir ou remover qualquer dado factual. Se o texto diz "dor há 3 dias", você não pode mudar para "dor crônica" nem omitir a duração. Mantenha nomes de hospitais, datas e valores exatos.
2.  **TOM PROFISSIONAL:** Mantenha a terminologia médica técnica (ex: use "dispneia" em vez de "falta de ar", "edema" em vez de "inchaço", se o contexto permitir, mas respeite o registro original se for uma citação direta do paciente).
3.  **ZERO ALUCINAÇÃO:** Se o texto original estiver confuso ou ambíguo, mantenha a ambiguidade ou use frases como "relato de..." para não criar fatos falsos.

### 🎯 OBJETIVOS DA REESCRITA:
1.  **ORDENAÇÃO CRONOLÓGICA (Prioridade Máxima):** Reorganize os fatos em uma linha do tempo linear e lógica:
    * Antecedentes Relevantes → Início dos Sintomas → Atendimentos Prévios (UPA/PS) → Admissão Atual → Evolução até o momento.
2.  **SINTAXE E COESÃO:** Transforme frases truncadas, uso excessivo de abreviações informais ou "textão" corrido em parágrafos estruturados e fluidos.
3.  **DENSIDADE INFORMATIVA:** Agrupe informações correlatas. (Ex: junte todos os sintomas respiratórios em uma oração, todos os dados hemodinâmicos em outra).

### FORMATO DE SAÍDA:
Retorne apenas o texto reescrito, pronto para ser colado no prontuário. Não use introduções como "Aqui está a reescrita"."""

def preencher_hmpa(texto, api_key, provider, modelo):
    if not texto or not texto.strip():
        return {}

    try:
        if "OpenAI" in provider or "GPT" in provider:
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=modelo if modelo.startswith("gpt") else "gpt-4o",
                messages=[
                    {"role": "system", "content": _PROMPT_HMPA},
                    {"role": "user",   "content": f"Texto Original:\n\n{texto}"}
                ]
            )
            reescrito = resp.choices[0].message.content.strip()
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name=modelo if modelo.startswith("gemini") else "gemini-2.5-flash",
                system_instruction=_PROMPT_HMPA
            )
            resp = model.generate_content(f"Texto Original:\n\n{texto}")
            reescrito = resp.text.strip()

        return {"hmpa_reescrito": reescrito}

    except Exception as e:
        return {"_erro": str(e)}


# ==============================================================================
# AGENTE 6: DISPOSITIVOS INVASIVOS
# ==============================================================================
_PROMPT_DISPOSITIVOS = """Você é um extrator de dados médicos. Extraia dispositivos invasivos do paciente.
REGRAS:
- Máximo 8 dispositivos.
- Dados ausentes = string vazia "".
- disp_X_status: EXATAMENTE "Ativo" ou "Removido".
- Datas: DD/MM/AAAA.
- Exemplos de dispositivos: CVC, TOT, TQT, SVD, SNE, SNG, PAM, PICC, Dreno.
- NÃO preencha conduta.
- Retorne APENAS JSON válido.

{
  "disp_1_nome": "", "disp_1_local": "", "disp_1_data_insercao": "", "disp_1_data_retirada": "", "disp_1_status": "Ativo",
  "disp_2_nome": "", "disp_2_local": "", "disp_2_data_insercao": "", "disp_2_data_retirada": "", "disp_2_status": "Ativo",
  "disp_3_nome": "", "disp_3_local": "", "disp_3_data_insercao": "", "disp_3_data_retirada": "", "disp_3_status": "Ativo",
  "disp_4_nome": "", "disp_4_local": "", "disp_4_data_insercao": "", "disp_4_data_retirada": "", "disp_4_status": "Ativo",
  "disp_5_nome": "", "disp_5_local": "", "disp_5_data_insercao": "", "disp_5_data_retirada": "", "disp_5_status": "Ativo",
  "disp_6_nome": "", "disp_6_local": "", "disp_6_data_insercao": "", "disp_6_data_retirada": "", "disp_6_status": "Ativo",
  "disp_7_nome": "", "disp_7_local": "", "disp_7_data_insercao": "", "disp_7_data_retirada": "", "disp_7_status": "Ativo",
  "disp_8_nome": "", "disp_8_local": "", "disp_8_data_insercao": "", "disp_8_data_retirada": "", "disp_8_status": "Ativo"
}"""

def preencher_dispositivos(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_DISPOSITIVOS, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    return r


# ==============================================================================
# AGENTE 7: CULTURAS
# ==============================================================================
_PROMPT_CULTURAS = """Você é um extrator de dados médicos. Extraia culturas microbiológicas.
REGRAS:
- Máximo 8 culturas.
- Dados ausentes = string vazia "".
- cult_X_status: EXATAMENTE uma das opções: "Pendente negativo", "Negativo", "Positivo Aguarda Antibiograma", "Positivo com Antibiograma".
- Datas: DD/MM/AAAA.
- NÃO preencha conduta.
- Retorne APENAS JSON válido.

{
  "cult_1_sitio": "", "cult_1_data_coleta": "", "cult_1_data_resultado": "", "cult_1_status": "Pendente negativo", "cult_1_micro": "", "cult_1_sensib": "",
  "cult_2_sitio": "", "cult_2_data_coleta": "", "cult_2_data_resultado": "", "cult_2_status": "Pendente negativo", "cult_2_micro": "", "cult_2_sensib": "",
  "cult_3_sitio": "", "cult_3_data_coleta": "", "cult_3_data_resultado": "", "cult_3_status": "Pendente negativo", "cult_3_micro": "", "cult_3_sensib": "",
  "cult_4_sitio": "", "cult_4_data_coleta": "", "cult_4_data_resultado": "", "cult_4_status": "Pendente negativo", "cult_4_micro": "", "cult_4_sensib": "",
  "cult_5_sitio": "", "cult_5_data_coleta": "", "cult_5_data_resultado": "", "cult_5_status": "Pendente negativo", "cult_5_micro": "", "cult_5_sensib": "",
  "cult_6_sitio": "", "cult_6_data_coleta": "", "cult_6_data_resultado": "", "cult_6_status": "Pendente negativo", "cult_6_micro": "", "cult_6_sensib": "",
  "cult_7_sitio": "", "cult_7_data_coleta": "", "cult_7_data_resultado": "", "cult_7_status": "Pendente negativo", "cult_7_micro": "", "cult_7_sensib": "",
  "cult_8_sitio": "", "cult_8_data_coleta": "", "cult_8_data_resultado": "", "cult_8_status": "Pendente negativo", "cult_8_micro": "", "cult_8_sensib": ""
}"""

def preencher_culturas(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_CULTURAS, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    return r


# ==============================================================================
# AGENTE 8: ANTIBIÓTICOS
# ==============================================================================
_PROMPT_ANTIBIOTICOS = """Você é um extrator de dados médicos. Extraia antibióticos/antimicrobianos.
REGRAS:
- Máximo 5 ATBs atuais (em uso) e 5 prévios (suspensos/completados).
- Dados ausentes = string vazia "".
- tipo: EXATAMENTE "Empírico" ou "Guiado".
- Datas: DD/MM/AAAA.
- NÃO preencha conduta.
- Retorne APENAS JSON válido.

{
  "atb_curr_1_nome": "", "atb_curr_1_tipo": "Empírico", "atb_curr_1_data_ini": "", "atb_curr_1_data_fim": "",
  "atb_curr_2_nome": "", "atb_curr_2_tipo": "Empírico", "atb_curr_2_data_ini": "", "atb_curr_2_data_fim": "",
  "atb_curr_3_nome": "", "atb_curr_3_tipo": "Empírico", "atb_curr_3_data_ini": "", "atb_curr_3_data_fim": "",
  "atb_curr_4_nome": "", "atb_curr_4_tipo": "Empírico", "atb_curr_4_data_ini": "", "atb_curr_4_data_fim": "",
  "atb_curr_5_nome": "", "atb_curr_5_tipo": "Empírico", "atb_curr_5_data_ini": "", "atb_curr_5_data_fim": "",
  "atb_prev_1_nome": "", "atb_prev_1_tipo": "Empírico", "atb_prev_1_data_ini": "", "atb_prev_1_data_fim": "", "atb_prev_1_obs": "",
  "atb_prev_2_nome": "", "atb_prev_2_tipo": "Empírico", "atb_prev_2_data_ini": "", "atb_prev_2_data_fim": "", "atb_prev_2_obs": "",
  "atb_prev_3_nome": "", "atb_prev_3_tipo": "Empírico", "atb_prev_3_data_ini": "", "atb_prev_3_data_fim": "", "atb_prev_3_obs": "",
  "atb_prev_4_nome": "", "atb_prev_4_tipo": "Empírico", "atb_prev_4_data_ini": "", "atb_prev_4_data_fim": "", "atb_prev_4_obs": "",
  "atb_prev_5_nome": "", "atb_prev_5_tipo": "Empírico", "atb_prev_5_data_ini": "", "atb_prev_5_data_fim": "", "atb_prev_5_obs": ""
}"""

def preencher_antibioticos(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_ANTIBIOTICOS, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    return r


# ==============================================================================
# AGENTE 9: COMPLEMENTARES
# ==============================================================================
_PROMPT_COMPLEMENTARES = """Você é um extrator de dados médicos. Extraia laudos de exames complementares (imagem, ecocardiograma, ECG, cintilografia, pareceres, etc.).
REGRAS:
- Máximo 8 exames.
- Dados ausentes = string vazia "".
- Coloque o laudo COMPLETO no campo (tipo, data e resultado).
- NÃO preencha conduta.
- Retorne APENAS JSON válido.

{
  "comp_1_laudo": "",
  "comp_2_laudo": "",
  "comp_3_laudo": "",
  "comp_4_laudo": "",
  "comp_5_laudo": "",
  "comp_6_laudo": "",
  "comp_7_laudo": "",
  "comp_8_laudo": ""
}"""

def preencher_complementares(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_COMPLEMENTARES, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    return r


# ==============================================================================
# AGENTE 10: LABORATORIAIS
# ==============================================================================
_PROMPT_LABORATORIAIS = """Você é um extrator de dados médicos. Extraia valores laboratoriais do exame mais recente (lab_1).
REGRAS:
- Todos os valores como strings numéricas (ex: "12.5", "150").
- Dados ausentes = string vazia "".
- lab_1_gas_tipo: EXATAMENTE "Arterial" ou "Venosa".
- Data: DD/MM/AAAA.
- Retorne APENAS JSON válido.

Referência dos campos:
- Hemograma: hb=hemoglobina, ht=hematócrito, vcm, hcm, rdw, leuco=leucócitos, plaq=plaquetas
- Renal/eletrólitos: cr=creatinina, ur=ureia, na=sódio, k=potássio, mg=magnésio, pi=fósforo, cat=cálcio total
- Hepático/pancreático: tgp, tgo, fal=fosfatase alcalina, ggt, bt=bilirrubina total, alb=albumina, amil=amilase, lipas=lipase
- Cardio/coag/inflamação: cpk, pcr=proteína C reativa, trop=troponina, tp=tempo protrombina, ttpa
- Gasometria: gas_ph, gas_pco2, gas_po2, gas_hco3, gas_be, gas_sat, gas_lac=lactato, gas_ag=ânion gap, gas_cl, gas_na, gas_k, gas_cai=cálcio iônico
- Gasometria venosa: gasv_pco2, svo2
- Urina: ur_dens=densidade, ur_le=leucócitos, ur_nit=nitrito, ur_leu=leucocitúria, ur_hm=hematúria, ur_prot=proteína, ur_cet=cetonas, ur_glic=glicose

{
  "lab_1_data": "",
  "lab_1_hb": "", "lab_1_ht": "", "lab_1_vcm": "", "lab_1_hcm": "", "lab_1_rdw": "", "lab_1_leuco": "", "lab_1_plaq": "",
  "lab_1_cr": "", "lab_1_ur": "", "lab_1_na": "", "lab_1_k": "", "lab_1_mg": "", "lab_1_pi": "", "lab_1_cat": "",
  "lab_1_tgp": "", "lab_1_tgo": "", "lab_1_fal": "", "lab_1_ggt": "", "lab_1_bt": "", "lab_1_alb": "", "lab_1_amil": "", "lab_1_lipas": "",
  "lab_1_cpk": "", "lab_1_pcr": "", "lab_1_trop": "", "lab_1_tp": "", "lab_1_ttpa": "",
  "lab_1_gas_tipo": "Arterial", "lab_1_gas_ph": "", "lab_1_gas_pco2": "", "lab_1_gas_po2": "", "lab_1_gas_hco3": "",
  "lab_1_gas_be": "", "lab_1_gas_sat": "", "lab_1_gas_lac": "", "lab_1_gas_ag": "",
  "lab_1_gas_cl": "", "lab_1_gas_na": "", "lab_1_gas_k": "", "lab_1_gas_cai": "",
  "lab_1_gasv_pco2": "", "lab_1_svo2": "",
  "lab_1_ur_dens": "", "lab_1_ur_le": "", "lab_1_ur_nit": "", "lab_1_ur_leu": "",
  "lab_1_ur_hm": "", "lab_1_ur_prot": "", "lab_1_ur_cet": "", "lab_1_ur_glic": "",
  "lab_1_outros": ""
}"""

def preencher_laboratoriais(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_LABORATORIAIS, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    return r


# ==============================================================================
# AGENTE 11: EVOLUÇÃO CLÍNICA (texto livre — passa direto)
# ==============================================================================
def preencher_evolucao(texto, api_key, provider, modelo):
    return {"evolucao_notas": texto.strip()} if texto and texto.strip() else {}


# ==============================================================================
# AGENTE 12: SISTEMAS
# ==============================================================================
_PROMPT_SISTEMAS = """Você é um extrator de dados médicos de terapia intensiva. Preencha os campos abaixo com base no texto do exame físico e evolução por sistemas.
REGRAS GERAIS:
- Dados ausentes = string vazia "".
- Campos Sim/Não: EXATAMENTE "Sim" ou "Não".
- Campos numéricos inteiros: retorne número (ex: 15, -2, 0).
- Campos booleanos (escape_manha/tarde/noite): true ou false.
- NÃO preencha campos de conduta (_conduta, _obs).
- Retorne APENAS JSON válido.

CAMPOS NEUROLÓGICOS:
sis_neuro_ecg (GCS 3-15, inteiro), sis_neuro_ecg_p (1-15, inteiro), sis_neuro_rass (-5 a +5, inteiro),
sis_neuro_delirium ("Sim"/"Não"), sis_neuro_cam_icu ("Positivo"/"Negativo"),
sis_neuro_pupilas_tam ("Miótica"/"Normal"/"Midríase"), sis_neuro_pupilas_simetria ("Simétricas"/"Anisocoria"),
sis_neuro_pupilas_foto ("Fotoreagente"/"Não fotoreagente"),
sis_neuro_analgesico_adequado ("Sim"/"Não"), sis_neuro_deficits_focais (texto),
sis_neuro_analgesia_1_tipo ("Fixa"/"Se necessário"), sis_neuro_analgesia_1_drogas, sis_neuro_analgesia_1_dose, sis_neuro_analgesia_1_freq,
sis_neuro_analgesia_2_tipo, sis_neuro_analgesia_2_drogas, sis_neuro_analgesia_2_dose, sis_neuro_analgesia_2_freq,
sis_neuro_analgesia_3_tipo, sis_neuro_analgesia_3_drogas, sis_neuro_analgesia_3_dose, sis_neuro_analgesia_3_freq,
sis_neuro_sedacao_1_drogas, sis_neuro_sedacao_1_dose, sis_neuro_sedacao_1_meta,
sis_neuro_sedacao_2_drogas, sis_neuro_sedacao_2_dose, sis_neuro_sedacao_2_meta,
sis_neuro_sedacao_3_drogas, sis_neuro_sedacao_3_dose, sis_neuro_sedacao_3_meta,
sis_neuro_bloqueador_dose, sis_neuro_vigilancia

CAMPOS RESPIRATÓRIOS:
sis_resp_ausculta (texto livre: MV+, roncos, creptos, etc.),
sis_resp_modo ("Ar Ambiente"/"Oxigenioterapia"/"VNI"/"Cateter de Alto Fluxo"/"Ventilação Mecânica"),
sis_resp_pressao, sis_resp_volume, sis_resp_fio2, sis_resp_peep, sis_resp_freq (parâmetros ventilatórios),
sis_resp_vent_protetora ("Sim"/"Não"), sis_resp_sincronico ("Sim"/"Não"), sis_resp_assincronia (texto),
sis_resp_complacencia, sis_resp_resistencia, sis_resp_dp, sis_resp_plato, sis_resp_pico (mecânica resp.),
sis_resp_disturbio_resp ("Sim"/"Não"),
sis_resp_dreno_1, sis_resp_dreno_1_debito, sis_resp_dreno_2, sis_resp_dreno_2_debito, sis_resp_dreno_3, sis_resp_dreno_3_debito

CAMPOS CARDIOVASCULARES:
sis_cardio_fc (frequência cardíaca), sis_cardio_cardioscopia (ex: "Sinusal", "FA"),
sis_cardio_pam (pressão arterial média),
sis_cardio_perfusao ("Normal"/"Lentificada"/"Flush"/"Tempo de enchimento capilar"),
sis_cardio_fluido_responsivo ("Sim"/"Não"), sis_cardio_fluido_tolerante ("Sim"/"Não"),
sis_cardio_dva_1_med, sis_cardio_dva_1_dose, sis_cardio_dva_2_med, sis_cardio_dva_2_dose,
sis_cardio_dva_3_med, sis_cardio_dva_3_dose, sis_cardio_dva_4_med, sis_cardio_dva_4_dose

CAMPOS RENAIS:
sis_renal_diurese, sis_renal_balanco, sis_renal_balanco_acum,
sis_renal_volemia ("Hipovolêmico"/"Euvolêmico"/"Hipervolêmico"),
sis_renal_cr_hoje, sis_renal_ur_hoje, sis_renal_cr_ontem, sis_renal_ur_ontem,
sis_renal_sodio ("Normal"/"Hiponatremia"/"Hipernatremia"),
sis_renal_potassio ("Normal"/"Hipocalemia"/"Hipercalemia"),
sis_renal_magnesio ("Normal"/"Hipomagnesemia"/"Hipermagnesemia"),
sis_renal_fosforo ("Normal"/"Hipofosfatemia"/"Hiperfosfatemia"),
sis_renal_calcio ("Normal"/"Hipocalcemia"/"Hipercalcemia"),
sis_renal_trs ("Sim"/"Não"), sis_renal_trs_via, sis_renal_trs_ultima, sis_renal_trs_proxima

CAMPOS INFECCIOSOS:
sis_infec_febre ("Sim"/"Não"), sis_infec_febre_vezes, sis_infec_febre_ultima,
sis_infec_atb ("Sim"/"Não"), sis_infec_atb_1, sis_infec_atb_2, sis_infec_atb_3,
sis_infec_atb_guiado ("Sim"/"Não"),
sis_infec_culturas_and ("Sim"/"Não"),
sis_infec_cult_1_sitio, sis_infec_cult_1_data, sis_infec_cult_2_sitio, sis_infec_cult_2_data,
sis_infec_cult_3_sitio, sis_infec_cult_3_data, sis_infec_cult_4_sitio, sis_infec_cult_4_data,
sis_infec_pcr_hoje, sis_infec_pcr_ult, sis_infec_pcr_antepen, sis_infec_pct,
sis_infec_isolamento ("Sim"/"Não"), sis_infec_isolamento_tipo, sis_infec_isolamento_motivo, sis_infec_patogenos

CAMPOS GASTROINTESTINAIS:
sis_gastro_exame_fisico (texto: RHA, palpação),
sis_gastro_dieta_oral, sis_gastro_dieta_enteral, sis_gastro_dieta_enteral_vol,
sis_gastro_dieta_parenteral, sis_gastro_dieta_parenteral_vol, sis_gastro_meta_calorica,
sis_gastro_na_meta ("Sim"/"Não"), sis_gastro_ingestao_quanto,
sis_gastro_escape_glicemico ("Sim"/"Não"), sis_gastro_escape_vezes,
sis_gastro_escape_manha (true/false), sis_gastro_escape_tarde (true/false), sis_gastro_escape_noite (true/false),
sis_gastro_insulino ("Sim"/"Não"), sis_gastro_insulino_dose,
sis_gastro_evacuacao ("Sim"/"Não"), sis_gastro_evacuacao_data, sis_gastro_laxativo

CAMPOS HEMATOLÓGICOS:
sis_hemato_anticoag ("Sim"/"Não"), sis_hemato_anticoag_motivo, sis_hemato_anticoag_tipo ("Profilática"/"Plena"),
sis_hemato_sangramento ("Sim"/"Não"), sis_hemato_sangramento_via, sis_hemato_sangramento_data,
sis_hemato_transf_data, sis_hemato_transf_1_comp, sis_hemato_transf_1_bolsas,
sis_hemato_transf_2_comp, sis_hemato_transf_2_bolsas, sis_hemato_transf_3_comp, sis_hemato_transf_3_bolsas,
sis_hemato_hb_hoje, sis_hemato_hb_ult, sis_hemato_plaq_hoje, sis_hemato_plaq_ult

CAMPOS MÚSCULO-ESQUELÉTICO/PELE:
sis_pele_lpp ("Sim"/"Não"),
sis_pele_lpp_local_1, sis_pele_lpp_grau_1, sis_pele_lpp_local_2, sis_pele_lpp_grau_2,
sis_pele_lpp_local_3, sis_pele_lpp_grau_3, sis_pele_polineuropatia ("Sim"/"Não")

Retorne JSON com TODOS os campos acima preenchidos (ausentes = "")."""

def preencher_sistemas(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_SISTEMAS, texto, api_key, provider, modelo)
    r.pop("_erro", None)

    # Garantir tipos corretos para campos inteiros
    for k in ["sis_neuro_ecg", "sis_neuro_ecg_p"]:
        if k in r:
            try: r[k] = int(r[k]) if r[k] != "" else 15
            except: r[k] = 15
    if "sis_neuro_rass" in r:
        try: r["sis_neuro_rass"] = int(r["sis_neuro_rass"]) if r["sis_neuro_rass"] != "" else 0
        except: r["sis_neuro_rass"] = 0

    # Garantir tipos corretos para booleanos
    for k in ["sis_gastro_escape_manha", "sis_gastro_escape_tarde", "sis_gastro_escape_noite"]:
        if k in r and isinstance(r[k], str):
            r[k] = r[k].lower() in ("true", "sim", "yes", "1")

    return r


# ==============================================================================
# AGENTE 13: CONTROLES & BALANÇO HÍDRICO
# ==============================================================================
_PROMPT_CONTROLES = """Você é um extrator de dados médicos especializado em sinais vitais e controles de UTI.
Leia o texto e extraia os valores de controle das últimas 24h (ou dos dias disponíveis: anteontem, ontem, hoje).

REGRAS:
- Extraia APENAS o que está explicitamente no texto. Dados ausentes = string vazia "".
- Para cada parâmetro com min e max: o menor valor é o mínimo, o maior é o máximo.
- Formato típico do texto: "PAS: 100 - 132 mmHg" → min=100, max=132
- "Balanço Hídrico Total: -492ml" → balanco="-492"
- "Diurese: 1600ml" → diurese="1600"
- A data pode aparecer como "> 18/02/2026" ou "18/02" — extraia no formato que aparecer.
- Se houver apenas um dia de dados, preencha os campos "hoje". Se houver dois dias, preencha "ontem" e "hoje". Se houver três, preencha os três.
- Retorne APENAS JSON válido, sem texto extra.

{
  "ctrl_hoje_data": "data do dia (ex: 18/02/2026)",
  "ctrl_ontem_data": "",
  "ctrl_anteontem_data": "",

  "ctrl_hoje_pas_min": "", "ctrl_hoje_pas_max": "",
  "ctrl_hoje_pad_min": "", "ctrl_hoje_pad_max": "",
  "ctrl_hoje_pam_min": "", "ctrl_hoje_pam_max": "",
  "ctrl_hoje_fc_min":  "", "ctrl_hoje_fc_max": "",
  "ctrl_hoje_fr_min":  "", "ctrl_hoje_fr_max": "",
  "ctrl_hoje_sato2_min": "", "ctrl_hoje_sato2_max": "",
  "ctrl_hoje_temp_min": "", "ctrl_hoje_temp_max": "",
  "ctrl_hoje_glic_min": "", "ctrl_hoje_glic_max": "",
  "ctrl_hoje_diurese": "",
  "ctrl_hoje_balanco": "",

  "ctrl_ontem_pas_min": "", "ctrl_ontem_pas_max": "",
  "ctrl_ontem_pad_min": "", "ctrl_ontem_pad_max": "",
  "ctrl_ontem_pam_min": "", "ctrl_ontem_pam_max": "",
  "ctrl_ontem_fc_min":  "", "ctrl_ontem_fc_max": "",
  "ctrl_ontem_fr_min":  "", "ctrl_ontem_fr_max": "",
  "ctrl_ontem_sato2_min": "", "ctrl_ontem_sato2_max": "",
  "ctrl_ontem_temp_min": "", "ctrl_ontem_temp_max": "",
  "ctrl_ontem_glic_min": "", "ctrl_ontem_glic_max": "",
  "ctrl_ontem_diurese": "",
  "ctrl_ontem_balanco": "",

  "ctrl_anteontem_pas_min": "", "ctrl_anteontem_pas_max": "",
  "ctrl_anteontem_pad_min": "", "ctrl_anteontem_pad_max": "",
  "ctrl_anteontem_pam_min": "", "ctrl_anteontem_pam_max": "",
  "ctrl_anteontem_fc_min":  "", "ctrl_anteontem_fc_max": "",
  "ctrl_anteontem_fr_min":  "", "ctrl_anteontem_fr_max": "",
  "ctrl_anteontem_sato2_min": "", "ctrl_anteontem_sato2_max": "",
  "ctrl_anteontem_temp_min": "", "ctrl_anteontem_temp_max": "",
  "ctrl_anteontem_glic_min": "", "ctrl_anteontem_glic_max": "",
  "ctrl_anteontem_diurese": "",
  "ctrl_anteontem_balanco": ""
}"""

def preencher_controles(texto, api_key, provider, modelo):
    r = _chamar_ia(_PROMPT_CONTROLES, texto, api_key, provider, modelo)
    r.pop("_erro", None)
    return r


# ==============================================================================
# MAPEAMENTO: seção → função agente e campo _notas
# ==============================================================================
_AGENTES = {
    "identificacao":  preencher_identificacao,
    "hd":             preencher_hd,
    "comorbidades":   preencher_comorbidades,
    "muc":            preencher_muc,
    "hmpa":           preencher_hmpa,
    "dispositivos":   preencher_dispositivos,
    "culturas":       preencher_culturas,
    "antibioticos":   preencher_antibioticos,
    "complementares": preencher_complementares,
    "laboratoriais":  preencher_laboratoriais,
    "controles":      preencher_controles,
    "evolucao":       preencher_evolucao,
    "sistemas":       preencher_sistemas,
}

_NOTAS_MAP = {
    "identificacao":  "identificacao_notas",
    "hd":             "hd_notas",
    "comorbidades":   "comorbidades_notas",
    "muc":            "muc_notas",
    "hmpa":           "hmpa_texto",
    "dispositivos":   "dispositivos_notas",
    "culturas":       "culturas_notas",
    "antibioticos":   "antibioticos_notas",
    "complementares": "complementares_notas",
    "laboratoriais":  "laboratoriais_notas",
    "controles":      "controles_notas",
    "evolucao":       "evolucao_notas",
    "sistemas":       "sistemas_notas",
}

NOMES_SECOES = {
    "identificacao":  "1. Identificação",
    "hd":             "2. Diagnósticos",
    "comorbidades":   "3. Comorbidades",
    "muc":            "4. MUC",
    "hmpa":           "5. HMPA",
    "dispositivos":   "6. Dispositivos",
    "culturas":       "7. Culturas",
    "antibioticos":   "8. Antibióticos",
    "complementares": "9. Complementares",
    "laboratoriais":  "10. Laboratoriais",
    "controles":      "11. Controles & Balanço",
    "evolucao":       "12. Evolução Clínica",
    "sistemas":       "13. Sistemas",
}


def preencher_todas_secoes(api_key: str, provider: str, modelo: str):
    """
    Lê os campos _notas já preenchidos pelo ia_extrator,
    roda cada um dos 12 agentes e retorna (resultado_dict, lista_erros).
    """
    resultado = {}
    erros = []

    for secao, fn_agente in _AGENTES.items():
        chave_notas = _NOTAS_MAP[secao]
        texto = st.session_state.get(chave_notas, "").strip()

        if not texto:
            continue

        dados = fn_agente(texto, api_key, provider, modelo)

        if "_erro" in dados:
            erros.append(f"{NOMES_SECOES[secao]}: {dados['_erro']}")
        else:
            resultado.update(dados)

    return resultado, erros
