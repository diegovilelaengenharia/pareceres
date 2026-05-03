"""
Memória Ativa de Precedentes — Motor GEM / SMOSU Oliveira-MG

Consulta o histórico de JSONs arquivados por registrar_aprendizado.py
e exibe os casos mais similares ao processo atual, para referência
de linguagem, conclusão e padrões de emissão.

Os JSONs são lidos de:
  _Sistema_Interno/01_Motor_Python/historico_pareceres/
"""

import json
from datetime import datetime
from pathlib import Path

SCRIPT_DIR    = Path(__file__).parent
HISTORICO_DIR = SCRIPT_DIR / "historico_pareceres"

_N_PADRAO = 3  # número de precedentes a exibir


# ── Carregamento do histórico ─────────────────────────────────────────────────

def _carregar_historico() -> list[dict]:
    """Carrega todos os JSONs de historico_pareceres/, do mais recente ao mais antigo."""
    if not HISTORICO_DIR.exists():
        return []

    arquivos = sorted(
        HISTORICO_DIR.glob("*.json"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )

    casos: list[dict] = []
    for arq in arquivos:
        try:
            dados = json.loads(arq.read_text(encoding="utf-8"))
            dados["_arquivo"] = arq.name
            dados["_mtime"]   = arq.stat().st_mtime
            casos.append(dados)
        except Exception:
            continue

    return casos


# ── Similaridade ──────────────────────────────────────────────────────────────

def _score(caso: dict, atual: dict) -> int:
    """Pontua similaridade. Maior = mais relevante."""
    score = 0

    # Mesmo tipo de documento → forte relevância
    if caso.get("tipo_relatorio") == atual.get("tipo_relatorio"):
        score += 10

    # Mesma zona urbanística
    zona_a = str(atual.get("zona_uso", "")).upper().strip()
    zona_c = str(caso.get("zona_uso", "")).upper().strip()
    if zona_a and zona_a == zona_c:
        score += 5

    # Mesmo bairro
    bairro_a = str(atual.get("bairro", "")).strip().lower()
    bairro_c = str(caso.get("bairro", "")).strip().lower()
    if bairro_a and bairro_c and bairro_a == bairro_c:
        score += 2

    # Flags similares (comparação textual rápida)
    texto_a = json.dumps(atual,  ensure_ascii=False).lower()
    texto_c = json.dumps(caso,   ensure_ascii=False).lower()
    for palavra in ("decadência", "multa", "art. 79", "anuência", "app", "as built"):
        if palavra in texto_a and palavra in texto_c:
            score += 1

    return score


# ── Busca principal ───────────────────────────────────────────────────────────

def buscar(dados: dict, n: int = _N_PADRAO) -> list[dict]:
    """
    Retorna os N casos mais similares ao processo atual.
    Cada item do resultado é o dict completo do JSON arquivado,
    com as chaves extras '_arquivo' e '_mtime'.
    """
    historico = _carregar_historico()
    if not historico:
        return []

    scorados = [(caso, _score(caso, dados)) for caso in historico]
    scorados.sort(key=lambda x: (-x[1], -x[0]["_mtime"]))

    # Retorna apenas casos com alguma similaridade (score > 0)
    return [c for c, s in scorados if s > 0][:n]


# ── Impressão formatada ───────────────────────────────────────────────────────

def imprimir_relatorio(dados: dict, n: int = _N_PADRAO) -> None:
    """Exibe precedentes similares ao processo atual."""
    SEP  = "-" * 62
    tipo = dados.get("tipo_relatorio", "?")

    print(f"\n{SEP}")
    print(f"  PRECEDENTES — Casos Similares (tipo: {tipo})")
    print(SEP)

    historico_dir_existe = HISTORICO_DIR.exists()
    tem_arquivos = historico_dir_existe and any(HISTORICO_DIR.glob("*.json"))

    if not historico_dir_existe or not tem_arquivos:
        print("  [i] Histórico ainda vazio.")
        print("      Após processar cada caso, execute:")
        print("      python registrar_aprendizado.py")
        print(SEP)
        return

    casos = buscar(dados, n)

    if not casos:
        print(f"  [i] Nenhum precedente similar encontrado (tipo='{tipo}').")
        print(SEP)
        return

    tipo_atual = dados.get("tipo_relatorio", "")

    for i, caso in enumerate(casos, 1):
        processo  = caso.get("numero_processo", "?")
        requerente = (
            caso.get("requerente") or
            caso.get("proprietario_nome") or
            "Desconhecido"
        )
        tipo_caso  = caso.get("tipo_relatorio", "?")
        zona_caso  = caso.get("zona_uso", "—")
        bairro_caso = caso.get("bairro", "—")
        arquivo    = caso.get("_arquivo", "")

        # Data a partir do nome do arquivo (prefixo YYYYMMDD_HHMMSS_)
        data_str = ""
        if arquivo and len(arquivo) >= 8 and arquivo[:8].isdigit():
            try:
                data_str = f" ({arquivo[6:8]}/{arquivo[4:6]}/{arquivo[:4]})"
            except Exception:
                pass

        # Conclusão resumida
        conclusao_completa = str(caso.get("conclusao", ""))
        conclusao_resumida = conclusao_completa[:120]
        if len(conclusao_completa) > 120:
            conclusao_resumida += "…"

        # Marcador de similaridade
        marcador = "[=]" if tipo_caso == tipo_atual else "[~]"

        print(f"\n  {marcador} {i}. Proc. {processo} — {requerente}{data_str}")
        print(f"      Tipo: {tipo_caso}  |  Zona: {zona_caso}  |  Bairro: {bairro_caso}")
        if conclusao_resumida:
            print(f"      Conclusão: {conclusao_resumida}")
        print(f"      Arquivo: historico_pareceres/{arquivo}")

    print(f"\n{SEP}")

