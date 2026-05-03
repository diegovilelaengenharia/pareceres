"""
Roteador de Peças Burocráticas — Motor GEM / SMOSU Oliveira-MG

Árvore de decisão SE→ENTÃO que, dado o resultado da inspeção documental
e os dados do processo, determina quais documentos devem ser emitidos.

Uso:
    from utils.roteador_pecas import rotear
    pecas = rotear(dados_json, resultado_inspecao)
"""

import re


# ── Regras de Roteamento ─────────────────────────────────────────────────────

def rotear(dados: dict, inspecao: dict) -> dict:
    """
    Determina as peças burocráticas a emitir.

    Args:
        dados:     JSON completo do processo
        inspecao:  resultado de inspetor_documental.inspecionar()

    Returns:
        dict com:
          pecas_primarias   — documentos principais a gerar
          pecas_paralelas   — documentos adicionais (ofícios, certidões extras)
          condicionantes    — condições a incluir no parecer
          justificativas    — explicação de cada decisão
    """
    tipo = dados.get("tipo_relatorio", "")
    veredito = inspecao.get("veredito", "INDETERMINADO")
    score = inspecao.get("score", 0)

    resultado = {
        "pecas_primarias": [],
        "pecas_paralelas": [],
        "condicionantes": [],
        "justificativas": [],
    }

    # ── REGRA 1: Bloqueantes faltando → Comunique-se ─────────────────────
    if veredito == "PENDÊNCIA" or inspecao.get("bloqueantes_faltando", 0) > 0:
        resultado["pecas_primarias"].append("comunicado_pendencia")
        pendencias = inspecao.get("pendencias", [])
        itens_comunique = [p["documento"] for p in pendencias if p.get("bloqueante")]
        resultado["justificativas"].append(
            f"REGRA 1 (Bloqueante): {len(itens_comunique)} documento(s) bloqueante(s) "
            f"ausente(s) → comunicado_pendencia. Itens: {', '.join(itens_comunique)}"
        )
        return resultado  # Não prosseguir — processo volta ao balcão

    # ── Coletar sinais do texto ──────────────────────────────────────────
    considerandos = " ".join(dados.get("considerandos", [])).lower() if dados.get("considerandos") else ""
    conclusao = str(dados.get("conclusao", "")).lower()
    texto_geral = considerandos + " " + conclusao
    extras = dados.get("extras_extraidos", {}) or {}

    # ── REGRA 2: Tipo de processo → Peça principal ───────────────────────
    # A peça principal é o próprio tipo_relatorio informado pelo Gemini
    if tipo:
        resultado["pecas_primarias"].append(tipo)
        resultado["justificativas"].append(
            f"REGRA 2 (Tipo): tipo_relatorio='{tipo}' → peça principal adicionada"
        )

    # ── REGRA 3: Decadência >5 anos → Certidão de Decadência paralela ───
    tem_decadencia = (
        "decadência" in texto_geral or "decadencia" in texto_geral
        or dados.get("data_conclusao_obra")
        or (isinstance(extras, dict) and extras.get("area_decadente_m2"))
    )
    if tem_decadencia and tipo not in ("certidao_averbacao_decadencia",):
        resultado["pecas_paralelas"].append("certidao_averbacao_decadencia")
        resultado["justificativas"].append(
            "REGRA 3 (Decadência): Evidência de decadência >5 anos detectada "
            "→ emitir certidao_averbacao_decadencia em paralelo"
        )

    # ── REGRA 4: APP/Córrego → Ofício Meio Ambiente ──────────────────────
    _TERMOS_APP = [
        "app", "área de preservação", "area de preservacao",
        "córrego", "corrego", "ribeirão", "ribeirao",
        "nascente", "mata ciliar", "codema",
    ]
    confrontantes = str(extras.get("confrontantes", "")).lower() if isinstance(extras, dict) else ""
    texto_ambiental = texto_geral + " " + confrontantes

    if any(t in texto_ambiental for t in _TERMOS_APP):
        if tipo not in ("oficio_meio_ambiente",):
            resultado["pecas_paralelas"].append("oficio_meio_ambiente")
            resultado["justificativas"].append(
                "REGRA 4 (APP): Termos ambientais detectados "
                "→ emitir oficio_meio_ambiente em paralelo"
            )

    # ── REGRA 5: Abertura na divisa → Condicionante ──────────────────────
    if "art. 43" in texto_geral or "abertura" in texto_geral and "divisa" in texto_geral:
        resultado["condicionantes"].append(
            "Apresentação de Termo de Anuência do confrontante "
            "(Art. 43, Lei 1.544/86) — abertura a <1,50m da divisa"
        )
        resultado["justificativas"].append(
            "REGRA 5 (Art. 43): Abertura na divisa detectada → condicionante de Termo de Anuência"
        )

    # ── REGRA 6: Ressalvas → Condicionantes no Parecer ───────────────────
    if veredito == "CONDICIONADO":
        for ressalva in inspecao.get("ressalvas", []):
            resultado["condicionantes"].append(
                f"Regularizar: {ressalva['documento']} — {ressalva.get('nota', '')}"
            )
        for pendencia in inspecao.get("pendencias", []):
            if not pendencia.get("bloqueante"):
                resultado["condicionantes"].append(
                    f"Apresentar: {pendencia['documento']} — {pendencia.get('nota', '')}"
                )
        if resultado["condicionantes"]:
            resultado["justificativas"].append(
                f"REGRA 6 (Condicionado): {len(resultado['condicionantes'])} "
                f"condicionante(s) adicionada(s) ao parecer"
            )

    # ── REGRA 7: Multa Art.79 detectada → Registrar ──────────────────────
    if "art. 79" in texto_geral or "art.79" in texto_geral:
        if "multa" not in str(resultado["pecas_primarias"]):
            resultado["justificativas"].append(
                "REGRA 7 (Multa): Art. 79 detectado nos considerandos "
                "→ verificar se valor da multa foi calculado e incluído"
            )

    # ── REGRA 8: Ajuste Automático de Pesos (Fase 6B.2) ──────────────────
    try:
        from analyzers import metricas_triagem
        mets = metricas_triagem.calcular_metricas()
        taxas = mets.get("taxas_rejeicao", {})
        
        pecas_filtradas = []
        for p in resultado["pecas_paralelas"]:
            rej = taxas.get(p, 0)
            if rej >= 80.0:
                resultado["justificativas"].append(
                    f"REGRA 8 (Auto-ajuste): '{p}' ignorada devido a alta taxa histórica de rejeição ({rej}%)."
                )
            else:
                pecas_filtradas.append(p)
                
        resultado["pecas_paralelas"] = pecas_filtradas
    except Exception:
        pass

    return resultado


# ── Impressão ────────────────────────────────────────────────────────────────

def imprimir_roteamento(resultado: dict) -> None:
    """Imprime relatório de roteamento."""
    SEP = "─" * 62
    print(f"\n{SEP}")
    print(f"  ROTEAMENTO DE PEÇAS")
    print(SEP)

    if resultado["pecas_primarias"]:
        print(f"  📄 PEÇAS PRIMÁRIAS:")
        for p in resultado["pecas_primarias"]:
            print(f"     → {p}")

    if resultado["pecas_paralelas"]:
        print(f"  📎 PEÇAS PARALELAS:")
        for p in resultado["pecas_paralelas"]:
            print(f"     → {p}")

    if resultado["condicionantes"]:
        print(f"  ⚠️  CONDICIONANTES ({len(resultado['condicionantes'])}):")
        for c in resultado["condicionantes"]:
            print(f"     • {c}")

    if resultado["justificativas"]:
        print(f"\n  🔍 JUSTIFICATIVAS:")
        for j in resultado["justificativas"]:
            print(f"     {j}")

    print(SEP)

