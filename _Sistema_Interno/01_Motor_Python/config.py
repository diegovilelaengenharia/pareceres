"""
Configuração central do sistema de geração de documentos — SMOSU Oliveira/MG.
Constantes, cores, fontes, caminhos e mapeamento de tipos.
"""

import os
from docx.shared import RGBColor

# ═══════════════════════════════════════════════════════════
#  CAMINHOS
# ═══════════════════════════════════════════════════════════
SCRIPT_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR     = os.path.dirname(SCRIPT_DIR)  # pasta raiz: 02. Pareceres
LOGO_BRASAO     = os.path.join(SCRIPT_DIR, "logos", "logo_brasao.jpeg")
LOGO_PREFEITURA = os.path.join(SCRIPT_DIR, "logos", "logo_prefeitura.png")
TEMPLATES_DIR   = os.path.join(SCRIPT_DIR, "templates")

# ═══════════════════════════════════════════════════════════
#  TIPOGRAFIA
# ═══════════════════════════════════════════════════════════
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
SZ_CORPO   = 11     # 11pt conforme solicitado
SZ_TABELA  = 9
SZ_CITACAO = 9
SZ_NOTA    = 8
SZ_RODAPE  = 8

# ═══════════════════════════════════════════════════════════
#  CORES PADRONIZADAS
# ═══════════════════════════════════════════════════════════
COR_INST         = '1F3864'
COR_LABEL_BG     = 'D6DCE4'
COR_BORDA_TABELA = 'C0C0C0'
COR_LABEL_FONT   = RGBColor(0x1F, 0x38, 0x64)
COR_CINZA_TEXTO  = RGBColor(0x44, 0x44, 0x44)
COR_CINZA_LEVE   = RGBColor(0x66, 0x66, 0x66)

# ═══════════════════════════════════════════════════════════
#  ESPAÇAMENTO PADRÃO
# ═══════════════════════════════════════════════════════════
PAR_AFTER = 120
LINE_SPC  = 276   # 1.15 linhas (276 twips)

# ═══════════════════════════════════════════════════════════
#  ASSINANTE PADRÃO
# ═══════════════════════════════════════════════════════════
ASSINANTE = {
    "nome":     "Diego Tarcísio Nunes Vilela",
    "titulo":   "Engenheiro Civil",
    "registro": "CREA 235.474/D",
}
CIDADE = "Oliveira"

# ═══════════════════════════════════════════════════════════
#  MAPEAMENTO tipo_relatorio → categoria de gerador
# ═══════════════════════════════════════════════════════════
TIPOS_DOCUMENTO = {
    # ── Pareceres Técnicos (completos, com dados do carimbo) ──
    "alvara_aprovacao":                   "parecer_tecnico",
    "alvara_regularizacao":               "parecer_tecnico",
    "alvara_ampliacao":                   "parecer_tecnico",
    "alvara_galpao_comercial":            "parecer_tecnico",
    "alvara_reforma_demolicao_ampliacao": "parecer_tecnico",
    "alvara_substituicao_projeto":        "parecer_tecnico",
    "regularizacao":                      "parecer_tecnico",  # compatibilidade

    # ── Pareceres Simples (sem dados do carimbo) ──
    "certidao_numero_2via":               "parecer_simples",
    "certidao_nome_rua":                  "parecer_simples",
    "certidao_localizacao":               "parecer_simples",
    "certidao_conjunta":                  "parecer_simples",
    "certidao_numero_comercial":          "parecer_simples",
    "habitese_comum":                     "parecer_simples",
    "habitese_multa":                     "parecer_simples",
    "certidao_averbacao_decadencia":      "parecer_simples",
    "habitese_2via":                      "parecer_simples",
    "habitese_inclusao_area":             "parecer_simples",
    "alvara_renovacao":                   "parecer_simples",
    "alvara_cancelamento":                "parecer_simples",
    "alvara_substituicao_titular":        "parecer_simples",
    "alvara_demolicao":                   "parecer_simples",
    "certidao_demolicao":                 "parecer_simples",
    "certidao_desmembramento":            "parecer_simples",
    "certidao_retificacao_area":          "parecer_simples",

    # ── Ofícios ──
    "oficio_meio_ambiente":               "oficio",
    "parecer_juridico":                   "oficio",
    "oficio_juridico_embargo":            "oficio",
    "oficio_interno_materiais":           "oficio",
    "oficio_decreto_utilidade":           "oficio",

    # ── Comunicados ──
    "comunicado_indeferimento":           "comunicado",
    "comunicado_pendencia":               "comunicado_pendencia",
    
    # ── Documentos de Emissão da Secretaria (Prontos / Balcão) ──
    "alvara_oficial":                     "documento_pronto",
    "carta_habitese_oficial":             "documento_pronto",
    "certidao_oficial":                   "documento_pronto",
}
