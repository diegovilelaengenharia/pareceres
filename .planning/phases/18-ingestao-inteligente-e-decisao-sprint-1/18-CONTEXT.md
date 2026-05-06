# Phase 18: Ingestão Inteligente e Decisão (Sprint 1) - Context

**Gathered:** 2026-05-06
**Status:** Ready for planning
**Source:** PLANO_ESTRATEGICO.md

<domain>
## Phase Boundary
Esta fase implementa as duas primeiras peças do Analista Digital (Pilar 1 e Pilar 3):
1. **Classificador de Documentos (P1-A):** Recebe um PDF e identifica automaticamente de qual tipo de processo se trata (Alvará, Habite-se, etc.).
2. **Árvore de Decisão Automática (P3-A):** Avalia as regras de negócio para os 5 tipos de processos mais comuns, verificando se os requisitos de aprovação foram atingidos.

**O que NÃO entra agora:**
- Leitura de plantas por visão computacional (P1-C - Sprint 5)
- Banco SQLite de matrículas e zonas (P2-A e P2-C - Sprints 2 e 4)
- Fila visual no painel GEM (P4-A - Sprint 3)
</domain>

<decisions>
## Implementation Decisions

### 1. Ingestão Inteligente (P1-A)
- **Tecnologia:** Gemini 2.5 Pro via API (através do componente existente MCP/Enricher ou novo extrator dedicado).
- **Entrada:** Caminho do arquivo PDF.
- **Saída:** Enumeração restrita do tipo de documento detectado (ex: `alvara_construcao_residencial`, `habitese_comum`).
- **Abordagem:** Utilizar a capacidade multimodal do Gemini (PDF reading) combinada com extração estruturada (JSON schema) para garantir a tipagem correta.
- **Módulo:** Criar um módulo em `Sistema/motor/analyzers/` focado em ingestão de PDF.

### 2. Árvore de Decisão (P3-A)
- **Escopo:** Cobrir apenas os 5 tipos de processos mais frequentes na triagem.
  - Alvará Aprovação
  - Habite-se Comum
  - Certidão Localização
  - Comunicado Pendência
  - Regularização
- **Abordagem:** Criar um motor de regras de negócio em Python (não dependente de IA para a lógica dura) que receba os dados brutos (parâmetros urbanísticos atuais) e valide contra a regra (ex: TO <= 70%).
- **Resultado:** A árvore de decisão deve anexar ao JSON processado a recomendação ("APROVADO", "PENDENCIA", "INDEFERIDO") para que o motor DOCX gere a minuta automaticamente com base nisso.

</decisions>

<canonical_refs>
## Canonical References
- `Sistema/motor/generators/compilador.py` — Entender o fluxo de geração atual.
- `Sistema/motor/generators/enricher.py` — Onde a IA já é acionada hoje.
- `Sistema/BASE_CONHECIMENTO_GUIA.md` — Para referenciar leis nas regras da árvore.
</canonical_refs>

---
*Contexto gerado automaticamente com base no Plano Estratégico.*
