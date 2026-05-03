"""
Calculadora de Índices Urbanísticos — Motor GEM / SMOSU Oliveira-MG

Valida TO, CA e TP informados pelo Gem contra os limites da zona urbanística,
e faz cross-check via soma de areas_matriz quando disponível.

Referência: LC 267/2019 (Uso e Ocupação do Solo) — Oliveira/MG
            §13 Art. 9º LC 267/2019 — isenção de lote <= 220m²

ATENÇÃO: Verifique os valores de LIMITES_ZONA contra o texto da LC 267/2019.
"""

import re
import json
from core.base_engine import BaseEngine

# ── Limites por zona urbanística (LC 267/2019 e Lei 313) ──────────────────────
# to_max : Taxa de Ocupação máxima (%)
# ca_max : Coeficiente de Aproveitamento máximo
# tp_min : Taxa de Permeabilidade mínima (%)
LIMITES_ZONA: dict[str, dict] = {
    "ZUR1": {"to_max": 50.0, "ca_max": 1.0,  "tp_min": 30.0}, # Exemplos de ZUR (confirmar valores)
    "ZUR2": {"to_max": 60.0, "ca_max": 2.0,  "tp_min": 20.0},
    "ZUR3": {"to_max": 70.0, "ca_max": 2.5,  "tp_min": 20.0},
    "ZUR":  {"to_max": 70.0, "ca_max": 2.0,  "tp_min": 20.0}, # Fallback genérico para ZUR
    "ZC":   {"to_max": 80.0, "ca_max": 3.0,  "tp_min": 10.0},
}

# Fallback quando zona não é identificada
_LIMITE_PADRAO = {"to_max": 70.0, "ca_max": 2.0, "tp_min": 20.0}

# Tipos de documento onde os índices urbanísticos são aplicáveis
_TIPOS_COM_INDICE = {
    "alvara_aprovacao", "alvara_regularizacao", "alvara_ampliacao",
    "alvara_galpao_comercial", "alvara_reforma_demolicao_ampliacao",
    "alvara_substituicao_projeto", "regularizacao",
    "habitese_comum", "habitese_multa", "habitese_inclusao_area",
}


# ── Utilitários ───────────────────────────────────────────────────────────────

def _normalizar_zona(z: str) -> str:
    """Normaliza sigla: remove espaços e zeros iniciais em números (ex: 'ZUR 02' → 'ZUR2')."""
    z = re.sub(r'\s+', '', z).upper()
    z = re.sub(r'(?<=[A-Z])0+(\d)', r'\1', z)
    return z


def _detectar_zona(dados: dict) -> str:
    """Retorna zona de 'zona_uso' ou varre todo o JSON em busca de sigla."""
    zona = _normalizar_zona(str(dados.get("zona_uso", "")))
    if zona in LIMITES_ZONA:
        return zona
    # Varredura textual com suporte a variantes com espaço e zero (ex: "ZUR 02")
    texto = json.dumps(dados, ensure_ascii=False).upper()
    for z in LIMITES_ZONA:
        if z in texto:
            return z
        m = re.match(r'^([A-Z]+)(\d+)$', z)
        if m:
            prefix, num = m.groups()
            if re.search(rf'{prefix}\s*0*{num}(?!\d)', texto):
                return z
    return ""


# ── Função principal ──────────────────────────────────────────────────────────

def calcular(dados: dict) -> dict:
    """
    Calcula e valida índices urbanísticos a partir do JSON do processo.

    Retorna dict com:
      aplicavel    — bool: se o tipo de documento usa índices
      zona         — str: zona identificada
      limites      — dict: to_max, ca_max, tp_min da zona
      gem          — dict: valores informados pelo Gem
      areas_calc   — dict: cálculo independente via areas_matriz (se presente)
      erros        — list: violações de limite (bloqueantes no parecer)
      avisos       — list: alertas não-bloqueantes
      divergencias — list: discrepâncias entre Gem e cálculo independente
    """
    tipo = dados.get("tipo_relatorio", "")
    resultado: dict = {
        "aplicavel":    tipo in _TIPOS_COM_INDICE,
        "zona":         "",
        "limites":      {},
        "gem":          {},
        "areas_calc":   {},
        "erros":        [],
        "avisos":       [],
        "divergencias": [],
    }

    if not resultado["aplicavel"]:
        return resultado

    # ── Zona e limites ────────────────────────────────────────────────────────
    zona = _detectar_zona(dados)
    resultado["zona"] = zona or "NÃO IDENTIFICADA"
    limites = LIMITES_ZONA.get(zona, _LIMITE_PADRAO)
    resultado["limites"] = limites

    if not zona:
        msg = (
            "Zona urbanística não identificada. Adicione 'zona_uso' ao JSON "
            "(ex: 'ZUR3', 'OCRE'). Usando limites genéricos: "
            f"TO<={_LIMITE_PADRAO['to_max']}%, CA<={_LIMITE_PADRAO['ca_max']}, "
            f"TP>={_LIMITE_PADRAO['tp_min']}%."
        )
        resultado["avisos"].append(msg)
        BaseEngine.log_report("WARN", msg, {"context": "identificacao_zona"})

    # ── Valores do Gem ────────────────────────────────────────────────────────
    to_g  = BaseEngine.parse_number(dados.get("taxa_ocupacao"))
    tp_g  = BaseEngine.parse_number(dados.get("taxa_permeabilidade"))
    ca_g  = BaseEngine.parse_number(dados.get("coef_aproveitamento"))
    at_g  = BaseEngine.parse_number(dados.get("area_terreno"))
    ac_g  = BaseEngine.parse_number(dados.get("area_total_construida"))

    resultado["gem"] = {
        "to": to_g, "tp": tp_g, "ca": ca_g,
        "area_terreno": at_g, "area_total": ac_g,
    }

    # ── Exceção de lote pequeno (§13 Art. 9º LC 267/2019) ────────────────────
    lote_pequeno = at_g is not None and at_g <= 220.0
    if lote_pequeno:
        resultado["avisos"].append(
            f"Lote <= 220m² ({at_g}m²) — §13 Art. 9º LC 267/2019: "
            "TO e TP não se aplicam (exceção de lei)."
        )

    # ── Cross-check via areas_matriz ──────────────────────────────────────────
    areas = dados.get("areas_matriz", [])
    if areas:
        total_calc = sum(
            (BaseEngine.parse_number(item.get("area_m2", 0)) or 0.0)
            for item in areas
            if isinstance(item, dict)
        )
        resultado["areas_calc"]["total_m2"] = round(total_calc, 2)

        if at_g and at_g > 0:
            resultado["areas_calc"]["ca_calc"] = round(total_calc / at_g, 2)

        if ac_g is not None and abs(total_calc - ac_g) > 0.5:
            resultado["divergencias"].append(
                f"Soma de areas_matriz ({total_calc:.2f}m²) ≠ "
                f"area_total_construida ({ac_g:.2f}m²) — "
                f"diferença de {abs(total_calc - ac_g):.2f}m²."
            )

    # ── Validações dos índices ────────────────────────────────────────────────
    if not lote_pequeno:
        if to_g is not None:
            if to_g > limites["to_max"]:
                msg = (
                    f"TO EXCEDE O LIMITE: {to_g:.2f}% > {limites['to_max']}% "
                    f"(zona {resultado['zona']}). Verificar multa ou exceção."
                )
                resultado["erros"].append(msg)
                BaseEngine.log_report("ERR", msg, {"to_gem": to_g, "to_lim": limites["to_max"], "zona": zona})
        else:
            msg = "'taxa_ocupacao' ausente — não foi possível validar TO."
            resultado["avisos"].append(msg)
            BaseEngine.log_report("WARN", msg)

        if tp_g is not None:
            if tp_g < limites["tp_min"]:
                msg = (
                    f"TP ABAIXO DO MÍNIMO: {tp_g:.2f}% < {limites['tp_min']}% "
                    f"(zona {resultado['zona']}). Verificar multa ou exceção."
                )
                resultado["erros"].append(msg)
                BaseEngine.log_report("ERR", msg, {"tp_gem": tp_g, "tp_lim": limites["tp_min"], "zona": zona})
        else:
            msg = "'taxa_permeabilidade' ausente — não foi possível validar TP."
            resultado["avisos"].append(msg)
            BaseEngine.log_report("WARN", msg)

    if ca_g is not None:
        if ca_g > limites["ca_max"]:
            msg = (
                f"CA EXCEDE O LIMITE: {ca_g:.2f} > {limites['ca_max']} "
                f"(zona {resultado['zona']}). Verificar multa ou exceção."
            )
            resultado["erros"].append(msg)
            BaseEngine.log_report("ERR", msg, {"ca_gem": ca_g, "ca_lim": limites["ca_max"], "zona": zona})
    else:
        msg = "'coef_aproveitamento' ausente — não foi possível validar CA."
        resultado["avisos"].append(msg)
        BaseEngine.log_report("WARN", msg)

    # Divergência CA entre Gem e soma de areas_matriz
    ca_calc = resultado["areas_calc"].get("ca_calc")
    if ca_g is not None and ca_calc is not None and abs(ca_g - ca_calc) > 0.05:
        resultado["divergencias"].append(
            f"CA diverge: Gem={ca_g} vs calculado via areas_matriz={ca_calc} "
            f"(dif={abs(ca_g - ca_calc):.2f})."
        )

    # ── Validar excecoes_aplicadas ────────────────────────────────────────────
    excecoes = dados.get("excecoes_aplicadas", [])
    if isinstance(excecoes, list):
        for exc in excecoes:
            if not isinstance(exc, dict):
                continue
            tipo_exc = str(exc.get("tipo", "")).lower()

            # Exceção de lote pequeno: verificar se área realmente ≤ 220m²
            if "lote_pequeno" in tipo_exc or "220" in tipo_exc:
                if at_g is not None and at_g > 220.0:
                    resultado["erros"].append(
                        f"EXCEÇÃO INVÁLIDA: 'excecoes_aplicadas' declara lote ≤ 220m² "
                        f"(Art. 15 LC 267/2019), mas area_terreno = {at_g}m². "
                        "Remova a exceção ou corrija a área."
                    )
                elif at_g is not None:
                    resultado["avisos"].append(
                        f"Exceção de lote pequeno confirmada: {at_g}m² ≤ 220m² "
                        "(Art. 15 LC 267/2019) — TO e TP não se aplicam."
                    )

            # Exceção de decadência: verificar se campo de data existe
            if "decad" in tipo_exc:
                tem_data = (
                    dados.get("data_conclusao_obra") or
                    dados.get("data_habitese_anterior") or
                    (isinstance(dados.get("extras_extraidos"), dict) and
                     dados["extras_extraidos"].get("habitese_anterior"))
                )
                if not tem_data:
                    resultado["avisos"].append(
                        "Exceção de decadência declarada em 'excecoes_aplicadas', "
                        "mas 'data_conclusao_obra' ou 'data_habitese_anterior' não encontrados. "
                        "Inclua a data para que o módulo de decadência possa confirmar o prazo."
                    )

    return resultado


# ── Impressão formatada ───────────────────────────────────────────────────────

def _status(ok) -> str:
    if ok is True:
        return "[OK]"
    if ok is False:
        return "[EXCEDE]"
    return "-"


def imprimir_relatorio(res: dict) -> None:
    """Imprime relatório formatado da verificação de índices."""
    if not res["aplicavel"]:
        return

    SEP = "-" * 62
    zona  = res["zona"]
    lim   = res["limites"]
    gem   = res["gem"]
    calc  = res["areas_calc"]

    print(f"\n{SEP}")
    print(f"  CALCULADORA DE ÍNDICES URBANÍSTICOS — {zona}")
    print(SEP)
    if lim:
        print(
            f"  Limites da zona:  "
            f"TO <= {lim.get('to_max')}%  |  "
            f"CA <= {lim.get('ca_max')}  |  "
            f"TP >= {lim.get('tp_min')}%"
        )
    at  = gem.get("area_terreno")
    atc = gem.get("area_total")
    print(f"  Área terreno: {at if at else '?'}m²  |  Área total: {atc if atc else '?'}m²")
    print()
    print(f"  {'Índice':<8} {'Gem informou':>14} {'Limite':>10} {'Status':>10}")
    print(f"  {'-'*8} {'-'*14} {'-'*10} {'-'*10}")

    # TO
    to_val = gem.get("to")
    to_ok  = (to_val <= lim["to_max"]) if to_val is not None and lim else None
    to_str = f"{to_val:.2f}%" if to_val is not None else "-"
    print(f"  {'TO':<8} {to_str:>14} {('<=' + str(lim.get('to_max')) + '%'):>10} {_status(to_ok):>10}")

    # CA
    ca_val = gem.get("ca")
    ca_ok  = (ca_val <= lim["ca_max"]) if ca_val is not None and lim else None
    ca_str = f"{ca_val}" if ca_val is not None else "-"
    print(f"  {'CA':<8} {ca_str:>14} {('<=' + str(lim.get('ca_max'))):>10} {_status(ca_ok):>10}")

    # TP
    tp_val = gem.get("tp")
    tp_ok  = (tp_val >= lim["tp_min"]) if tp_val is not None and lim else None
    tp_str = f"{tp_val:.2f}%" if tp_val is not None else "-"
    print(f"  {'TP':<8} {tp_str:>14} {('>=' + str(lim.get('tp_min')) + '%'):>10} {_status(tp_ok):>10}")

    if calc:
        ca_c = calc.get("ca_calc")
        print(
            f"\n  [i] Cross-check via areas_matriz: "
            f"total={calc.get('total_m2')}m²"
            + (f"  CA={ca_c}" if ca_c else "")
        )

    for d in res["divergencias"]:
        print(f"\n  [!] DIVERGÊNCIA: {d}")
    for e in res["erros"]:
        print(f"\n  [X] {e}")
    for a in res["avisos"]:
        print(f"\n  [i] {a}")

    print(SEP)

