"""
Verificador de Cobertura Temática dos Considerandos — Motor GEM / SMOSU Oliveira-MG

Mapeia os considerandos de um parecer aos 8 temas obrigatórios de uma
análise urbanística completa, detectando pareceres "rasos" onde o AI
atalhou a análise sem cobrir todos os ângulos relevantes.

Temas verificados:
  1. propriedade  — identificação do imóvel (matrícula, registro, inscrição)
  2. fiscal       — vistoria, agente fiscal, inspeção
  3. responsabilidade — profissional responsável, ART/RRT/TRT
  4. indices      — TO, CA, TP, parâmetros urbanísticos
  5. excecoes     — Art. 15, lote ≤220m², decadência, CTN
  6. multas       — Art. 79, valores R$, cálculo de multa
  7. condicoes    — pendências, condicionantes, emissão condicionada
  8. ambiental    — APP, córrego, CODEMA, preservação

Uso como módulo: verificar(dados) → (erros, avisos, temas_cobertos, temas_faltando)
Uso standalone: python cobertura_considerandos.py processo.json
"""

import re
import json
import sys

# ── Mapeamento de temas → palavras-chave ──────────────────────────────────────
_TEMAS: dict[str, list[str]] = {
    "propriedade": [
        "matrícula", "matricula", "registro de imóvel", "registro do imóvel",
        "inscrição municipal", "inscricao municipal", "imóvel", "imovel",
        "lote", "quadra", "logradouro", "bairro",
    ],
    "fiscal": [
        "vistoria", "fiscal", "agente fiscal", "inspeção", "inspecao",
        "embargo", "auto de infração", "auto de infracao",
        "fiscalização", "fiscalizacao", "agente",
    ],
    "responsabilidade": [
        "art", "rrt", "trt", "responsável técnico", "responsavel tecnico",
        "profissional responsável", "profissional responsavel",
        "anotação de responsabilidade", "anotacao de responsabilidade",
        "engenheiro", "arquiteto",
    ],
    "indices": [
        "taxa de ocupação", "taxa de ocupacao", " to ", "to=", "to:",
        "coeficiente de aproveitamento", " ca ", "ca=", "ca:",
        "taxa de permeabilidade", "taxa permeabilidade", " tp ", "tp=", "tp:",
        "parâmetro", "parametro", "índice urbanístico", "indice urbanistico",
        "zona", "zoneamento",
    ],
    "excecoes": [
        "art. 15", "art.15", "220m", "220 m", "lote pequeno",
        "decadência", "decadencia", "ctn", "art. 150", "art.150",
        "cinco anos", "5 anos", "isenção", "isencao", "exceção", "excecao",
    ],
    "multas": [
        "art. 79", "art.79", "multa", "r$", "reais",
        "cálculo", "calculo", "percentual", "urm",
        "art. 38", "art. 39", "art.38", "art.39",
        "construção sem licença", "construcao sem licenca",
    ],
    "condicoes": [
        "pendente", "pendência", "pendencia", "condicional", "condicionado",
        "emissão condicionada", "emissao condicionada",
        "condicionante", "sujeito a", "mediante apresentação",
        "após apresentação", "apos apresentacao",
    ],
    "ambiental": [
        "app", "área de preservação", "area de preservacao",
        "córrego", "corrego", "rio", "ribeirão", "ribeirao",
        "codema", "meio ambiente", "nascente", "faixa de proteção",
        "faixa de protecao", "lei 6.766", "lei federal",
    ],
    "cronologia": [
        "em ", "/20", "/19", "data de", "datado", "datada",
        "emitido em", "emitida em", "expedido em", "expedida em",
        "protocolo", "protocolado", "habite-se nº", "alvará nº",
        "processo nº", "planta cadastral", "histórico", "historico",
        "anteriormente", "anteriores", "apensado",
    ],
}

# ── Limiares de cobertura por grupo de tipo de documento ─────────────────────
_TECNICO = {
    "alvara_aprovacao", "alvara_regularizacao", "alvara_ampliacao",
    "alvara_galpao_comercial", "alvara_reforma_demolicao_ampliacao",
    "alvara_substituicao_projeto", "regularizacao",
}
_HABITE_SE = {
    "habitese_comum", "habitese_multa", "habitese_inclusao_area",
}

# Temas exigidos por grupo (mínimo para não gerar ERRO)
_TEMAS_OBRIGATORIOS: dict[str, set[str]] = {
    "tecnico":    {"propriedade", "fiscal", "responsabilidade", "indices"},
    "habite_se":  {"propriedade", "fiscal", "responsabilidade"},
    "generico":   {"propriedade"},
}

# Temas cuja ausência gera WARNING (não erro) nos tipos técnicos
_TEMAS_RECOMENDADOS_TECNICO = {"excecoes", "multas", "condicoes", "cronologia"}


def _texto_considerandos(dados: dict) -> str:
    """Concatena todos os considerandos em uma única string normalizada."""
    cons = dados.get("considerandos", [])
    if isinstance(cons, list):
        texto = " ".join(str(c) for c in cons)
    else:
        texto = str(cons)
    # Incluir abertura e conclusão para temas que podem estar fora dos considerandos
    texto += " " + str(dados.get("paragrafo_abertura", ""))
    texto += " " + str(dados.get("conclusao", ""))
    texto += " " + str(dados.get("fundamentacao_legal", ""))
    return texto.lower()


def _cobertos(texto: str) -> set[str]:
    """Retorna o conjunto de temas cobertos pelo texto."""
    cobertos = set()
    for tema, palavras in _TEMAS.items():
        for palavra in palavras:
            if palavra.lower() in texto:
                cobertos.add(tema)
                break
    return cobertos


def verificar(dados: dict) -> tuple[list[str], list[str], set[str], set[str]]:
    """
    Verifica a cobertura temática dos considerandos.

    Retorna:
        erros          — temas obrigatórios ausentes
        avisos         — temas recomendados ausentes
        temas_cobertos — conjunto de temas encontrados
        temas_faltando — conjunto de temas não encontrados
    """
    erros:  list[str] = []
    avisos: list[str] = []

    tipo = dados.get("tipo_relatorio", "")

    # Apenas tipos com análise real (ignorar certidões simples e ofícios)
    _COM_ANALISE = _TECNICO | _HABITE_SE | {
        "habitese_2via", "certidao_averbacao_decadencia",
        "alvara_renovacao", "alvara_demolicao", "certidao_demolicao",
        "certidao_desmembramento", "certidao_retificacao_area",
    }
    if tipo not in _COM_ANALISE:
        return erros, avisos, set(), set()

    # Determinar grupo
    if tipo in _TECNICO:
        grupo = "tecnico"
    elif tipo in _HABITE_SE:
        grupo = "habite_se"
    else:
        grupo = "generico"

    texto = _texto_considerandos(dados)
    temas_cobertos = _cobertos(texto)
    todos_os_temas = set(_TEMAS.keys())
    temas_faltando = todos_os_temas - temas_cobertos

    # Verificar obrigatórios
    obrigatorios = _TEMAS_OBRIGATORIOS.get(grupo, set())
    faltam_obrig = obrigatorios - temas_cobertos
    for tema in sorted(faltam_obrig):
        erros.append(
            f"Tema obrigatório ausente nos considerandos: '{tema}'. "
            f"Esperado em pareceres do tipo '{tipo}'. "
            f"Adicione ao menos um considerando que aborde este aspecto."
        )

    # Verificar recomendados (apenas para tipos técnicos)
    if grupo == "tecnico":
        faltam_rec = _TEMAS_RECOMENDADOS_TECNICO - temas_cobertos
        for tema in sorted(faltam_rec):
            avisos.append(
                f"Tema recomendado não coberto nos considerandos: '{tema}'. "
                "Verifique se este aspecto é aplicável ao caso e, se sim, inclua-o."
            )

    return erros, avisos, temas_cobertos, temas_faltando


def imprimir_relatorio(
    erros: list[str],
    avisos: list[str],
    temas_cobertos: set[str],
    temas_faltando: set[str],
) -> None:
    """Imprime relatório de cobertura temática."""
    if not temas_cobertos and not erros and not avisos:
        return

    SEP = "-" * 62
    todos = set(_TEMAS.keys())
    n_cob = len(temas_cobertos)
    n_tot = len(todos)

    print(f"\n{SEP}")
    print(f"  COBERTURA TEMÁTICA DOS CONSIDERANDOS  ({n_cob}/{n_tot})")
    print(SEP)

    for tema in sorted(todos):
        marca = "[OK]" if tema in temas_cobertos else "[ - ]"
        print(f"  {marca}  {tema}")

    for e in erros:
        print(f"\n  [TEMA FALTANDO] {e}")
    for a in avisos:
        print(f"\n  [AVISO] {a}")

    if not erros and not avisos:
        print(f"\n  [OK] Cobertura temática adequada ({n_cob}/{n_tot} temas).")

    print(SEP)


def main():
    if len(sys.argv) < 2:
        print("Uso: python cobertura_considerandos.py processo.json")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        dados = json.load(f)
    erros, avisos, cobertos, faltando = verificar(dados)
    imprimir_relatorio(erros, avisos, cobertos, faltando)
    sys.exit(0 if not erros else 1)


if __name__ == "__main__":
    main()
