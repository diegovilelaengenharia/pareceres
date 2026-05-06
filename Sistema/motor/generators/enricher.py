"""
Enricher — estágio de enriquecimento de dados com modelos do template.

Interpola os campos [campo] dos modelos narrativos (modelo_abertura,
modelo_considerandos, modelo_conclusao, documentos_tipicos) com os
dados concretos do processo. Só preenche campos AUSENTES ou VAZIOS —
jamais sobrescreve o que o Gemini já produziu.
"""

import re


# ═══════════════════════════════════════════════════════════
#  INTERPOLAÇÃO DE PLACEHOLDERS
# ═══════════════════════════════════════════════════════════

def _interpolar(texto: str, dados: dict) -> str:
    """
    Substitui [campo] pelo valor de dados['campo'].
    Regras:
    - Se campo existe em dados → substitui pelo valor
    - Se campo contém '_ex_' ou tem mais de 40 chars → placeholder descritivo → remove
    - Se campo ausente (sem _ex_, curto) → mantém [campo] intacto
    """
    def repl(m):
        chave = m.group(1)
        # Placeholder descritivo (instrução para o Gemini, não campo real)
        if "_ex_" in chave or len(chave) > 40:
            return ""
        val = dados.get(chave, "")
        return str(val) if val else m.group(0)  # mantém se ausente

    return re.sub(r'\[([^\]]+)\]', repl, texto)


def _tratar_condicional(item: str, dados: dict) -> str | None:
    """
    Trata a sintaxe [SE campo] texto...
    - Se campo presente em dados → retorna texto sem o prefixo [SE campo]
    - Se campo ausente → retorna None (item deve ser omitido da lista)
    - Se item não começa com [SE ...] → retorna item sem alteração
    """
    m = re.match(r'^\[SE ([^\]]+)\]\s*(.*)', item, re.DOTALL)
    if m:
        campo = m.group(1).strip()
        resto = m.group(2).strip()
        return resto if dados.get(campo) else None
    return item  # não é condicional


# ═══════════════════════════════════════════════════════════
#  ENRIQUECIMENTO PRINCIPAL
# ═══════════════════════════════════════════════════════════

def enriquecer_dados(dados: dict, template: dict) -> dict:
    """
    Aplica os modelos do template em campos ausentes do dict de dados.
    Preserva 100% do conteúdo que o Gemini já produziu.

    Campos enriquecidos (somente se ausentes/vazios):
    - paragrafo_abertura  ← modelo_abertura
    - considerandos       ← modelo_considerandos (lista, com tratamento [SE campo])
    - conclusao           ← modelo_conclusao
    - documentos_emitir   ← documentos_tipicos
    """
    # ── paragrafo_abertura ─────────────────────────────────────────────────────
    if not dados.get("paragrafo_abertura"):
        modelo = template.get("modelo_abertura", "")
        if modelo:
            interpolado = _interpolar(modelo, dados).strip()
            if interpolado:
                dados["paragrafo_abertura"] = interpolado

    # ── considerandos ──────────────────────────────────────────────────────────
    considerandos_atuais = dados.get("considerandos")
    if not considerandos_atuais or (
        isinstance(considerandos_atuais, list) and len(considerandos_atuais) == 0
    ):
        modelos = template.get("modelo_considerandos", [])
        if modelos:
            resultado = []
            for item in modelos:
                # Remove prefixo [OBRIGATÓRIO] se presente (era instrução para Gemini)
                item_limpo = re.sub(r'^\[OBRIGATÓRIO\]\s*', '', item).strip()
                # Trata condicionais [SE campo]
                tratado = _tratar_condicional(item_limpo, dados)
                if tratado is None:
                    continue  # campo condicional ausente → omite
                # Interpola placeholders reais
                interpolado = _interpolar(tratado, dados).strip()
                if interpolado:
                    resultado.append(interpolado)
            if resultado:
                dados["considerandos"] = resultado

    # ── conclusao ──────────────────────────────────────────────────────────────
    if not dados.get("conclusao"):
        modelo = template.get("modelo_conclusao", "")
        if modelo:
            interpolado = _interpolar(modelo, dados).strip()
            if interpolado:
                dados["conclusao"] = interpolado

    # ── documentos_emitir ──────────────────────────────────────────────────────
    if not dados.get("documentos_emitir"):
        tipicos = template.get("documentos_tipicos", [])
        if tipicos:
            docs = []
            for d in tipicos:
                tipo_interpolado = _interpolar(d.get("tipo", ""), dados).strip()
                obs_raw = d.get("obs", "")
                obs_interpolado = _interpolar(obs_raw, dados).strip() if obs_raw else None
                if tipo_interpolado:
                    docs.append({
                        "tipo": tipo_interpolado,
                        "obs": obs_interpolado if obs_interpolado else None,
                    })
            if docs:
                dados["documentos_emitir"] = docs

    return dados
