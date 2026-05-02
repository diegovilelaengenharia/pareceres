# Gerador Automático de Documentos SMOSU

**What This Is:**
Um sistema em Python desenvolvido para a Prefeitura de Oliveira/MG (SMOSU) que orquestra a validação e geração automática de pareceres técnicos, ofícios e comunicados a partir de arquivos JSON de entrada, utilizando templates estruturados no Microsoft Word (.docx).

**Core Value:**
Automatizar o trabalho repetitivo de redação técnica, garantindo padronização, precisão (com cálculos automáticos de índices e prazos) e conformidade legal nos documentos emitidos pela prefeitura.

**Target Audience:**
Engenheiros e servidores públicos do PMO (Prefeitura Municipal de Oliveira).

**Key Constraints:**
- A execução deve permanecer local no Windows para proteção dos dados municipais.
- O formato de saída estrito é o DOCX (padrão prefeitura).
- Qualquer mudança na estrutura não deve quebrar a compatibilidade com a geração de lotes em JSON.

## Requirements

### Validated

- ✓ Leitura em lote e individual de arquivos JSON.
- ✓ Validação semântica e cálculo de índices urbanísticos (Permeabilidade, Ocupação).
- ✓ Verificação de pendências e decadência.
- ✓ Geração de DOCX utilizando templates baseados em `python-docx`.
- ✓ Interface de pré-visualização web (painel HTML) com alertas em tempo real.
- ✓ Integração com múltiplas sub-rotinas especializadas para diferentes tipos documentais (Pareceres, Ofícios, Comunicados, Multas, SERO).

### Active

- [ ] Milestone v2.0: portabilidade de paths hardcoded, refatoração de lógica legada, sincronização automática de templates.

### Out of Scope

- [N/A no momento]

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Embarque no GSD | O objetivo não é criar uma feature pontual agora, mas sim colocar o sistema sob os trilhos e processos do GSD para permitir auditorias, reviews e elevação da qualidade arquitetural. | ✅ Completo (v1.0) |
| Logging persistente | Motor precisava de rastreabilidade de erros em produção além dos prints no terminal. | ✅ `logger.py` + `motor.log` (v1.0 Phase 2) |
| Validação de tipos no schema | Campos textuais aceitavam int/bool silenciosamente, causando falhas no python-docx. | ✅ `isinstance` checks no schema_validator (v1.0 Phase 2) |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-01 after initialization*
