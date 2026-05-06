# Roadmap

This document outlines the phased execution plan.

## ✅ Milestone v1.0 — Integração e Elevação de Padrões *(archived 2026-05-01)*

> Brownfield integration: dependências formalizadas, logging persistente, validação de tipos, testes negativos. → [Detalhes](milestones/v1.0-ROADMAP.md)

---

## Milestone v2.0 — Qualidade Interna e Manutenibilidade

*Objetivo: Eliminar dívida técnica acumulada sem introduzir novas features. Quatro frentes: portabilidade de paths, limpeza de lógica legada, detector de dessincronização de templates, e documentação de desenvolvedor.*

### ✅ Phase 3: Portabilidade de Paths *(concluída 2026-05-01)*
- **Goal**: Substituir todos os paths hardcoded em código Python e scripts `.bat` por resoluções relativas (`pathlib.Path(__file__).parent`, `%~dp0`), garantindo que o motor funcione após clonar em qualquer diretório.
- **Requirements**: FR-01, NFR-01, NFR-02
- **Status**: [complete]

### ✅ Phase 4: Limpeza de Lógica Legada no Compilador *(concluída 2026-05-02)*
- **Goal**: Consolidar e remover o código de despacho de "tipos descritivos legados" em `compilador.py`. Toda lógica de mapeamento de tipos deve fluir exclusivamente via `config.TIPOS_DOCUMENTO`.
- **Requirements**: FR-02, NFR-01
- **Status**: [complete]

### ✅ Phase 5: Detector de Dessincronização de Templates *(concluída 2026-05-02)*
- **Goal**: Criar `template_checker.py` que compara placeholders e campos nos arquivos JSON de `0_Modelos_Prontos/` e `templates/` com os campos injetados/requisitados pelos geradores.
- **Requirements**: FR-03, NFR-01
- **Status**: [complete]
- **Plans**:
    - [x] 05-01-PLAN.md — Criação do Detector de Dessincronização

### ✅ Phase 6: Excelência Arquitetural e Inteligência Operacional *(concluída 2026-05-02)*
- **Goal**: Elevar a qualidade arquitetural através da abstração de motores, sincronização dinâmica de schema e observabilidade via painel JSON-aware. 
- **Requirements**: FR-03, NFR-01
- **Status**: [complete]
- **Plans**:
    - [x] 06-01-PLAN.md — Abstração de Motores e Sincronização de Schema

### ✅ Phase 7: Integração de OCR de Alta Fidelidade (Local) *(concluída 2026-05-02)*
- **Goal**: Implementar fluxo de entrada baseado em Docling + PaddleOCR para extração de dados de PDFs complexos, eliminando a dependência de APIs externas.    
- **Requirements**: FR-05, NFR-01, NFR-02
- **Status**: [complete]
- **Plans**:
    - [x] 07-01-PLAN.md — Implementação e Validação de OCR Local Híbrido

### ✅ Phase 9: Reorganização Estrutural e Consolidação *(concluída 2026-05-02)*
- **Goal**: Reorganizar o motor Python em subpacotes, limpar a raiz do projeto e consolidar o planejamento em `.planning/`.
- **Requirements**: ARCH-01, ARCH-02, ARCH-03
- **Status**: [complete]
- **Plans**:
    - [x] 09-01-PLAN.md — Reorganização e Consolidação de Estrutura

### ✅ Phase 10: Manutenção e Finalização *(concluída 2026-05-02)*
- **Goal**: Refinar a UI/UX, consolidar a documentação e preparar o sistema para entrega final (Produto Final).
- **Requirements**: FR-04, NFR-01, NFR-02
- **Status**: [complete]
- **Plans**:
    - [x] 10-01-PLAN.md — Refinamento Estrutural e Documentação
    - [x] 10-02-PLAN.md — Evolução UI/UX (Painel GEM)

### ✅ Phase 11: Qualidade e Inteligência dos Pareceres *(concluída 2026-05-02)*
- **Goal**: Elevar a qualidade dos documentos gerados pelo GEM — reescrever prompts, criar gabaritos, adicionar cálculos explícitos (TO, CA, TP, multas), formato de considerandos narrativo+legal, fluxo de confirmação de documentos antes da geração do JSON.
- **Requirements**: FR-01, FR-02, FR-06
- **Status**: [complete]
- **Plans**:
    - [x] 11-01-PLAN.md — Reescrita de Prompts e Gabarito de Qualidade
    - [ ] 11-02-PLAN.md — Novos Modelos JSON (alvará_regularização, habitese_multa)
- **Context**: [11-CONTEXT.md](phases/11-qualidade-inteligencia/11-CONTEXT.md)

### ✅ Phase 13: Excelência Operacional e Conformidade Legal *(concluída 2026-05-06)*
- **Goal**: Garantir que todos os pareceres sigam o Decreto 4.149/2019, implementar validação cruzada JSON vs DOCX, atualizar templates para nova estrutura GEM e consolidar o Golden Dataset de auditoria.
- **Requirements**: conformidade legal, excelência operacional, design impecável
- **Status**: [complete]
- **Plans**: 3 plans
    - [x] 13-01-PLAN.md — Alinhamento Legal e Evolução de Templates
    - [x] 13-02-PLAN.md — Golden Dataset e Validação Cruzada
    - [x] 13-03-PLAN.md — Excelência Visual e Documentação Final

---

## Milestone v2.1 — Inteligência Gerativa Superior

*Objetivo: Garantir que o GEM entregue textos finais prontos para emissão, respeitando a hierarquia normativa e o padrão de redação tripartite (Fato -> Artigo -> Cálculo).*

### ✅ Phase 02.1: Inteligência e Prompts (v2.1) *(concluída 2026-05-05)*
- **Goal**: Atualizar o motor de inteligência para gerar campos narrativos sem placeholders, priorizando o Decreto 4.149/2019 e aplicando o estilo tripartite nos considerandos.
- **Requirements**: INT-01
- **Status**: [complete]
- **Plans**: 1 plan
    - [x] 02.1-01-PLAN.md — Atualização de Prompts e Gabaritos (Texto Final)

### ✅ Phase 02.2: Refatoração do Motor (Surgical Update) (v2.1) *(concluída 2026-05-05)*
- **Goal**: Ajustar o comportamento do motor para respeitar a soberania do conteúdo gerado pela IA, tornando prefixos opcionais e suprimindo marcadores intrusivos.
- **Requirements**: INT-01
- **Status**: [complete]
- **Plans**: 1 plan
    - [x] 02.2-01-PLAN.md — Inteligência de Prefixo, Supressão de Marcadores e Auditoria

---

## Milestone v2.2 — Automação e Fluxo Contínuo

*Objetivo: Integrar as ferramentas MCP ao fluxo de análise interativa, eliminando a subjetividade e garantindo precisão matemática e legal.*

### ✅ Phase 03.1: Integração de Ferramentas MCP (SIA v1.1) *(concluída 2026-05-06)*
- **Goal**: Sincronizar o SIA com as ferramentas do servidor MCP SMOSU para cálculos, validações e fundamentação legal automática.
- **Requirements**: INT-01
- **Status**: [complete]
- **Plans**: 1 plan
    - [x] 02.2-02-PLAN.md — Integração de Ferramentas MCP e Protocolo de Rigor

---

## Milestone v3.0 — Expansão da Inteligência e Geoprocessamento

*Objetivo: Integrar legislações de 2025, diretrizes de preservação histórica (IEPHA) e automação de cruzamento geográfico.*

### ✅ Phase 12: Upgrade dos Compiladores DOCX/PDF *(concluída 2026-05-03)*
- **Goal**: Elevar a fidelidade visual e robustez técnica dos documentos gerados. Corrigir bugs de layout (margens de célula, largura de rodapé/cards), adicionar section headings coloridos para multas (vermelho) e condicionantes (verde), caixa sombreada para memória de cálculo, borda lateral nos itens de documentos, e unificar `compilador_livre.py` com o pipeline principal.
- **Requirements**: qualidade visual, fidelidade DOCX/PDF, profissionalismo dos pareceres
- **Status**: [complete]

### Phase 8: Expansão da Inteligência e Integração de Legislações
- **Goal**: Processar a pasta "LEGISLAÇÕES PARA TREINAR E REVISAR", extrair informações cruciais e atualizar a base de conhecimento e lógica do motor (IEPHA, Multas 2025, LEI 4.071/2025).
- **Requirements**: FR-06, FR-07
- **Status**: [planned]
- **Plans**:
    - [ ] 08-01-PLAN.md — Integração de Legislações 2025 e IEPHA

### Phase 14: Suporte a Múltiplas Certidões Separadas
- **Goal**: Implementar a geração de múltiplos documentos (Parecer, Localização, Confrontação) a partir de um único JSON usando o tipo mestre `certidoes_separadas_localizacao_confrontacao`.
- **Requirements**: FR-01, FR-02, ARCH-01
- **Status**: [planned]
- **Plans**:
    - [x] 14-01-PLAN.md — Implementação do Pipeline de Certidões em Lote

### ✅ Phase 15: Refino de Layout Administrativo *(concluída 2026-05-06)*
- **Goal**: Implementar o layout "Parecer Administrativo" (limpo) para processos de certidões, removendo tabelas de índices urbanísticos desnecessárias.
- **Requirements**: FR-01, FR-02, ARCH-01
- **Status**: [complete]
- **Plans**:
    - [x] 15-01-PLAN.md — Criação do Layout Administrativo Limpo

### ✅ Phase 16: Refatoração do Gerador DOCX *(concluída 2026-05-05)*
- **Goal**: Refatorar completamente o pipeline de geração DOCX para corrigir problemas de conteúdo/texto nos pareceres, simplificar os modelos, melhorar o preview HTML e criar um fluxo mais inteligente de template → preview → DOCX.
- **Requirements**: NFR-01, NFR-02, FR-01
- **Depends on**: Phase 15
- **Status**: [complete]
- **Plans**: 4 plans
    - [x] 16-01-PLAN.md — Criar enricher.py e integrar ao geradores_core.py
    - [x] 16-02-PLAN.md — Corrigir preview_html.py (4 divergências estruturais)
    - [x] 16-03-PLAN.md — Quebrar componentes.py em pacote componentes/
    - [x] 16-04-PLAN.md — Limpar templates JSON e validar pipeline end-to-end

---
*Roadmap updated: 2026-05-05*
