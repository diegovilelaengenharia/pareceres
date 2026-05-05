"""
Configuração central do sistema de geração de documentos — SMOSU Oliveira/MG.
Centraliza caminhos, constantes visuais (cores/fontes) e mapeamentos técnicos.
"""

import os
from docx.shared import RGBColor

# ═══════════════════════════════════════════════════════════
#  CAMINHOS
# ═══════════════════════════════════════════════════════════
"""Configuração de caminhos base do projeto."""
SCRIPT_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR     = os.path.dirname(SCRIPT_DIR)  # pasta _Sistema_Interno
PROJECT_ROOT    = os.path.dirname(PROJECT_DIR)  # pasta raiz: 02. Pareceres
PASTA_ENTRADA        = os.path.join(PROJECT_ROOT, "Entrada")
PASTA_SAIDA          = os.path.join(PROJECT_ROOT, "Saida")
PASTA_MODELOS        = os.path.join(PROJECT_DIR, "modelos")
PASTA_TREINO         = os.path.join(PROJECT_ROOT, "Sistema", "inteligencia", "Treinar GEM")
PASTA_BASE_CONHECIMENTO = os.path.join(PROJECT_ROOT, "Sistema", "base_conhecimento")
PASTA_LOGS           = os.path.join(PROJECT_ROOT, "Sistema", "logs")
PASTA_HISTORICO      = os.path.join(PROJECT_ROOT, "Saida", "_Historico")
LOGO_BRASAO     = os.path.join(SCRIPT_DIR, "logos", "logo_brasao.jpeg")
LOGO_PREFEITURA = os.path.join(SCRIPT_DIR, "logos", "logo_prefeitura.png")
TEMPLATES_DIR   = os.path.join(SCRIPT_DIR, "templates")

# ═══════════════════════════════════════════════════════════
#  TIPOGRAFIA
# ═══════════════════════════════════════════════════════════
"""Configurações de fontes para o gerador DOCX."""
# • Corpo do texto:   Calibri 11pt  — sans-serif moderna, excelente leitura
# • Títulos/Labels:   Cambria bold   — serifa clássica, peso institucional
# • Cabeçalho:        Cambria (nome) + Calibri (detalhes)
# • Tabelas:          Calibri 8-9pt  — compacta e limpa
FONT_CORPO   = "Calibri"     # sans-serif para texto corrido
FONT_TITULO  = "Cambria"     # serifa para títulos e peso institucional
FONT_HEADER  = "Cambria"     # serifa para nome da prefeitura
FONT_DETALHE = "Calibri"     # sans-serif para contato, notas

# ═══════════════════════════════════════════════════════════
#  TAMANHOS DE FONTE
# ═══════════════════════════════════════════════════════════
"""Tamanhos padronizados (em pontos)."""
SZ_CORPO   = 11     # 11pt conforme solicitado
SZ_TABELA  = 9
SZ_CITACAO = 9
SZ_NOTA    = 8
SZ_RODAPE  = 8

# ═══════════════════════════════════════════════════════════
#  CORES PADRONIZADAS
# ═══════════════════════════════════════════════════════════
"""Paleta de cores institucional da SMOSU."""
COR_INST         = '1F3864'
COR_LABEL_BG     = 'D6DCE4'
COR_BORDA_TABELA = 'C0C0C0'
COR_LABEL_FONT   = RGBColor(0x1F, 0x38, 0x64)
COR_CINZA_TEXTO  = RGBColor(0x44, 0x44, 0x44)
COR_CINZA_LEVE   = RGBColor(0x66, 0x66, 0x66)

# ═══════════════════════════════════════════════════════════
#  ESPAÇAMENTO PADRÃO
# ═══════════════════════════════════════════════════════════
"""Configuração de layout e ritmo vertical."""
PAR_AFTER = 120
LINE_SPC  = 276   # 1.15 linhas (276 twips)
INDENT_PADRAO = 1.25 # Identação padrão em cm

# ═══════════════════════════════════════════════════════════
#  DESIGN SYSTEM / LAYOUT (Tabelas e Cards)
# ═══════════════════════════════════════════════════════════
"""Dimensões (em twips) e cores para componentes visuais."""

# Tabela de Identificação
W_IDENT_LABEL = 2268
W_IDENT_VALUE = 7938

# Tabela de Dados Técnicos (Carimbo)
W_CARIMBO_L1 = 2000
W_CARIMBO_V1 = 3500
W_CARIMBO_L2 = 2000
W_CARIMBO_V2 = 2700

# Tabela de Partes Envolvidas
W_PARTES_LABEL = 2800
W_PARTES_VALUE = 7400

# Tabela de Histórico Cronológico
W_HIST_DATA  = 1400
W_HIST_EVENT = 6200
W_HIST_REF   = 2600

# Comunicado de Pendência (Cards)
W_CARD_TOTAL = 10200  # corrigido: cobre a área útil completa (~18cm)
COR_PENDENCIA_FILL  = 'FFFDF2'
COR_PENDENCIA_BORDA = 'F2C94C'
COR_PENDENCIA_TEXTO = RGBColor(0x5C, 0x4A, 0x21)
COR_PENDENCIA_ICON  = RGBColor(0x99, 0x65, 0x15)

COR_SUCESSO_FILL  = 'F5FCF5'
COR_SUCESSO_BORDA = '81C784'
COR_SUCESSO_TEXTO = RGBColor(0x26, 0x4D, 0x26)
COR_SUCESSO_ICON  = RGBColor(0x2E, 0x7D, 0x32)

# Alertas e Destaques
COR_ALERTA_RED   = RGBColor(0xCC, 0x00, 0x00)
COR_ALERTA_GREEN = RGBColor(0x00, 0x80, 0x00)
COR_DOC_BOX_FILL = 'EBF0FA'

# Área útil da página (Cm(21) - Cm(1.5) - Cm(1.5) ≈ 10205 twips; conservativo)
AREA_UTIL_TWIPS = 10200

# ═══════════════════════════════════════════════════════════
#  ASSINANTE PADRÃO
# ═══════════════════════════════════════════════════════════
"""Dados para o carimbo de assinatura automático."""
ASSINANTE = {
    "nome":     "Diego Tarcísio Nunes Vilela",
    "titulo":   "Engenheiro Civil",
    "registro": "CREA 235.474/D",
}
CIDADE = "Oliveira"

# ═══════════════════════════════════════════════════════════
#  MAPEAMENTO tipo_relatorio → categoria de gerador
# ═══════════════════════════════════════════════════════════
"""Dicionário mestre que define quais peças técnicas o sistema é capaz de gerar."""
TIPOS_DOCUMENTO = {
    # ── Pareceres Técnicos (completos, com dados do carimbo) ──
    "parecer_tecnico":                    "parecer_tecnico",
    "alvara_aprovacao":                   "parecer_tecnico",
    "alvara_mcmv":                        "parecer_tecnico",
    "alvara_construcao_comercial":        "parecer_tecnico",
    "alvara_regularizacao":               "parecer_tecnico",
    "alvara_ampliacao":                   "parecer_tecnico",
    "alvara_reforma":                     "parecer_tecnico",
    "alvara_galpao_comercial":            "parecer_tecnico",
    "alvara_reforma_demolicao_ampliacao": "parecer_tecnico",
    "alvara_substituicao_projeto":        "parecer_tecnico",
    "alvara_troca_responsavel_tecnico":   "parecer_simples",
    "regularizacao_complexa_multipla":    "parecer_tecnico",
    # ── Pareceres Administrativos (Layout limpo para certidões) ──
    "parecer_administrativo":             "parecer_administrativo",
    "certidoes_separadas_localizacao_confrontacao": "parecer_administrativo",

    # ── Pareceres Simples (sem dados do carimbo) ──
    "certidao_numero_2via":               "parecer_simples",
    "certidao_nome_rua":                  "parecer_simples",
    "certidao_localizacao":               "parecer_simples",
    "certidao_confrontacao":              "parecer_simples",
    "certidao_localizacao_corretiva":     "parecer_simples",
    "certidao_conjunta":                  "parecer_simples",
    "certidao_numero_comercial":          "parecer_simples",
    "certidao_averbacao":                 "parecer_simples",
    "certidao_decadencia":                "parecer_simples",
    "certidao_averbacao_decadencia":      "parecer_simples",
    "habitese_comum":                     "parecer_simples",
    "habitese_condominio":                "parecer_simples",
    "habitese_multa":                     "parecer_simples",
    "habitese_2via":                      "parecer_simples",
    "habitese_inclusao_area":             "parecer_tecnico",
    "alvara_renovacao":                   "parecer_simples",
    "alvara_cancelamento":                "parecer_simples",
    "alvara_substituicao_titular":        "parecer_simples",
    "alvara_demolicao":                   "parecer_simples",
    "certidao_demolicao":                 "parecer_simples",
    "certidao_desmembramento":            "parecer_simples",
    "certidao_retificacao_area":          "parecer_simples",
    "certidao_zue":                       "parecer_simples",

    # ── Ofícios e Memorandos ──
    "oficio_meio_ambiente":               "oficio",
    "parecer_juridico":                   "oficio",
    "oficio_juridico_embargo":            "oficio",
    "oficio_interno_materiais":           "oficio",
    "oficio_decreto_utilidade":           "oficio",
    "memorando":                          "oficio",

    # ── Comunicados ──
    "comunicado_indeferimento":           "comunicado",
    "comunicado_pendencia":               "comunicado_pendencia",
    "comunicado_baixa_cei":               "comunicado",
    "comunicado_decadencia":              "comunicado",
}

