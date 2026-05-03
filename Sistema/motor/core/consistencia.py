"""
Verificador de Consistência Semântica — Motor GEM / SMOSU Oliveira-MG

Realiza checagens cruzadas que o schema_validator não faz:
detecta contradições internas entre os campos do JSON — campos que são
estruturalmente válidos mas semanticamente inconsistentes entre si.

Diferença do schema_validator:
  schema_validator  → "a chave existe e tem o tipo certo?"
  consistencia      → "os valores fazem sentido juntos?"
"""

import re

# ── Agrupamentos de tipos por categoria semântica ─────────────────────────────

_APROVACAO = {
    "alvara_aprovacao", "alvara_regularizacao", "alvara_ampliacao",
    "alvara_galpao_comercial", "alvara_reforma_demolicao_ampliacao",
    "alvara_substituicao_projeto", "regularizacao",
    "habitese_comum", "habitese_multa", "habitese_inclusao_area",
    "certidao_averbacao_decadencia",
    "certidao_numero_2via", "certidao_nome_rua", "certidao_localizacao",
    "certidao_conjunta", "certidao_numero_comercial",
    "alvara_renovacao", "alvara_cancelamento", "alvara_substituicao_titular",
    "alvara_demolicao", "certidao_demolicao",
    "certidao_desmembramento", "certidao_retificacao_area",
    "habitese_2via",
}

_PENDENCIA  = {"comunicado_pendencia"}
_RECUSA     = {"comunicado_indeferimento"}

_HABITE_SE  = {"habitese_comum", "habitese_multa", "habitese_inclusao_area", "habitese_2via"}

_PRECISA_DATA_DECADENCIA = {
    "habitese_multa", "certidao_averbacao_decadencia",
    "alvara_regularizacao", "regularizacao",
    "alvara_reforma_demolicao_ampliacao",
}

_TECNICO = {
    "alvara_aprovacao", "alvara_regularizacao", "alvara_ampliacao",
    "alvara_galpao_comercial", "alvara_reforma_demolicao_ampliacao",
    "alvara_substituicao_projeto", "regularizacao",
}

# Termos ambientais que sinalizam necessidade de ofício ao CODEMA
_TERMOS_AMBIENTAIS = [
    "app", "área de preservação permanente", "area de preservacao permanente",
    "córrego", "corrego", "rio ", "ribeirão", "ribeirao", "nascente",
    "faixa de proteção", "faixa de protecao", "faixa marginal",
    "codema", "meio ambiente", "lei 3.971", "lei 6.766",
    "reserva legal", "mata ciliar",
]

# Palavras que indicam que a conclusão é negativa/pendente
_PALAVRAS_NEGATIVAS = [
    "pendência", "pendente", "indefiro", "indeferido", "indeferimento",
    "não atende", "não conformidade", "aguardando", "impossibilidade",
]

# Palavras que "salvam" um texto negativo (situação resolvida)
_PALAVRAS_SALVO = ["sanado", "sanou", "cumprido", "cumpriu", "resolvido"]


# ── Utilitários ───────────────────────────────────────────────────────────────

def _num(texto) -> float | None:
    """
    Converte texto para float, removendo caracteres não numéricos exceto ponto e vírgula.
    Interno para o módulo de consistência.
    """
    if not texto:
        return None
    limpo = re.sub(r"[^\d,.]", "", str(texto)).replace(",", ".")
    try:
        return float(limpo) if limpo else None
    except ValueError:
        return None


def _texto_campo(dados: dict, *chaves) -> str:
    """
    Concatena o texto de várias chaves (string ou lista de strings) para busca textual.
    
    Args:
        dados: Dicionário do processo.
        *chaves: Nomes das chaves a serem concatenadas.
        
    Returns:
        String única em minúsculas com o conteúdo dos campos.
    """
    partes = []
    for chave in chaves:
        v = dados.get(chave, "")
        if isinstance(v, list):
            partes.extend(str(i) for i in v)
        elif v:
            partes.append(str(v))
    return " ".join(partes).lower()


# ── Verificações ──────────────────────────────────────────────────────────────

def verificar(dados: dict) -> tuple[list[str], list[str]]:
    """
    Verifica a consistência semântica do JSON do processo administrativo.
    Identifica contradições entre campos (ex: tipo de aprovação com conclusão negativa).

    Args:
        dados: O dicionário JSON extraído do processo.

    Returns:
        Uma tupla (erros, avisos) contendo as strings de inconsistência detectadas.
    """
    erros:  list[str] = []
    avisos: list[str] = []

    tipo       = dados.get("tipo_relatorio", "")
    conclusao  = str(dados.get("conclusao",  "")).lower()
    considerandos_txt = _texto_campo(dados, "considerandos")
    fund_txt   = _texto_campo(dados, "fundamentacao_legal")
    condicoes  = dados.get("condicoes_pendentes", [])
    docs_emitir = dados.get("documentos_emitir", [])

    # ── 1. Comunicado de pendência com documento final na lista de emissão ────
    if tipo in _PENDENCIA:
        for doc in docs_emitir:
            tipo_doc = str(doc.get("tipo", "") if isinstance(doc, dict) else doc).lower()
            if re.search(r"alvar[aá]|habite[-\s]?se", tipo_doc):
                erros.append(
                    f"CONTRADIÇÃO: tipo='{tipo}' (comunicado de pendência) mas "
                    f"documentos_emitir contém '{tipo_doc[:70]}'. "
                    "Comunicados de pendência não emitem alvarás — verifique o tipo_relatorio."
                )

    # ── 2. Tipo de aprovação mas conclusão sugere recusa/pendência ────────────
    if tipo in _APROVACAO:
        conclusao_negativa = any(p in conclusao for p in _PALAVRAS_NEGATIVAS)
        conclusao_salva    = any(p in conclusao for p in _PALAVRAS_SALVO)
        if conclusao_negativa and not conclusao_salva:
            palavra_encontrada = next(p for p in _PALAVRAS_NEGATIVAS if p in conclusao)
            avisos.append(
                f"POSSÍVEL CONTRADIÇÃO: tipo='{tipo}' sugere aprovação, mas a conclusão "
                f"contém '{palavra_encontrada}'. "
                "Verifique se o tipo de documento está correto."
            )

    # ── 3. condicoes_pendentes não vazio sem tipo ou conclusão condicionada ───
    if isinstance(condicoes, list) and condicoes:
        tipo_eh_pendencia  = tipo in _PENDENCIA
        conclusao_cond     = "condicionado" in conclusao or "condicionante" in conclusao
        if not tipo_eh_pendencia and not conclusao_cond:
            avisos.append(
                f"'condicoes_pendentes' tem {len(condicoes)} item(ns) preenchido(s), "
                f"mas tipo='{tipo}' não é comunicado_pendencia e a conclusão não menciona "
                "'condicionado'. Verifique se o modo de emissão está correto."
            )

    # ── 4. Parecer técnico sem fundamentação legal ────────────────────────────
    if tipo in _TECNICO and not dados.get("fundamentacao_legal"):
        avisos.append(
            f"Parecer técnico ('{tipo}') sem 'fundamentacao_legal'. "
            "Pareceres técnicos devem ter fundamentação legal explícita para solidez jurídica."
        )

    # ── 5. Divergência entre area_total_construida e soma de areas_matriz ─────
    areas   = dados.get("areas_matriz", [])
    at_gem  = _num(dados.get("area_total_construida"))
    if areas and at_gem is not None:
        total_calc = sum(
            (_num(item.get("area_m2", 0)) or 0.0)
            for item in areas
            if isinstance(item, dict)
        )
        if abs(total_calc - at_gem) > 0.5:
            avisos.append(
                f"area_total_construida ({at_gem}m²) ≠ soma de areas_matriz "
                f"({total_calc:.2f}m²) — diferença de {abs(total_calc - at_gem):.2f}m². "
                "Confira o quadro de áreas."
            )

    # ── 6. Tipo que exige análise de decadência sem qualquer data de referência
    if tipo in _PRECISA_DATA_DECADENCIA:
        tem_data = (
            dados.get("data_conclusao_obra") or
            dados.get("data_habitese_anterior") or
            dados.get("habite_se_anterior") or
            (isinstance(dados.get("extras_extraidos"), dict) and
             dados["extras_extraidos"].get("habitese_anterior"))
        )
        if not tem_data:
            # Última tentativa: buscar padrão de habite-se nos considerandos
            tem_data = bool(re.search(
                r"[Hh]abite[-\s]?se|conclus[ãa]o\s+de\s+obra|decad[eê]ncia",
                considerandos_txt,
            ))
        if not tem_data:
            avisos.append(
                f"Tipo '{tipo}' normalmente exige análise de decadência, mas nenhuma "
                "data de conclusão de obra ou habite-se anterior foi encontrada no JSON. "
                "Verifique se a decadência foi considerada e registre "
                "'data_conclusao_obra' ou 'data_habitese_anterior'."
            )

    # ── 7. Art. 79 citado sem valor monetário correspondente ──────────────────
    cita_art79 = "art. 79" in fund_txt or "art.79" in fund_txt
    if cita_art79:
        tem_valor = (
            dados.get("valor_total_multas") or
            dados.get("valor_multa") or
            re.search(r"r\$\s*[\d.,]+", considerandos_txt)
        )
        if not tem_valor:
            avisos.append(
                "Art. 79 (multa por construção sem licença) citado na fundamentação legal, "
                "mas nenhum valor monetário (R$) foi encontrado em considerandos ou campos "
                "'valor_total_multas'/'valor_multa'. "
                "Confirme se o memorial de cálculo da multa está incluído."
            )

    # ── 8. Habite-se sem referência a vistoria ou fiscal ─────────────────────
    if tipo in _HABITE_SE:
        texto_geral = considerandos_txt + " " + _texto_campo(dados, "paragrafo_abertura")
        tem_vistoria = re.search(r"fiscal|vistoria|agente|inspe[çc][ãa]o", texto_geral)
        if not tem_vistoria and not dados.get("data_vistoria") and not dados.get("fiscal_responsavel"):
            avisos.append(
                f"Habite-se ('{tipo}') sem referência a vistoria ou agente fiscal nos "
                "considerandos. Habite-se normalmente exige vistoria prévia — "
                "verifique se está documentada."
            )

    # ── 9. FAVORÁVEL na conclusão sem documentos a emitir ────────────────────
    if tipo in _APROVACAO and "favorável" in conclusao and not docs_emitir:
        avisos.append(
            "Conclusão FAVORÁVEL mas 'documentos_emitir' está vazio. "
            "Confirme quais documentos serão emitidos como resultado do parecer."
        )

    # ── 10. TRT: técnico CFT sem número TRT no paragrafo_abertura ────────────
    prof_nome = str(dados.get("profissional_nome", "")).lower()
    abertura  = str(dados.get("paragrafo_abertura", "")).lower()
    if re.search(r"\bcft\b|\bcrt\b|técnico em edificações|tecnico em edificacoes", prof_nome):
        if not re.search(r"\btrt\b|n[oº°]\s*[a-z0-9]{8,}", abertura):
            avisos.append(
                "ATENÇÃO TRT: 'profissional_nome' indica Técnico em Edificações (CFT/CRT), "
                "mas o número do TRT não foi encontrado em 'paragrafo_abertura'. "
                "O TRT deve aparecer: (a) no paragrafo_abertura junto ao nome do profissional; "
                "(b) em um considerando específico. Ver CASO-5 (Proc. 8901/2025)."
            )

    # ── 11. Decreto 4.149/2019 ausente na fundamentação de pareceres técnicos ─
    if tipo in _TECNICO and dados.get("fundamentacao_legal"):
        fund_list = dados["fundamentacao_legal"]
        fund_completa = " ".join(str(i) for i in fund_list).lower() if isinstance(fund_list, list) else str(fund_list).lower()
        if "4.149" not in fund_completa and "decreto" not in fund_completa:
            avisos.append(
                f"Parecer técnico ('{tipo}') sem referência ao Decreto 4.149/2019 na "
                "'fundamentacao_legal'. O Decreto deve ser citado como primeiro instrumento, "
                "antes da Lei 1.544/86 e da LC 267/2019. Ver CASO-5 (Proc. 8901/2025)."
            )
        elif "4.149" in fund_completa:
            # Verificar se é o primeiro item da lista
            if isinstance(fund_list, list) and fund_list:
                primeiro = str(fund_list[0]).lower()
                if "4.149" not in primeiro:
                    avisos.append(
                        "Decreto 4.149/2019 encontrado na fundamentação legal, mas não é o "
                        "primeiro item. Deve preceder a Lei 1.544/86 e a LC 267/2019."
                    )

    # ── 12. Auto-routing ambiental (APP/CODEMA) ───────────────────────────────
    _NAO_APLICA_AMBIENTAL = {"oficio_meio_ambiente", "comunicado_pendencia", "comunicado_indeferimento"}
    if tipo not in _NAO_APLICA_AMBIENTAL:
        texto_ambiental = _texto_campo(
            dados, "considerandos", "paragrafo_abertura",
            "conclusao", "observacoes_fiscais",
        )
        extras = dados.get("extras_extraidos", {})
        if isinstance(extras, dict):
            texto_ambiental += " " + str(extras.get("observacoes_fiscais", "")).lower()

        detectou_ambiental = any(t in texto_ambiental for t in _TERMOS_AMBIENTAIS)
        if detectou_ambiental:
            # Verificar se já há ofício ambiental nos documentos a emitir
            tipos_docs_emitir = [
                str(d.get("tipo", "") if isinstance(d, dict) else d).lower()
                for d in docs_emitir
            ]
            tem_oficio_amb = any("meio ambiente" in t or "codema" in t or "ambiental" in t
                                 for t in tipos_docs_emitir)
            if not tem_oficio_amb:
                avisos.append(
                    "AUTO-ROUTING AMBIENTAL: Termos de APP/CODEMA detectados no texto do processo. "
                    "Verifique se é necessário emitir 'oficio_meio_ambiente' em paralelo ao parecer. "
                    "Se sim, adicione-o em 'documentos_emitir' ou gere um JSON separado."
                )

    return erros, avisos


# ── Impressão formatada ───────────────────────────────────────────────────────

def imprimir_relatorio(erros: list[str], avisos: list[str], tipo: str) -> None:
    """Imprime relatório de consistência semântica."""
    if not erros and not avisos:
        return

    SEP = "-" * 62
    print(f"\n{SEP}")
    print(f"  CONSISTÊNCIA SEMÂNTICA — {tipo}")
    print(SEP)

    for e in erros:
        print(f"  [ERRO]  {e}")
    for a in avisos:
        print(f"  [AVISO] {a}")

    print(SEP)

