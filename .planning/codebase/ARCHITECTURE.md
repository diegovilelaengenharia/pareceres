<!-- refreshed: 2026-05-06 -->
# Architecture

**Analysis Date:** 2026-05-06 (atualizado pós-Milestone v3.0)

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    Interface de Usuário                      │
│       GERAR_DOCUMENTOS.bat  →  Painel GEM (Navegador)       │
│                 Sistema/motor/ui/painel_gem.py               │
└──────────────────┬──────────────────┬───────────────────────┘
                   │                  │
                   ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Orquestrador Central                       │
│            Sistema/motor/generators/compilador.py             │
│       (Pré-voo → Preview HTML → Despacho → Pós-voo)         │
└────────┬──────────────────┬──────────────────┬──────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   Validadores    │ │   Processadores  │ │    Geradores     │
│ core/            │ │ utils/           │ │ generators/      │
│ ├ consistencia   │ │ ├ calculadora    │ │ ├ geradores_core  │
│ ├ schema_valid.  │ │ ├ alertas_dec.   │ │ ├ componentes/   │
│ └ base_engine    │ │ ├ verificador_m  │ │ ├ enricher       │
│                  │ │ └ cobertura_cons │ │ ├ formatacao     │
│  analyzers/      │ │                  │ │ ├ cabecalho      │
│ ├ inspetor_doc   │ │  extractors/     │ │ └ _aliases       │
│ ├ analisador_pdf │ │ ├ extrator_pdf   │ │                  │
│ └ metricas_tria  │ │ ├ hybrid_extr.   │ │  ui/             │
│                  │ │ └ ocr_engine     │ │ ├ painel_gem     │
│                  │ │                  │ │ └ preview_html   │
└──────────────────┘ └──────────────────┘ └──────────────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Camada de Persistência e Saída                  │
│        Sistema/modelos/ (Modelos JSON de Referência)         │
│        motor/templates/ (Templates JSON por Tipo)            │
│        Entrada/ (JSON de entrada)                            │
│        Saida/ (DOCX gerados)                                 │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              Camada de Inteligência                          │
│        Sistema/base_conhecimento/ (39 docs legais)           │
│        Sistema/inteligencia/Knowledge/ (SIA v1.1)            │
│        Sistema/mcp-smosu/ (Servidor MCP — 13 ferramentas)    │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Painel GEM | Interface web para validação e compilação | `Sistema/motor/ui/painel_gem.py` |
| Compilador | Orquestração do fluxo completo (pré-voo → geração) | `Sistema/motor/generators/compilador.py` |
| Geradores Core | Despacho por categoria e geração de DOCX | `Sistema/motor/generators/geradores_core.py` |
| Enricher | Enriquecimento de dados ausentes via modelos do template | `Sistema/motor/generators/enricher.py` |
| Aliases | Normalização de variáveis do JSON (30+ campos canônicos) | `Sistema/motor/generators/_aliases.py` |
| Componentes | Construção de blocos visuais do DOCX (título, tabelas, corpo) | `Sistema/motor/generators/componentes/` |
| Configuração | Caminhos, cores, fontes, mapeamento de tipos | `Sistema/motor/core/config.py` |
| Consistência | Verificação semântica dos dados | `Sistema/motor/core/consistencia.py` |
| Schema Validator | Validação de tipos e estrutura do JSON | `Sistema/motor/core/schema_validator.py` |
| Calculadora | Cálculos de índices urbanísticos (TO, TP, CA) | `Sistema/motor/utils/calculadora_indices.py` |
| Alertas | Verificação de decadência tributária | `Sistema/motor/utils/alertas_decadencia.py` |
| Cobertura | Análise de completude dos considerandos | `Sistema/motor/utils/cobertura_considerandos.py` |
| Inspetor | Verificação de conformidade documental | `Sistema/motor/analyzers/inspetor_documental.py` |
| Preview HTML | Geração de preview no navegador antes do DOCX | `Sistema/motor/ui/preview_html.py` |
| MCP SMOSU | Servidor MCP com ferramentas de cálculo e validação legal | `Sistema/mcp-smosu/server.py` |

## Pattern Overview

**Overall:** Orchestrator-Worker (Dispatcher) com Pipeline de Enriquecimento

**Key Characteristics:**
- **Decoupling**: O compilador não conhece a lógica de cada tipo — delega para `geradores_core.py` via mapeamento `TIPOS_DOCUMENTO`.
- **Centralized Config**: Todos os caminhos, cores e mapeamentos vivem em `core/config.py`.
- **Validation First**: Documentos só são gerados após aprovação no pré-voo (cálculos, consistência, cobertura).
- **Enrichment Pipeline**: O `enricher.py` preenche lacunas com modelos narrativos do template antes da geração.
- **Alias Resolution**: O `_aliases.py` normaliza variações de nomenclatura do LLM antes de tudo.

## Layers

**Input Layer:**
- Purpose: Entrada de dados para o usuário.
- Location: `Entrada/`
- Contains: Arquivos JSON (colados manualmente ou gerados pelo Gemini).
- Depends on: None.
- Used by: Compilador.

**Intelligence Layer (novo):**
- Purpose: Base de conhecimento e ferramentas de IA.
- Location: `Sistema/base_conhecimento/`, `Sistema/inteligencia/`, `Sistema/mcp-smosu/`
- Contains: Leis, decretos, raciocínio técnico, prompts, ferramentas MCP.
- Depends on: None.
- Used by: Gemini/Claude durante a análise interativa.

**Logic Layer:**
- Purpose: Validação, cálculo e análise.
- Location: `Sistema/motor/core/`, `Sistema/motor/utils/`, `Sistema/motor/analyzers/`
- Contains: Módulos de validação, cálculos urbanísticos e inspeção documental.
- Depends on: `core/config.py`.
- Used by: Compilador (pré-voo).

**Generation Layer:**
- Purpose: Preenchimento de templates e exportação DOCX.
- Location: `Sistema/motor/generators/`
- Contains: Geradores por categoria, componentes visuais, enricher, aliases.
- Depends on: `python-docx`, `core/config.py`.
- Used by: Compilador.

**Presentation Layer:**
- Purpose: Interface web para revisão e aprovação.
- Location: `Sistema/motor/ui/`
- Contains: Painel GEM (HTML/CSS/Python), Preview HTML.
- Depends on: Webbrowser, HTTP server embutido.
- Used by: Usuário final.

## Data Flow

### Primary Request Path (DOCX Generation)

1. **Entry**: Usuário executa `GERAR_DOCUMENTOS.bat` → abre Painel GEM no navegador.
2. **Scan**: `compilador.py` escaneia `Entrada/` para arquivos JSON.
3. **Normalize**: `_aliases.py` resolve sinônimos de campos.
4. **Validate**: Pré-voo com `consistencia.py`, `calculadora_indices.py`, `alertas_decadencia.py`, `cobertura_considerandos.py`.
5. **Preview**: `preview_html.py` gera visualização no navegador para aprovação humana.
6. **Enrich**: `enricher.py` interpola modelos narrativos para campos ausentes.
7. **Generate**: `geradores_core.py` despacha para o gerador da categoria (`parecer_tecnico`, `parecer_simples`, `oficio`, etc.).
8. **Output**: DOCX salvo em `Saida/Processo XXXX-YYYY - Nome/`.

### Intelligence Flow (via MCP)

1. **Análise**: Usuário envia PDF ao Gemini/Claude com contexto do SIA.
2. **Ferramentas**: IA invoca ferramentas MCP (`calcular_indices`, `validar_conformidade`, `fundamentar_legalmente`).
3. **Output**: IA gera JSON estruturado conforme modelo de referência.
4. **Pipeline**: JSON é processado pelo motor normalmente.

**State Management:**
- Stateless por execução — informações passam via dicts/JSON entre módulos.

## Architectural Constraints

- **Threading**: Single-threaded (processamento síncrono).
- **Global state**: Evitado; `config.py` atua como estado imutável global.
- **Circular imports**: Prevenidos pela separação core ↔ generators ↔ utils.
- **Windows-only**: Execução 100% local no Windows por proteção dos dados municipais.
- **DOCX-only**: Formato de saída estrito é DOCX (padrão da prefeitura).

## Error Handling

**Strategy**: Stop-on-error para validação, logging para execução.

**Patterns**:
- Try-Except no `compilador.py` capturando exceções dos geradores.
- Logging via `core/logger.py` para `Sistema/logs/motor.log`.
- Campos críticos ausentes são substituídos por `[PREENCHER: campo]` no DOCX.
- Pré-voo exibe alertas visuais mas não bloqueia a geração (decisão do operador).

---

*Architecture analysis: 2026-05-06 (pós-Milestone v3.0)*
