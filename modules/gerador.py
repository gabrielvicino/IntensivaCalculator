import streamlit as st


def _get(key, default=""):
    """Lê do session_state de forma segura."""
    return st.session_state.get(key, default)


def _secao_identificacao() -> list[str]:
    """
    Gera as linhas da seção '# Identificação & Scores'.
    Regra geral: campo vazio → linha não aparece.
    O cabeçalho só aparece se ao menos uma linha de conteúdo for gerada.
    """
    corpo = []

    # 1. Nome + Idade
    nome = _get("nome")
    idade = _get("idade", 0)
    if nome:
        linha = f"Nome: {nome}"
        if idade:
            linha += f", {idade} anos"
        corpo.append(linha)

    # 2. Sexo
    sexo = _get("sexo")
    if sexo:
        corpo.append(f"Sexo: {sexo}")

    # 3. Prontuário + Leito
    prontuario = _get("prontuario")
    leito = _get("leito")
    if prontuario or leito:
        partes = []
        if prontuario:
            partes.append(f"HC: {prontuario}")
        if leito:
            partes.append(f"Leito: {leito}")
        corpo.append(" / ".join(partes))

    # 4. Origem
    origem = _get("origem")
    if origem:
        corpo.append(f"Origem: {origem}")

    # 5. Equipe
    equipe = _get("equipe")
    if equipe:
        corpo.append(f"Equipe responsável: {equipe}")

    # 6. Data internação hospitalar
    di_hosp = _get("di_hosp")
    if di_hosp:
        corpo.append(f"Data de internação hospitalar: {di_hosp}")

    # 7. Data entrada UTI
    di_uti = _get("di_uti")
    if di_uti:
        corpo.append(f"Data de entrada na UTI: {di_uti}")

    # 8. Data entrada enfermaria — só aparece se preenchida
    di_enf = _get("di_enf")
    if di_enf:
        corpo.append(f"Data de entrada em enfermaria: {di_enf}")

    # 9. SAPS 3
    saps3 = _get("saps3")
    if saps3:
        corpo.append(f"SAPS 3: {saps3}")

    # 10. SOFA admissão
    sofa_adm = _get("sofa_adm", 0)
    try:
        sofa_adm = int(sofa_adm)
    except (ValueError, TypeError):
        sofa_adm = 0
    if sofa_adm:
        corpo.append(f"SOFA admissão: {sofa_adm}")

    # 11. PPS
    pps = _get("pps")
    if pps:
        corpo.append(f"PPS: {pps}")

    # 12. mRS prévio
    mrs = _get("mrs")
    if mrs:
        corpo.append(f"mRS prévio: {mrs}")

    # 13. CFS
    cfs = _get("cfs")
    if cfs:
        corpo.append(f"CFS: {cfs}")

    # 14. Paliativo — somente se True, em caixa alta, sem prefixo
    if _get("paliativo", False):
        corpo.append("")
        corpo.append("PACIENTE EM CUIDADOS PROPORCIONAIS")

    # Cabeçalho só aparece se houver conteúdo
    if not corpo:
        return []
    return ["# Identificação & Scores", ""] + corpo


def gerar_texto_final() -> str:
    """
    Monta o texto final do prontuário concatenando todas as seções.
    Cada seção retorna uma lista de linhas; seções vazias são ignoradas.
    """
    secoes = []

    secoes.append(_secao_identificacao())

    # Futuras seções serão adicionadas aqui:
    # secoes.append(_secao_diagnosticos())
    # secoes.append(_secao_comorbidades())
    # ...

    # Junta todas as seções com linha em branco entre elas
    blocos = ["\n".join(s) for s in secoes if s]
    return "\n\n".join(blocos)
