"""
Gerador de Metadata SERO/INSS — Motor GEM / SMOSU Oliveira-MG

Processa o campo opcional 'sero_metadata' do JSON e:
  1. Valida a consistência das sub-áreas vs area_total_construida
  2. Gera automaticamente o bloco de observação SERO/INSS
     para injeção em documentos_emitir[].obs do habite-se

A obs gerada lembra o requerente de averbar a obra no SERO/RFB
para obtenção da CND de pessoa física antes do registro cartorário,
usando os valores exatos de área declarados no JSON.

Uso como módulo:
    obs = gerar_obs_sero(sero_meta, area_total_str)
    erros, avisos = validar(dados)

Uso standalone: python gerador_sero.py processo.json
"""

import re
import json
import sys

# Tipos de habite-se onde o disclaimer SERO é obrigatório
_HABITE_SE = {"habitese_comum", "habitese_multa", "habitese_inclusao_area"}


def _num(texto) -> float | None:
    """Extrai float de string, aceita vírgula como decimal."""
    if texto is None:
        return None
    limpo = re.sub(r"[^\d,.]", "", str(texto)).replace(",", ".")
    try:
        return float(limpo) if limpo else None
    except ValueError:
        return None


def _fmt(valor: float) -> str:
    """Formata float como '120,00m²'."""
    return f"{valor:.2f}".replace(".", ",") + "m²"


def gerar_obs_sero(sero_meta: dict, area_total_str: str = "") -> str:
    """
    Gera o texto de observação SERO/INSS para documentos_emitir[].obs.

    sero_meta       — dict com os campos sero_metadata do JSON
    area_total_str  — string de area_total_construida para referência

    Retorna string multilinha com o disclaimer completo.
    """
    principal  = _num(sero_meta.get("area_principal_coberta_m2")) or 0.0
    comp_cob   = _num(sero_meta.get("area_complementar_coberta_m2")) or 0.0
    comp_desc  = _num(sero_meta.get("area_complementar_descoberta_m2")) or 0.0

    eh_reforma     = bool(sero_meta.get("eh_reforma_ampliacao", False))
    eh_popular     = bool(sero_meta.get("eh_habi_popular", False))
    pre_moldada    = bool(sero_meta.get("estrutura_pre_moldada", False))
    fator_social   = _num(sero_meta.get("fator_social_pct")) or 0.0

    total_cob  = principal + comp_cob
    total_geral = total_cob + comp_desc

    linhas = [
        "Averbação Cartorária e SERO/INSS:",
        "Este Habite-se não exime da aferição da obra no sistema SERO da RFB "
        "para emissão da CND de pessoa física, necessária ao registro no Cartório de Imóveis.",
        "",
        f"Segregação de áreas para fins de INSS/SERO:",
        f"  • Área Principal Coberta (SERO): {_fmt(principal)}",
    ]

    if comp_cob > 0:
        linhas.append(f"  • Área Complementar Coberta (garagem/varanda/etc.): {_fmt(comp_cob)}")
    if comp_desc > 0:
        linhas.append(f"  • Área Complementar Descoberta (pátio/quintal): {_fmt(comp_desc)}")

    linhas.append(f"  • Total Coberto (base de cálculo INSS): {_fmt(total_cob)}")
    if area_total_str:
        linhas.append(f"  • Área Total Construída (município): {area_total_str}")

    if eh_reforma:
        linhas.append("")
        linhas.append(
            "Reforma/Ampliação: aplica-se desconto sobre a área reformada conforme "
            "IN RFB vigente — o contribuinte deve apresentar documentação da área pré-existente."
        )

    if eh_popular:
        linhas.append("")
        linhas.append(
            "Habitação Popular: verificar enquadramento nos critérios de isenção "
            "de INSS (obras de até 70m² com proprietário pessoa física de baixa renda — "
            "Lei 9.528/97)."
        )

    if pre_moldada:
        linhas.append("")
        linhas.append(
            "Estrutura Pré-Moldada: informar na SERO o uso de elementos pré-fabricados "
            "para aplicação dos créditos de INSS já recolhidos pelo fabricante "
            "(IN RFB 2.021/2021 e atualizações)."
        )

    if fator_social > 0:
        linhas.append("")
        linhas.append(
            f"Fator Social aplicável: {fator_social:.0f}% de redução sobre a base de cálculo, "
            "conforme enquadramento socioeconômico a ser comprovado perante a RFB."
        )

    linhas.append("")
    linhas.append(
        "O proprietário é responsável pelo recolhimento do INSS sobre mão de obra "
        "e pela regularização junto à RFB antes do registro cartorário."
    )

    return "\n".join(linhas)


def validar(dados: dict) -> tuple[list[str], list[str]]:
    """
    Valida sero_metadata e sua consistência com area_total_construida.

    Retorna:
        erros  — inconsistências bloqueantes
        avisos — alertas não-bloqueantes
    """
    erros:  list[str] = []
    avisos: list[str] = []

    tipo = dados.get("tipo_relatorio", "")

    # Apenas habite-se precisa de SERO
    if tipo not in _HABITE_SE:
        return erros, avisos

    sero_meta = dados.get("sero_metadata")

    if sero_meta is None:
        avisos.append(
            f"Tipo '{tipo}' não contém 'sero_metadata'. "
            "Adicione o campo para geração automática do disclaimer SERO/INSS "
            "e validação de sub-áreas (area_principal_coberta_m2, "
            "area_complementar_coberta_m2, area_complementar_descoberta_m2)."
        )
        return erros, avisos

    if not isinstance(sero_meta, dict):
        erros.append("'sero_metadata' deve ser um objeto JSON ({...}).")
        return erros, avisos

    # Verificar sub-áreas vs total
    principal = _num(sero_meta.get("area_principal_coberta_m2")) or 0.0
    comp_cob  = _num(sero_meta.get("area_complementar_coberta_m2")) or 0.0
    comp_desc = _num(sero_meta.get("area_complementar_descoberta_m2")) or 0.0
    total_sub = principal + comp_cob + comp_desc

    area_total = _num(dados.get("area_total_construida"))

    if area_total is not None and total_sub > 0:
        if abs(total_sub - area_total) > 1.0:
            avisos.append(
                f"sero_metadata: soma de sub-áreas ({total_sub:.2f}m²) difere de "
                f"area_total_construida ({area_total:.2f}m²) em "
                f"{abs(total_sub - area_total):.2f}m². "
                "Confira a segregação de áreas."
            )
    elif total_sub == 0:
        avisos.append(
            "sero_metadata: nenhuma sub-área preenchida. "
            "Preencha ao menos 'area_principal_coberta_m2'."
        )

    return erros, avisos


def imprimir_relatorio(erros: list[str], avisos: list[str], obs: str = "") -> None:
    """Imprime relatório do módulo SERO."""
    if not erros and not avisos and not obs:
        return

    SEP = "-" * 62
    print(f"\n{SEP}")
    print("  GERADOR SERO/INSS")
    print(SEP)

    for e in erros:
        print(f"  [ERRO] {e}")
    for a in avisos:
        print(f"  [AVISO] {a}")

    if obs:
        print("\n  Obs gerada para documentos_emitir:")
        for linha in obs.splitlines():
            print(f"    {linha}")
    elif not erros and not avisos:
        print("  [OK] sero_metadata não aplicável a este tipo de documento.")

    print(SEP)


def main():
    if len(sys.argv) < 2:
        print("Uso: python gerador_sero.py processo.json")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        dados = json.load(f)

    erros, avisos = validar(dados)

    obs = ""
    sero_meta = dados.get("sero_metadata")
    if sero_meta and isinstance(sero_meta, dict):
        obs = gerar_obs_sero(sero_meta, dados.get("area_total_construida", ""))

    imprimir_relatorio(erros, avisos, obs)
    sys.exit(0 if not erros else 1)


if __name__ == "__main__":
    main()
