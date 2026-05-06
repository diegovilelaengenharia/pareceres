# 🏗️ Plano Estratégico — SMOSU do Futuro

**Para:** Diego Vilela — Engenheiro Civil, Analista PMO Oliveira/MG  
**Data:** 06/05/2026  
**Visão:** Transformar o sistema de um *gerador de documentos* em um **analista digital completo** que trabalha ao seu lado.

---

## Diagnóstico

O motor DOCX está excelente (17 fases concluídas, 53 modelos, 42 templates). Mas o gargalo real está **antes do motor**: a leitura, interpretação e decisão consome 80% do tempo do engenheiro.

**Fluxo atual:** PDF → Leitura humana (30 min) → JSON manual → Motor DOCX → Revisão  
**Fluxo futuro:** PDF → IA analisa tudo (2 min) → Parecer pronto → Validação humana (3 min)

---

## Os 5 Pilares

### Pilar 1 — Ingestão Inteligente de PDFs
- P1-A: Classificador de Documentos (tipo de processo)
- P1-B: Extrator de dados por tipo de documento
- P1-C: Leitor de Plantas Arquitetônicas (visão Gemini)
- P1-D: Montador de Dossiê (múltiplos PDFs → 1 JSON)

### Pilar 2 — Base Cadastral Integrada
- P2-A: Cadastro de Lotes (SQLite)
- P2-B: Histórico de Processos indexado
- P2-C: Mapa de Zoneamento com parâmetros urbanísticos
- P2-D: Ferramenta MCP `consultar_lote`

### Pilar 3 — Motor de Decisão Automática
- P3-A: Árvore de Decisão por Tipo (top 5)
- P3-B: Detector de Pendências automático
- P3-C: Calculadora de Multas completa
- P3-D: Sugestor de Documentos a Emitir

### Pilar 4 — Fila de Trabalho e Produtividade
- P4-A: Fila de Processos no Painel GEM
- P4-B: Status e Prioridade por processo
- P4-C: Dashboard de Produtividade
- P4-D: Modo "Fila Rápida"

### Pilar 5 — Aprendizado Contínuo
- P5-A: Registro de Correções (diff DOCX)
- P5-B: Banco de Precedentes Ativo
- P5-C: Fine-tuning automático de Prompts
- P5-D: Relatório de Jurisprudência mensal

---

## Ordem de Sprints

| Sprint | Fases | Foco | Impacto |
|--------|-------|------|---------|
| 1 (1 sem) | P1-A + P3-A | Classificar PDF + Decidir automaticamente | ⭐⭐⭐⭐⭐ |
| 2 (1 sem) | P2-A + P3-B | Cadastro de lotes + Detector de pendências | ⭐⭐⭐⭐ |
| 3 (1 sem) | P4-A + P1-B | Fila de trabalho + Extração de dados | ⭐⭐⭐⭐ |
| 4 (1 sem) | P2-C + P3-C | Zoneamento + Multas | ⭐⭐⭐ |
| 5 (2 sem) | P1-C + P5-B | Leitor de Plantas + Precedentes | ⭐⭐⭐ |
| 6+ (cont) | P4-D + P5-A + P1-D | Fila rápida + Aprendizado + Dossiê | ⭐⭐ |

---

*Documento de referência para o Milestone v4.0+*
