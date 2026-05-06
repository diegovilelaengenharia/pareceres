# Gerador Automático de Documentos SMOSU

**What This Is:**
Um sistema em Python desenvolvido para a Prefeitura de Oliveira/MG (SMOSU) que orquestra a validação e geração automática de pareceres técnicos, ofícios, comunicados e certidões a partir de arquivos JSON de entrada. Integra um motor de inteligência artificial (SIA v1.1), servidor MCP com 13 ferramentas de cálculo e validação, e uma base de conhecimento jurídica completa.

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

- ✓ Leitura em lote e individual de arquivos JSON. *(v1.0)*
- ✓ Validação semântica e cálculo de índices urbanísticos (TO, TP, CA). *(v1.0)*
- ✓ Verificação de pendências e decadência. *(v1.0)*
- ✓ Geração de DOCX utilizando componentes modulares via `python-docx`. *(v1.0, v2.0)*
- ✓ Interface de pré-visualização web (Painel GEM) com alertas em tempo real. *(v2.0)*
- ✓ Portabilidade de paths — motor funciona em qualquer diretório. *(v2.0 Fase 3)*
- ✓ Consolidação de lógica legada — tipos unificados em `TIPOS_DOCUMENTO`. *(v2.0 Fase 4)*
- ✓ Detector de dessincronização de templates. *(v2.0 Fase 5)*
- ✓ Arquitetura modular com subpacotes (core, generators, analyzers, extractors, utils, ui). *(v2.0 Fase 9)*
- ✓ Inteligência gerativa com prompts tripartite (Fato→Artigo→Cálculo). *(v2.1)*
- ✓ Enricher de dados via modelos do template. *(v2.0 Fase 16)*
- ✓ Integração MCP com 13 ferramentas de cálculo e validação legal. *(v2.2)*
- ✓ 53 modelos de documento cobrindo todos os tipos emitidos pela SMOSU. *(v3.0)*
- ✓ Golden Dataset e Validador de Fidelidade para auditoria cruzada. *(v2.0 Fase 13)*
- ✓ Conformidade auditada com Decreto 4.149/2019. *(v2.0 Fase 13)*

### Active

- [ ] (Nenhum requisito ativo — projeto em estado estável)

### Out of Scope

- Integração com sistemas externos de banco de dados SQL (→ v4.0+)
- Interface web nova / SPA (→ backlog)
- Conversão automática para PDF (desativada por decisão do usuário)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Embarque no GSD | Colocar o sistema sob processos GSD para auditorias e qualidade. | ✅ Completo (v1.0) |
| Logging persistente | Rastreabilidade de erros em produção. | ✅ `logger.py` + `motor.log` (v1.0) |
| Validação de tipos no schema | Campos textuais aceitavam int/bool silenciosamente. | ✅ `isinstance` checks (v1.0) |
| Enricher de dados | Templates preenchem campos ausentes sem sobrescrever IA. | ✅ `enricher.py` (v2.0 Fase 16) |
| Aliases normalizados | LLM gera variações de nomes de campos. | ✅ `_aliases.py` com 30+ campos (v2.0 Fase 16) |
| Servidor MCP | Ferramentas de cálculo acessíveis pela IA durante análise. | ✅ 13 ferramentas (v2.2) |
| Layout Administrativo | Certidões não precisam de tabela de índices urbanísticos. | ✅ `parecer_administrativo` (v3.0 Fase 15) |
| Pacote componentes/ | Componentes.py monolítico quebrado em módulos temáticos. | ✅ 6 módulos (v2.0 Fase 16) |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition:**
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone:**
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-06 (auditoria pós-Milestone v3.0)*
