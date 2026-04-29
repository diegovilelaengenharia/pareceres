"""
Verificador de Cálculo de Multas — Motor GEM / SMOSU Oliveira-MG

Valida o campo opcional 'multas_calculadas' do JSON, conferindo:
  - Faixa correta conforme a área declarada
  - Percentual URM correto para a faixa
  - Cálculo aritmético: area_m2 × valor_urm = resultado_r$

Referências legais verificadas:
  Art. 79 Lei 1.544/86  — Obra sem licença (faixas por área)
  Arts. 38-39 LC 267/2019 — Violação de parâmetros urbanísticos

Uso como módulo: verificar(dados) → (erros, avisos, resumo)
Uso standalone: python verificador_multas.py processo.json
"""

import re
import json
import sys
import os

# ── Tabela de faixas — Art. 79 Lei 1.544/86 ──────────────────────────────────
# (area_min, area_max_inclusive, percentual_urm_esperado, label)
_FAIXAS_ART79 = [
    (0.01,  60.00, 1.0, "até 60m²"),
    (60.01, 75.00, 3.0, "61-75m²"),
    (75.01, 100.00, 4.0, "76-100m²"),
    (100.01, float("inf"), 5.0, "acima de 100m²"),
]

_TOLERANCIA_R = 0.50   # Tolerância aritmética em R$
_TOLERANCIA_P = 0.001  # Tolerância de percentual (comparação float)


def _num(texto) -> float | None:
    """Extrai float de string, aceita vírgula como decimal."""
    if texto is None:
        return None
    limpo = re.sub(r"[^\d,.]", "", str(texto)).replace(",", ".")
    try:
        return float(limpo) if limpo else None
    except ValueError:
        return None


def _faixa_esperada(area: float) -> tuple[float, str]:
    """Retorna (percentual_urm_esperado, label_faixa) para uma área em m²."""
    for a_min, a_max, pct, label in _FAIXAS_ART79:
        if a_min <= area <= a_max:
            return pct, label
    return 5.0, "acima de 100m²"


def _verificar_item(item: dict, idx: int) -> tuple[list[str], list[str]]:
    """Valida um único item de multas_calculadas. Retorna (erros, avisos)."""
    erros:  list[str] = []
    avisos: list[str] = []

    base_legal = item.get("base_legal", "?")
    prefixo    = f"multas_calculadas[{idx}] ({base_legal})"

    area      = _num(item.get("area_m2"))
    pct_urm   = _num(item.get("percentual_urm"))
    valor_urm = _num(item.get("valor_urm"))
    resultado = _num(item.get("resultado_r$") or item.get("resultado_rs"))
    excecao   = item.get("excecao_aplicada")

    # Exceção aplicada — se resultado deve ser 0, apenas confirmar
    if excecao:
        if resultado is not None and resultado > 0.01:
            avisos.append(
                f"{prefixo}: 'excecao_aplicada' preenchida ('{excecao}'), "
                f"mas resultado_r$ = R${resultado:.2f} (esperado R$0,00 ou valor reduzido). "
                "Confirme se a exceção anula totalmente a multa."
            )
        return erros, avisos

    # ── Art. 79: validar faixa e percentual ──────────────────────────────────
    base_lower = str(base_legal).lower()
    if "art. 79" in base_lower or "art.79" in base_lower:
        if area is None:
            erros.append(f"{prefixo}: 'area_m2' ausente — não é possível validar faixa.")
        else:
            pct_esperado, label_esperado = _faixa_esperada(area)

            faixa_decl = str(item.get("faixa", "")).lower()
            if faixa_decl and label_esperado.lower() not in faixa_decl and faixa_decl not in label_esperado.lower():
                avisos.append(
                    f"{prefixo}: Faixa declarada ('{item.get('faixa')}') pode não corresponder "
                    f"à área {area}m² — faixa esperada: '{label_esperado}'."
                )

            if pct_urm is not None and abs(pct_urm - pct_esperado) > _TOLERANCIA_P:
                erros.append(
                    f"{prefixo}: percentual_urm={pct_urm}% incorreto para {area}m² "
                    f"(faixa '{label_esperado}' exige {pct_esperado}%). "
                    "Verifique a tabela do Art. 79 Lei 1.544/86."
                )

    # ── Verificação aritmética: area × valor_urm = resultado ─────────────────
    if area is not None and valor_urm is not None and resultado is not None:
        esperado  = round(area * valor_urm, 2)
        diferenca = abs(esperado - resultado)
        if diferenca > _TOLERANCIA_R:
            erros.append(
                f"{prefixo}: Cálculo incorreto — "
                f"{area}m² × R${valor_urm:.2f}/m² = R${esperado:.2f}, "
                f"mas resultado_r$ = R${resultado:.2f} "
                f"(diferença de R${diferenca:.2f}). "
                "Corrija o valor antes de compilar."
            )
    elif area is not None and valor_urm is not None and resultado is None:
        avisos.append(
            f"{prefixo}: 'resultado_r$' ausente. "
            f"Valor esperado: {area:.2f}m² × R${valor_urm:.2f}/m² = R${area * valor_urm:.2f}."
        )

    return erros, avisos


def verificar(dados: dict) -> tuple[list[str], list[str], list[dict]]:
    """
    Verifica o campo 'multas_calculadas' do JSON.

    Retorna:
        erros    — erros bloqueantes (cálculo errado)
        avisos   — alertas não-bloqueantes
        resumo   — lista de dicts por item verificado
    """
    erros:  list[str] = []
    avisos: list[str] = []
    resumo: list[dict] = []

    multas = dados.get("multas_calculadas")
    if not multas:
        return erros, avisos, resumo

    if not isinstance(multas, list):
        erros.append("'multas_calculadas' deve ser uma lista JSON (array).")
        return erros, avisos, resumo

    for i, item in enumerate(multas):
        if not isinstance(item, dict):
            avisos.append(f"multas_calculadas[{i}]: item não é um objeto JSON — ignorado.")
            continue
        e, a = _verificar_item(item, i)
        erros.extend(e)
        avisos.extend(a)
        resultado = _num(item.get("resultado_r$") or item.get("resultado_rs")) or 0.0
        resumo.append({
            "base_legal":   item.get("base_legal", "?"),
            "area_m2":      _num(item.get("area_m2")),
            "resultado_r$": resultado,
            "excecao":      item.get("excecao_aplicada"),
        })

    return erros, avisos, resumo


def imprimir_relatorio(erros: list[str], avisos: list[str], resumo: list[dict]) -> None:
    """Imprime relatório formatado da verificação de multas."""
    if not resumo and not erros and not avisos:
        return

    SEP = "-" * 62
    print(f"\n{SEP}")
    print("  VERIFICADOR DE MULTAS")
    print(SEP)

    if resumo:
        total_geral = sum(r["resultado_r$"] for r in resumo)
        for r in resumo:
            exc_str  = f"  [EXCECAO: {r['excecao']}]" if r["excecao"] else ""
            area_str = f"{r['area_m2']}m²" if r["area_m2"] is not None else "?"
            print(
                f"  {r['base_legal']:<35} "
                f"{area_str:>8}  "
                f"R$ {r['resultado_r$']:>8.2f}"
                f"{exc_str}"
            )
        if len(resumo) > 1:
            print(f"  {'TOTAL':>44}  R$ {total_geral:>8.2f}")

    for e in erros:
        print(f"\n  [ERRO DE CÁLCULO] {e}")
    for a in avisos:
        print(f"\n  [AVISO] {a}")

    if not erros and not avisos and resumo:
        print("\n  [OK] Todos os cálculos de multa conferidos.")

    print(SEP)


def main():
    if len(sys.argv) < 2:
        print("Uso: python verificador_multas.py processo.json")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        dados = json.load(f)
    erros, avisos, resumo = verificar(dados)
    imprimir_relatorio(erros, avisos, resumo)
    sys.exit(0 if not erros else 1)


if __name__ == "__main__":
    main()
