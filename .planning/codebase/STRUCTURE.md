# Codebase Structure

**Analysis Date:** 2026-05-06 (atualizado pós-Milestone v3.0)

## Directory Layout

```text
02. Pareceres/                          <- RAIZ
├── GERAR_DOCUMENTOS.bat                <- Entry point
├── Entrada/                            <- JSONs de entrada
├── Saida/                              <- DOCX gerados
├── PARECERES PEDRO/                    <- Dados de produção
├── Sistema/
│   ├── AJUDA.md                        <- Manual do usuário
│   ├── base_conhecimento/              <- 39 docs legais
│   ├── inteligencia/Knowledge/         <- 8 docs do SIA
│   ├── logs/                           <- motor.log
│   ├── mcp-smosu/                      <- Servidor MCP (13 tools)
│   ├── modelos/                        <- 53 modelos JSON
│   └── motor/
│       ├── core/                       <- config, logger, schema, consistencia
│       ├── generators/                 <- compilador, geradores, enricher, aliases
│       │   └── componentes/            <- Blocos visuais DOCX
│       ├── analyzers/                  <- Análise de PDFs e triagem
│       ├── extractors/                 <- OCR e extração
│       ├── utils/                      <- Cálculos, alertas, multas
│       ├── ui/                         <- Painel GEM + preview HTML
│       ├── templates/                  <- 42 templates JSON por tipo
│       ├── tests/                      <- Testes + golden dataset
│       ├── scripts/                    <- Utilitários (validador, checker)
│       ├── json/                       <- Matriz documental
│       └── logos/                      <- Imagens institucionais
└── .planning/                          <- Infraestrutura GSD
```

## Key File Locations

**Entry Points:**
- `GERAR_DOCUMENTOS.bat` → abre o Painel GEM
- `Sistema/motor/ui/painel_gem.py` → servidor HTTP do painel
- `Sistema/motor/generators/compilador.py` → orquestrador central

**Configuration:**
- `Sistema/motor/core/config.py` → caminhos, cores, fontes, TIPOS_DOCUMENTO

**Core Logic:**
- `Sistema/motor/generators/geradores_core.py` → despacho + geração DOCX
- `Sistema/motor/generators/enricher.py` → enriquecimento via templates
- `Sistema/motor/generators/_aliases.py` → normalização de variáveis

**Testing:**
- `Sistema/motor/scripts/run_tests.py` → testes E2E
- `Sistema/motor/tests/test_geradores.py` → testes automatizados

## Where to Add New Code

**Novo tipo de documento:**
1. Modelo JSON em `Sistema/modelos/MODELO_NN_*.json`
2. Mapear em `core/config.py` → `TIPOS_DOCUMENTO`
3. Template JSON em `motor/templates/` (se necessário)
4. Atualizar `catalogo_modelos.json`

**Nova regra de validação:**
- Adicionar em `motor/utils/` ou `core/consistencia.py`
- Integrar no pré-voo do `compilador.py`

**Novo componente visual:**
- Criar em `motor/generators/componentes/`
- Re-exportar no `componentes/__init__.py`

---
*Structure analysis: 2026-05-06*
