"""
Validador de Schema JSON — Motor GEM / SMOSU Oliveira-MG

Verifica chaves obrigatórias e tipos de dado antes de enviar ao compilador.
Um erro bloqueante significa que o compilador vai travar ou gerar documento errado.

Uso:
    python schema_validator.py processo.json
    python schema_validator.py 1_Colar_JSON_Aqui/
"""

import json
import sys
import os
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from config import TIPOS_DOCUMENTO

# ── Chaves obrigatórias por categoria de gerador ────────────────────────────
_CHAVES_CATEGORIA = {
    "parecer_tecnico": [
        "numero_processo", "requerente",
        "paragrafo_abertura", "considerandos", "conclusao",
    ],
    "parecer_simples": [
        "numero_processo", "requerente",
        "paragrafo_abertura", "considerandos", "conclusao",
    ],
    "oficio": [
        "numero_processo", "considerandos", "conclusao",
    ],
    "comunicado": [
        "numero_processo", "requerente",
        "paragrafo_abertura", "considerandos", "conclusao",
    ],
    "comunicado_pendencia": [
        "numero_processo", "requerente",
        "paragrafo_abertura", "considerandos", "conclusao",
    ],
}

# Chaves extras para documentos_pronto (secretaria)
_CHAVES_DOCUMENTO_PRONTO = {
    "alvara_oficial": [
        "numero_documento", "data_aprovacao", "nome_obra",
        "logradouro", "bairro",
        "proprietario_nome", "proprietario_cpf_cnpj",
        "area_total_obra", "areas_matriz",
    ],
    "carta_habitese_oficial": [
        "numero_documento", "logradouro", "bairro",
        "proprietario_nome", "proprietario_cpf_cnpj",
        "responsavel_execucao_nome", "responsavel_execucao_cpf_cnpj",
        "texto_despacho_responsavel_tecnico",
        "area_total_obra", "areas_matriz",
    ],
    "certidao_oficial": [
        "titulo_documento", "texto_certidao", "assinantes",
    ],
}

# Chaves que devem ser listas, nunca strings
_DEVE_SER_LISTA = [
    "considerandos", "fundamentacao_legal",
    "documentos_emitir", "areas_matriz", "assinantes",
    "observacoes_finais",
]


def validar(dados: dict) -> tuple:
    """
    Valida as chaves e tipos de um JSON de processo.

    Retorna:
        erros  — lista de problemas bloqueantes (o compilador vai travar)
        avisos — lista de alertas não-bloqueantes (qualidade do documento)
    """
    erros = []
    avisos = []

    # ── 1. tipo_relatorio presente e reconhecido ─────────────────────────────
    tipo = dados.get("tipo_relatorio")
    if not tipo:
        erros.append("Chave 'tipo_relatorio' ausente. O compilador não sabe qual documento gerar.")
        return erros, avisos

    categoria = TIPOS_DOCUMENTO.get(tipo)
    if not categoria:
        validos = ", ".join(sorted(TIPOS_DOCUMENTO.keys()))
        erros.append(
            f"tipo_relatorio='{tipo}' não reconhecido.\n"
            f"  Tipos válidos: {validos}"
        )
        return erros, avisos

    # ── 2. Chaves obrigatórias da categoria ──────────────────────────────────
    for chave in _CHAVES_CATEGORIA.get(categoria, []):
        if not dados.get(chave):
            erros.append(f"Chave obrigatória ausente/vazia: '{chave}' (categoria '{categoria}')")

    # ── 3. Chaves extras para documento_pronto ───────────────────────────────
    if categoria == "documento_pronto" and tipo in _CHAVES_DOCUMENTO_PRONTO:
        for chave in _CHAVES_DOCUMENTO_PRONTO[tipo]:
            if not dados.get(chave):
                erros.append(f"Chave obrigatória ausente/vazia: '{chave}' (tipo '{tipo}')")

    # ── 4. Tipos de dado ─────────────────────────────────────────────────────
    for chave in _DEVE_SER_LISTA:
        val = dados.get(chave)
        if val is not None and not isinstance(val, list):
            erros.append(
                f"'{chave}' deve ser uma lista JSON (array), mas recebeu {type(val).__name__}. "
                f"Corrija: coloque colchetes [ ] em volta dos itens."
            )

    # ── 5. areas_matriz: cada item deve ter as 4 chaves ──────────────────────
    for item in dados.get("areas_matriz", []):
        if isinstance(item, dict):
            for sub in ("categoria", "destinacao", "tipo_obra", "area_m2"):
                if sub not in item:
                    erros.append(
                        f"Item de 'areas_matriz' está faltando a chave '{sub}'. "
                        f"Item recebido: {item}"
                    )

    # ── 6. Avisos de qualidade ───────────────────────────────────────────────
    if categoria in ("parecer_tecnico", "parecer_simples"):
        if not dados.get("fundamentacao_legal"):
            avisos.append(
                "'fundamentacao_legal' está vazia. "
                "Pareceres ficam mais sólidos com fundamentação legal explícita."
            )
        if not dados.get("documentos_emitir"):
            avisos.append(
                "'documentos_emitir' está vazia. "
                "Confirme se nenhum documento precisa ser emitido."
            )
        if not dados.get("data_processo"):
            avisos.append("'data_processo' ausente. Inclua a data por extenso (ex: '22 de abril de 2026').")

    # ── 7. Placeholders ⚠️ VERIFICAR ─────────────────────────────────────────
    texto_completo = json.dumps(dados, ensure_ascii=False)
    ocorrencias = texto_completo.count("VERIFICAR")
    if ocorrencias:
        avisos.append(
            f"Encontrado(s) {ocorrencias} placeholder(s) 'VERIFICAR' no JSON. "
            f"Confira os campos antes de compilar."
        )

    # ── 8. Negrito em comunicado_pendencia ───────────────────────────────────
    if tipo == "comunicado_pendencia":
        itens = dados.get("considerandos", [])
        for i, item in enumerate(itens):
            if isinstance(item, str) and item.startswith("__") and not item.startswith("**"):
                avisos.append(
                    f"considerandos[{i}] usa '__' (itálico) onde provavelmente deveria usar '**' (negrito). "
                    f"O engine do comunicado exige '**texto**' para destacar os títulos dos itens."
                )

    return erros, avisos


def validar_arquivo(caminho: str) -> bool:
    """Valida um arquivo JSON. Retorna True se não houver erros bloqueantes."""
    nome = os.path.basename(caminho)

    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  [✗] {nome}")
        print(f"        ERRO: JSON inválido — {e}")
        return False
    except FileNotFoundError:
        print(f"  [✗] {nome}")
        print(f"        ERRO: Arquivo não encontrado.")
        return False

    erros, avisos = validar(dados)
    tipo = dados.get("tipo_relatorio", "?")

    if not erros and not avisos:
        print(f"  [OK] {nome}  ({tipo})")
        return True

    if erros:
        print(f"  [ERRO] {nome}  ({tipo})  -- {len(erros)} erro(s) bloqueante(s):")
        for e in erros:
            print(f"        ERRO: {e}")

    if avisos:
        marcador = "  [AVISO]" if not erros else "        "
        if not erros:
            print(f"{marcador} {nome}  ({tipo})  -- {len(avisos)} aviso(s):")
        for a in avisos:
            print(f"        AVISO: {a}")

    return len(erros) == 0


def main():
    if len(sys.argv) < 2:
        print("Uso: python schema_validator.py arquivo.json")
        print("     python schema_validator.py pasta/")
        sys.exit(1)

    alvo = sys.argv[1]

    if os.path.isdir(alvo):
        arquivos = sorted(glob.glob(os.path.join(alvo, "*.json")))
        if not arquivos:
            print(f"Nenhum .json encontrado em '{alvo}'")
            sys.exit(1)
    else:
        arquivos = [alvo]

    print("-" * 55)
    print("  Validador de Schema - Motor GEM / SMOSU Oliveira-MG")
    print("-" * 55)

    resultados = [validar_arquivo(a) for a in arquivos]

    if len(arquivos) > 1:
        ok = sum(resultados)
        falhos = len(resultados) - ok
        print("-" * 55)
        print(f"  {ok}/{len(arquivos)} OK  |  {falhos} com erro(s)")
        print("-" * 55)

    sys.exit(0 if all(resultados) else 1)


if __name__ == "__main__":
    main()
