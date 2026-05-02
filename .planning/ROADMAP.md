# Roadmap

This document outlines the phased execution plan.

## ✅ Milestone v1.0 — Integração e Elevação de Padrões *(archived 2026-05-01)*

> Brownfield integration: dependências formalizadas, logging persistente, validação de tipos, testes negativos. → [Detalhes](milestones/v1.0-ROADMAP.md)

---

## Milestone v2.0 — Qualidade Interna e Manutenibilidade

*Objetivo: Eliminar dívida técnica acumulada sem introduzir novas features. Quatro frentes: portabilidade de paths, limpeza de lógica legada, detector de dessincronização de templates, e documentação de desenvolvedor.*

### Phase 3: Portabilidade de Paths
- **Goal**: Substituir todos os paths hardcoded em código Python e scripts `.bat` por resoluções relativas (`pathlib.Path(__file__).parent`, `%~dp0`), garantindo que o motor funcione após clonar em qualquer diretório.
- **Requirements**: FR-01, NFR-01, NFR-02
- **Status**: [pending_planning]

### Phase 4: Limpeza de Lógica Legada no Compilador
- **Goal**: Consolidar e remover o código de despacho de "tipos descritivos legados" em `compilador.py`. Toda lógica de mapeamento de tipos deve fluir exclusivamente via `config.TIPOS_DOCUMENTO`.
- **Requirements**: FR-02, NFR-01
- **Status**: [pending_planning]

### Phase 5: Detector de Dessincronização de Templates
- **Goal**: Criar `template_checker.py` que compara placeholders nos arquivos `.docx` de `0_Modelos_Prontos/` com os campos injetados pelos geradores, emitindo relatório de divergências.
- **Requirements**: FR-03, NFR-01
- **Status**: [pending_planning]

### Phase 6: Documentação de Desenvolvedor
- **Goal**: Docstrings de módulo em todos os arquivos Python do motor, docstrings em funções públicas longas, e criação de `ARCHITECTURE.md` descrevendo o fluxo completo do sistema.
- **Requirements**: FR-04
- **Status**: [pending_planning]

---
*Roadmap updated: 2026-05-01*
