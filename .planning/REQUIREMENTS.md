# Requirements — Milestones v1.0 → v3.0 (Todos Completos)

**Consolidado em:** 2026-05-06

---

## ✅ Functional Requirements (Todos Validados)

### FR-01 — Portabilidade de Paths *(v2.0 Fase 3)*
- ✅ Motor executável sem edição manual de caminhos após clonar o repositório.

### FR-02 — Limpeza de Lógica Legada *(v2.0 Fase 4)*
- ✅ Tipos consolidados exclusivamente via `config.TIPOS_DOCUMENTO`.

### FR-03 — Detector de Dessincronização de Templates *(v2.0 Fase 5)*
- ✅ `template_checker.py` compara placeholders com chaves dos geradores.

### FR-04 — Documentação de Desenvolvedor *(v2.0 Fase 10)*
- ✅ ARCHITECTURE.md, STRUCTURE.md, CONCERNS.md, TESTING.md criados e mantidos.

### FR-05 — Integração de OCR *(v2.0 Fase 7)*
- ✅ Docling + PaddleOCR para extração local de PDFs.

### ARCH-01 — Arquitetura de Pacotes Python *(v2.0 Fase 9)*
- ✅ Motor organizado em core/, generators/, analyzers/, extractors/, utils/, ui/.

### ARCH-02 — Limpeza da Raiz do Projeto *(v2.0 Fase 9)*
- ✅ Raiz contém apenas Entrada/, Saida/, Sistema/ e GERAR_DOCUMENTOS.bat.

### ARCH-03 — Consolidação de Planejamento *(v2.0 Fase 9)*
- ✅ Documentação de planejamento unificada em `.planning/`.

### INT-01 — Inteligência Gerativa Superior *(v2.1 Fases 02.1, 02.2)*
- ✅ Prompts tripartite, soberania de conteúdo da IA, enricher de dados.

### MCP-01 — Integração de Ferramentas MCP *(v2.2 Fase 03.1)*
- ✅ 13 ferramentas MCP operacionais com Protocolo de Rigor Técnico.

---

## ✅ Non-Functional Requirements (Todos Validados)

### NFR-01 — Sem Quebra de Compatibilidade
- ✅ Geração de documentos existentes funcional em todas as fases.

### NFR-02 — Execução Local Windows
- ✅ Sistema 100% local no Windows. Única dependência externa é a API Gemini (para análise, não para geração).

---

## Out of Scope

- Integração com banco de dados SQL (→ v4.0+)
- Interface web SPA (→ backlog)
- Conversão automática para PDF (desativada)

---
*Requirements consolidation: 2026-05-06*
