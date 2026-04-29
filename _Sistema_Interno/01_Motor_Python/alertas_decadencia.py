"""
Alertas de Decadência Tributária — Motor GEM / SMOSU Oliveira-MG

Verifica se a área construída pode estar sujeita à decadência prevista no
Art. 150 §4º do CTN (prazo de 5 anos para lançamento do crédito tributário),
usando como evidência apenas documentos confiáveis de data de obra:

  • Habite-se anterior
  • Espelho Cadastral
  • Planta Cadastral

Referência legal:
  Art. 150, §4º CTN — decadência do direito de lançar tributo
  Art. 173 CTN       — prazo decadencial geral de 5 anos
"""

import re
from datetime import date

# Tipos onde a análise de decadência é pertinente
_TIPOS_RELEVANTES = {
    "habitese_comum", "habitese_multa", "habitese_inclusao_area",
    "certidao_averbacao_decadencia",
    "alvara_regularizacao", "regularizacao",
    "alvara_ampliacao", "alvara_reforma_demolicao_ampliacao",
}

_MESES = {
    "janeiro": 1, "fevereiro": 2, "marco": 3, "março": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
    "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12,
}


# ── Parsers de data ───────────────────────────────────────────────────────────

def _parse_data(texto: str) -> date | None:
    """Tenta extrair uma data de múltiplos formatos textuais."""
    if not texto:
        return None
    s = str(texto).strip()

    # DD/MM/AAAA ou DD-MM-AAAA
    m = re.search(r"(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})", s)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass

    # "DD de Mês de AAAA"
    m = re.search(r"(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})", s.lower())
    if m:
        mes = _MESES.get(m.group(2))
        if mes:
            try:
                return date(int(m.group(3)), mes, int(m.group(1)))
            except ValueError:
                pass

    # Só ano: "2005", "desde 2005"
    m = re.search(r"\b(19|20)(\d{2})\b", s)
    if m:
        try:
            return date(int(m.group(0)), 7, 1)  # assume meio do ano
        except ValueError:
            pass

    return None


# ── Extratores por fonte documental ──────────────────────────────────────────

def _datas_habite_se(dados: dict) -> list[tuple[date, str]]:
    """Extrai datas de habite-se anterior de campos diretos e considerandos."""
    encontradas: list[tuple[date, str]] = []

    # Campos diretos
    for campo in ("data_habitese_anterior", "data_habite_se_anterior", "habite_se_data"):
        v = dados.get(campo)
        if v:
            d = _parse_data(str(v))
            if d:
                encontradas.append((d, f"campo '{campo}'"))

    # extras_extraidos
    extras = dados.get("extras_extraidos", {})
    if isinstance(extras, dict):
        for campo in ("habitese_anterior", "habite_se_anterior", "data_habitese"):
            v = extras.get(campo)
            if v:
                d = _parse_data(str(v))
                if d:
                    encontradas.append((d, f"extras_extraidos.{campo}"))

    # Considerandos: "Habite-se nº 928/2010, datado de 06/01/2010"
    texto = " ".join(
        str(c) for c in dados.get("considerandos", []) if isinstance(c, str)
    )
    for m in re.finditer(
        r"[Hh]abite[-\s]?se\s+n[ºo]?\s*[\w/\-]+[,\s]+datado\s+de\s+([\d/\-]+)",
        texto,
    ):
        d = _parse_data(m.group(1))
        if d:
            encontradas.append((d, "habite-se mencionado nos considerandos"))

    # "Habite-se nº XXXX/AAAA" sem data explícita → usa o ano do número
    for m in re.finditer(
        r"[Hh]abite[-\s]?se\s+n[ºo]?\s*\w+[/\-](\d{4})\b",
        texto,
    ):
        ano = int(m.group(1))
        if 1950 < ano <= date.today().year:
            encontradas.append((date(ano, 7, 1), f"ano do número do habite-se (/{ano})"))

    return encontradas


def _datas_espelho_planta(dados: dict) -> list[tuple[date, str]]:
    """Extrai datas de espelho cadastral e planta cadastral."""
    encontradas: list[tuple[date, str]] = []

    for campo in ("data_espelho_cadastral", "data_planta_cadastral", "data_cadastro"):
        v = dados.get(campo)
        if v:
            d = _parse_data(str(v))
            if d:
                encontradas.append((d, f"campo '{campo}'"))

    extras = dados.get("extras_extraidos", {})
    if isinstance(extras, dict):
        for campo in ("espelho_cadastral_data", "planta_cadastral_data"):
            v = extras.get(campo)
            if v:
                d = _parse_data(str(v))
                if d:
                    encontradas.append((d, f"extras_extraidos.{campo}"))

    return encontradas


def _datas_conclusao(dados: dict) -> list[tuple[date, str]]:
    """Extrai data_conclusao_obra de campos diretos."""
    encontradas: list[tuple[date, str]] = []
    for campo in ("data_conclusao_obra", "data_conclusao", "data_obra_concluida"):
        v = dados.get(campo)
        if v:
            d = _parse_data(str(v))
            if d:
                encontradas.append((d, f"campo '{campo}'"))
    return encontradas


# ── Função principal ──────────────────────────────────────────────────────────

def verificar(dados: dict) -> dict:
    """
    Verifica possibilidade de decadência tributária no processo.

    Retorna dict com:
      aplicavel       — bool: se o tipo de documento é relevante para decadência
      status          — "PLENA" | "PROXIMA" | "NAO_DECADENTE" | "INDETERMINADA"
      anos            — float: anos decorridos desde a data de referência
      data_referencia — str:   data de referência no formato DD/MM/AAAA
      fonte           — str:   descrição da fonte que forneceu a data
      avisos          — list:  alertas e recomendações
    """
    tipo = dados.get("tipo_relatorio", "")
    resultado: dict = {
        "aplicavel":       tipo in _TIPOS_RELEVANTES,
        "status":          None,
        "anos":            None,
        "data_referencia": None,
        "fonte":           None,
        "avisos":          [],
    }

    if not resultado["aplicavel"]:
        return resultado

    hoje = date.today()

    # Coleta de todas as candidatas (prioridade: conclusão > habite-se > espelho/planta)
    candidatas: list[tuple[date, str]] = (
        _datas_conclusao(dados) +
        _datas_habite_se(dados) +
        _datas_espelho_planta(dados)
    )

    # Filtra datas futuras (erro de digitação)
    candidatas = [(d, f) for d, f in candidatas if d < hoje]

    if not candidatas:
        resultado["status"] = "INDETERMINADA"
        resultado["avisos"].append(
            "Nenhuma data de conclusão de obra, habite-se ou cadastro encontrada. "
            "Verifique manualmente se há decadência aplicável (Art. 150 §4º CTN). "
            "Para registrar: adicione 'data_conclusao_obra' ou 'data_habitese_anterior' ao JSON."
        )
        return resultado

    # Usa a data mais antiga como referência (máximo benefício ao proprietário)
    data_ref, fonte = min(candidatas, key=lambda x: x[0])
    anos = (hoje - data_ref).days / 365.25

    resultado["data_referencia"] = data_ref.strftime("%d/%m/%Y")
    resultado["fonte"]           = fonte
    resultado["anos"]            = round(anos, 1)

    if anos >= 5.0:
        resultado["status"] = "PLENA"
        resultado["avisos"].append(
            f"Decadência PLENA: {anos:.1f} anos decorridos. "
            "A multa do Art. 79 Lei 1.544/86 pode estar dispensada sobre a área decadente. "
            "Verificar emissão de certidao_averbacao_decadencia."
        )
    elif anos >= 4.0:
        meses_restantes = int(round((5.0 - anos) * 12))
        resultado["status"] = "PROXIMA"
        resultado["avisos"].append(
            f"Decadência PRÓXIMA: {anos:.1f} anos (prazo vence em ~{meses_restantes} mês(es)). "
            "Verificar urgência da emissão e se a contagem está correta."
        )
    else:
        resultado["status"] = "NAO_DECADENTE"

    return resultado


# ── Impressão formatada ───────────────────────────────────────────────────────

def imprimir_relatorio(res: dict) -> None:
    """Imprime relatório formatado da análise de decadência."""
    if not res["aplicavel"]:
        return

    SEP    = "-" * 62
    status = res["status"]
    anos   = res["anos"]
    data_r = res["data_referencia"]
    fonte  = res["fonte"]

    print(f"\n{SEP}")
    print("  ANÁLISE DE DECADÊNCIA TRIBUTÁRIA (Art. 150 §4º CTN)")
    print(SEP)

    if status == "PLENA":
        print(f"  [DECADÊNCIA PLENA]  {anos} anos desde {data_r}")
        print(f"  Fonte: {fonte}")
        print("  → Prazo de 5 anos VENCIDO.")
        print("    Multa do Art. 79 dispensável na área decadente.")
        print("    Incluir certidao_averbacao_decadencia nos documentos a emitir.")
    elif status == "PROXIMA":
        print(f"  [ATENÇÃO — PRÓXIMA]  {anos} anos desde {data_r}")
        print(f"  Fonte: {fonte}")
        print("  → Prazo de 5 anos ainda não vencido, mas próximo.")
    elif status == "NAO_DECADENTE":
        print(f"  [OK — SEM DECADÊNCIA]  {anos} anos desde {data_r}")
        print(f"  Fonte: {fonte}")
        print("  → Multas do Art. 79 aplicáveis normalmente.")
    else:
        print("  [?] INDETERMINADA — nenhuma data de obra encontrada no JSON.")

    for a in res["avisos"]:
        print(f"\n  [i] {a}")

    print(SEP)
