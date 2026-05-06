# External Integrations

**Analysis Date:** 2026-05-06 (atualizado pós-Milestone v3.0)

## APIs & External Services

**Gemini API:**
- Usado pelo SIA (Sistema Interativo de Análise) para leitura de PDFs e geração de JSON.
- Não é dependência do motor de geração — a geração funciona 100% offline.
- Configuração: via chave de API no ambiente do Gemini CLI.

**MCP SMOSU (Model Context Protocol):**
- Servidor local com 13 ferramentas de cálculo e validação.
- Location: `Sistema/mcp-smosu/server.py`
- Ferramentas incluem: cálculo de índices urbanísticos, validação de conformidade legal, fundamentação jurídica automática, busca semântica na base de conhecimento.

## Data Storage

**Databases:**
- N/A (arquivos JSON como fonte de dados)

**File Storage:**
- Filesystem local (sincronizado via Google Drive)
  - Entradas: `Entrada/`
  - Saídas: `Saida/`
  - Modelos: `Sistema/modelos/`
  - Templates: `Sistema/motor/templates/`
  - Base de conhecimento: `Sistema/base_conhecimento/`

**Indices:**
- FAISS: `Sistema/mcp-smosu/vector_index.faiss` (busca vetorial)
- Metadata: `Sistema/mcp-smosu/vector_metadata.pkl`

## Monitoring & Observability

**Error Tracking:**
- Custom logger em `Sistema/motor/core/logger.py`
- Log textual: `Sistema/logs/motor.log`
- Log JSON: `Sistema/logs/motor.json.log`

**Logs:**
- Console output via `colorama` (com ícones e cores)
- File logging persistente

## CI/CD & Deployment

**Hosting:** Local Windows Machine
**CI Pipeline:** Nenhum (testes manuais via `run_tests.py`)
**Deploy:** Cópia via Google Drive para Desktop

---
*Integration audit: 2026-05-06*
