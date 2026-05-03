"""
Inspetor Documental — Motor GEM / SMOSU Oliveira-MG

Lê a chave 'analise_documental' do JSON do processo e executa
validações programáticas contra a matriz_documental.json.

Gera:
  - Score de Saúde do Processo (0-100%)
  - Lista de pendências com gravidade
  - Sugestão de peças a emitir (roteamento)

Integra-se ao pipeline de validação:
  1. schema_validator  → chaves e tipos
  2. consistencia      → semântica cruzada
  3. inspetor_documental (ESTE) → documentos presentes e regulares?
  4. verificador_multas → cálculos de multa
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MATRIZ_PATH = os.path.join(SCRIPT_DIR, "json", "matriz_documental.json")

# ── Carregar Matriz ──────────────────────────────────────────────────────────

def _carregar_matriz() -> dict:
    """Carrega a matriz_documental.json."""
    try:
        with open(MATRIZ_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  [ERRO] Não foi possível carregar matriz_documental.json: {e}")
        return {}


def _resolver_tipo_matriz(tipo_relatorio: str, matriz: dict) -> dict | None:
    """Resolve o tipo de relatório para a entrada correspondente na matriz."""
    tipos = matriz.get("tipos_processo", {})

    # Mapeamento direto de tipo_relatorio → chave na matriz
    MAPA = {
        "alvara_aprovacao": "alvara_construcao",
        "alvara_mcmv": "alvara_construcao",
        "alvara_construcao_comercial": "alvara_construcao",
        "alvara_galpao_comercial": "alvara_construcao",
        "alvara_substituicao_projeto": "alvara_construcao",
        "alvara_regularizacao": "regularizacao_obra",
        "regularizacao": "regularizacao_obra",
        "regularizacao_complexa_multipla": "regularizacao_obra",
        "habitese_comum": "habitese_comum",
        "habitese_multa": "habitese_comum",
        "habitese_condominio": "habitese_comum",
        "habitese_2via": "certidao_simples",
        "habitese_inclusao_area": "habitese_comum",
        "alvara_demolicao": "alvara_demolicao",
        "certidao_demolicao": "alvara_demolicao",
        "alvara_reforma": "alvara_reforma_ampliacao",
        "alvara_ampliacao": "alvara_reforma_ampliacao",
        "alvara_reforma_demolicao_ampliacao": "alvara_reforma_ampliacao",
        "certidao_desmembramento": "certidao_desmembramento",
        "certidao_retificacao_area": "certidao_desmembramento",
        "certidao_nome_rua": "certidao_simples",
        "certidao_localizacao": "certidao_simples",
        "certidao_conjunta": "certidao_simples",
        "certidao_numero_2via": "certidao_simples",
        "certidao_numero_comercial": "certidao_simples",
        "certidao_averbacao_decadencia": "certidao_decadencia",
        "certidao_zue": "certidao_simples",
        "alvara_renovacao": "certidao_simples",
        "alvara_cancelamento": "certidao_simples",
        "alvara_substituicao_titular": "certidao_simples",
        "alvara_troca_responsavel_tecnico": "certidao_simples",
    }

    chave = MAPA.get(tipo_relatorio, tipo_relatorio)
    return tipos.get(chave)


# ── Motor de Inspeção ────────────────────────────────────────────────────────

def inspecionar(dados: dict) -> dict:
    """
    Executa inspeção documental completa.

    Args:
        dados: JSON do processo (deve conter 'analise_documental' e 'tipo_relatorio')

    Returns:
        dict com: score, pendencias, sugestoes, resumo
    """
    resultado = {
        "score": 0,
        "total_obrigatorios": 0,
        "total_regulares": 0,
        "total_ressalvas": 0,
        "total_pendentes": 0,
        "bloqueantes_faltando": 0,
        "pendencias": [],
        "ressalvas": [],
        "sugestoes_pecas": [],
        "veredito": "INDETERMINADO",
        "justificativa": "",
    }

    tipo = dados.get("tipo_relatorio", "")
    analise = dados.get("analise_documental", {})

    if not analise:
        resultado["justificativa"] = (
            "Chave 'analise_documental' ausente no JSON. "
            "O Gemini deve incluir esta seção na Fase Zero."
        )
        return resultado

    # Carregar matriz para cruzamento
    matriz = _carregar_matriz()
    tipo_matriz = _resolver_tipo_matriz(tipo, matriz) if matriz else None

    itens = analise.get("itens", [])
    if not itens:
        resultado["justificativa"] = "'analise_documental.itens' está vazio."
        return resultado

    # Contar por status
    for item in itens:
        status = item.get("status", "").lower()
        gravidade = item.get("gravidade", "").lower()
        nome = item.get("nome", item.get("id", "?"))

        resultado["total_obrigatorios"] += 1

        if status == "regular":
            resultado["total_regulares"] += 1
        elif status == "ressalva":
            resultado["total_ressalvas"] += 1
            resultado["ressalvas"].append({
                "documento": nome,
                "nota": item.get("nota", ""),
                "gravidade": gravidade,
            })
        elif status == "pendente":
            resultado["total_pendentes"] += 1
            eh_bloqueante = gravidade == "bloqueante" or item.get("bloqueante", False)
            if eh_bloqueante:
                resultado["bloqueantes_faltando"] += 1
            resultado["pendencias"].append({
                "documento": nome,
                "nota": item.get("nota", "Não apresentado"),
                "bloqueante": eh_bloqueante,
            })

    # Calcular score
    total = resultado["total_obrigatorios"]
    if total > 0:
        pontos = (
            resultado["total_regulares"] * 1.0
            + resultado["total_ressalvas"] * 0.5
        )
        resultado["score"] = round((pontos / total) * 100, 1)

    # Regra de Ouro: bloqueante faltando → score trava em 0
    if resultado["bloqueantes_faltando"] > 0:
        resultado["score"] = 0

    # Determinar veredito e sugestões
    if resultado["bloqueantes_faltando"] > 0:
        resultado["veredito"] = "PENDÊNCIA"
        resultado["sugestoes_pecas"] = ["comunicado_pendencia"]
        resultado["justificativa"] = (
            f"{resultado['bloqueantes_faltando']} documento(s) bloqueante(s) "
            f"ausente(s). Processo deve retornar ao balcão."
        )
    elif resultado["total_pendentes"] > 0:
        resultado["veredito"] = "CONDICIONADO"
        resultado["sugestoes_pecas"] = _sugerir_pecas(tipo, dados)
        resultado["justificativa"] = (
            f"{resultado['total_pendentes']} documento(s) pendente(s) "
            f"(não-bloqueantes). Análise pode prosseguir com condicionantes."
        )
    elif resultado["total_ressalvas"] > 0:
        resultado["veredito"] = "CONDICIONADO"
        resultado["sugestoes_pecas"] = _sugerir_pecas(tipo, dados)
        resultado["justificativa"] = (
            f"{resultado['total_ressalvas']} documento(s) com ressalva. "
            f"Análise pode prosseguir, registrar condicionantes no parecer."
        )
    else:
        resultado["veredito"] = "APTO"
        resultado["sugestoes_pecas"] = _sugerir_pecas(tipo, dados)
        resultado["justificativa"] = (
            "Todos os documentos obrigatórios estão regulares. "
            "Processo apto para análise técnica completa."
        )

    return resultado


def _sugerir_pecas(tipo: str, dados: dict) -> list[str]:
    """Sugere peças a emitir baseado no tipo e dados do processo."""
    sugestoes = []

    # Roteamento básico por tipo
    PECAS_POR_TIPO = {
        "alvara_aprovacao": ["parecer_tecnico", "alvara_oficial"],
        "alvara_regularizacao": ["parecer_tecnico", "alvara_oficial"],
        "regularizacao": ["parecer_tecnico", "alvara_oficial"],
        "alvara_ampliacao": ["parecer_tecnico", "alvara_oficial"],
        "alvara_reforma": ["parecer_tecnico", "alvara_oficial"],
        "alvara_reforma_demolicao_ampliacao": ["parecer_tecnico", "alvara_oficial"],
        "habitese_comum": ["parecer_simples", "carta_habitese_oficial"],
        "habitese_multa": ["parecer_simples", "carta_habitese_oficial"],
        "certidao_nome_rua": ["certidao_oficial"],
        "certidao_localizacao": ["certidao_oficial"],
        "certidao_conjunta": ["certidao_oficial"],
        "certidao_averbacao_decadencia": ["certidao_oficial"],
        "certidao_desmembramento": ["certidao_oficial"],
    }

    sugestoes = PECAS_POR_TIPO.get(tipo, ["parecer_tecnico"])

    # Verificações cruzadas para peças adicionais
    considerandos = " ".join(dados.get("considerandos", [])).lower() if dados.get("considerandos") else ""
    conclusao = str(dados.get("conclusao", "")).lower()

    # Decadência detectada → adicionar certidão
    if "decadência" in considerandos or "decadencia" in considerandos:
        if "certidao_oficial" not in sugestoes and "certidao_averbacao_decadencia" not in sugestoes:
            sugestoes.append("certidao_averbacao_decadencia")

    # APP/córrego detectado → adicionar ofício
    termos_app = ["app", "córrego", "corrego", "nascente", "ribeirão", "codema"]
    if any(t in considerandos for t in termos_app):
        sugestoes.append("oficio_meio_ambiente")

    return sugestoes


# ── Impressão ────────────────────────────────────────────────────────────────

def imprimir_relatorio(resultado: dict, tipo: str) -> None:
    """Imprime relatório de inspeção documental."""
    SEP = "─" * 62

    print(f"\n{SEP}")
    print(f"  INSPEÇÃO DOCUMENTAL — {tipo}")
    print(SEP)

    score = resultado["score"]
    veredito = resultado["veredito"]

    # Emoji do score
    if score >= 100:
        emoji = "🟢"
    elif score >= 70:
        emoji = "🟡"
    elif score > 0:
        emoji = "🟠"
    else:
        emoji = "🔴"

    print(f"  {emoji} Score de Saúde: {score}%")
    print(f"  Veredito: {veredito}")
    print(f"  {resultado['justificativa']}")
    print()

    if resultado["pendencias"]:
        print(f"  📋 PENDÊNCIAS ({len(resultado['pendencias'])}):")
        for p in resultado["pendencias"]:
            bloq = " [BLOQUEANTE]" if p["bloqueante"] else ""
            print(f"     🔴 {p['documento']}{bloq} — {p['nota']}")
        print()

    if resultado["ressalvas"]:
        print(f"  📋 RESSALVAS ({len(resultado['ressalvas'])}):")
        for r in resultado["ressalvas"]:
            print(f"     🟡 {r['documento']} — {r['nota']}")
        print()

    if resultado["sugestoes_pecas"]:
        print(f"  📄 PEÇAS SUGERIDAS:")
        for s in resultado["sugestoes_pecas"]:
            print(f"     → {s}")

    print(SEP)


# ── API para o Painel ────────────────────────────────────────────────────────

def inspecionar_arquivo(caminho: str) -> dict:
    """Inspeciona um arquivo JSON. Retorna resultado completo."""
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {"score": 0, "veredito": "ERRO", "justificativa": str(e)}

    resultado = inspecionar(dados)
    tipo = dados.get("tipo_relatorio", "?")
    imprimir_relatorio(resultado, tipo)
    return resultado


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python inspetor_documental.py processo.json")
        sys.exit(1)
    inspecionar_arquivo(sys.argv[1])

