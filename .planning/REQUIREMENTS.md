# Requirements — Milestone v2.0 & v3.0

**Milestone:** v2.0 — Qualidade Interna e Manutenibilidade
**Milestone:** v3.0 — Expansão da Inteligência e Geoprocessamento
**Created:** 2026-05-01 (v2.0), 2026-05-02 (v3.0)

---

## Functional Requirements (v2.0)

### FR-01 — Portabilidade de Paths
- O motor deve ser executável sem edição manual de caminhos após clonar o repositório.
- **Acceptance:** `grep -r "C:\\" _Sistema_Interno/` retorna zero resultados em código Python.

### FR-02 — Limpeza de Lógica Legada no Compilador
- Remover ou consolidar a lógica de "tipos descritivos legados" em `compilador.py`.
- **Acceptance:** `compilador.py` não contém branches `if tipo in [...]` com listas hardcoded de tipos antigos.

### FR-03 — Mecanismo de Detecção de Dessincronização de Templates
- Criar um utilitário que compare os placeholders existentes nos templates Word com as chaves injetadas pelos geradores.
- **Acceptance:** Executar `python template_checker.py` produz relatório sem erros críticos nos templates atuais.

### FR-04 — Documentação de Desenvolvedor
- Documentar módulos e funções públicas. Criar `ARCHITECTURE.md`.

### FR-05 — Integração de OCR com Gemini CLI
- Utilizar capacidades do Gemini para ler PDFs complexos e gerar JSON.

### ARCH-01 — Arquitetura de Pacotes Python
- Organizar o motor Python em subpacotes (core, generators, analyzers, extractors, ui, utils).
- **Acceptance:** Não existem arquivos `.py` (exceto `__init__.py`) diretamente na raiz de `01_Motor_Python/`.

### ARCH-02 — Limpeza da Raiz do Projeto
- Remover scripts utilitários da raiz do projeto, movendo-os para pastas internas do sistema.
- **Acceptance:** A raiz contém apenas pastas numeradas e o entry-point `.bat`.

### ARCH-03 — Consolidação de Planejamento
- Unificar toda a documentação de planejamento e requisitos em um único local (`.planning/`).
- **Acceptance:** O diretório `.gemini/plans/` foi removido ou está vazio após a consolidação.

---

## Non-Functional Requirements

### NFR-01 — Sem Quebra de Compatibilidade
- Nenhuma alteração pode quebrar a geração de documentos existentes.
- A suite `run_tests.py --motor` deve passar 100% após cada fase.

### NFR-02 — Execução Local Windows
- O sistema deve continuar executando 100% local no Windows sem dependências externas novas (exceto API Gemini já em uso).

---

## Out of Scope

- Integração com sistemas externos de banco de dados SQL (→ v4.0+)
- Interface web nova (→ backlog)
