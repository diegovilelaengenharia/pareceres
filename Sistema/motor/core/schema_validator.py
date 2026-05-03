"""
Validador de Schema JSON — Motor GEM / SMOSU Oliveira-MG

Verifica chaves obrigatórias e tipos de dado antes de enviar ao compilador.
Um erro bloqueante significa que o compilador vai travar ou gerar documento errado.

Uso:
    python schema_validator.py processo.json
    python schema_validator.py <pasta_entrada>/
"""

import json
import sys
import os
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from core.config import TIPOS_DOCUMENTO
from core.logger import log_ok, log_warn, log_err, log_info

# ── Carregamento do Esquema Base Dinâmico ───────────────────────────────────
ESQUEMA_BASE_PATH = os.path.join(SCRIPT_DIR, "templates", "_esquema_base.json")

def carregar_esquema_base():
    if os.path.exists(ESQUEMA_BASE_PATH):
        try:
            with open(ESQUEMA_BASE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

ESQUEMA_BASE = carregar_esquema_base()
CHAVES_CONHECIDAS = set(ESQUEMA_BASE.get("todas_chaves", []))
TIPOS_CONHECIDOS = set(ESQUEMA_BASE.get("tipos_disponiveis", []))

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
    "observacoes_finais", "multas_calculadas", "excecoes_aplicadas",
]

# Chaves que devem ser strings
_DEVE_SER_STRING = [
    "numero_processo", "requerente", "paragrafo_abertura", "conclusao"
]

# ── Criticidade de dados ausentes (⚠️ VERIFICAR) ────────────────────────────
# TIER_A — bloqueante: ausência impede análise urbanística
# TIER_B — condicional: gera aviso, mas permite compilação
# TIER_C — informacional: não alertado (só em log)
_TIER_A_CAMPOS = set()
_TIER_B_CAMPOS = {
    "inscricao_municipal", "area_terreno",
    "profissional_nome", "profissional_registro",
    "desenhista", "lote", "quadra",
    "zona_uso", "pavimentos", "vagas_garagem",
    "tipo_multa_especifica", "modo_recebimento_projeto",
    "assinante_parecer"
}


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
        validos = ", ".join(sorted(TIPOS_CONHECIDOS)) if TIPOS_CONHECIDOS else ", ".join(sorted(TIPOS_DOCUMENTO.keys()))
        erros.append(
            f"tipo_relatorio='{tipo}' não reconhecido.\n"
            f"  Tipos válidos: {validos}"
        )
        return erros, avisos

    # ── 1.1 Chaves conhecidas (Aviso) ────────────────────────────────────────
    if CHAVES_CONHECIDAS:
        for k in dados.keys():
            # Ignora chaves internas e estruturadas (ponto ou colchete indicam subchaves que já validamos o prefixo)
            if k not in CHAVES_CONHECIDAS and not k.startswith("_") and "." not in k and "[" not in k:
                avisos.append(f"Chave '{k}' não consta no esquema base de templates. Verifique se o nome está correto.")

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

    for chave in _DEVE_SER_STRING:
        val = dados.get(chave)
        if val is not None and not isinstance(val, str):
            erros.append(
                f"'{chave}' deve ser texto (string), mas recebeu {type(val).__name__}. "
                f"Corrija: certifique-se que o valor está entre aspas."
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

    # ── 7. Placeholders ⚠️ VERIFICAR — com tiering de criticidade ────────────
    texto_completo = json.dumps(dados, ensure_ascii=False)
    ocorrencias = texto_completo.count("VERIFICAR")
    if ocorrencias:
        avisos.append(
            f"Encontrado(s) {ocorrencias} placeholder(s) 'VERIFICAR' no JSON. "
            f"Confira os campos antes de compilar."
        )

    # Tier A: campos críticos com VERIFICAR → bloqueante
    for campo in _TIER_A_CAMPOS:
        val = str(dados.get(campo, ""))
        if "VERIFICAR" in val:
            erros.append(
                f"DADO CRÍTICO ausente (Tier A): '{campo}' contém '⚠️ VERIFICAR'. "
                "Este campo é essencial para a análise urbanística. "
                "Localize o dado no processo antes de compilar."
            )

    # Tier B: campos relevantes com VERIFICAR → aviso
    for campo in _TIER_B_CAMPOS:
        val = str(dados.get(campo, ""))
        if "VERIFICAR" in val:
            avisos.append(
                f"Dado relevante (Tier B): '{campo}' contém '⚠️ VERIFICAR'. "
                "Tente localizar no processo; se genuinamente ausente, mantenha a marcação."
            )

    # ── 8. Validar estrutura de multas_calculadas ────────────────────────────
    for i, item in enumerate(dados.get("multas_calculadas", [])):
        if isinstance(item, dict):
            for sub in ("base_legal", "area_m2", "resultado_r$"):
                if sub not in item:
                    avisos.append(
                        f"multas_calculadas[{i}] está faltando '{sub}'. "
                        "O verificador de multas não conseguirá conferir este item."
                    )

    # ── 9. Validar estrutura de excecoes_aplicadas ───────────────────────────
    for i, item in enumerate(dados.get("excecoes_aplicadas", [])):
        if isinstance(item, dict):
            for sub in ("tipo", "base_legal", "efeito"):
                if sub not in item:
                    avisos.append(
                        f"excecoes_aplicadas[{i}] está faltando '{sub}'. "
                        "Inclua tipo, base_legal e efeito para auditoria completa."
                    )

    # ── 10. Negrito em comunicado_pendencia ──────────────────────────────────
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
        log_err(f"{nome} - JSON inválido — {e}")
        return False
    except FileNotFoundError:
        log_err(f"{nome} - Arquivo não encontrado.")
        return False

    erros, avisos = validar(dados)
    tipo = dados.get("tipo_relatorio", "?")

    if not erros and not avisos:
        log_ok(f"{nome} ({tipo})")
        return True

    if erros:
        log_err(f"{nome} ({tipo}) -- {len(erros)} erro(s) bloqueante(s):", data={"arquivo": nome, "tipo": tipo, "erros": erros})
        for e in erros:
            log_err(f"  -> {e}")

    if avisos:
        log_warn(f"{nome} ({tipo}) -- {len(avisos)} aviso(s):", data={"arquivo": nome, "tipo": tipo, "avisos": avisos})
        for a in avisos:
            log_warn(f"  -> {a}")

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

