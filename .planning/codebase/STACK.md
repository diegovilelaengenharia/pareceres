# Technology Stack

**Analysis Date:** 2026-05-06 (atualizado pós-Milestone v3.0)

## Languages

**Primary:**
- Python 3.x — Motor de geração em `Sistema/motor/`

**Secondary:**
- HTML/CSS — Painel GEM (`ui/painel_gem.html`, 85KB) e Preview HTML
- JSON — Modelos (53), Templates (42), Base de conhecimento

## Runtime

**Environment:**
- Python Runtime (Windows local)

**Package Manager:**
- pip
- Dependências: `Sistema/motor/requirements.txt`

## Frameworks

**Core:**
- `python-docx` — Geração de documentos Word
- `jinja2` — Renderização HTML para previews

**AI/MCP:**
- Servidor MCP (Model Context Protocol) — `Sistema/mcp-smosu/`
- FAISS — Busca vetorial para recuperação semântica de legislação
- Gemini API — Análise de PDFs e geração de JSON (via SIA)

**Testing:**
- Custom test runner: `scripts/run_tests.py`
- Golden Dataset: `tests/golden_dataset/`

**Build/Dev:**
- Windows Batch Scripts (.bat) — Entry point

## Key Dependencies

**Critical:**
- `python-docx` — Geração dos documentos DOCX
- `colorama` — Output formatado no terminal
- `faiss-cpu` — Índice vetorial para o MCP
- `sentence-transformers` — Embeddings para busca semântica

**Configuration:**
- Centralizado em `Sistema/motor/core/config.py`

## Platform Requirements

**Development:**
- Python 3.9+
- Windows 10/11

**Production:**
- Execução local em estações Windows da prefeitura
- Google Drive para sincronização de arquivos

---
*Stack analysis: 2026-05-06*
