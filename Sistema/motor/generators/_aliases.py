"""
Dicionário de aliases para normalização de variáveis do JSON de entrada.

Chave = nome CANÔNICO (usado internamente pelo motor).
Valor = lista de sinônimos que o Gemini pode gerar.

A função normalizar_dados() resolve os aliases antes de qualquer processamento.
"""

ALIASES = {
    # ─── Responsável Técnico ───────────────────────────────────────────────
    "responsavel_tecnico": [
        "tecnico_responsavel",
        "responsavel_tecnico_obra",
        "responsavel_pelo_projeto",
        "tecnico_responsavel_obra",
        "eng_responsavel",
        "arq_responsavel",
        "profissional_responsavel",
        "rt",
    ],
    # ─── Nome do Profissional ─────────────────────────────────────────────
    "profissional_nome": [
        "nome_profissional",
        "nome_do_profissional",
        "profissional",
        "responsavel_tecnico",
    ],
    # ─── ART / RRT ────────────────────────────────────────────────────────
    "art_rrt": [
        "art_rrt_numero",
        "numero_art",
        "art_numero",
        "art",
        "rrt",
        "numero_rrt",
        "art_ou_rrt",
        "numero_art_rrt",
    ],
    # ─── Requerente / Proprietário ────────────────────────────────────────
    "requerente": [
        "proprietario",
        "proprietario_nome",
        "interessado",
        "solicitante",
        "nome_requerente",
    ],
    # ─── Endereço / Logradouro ────────────────────────────────────────────
    "logradouro": [
        "endereco",
        "endereco_obra",
        "rua",
        "rua_obra",
        "avenida",
        "logradouro_obra",
    ],
    # ─── Bairro ───────────────────────────────────────────────────────────
    "bairro": [
        "bairro_obra",
        "distrito",
        "neighborhood",
    ],
    # ─── Inscrição Municipal ──────────────────────────────────────────────
    "inscricao_municipal": [
        "inscricao",
        "insc_municipal",
        "im",
        "numero_inscricao",
        "inscricao_imobiliaria",
        "cadastro_imobiliario",
    ],
    # ─── Área do Terreno ──────────────────────────────────────────────────
    "area_terreno": [
        "area_lote",
        "area_total_terreno",
        "terreno_area",
        "area_do_terreno",
        "area_do_lote",
    ],
    # ─── Taxa de Ocupação ─────────────────────────────────────────────────
    "taxa_ocupacao": [
        "ocupacao",
        "taxa_de_ocupacao",
        "to",
        "ocupacao_solo",
        "taxa_ocupacao_solo",
    ],
    # ─── Taxa de Permeabilidade ───────────────────────────────────────────
    "taxa_permeabilidade": [
        "permeabilidade",
        "taxa_de_permeabilidade",
        "tp",
    ],
    # ─── Coeficiente de Aproveitamento ────────────────────────────────────
    "coef_aproveitamento": [
        "ca",
        "coeficiente_aproveitamento",
        "coef_de_aproveitamento",
        "coeficiente_de_aproveitamento",
    ],
    # ─── Agentes Fiscais ──────────────────────────────────────────────────
    "agentes_fiscais": [
        "fiscal",
        "fiscais",
        "agente_fiscal",
        "fiscal_responsavel",
        "vistoriadores",
        "fiscal_vistoriador",
    ],
    # ─── Assinante do Parecer ─────────────────────────────────────────────
    "assinante_parecer": [
        "assinante",
        "responsavel_parecer",
        "engenheiro_assinante",
        "autor_parecer",
    ],
    # ─── Multas Aplicáveis ────────────────────────────────────────────────
    "multas_aplicaveis": [
        "multas",
        "multa_aplicavel",
        "autos_infracao",
        "multas_cabiveis",
        "multas_cabíveis",
        "penalidades_aplicaveis",
    ],
    # ─── Condicionantes de Aprovação ──────────────────────────────────────
    "condicionantes_aprovacao": [
        "condicionantes",
        "condicoes_aprovacao",
        "requisitos_aprovacao",
        "condicionantes_para_aprovacao",
        "exigencias_aprovacao",
    ],
    # ─── Número do Processo ───────────────────────────────────────────────
    "numero_processo": [
        "processo",
        "num_processo",
        "protocolo",
        "numero_protocolo",
        "n_processo",
    ],
    # ─── Pavimentos ───────────────────────────────────────────────────────
    "pavimentos": [
        "numero_pavimentos",
        "qtd_pavimentos",
        "andares",
        "numero_andares",
        "n_pavimentos",
    ],
    # ─── Vagas de Garagem ─────────────────────────────────────────────────
    "vagas_garagem": [
        "vagas",
        "garagem",
        "numero_vagas",
        "qtd_vagas",
        "vagas_de_garagem",
    ],
    # ─── Matrícula SRI ────────────────────────────────────────────────────
    "matricula_sri": [
        "matricula",
        "matricula_nova",
        "matricula_antiga",
        "numero_matricula",
        "matricula_imovel",
        "matricula_numero",  # usado em extras_extraidos de processos reais
    ],
    # ─── Área Decadente ───────────────────────────────────────────────────
    "area_decadente_m2": [
        "area_decadente",
        "area_com_decadencia",
        "area_decadencia",
        "m2_decadentes",
        "area_prescrita",
    ],
    # ─── Lição Aprendida ──────────────────────────────────────────────────
    "licao_aprendida": [
        "licao",
        "insight_processo",
        "aprendizado",
        "observacao_especial",
        "nota_aprendizado",
    ],
    # ─── Observações Fiscais ──────────────────────────────────────────────
    "observacoes_fiscais": [
        "observacao_fiscal",
        "nota_fiscal",
        "parecer_fiscal_texto",
        "relato_fiscal",
        "obs_fiscais",
    ],
    # ─── Confrontantes ────────────────────────────────────────────────────
    "confrontantes": [
        "confrontantes_nomes",
        "vizinhos",
        "lindeiros",
        "confrontante",
        "proprietarios_confrontantes",
    ],
    # ─── Proprietário do Imóvel ───────────────────────────────────────────
    "proprietario": [
        "proprietario_nome",
        "titular_imovel",
        "dono_imovel",
        "proprietario_registrado",
    ],
    # ─── Área Total Construída ────────────────────────────────────────────
    "area_total_construida": [
        "area_construida",
        "area_edificada",
        "area_total_edificada",
        "area_total",
        "area_obra",
    ],
    # ─── CNO / CEI ───────────────────────────────────────────────────────
    "cno_numero": [
        "cno",
        "cei",
        "numero_cno",
        "numero_cei",
        "cadastro_nacional_obra",
        "certificado_empreendimento",
    ],
    # ─── Número do Alvará ─────────────────────────────────────────────────
    "numero_alvara": [
        "alvara",
        "numero_do_alvara",
        "alvara_anterior",
        "alvaras_anteriores",
        "alvara_construcao",
    ],
    # ─── Data Parecer Fiscal ──────────────────────────────────────────────
    "data_parecer_fiscal": [
        "data_vistoria",
        "data_fiscalizacao",
        "data_do_parecer_fiscal",
        "data_parecer",
    ],
}


def normalizar_dados(dados: dict) -> dict:
    """
    Resolve aliases: se o campo canônico estiver ausente, busca entre os
    sinônimos e promove o primeiro valor encontrado para o nome canônico.
    Também verifica dentro de extras_extraidos caso existam variáveis lá.

    Aplica antes de qualquer processamento de template.
    """
    extras = dados.get("extras_extraidos", {})
    for campo_canonico, sinonimos in ALIASES.items():
        if not dados.get(campo_canonico):
            for sinonimo in sinonimos:
                if dados.get(sinonimo):
                    dados[campo_canonico] = dados[sinonimo]
                    break
                if sinonimo in extras:
                    dados[campo_canonico] = extras[sinonimo]
                    break
    return dados

