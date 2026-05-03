---
phase: 11
title: Qualidade e Inteligência dos Pareceres
milestone: v2.0
status: complete
date: 2026-05-02
completed: 2026-05-02
---

# Phase 11 — CONTEXT.md
## Qualidade e Inteligência dos Pareceres

### Goal
Elevar drasticamente a qualidade dos documentos gerados pelo sistema GEM: os pareceres e certidões devem leer como análise completa de engenheiro civil — bem embasados, com cálculos explícitos, fundamentação legal específica e conclusões claras.

---

## Locked Decisions

### D1 — Escopo completo (todos os 4 componentes)
Todos os componentes entram na fase:
1. **Reescrever prompts da IA** (`3_Treinar_Inteligencia/00_INSTRUCAO_SISTEMA_GEMINI.md` e `01_GEM_INSTRUCOES.md`)
2. **Melhorar/criar modelos JSON** em `0_Modelos_Prontos/` (incluindo novos: alvará_regularização, habitese_multa)
3. **Criar gabarito de qualidade** — parecer manual do engenheiro como referência
4. **Melhorar o texto nos DOCX gerados** (considerandos, fundamentação, conclusão)

### D2 — Arquitetura: Wizard Interativo de 3 Camadas
O fluxo deixa de ser automático e passa a ser um wizard guiado:

**Camada 1 — Pré-seleção (10 seg do engenheiro)**
- Ao receber os arquivos, a IA apresenta um menu de 10 categorias
- A IA destaca sua sugestão com base nos documentos lidos
- Engenheiro confirma ou escolha outra categoria

**Camada 2 — Análise dirigida (IA com foco)**
- Com a categoria confirmada, a IA sabe exatamente quais campos extrair
- Executa checklist específico da categoria
- Faz no máximo 1-2 perguntas de disambiguação (ex: "residencial ou comercial?")
- Calcula índices e multas com fórmulas explícitas

**Camada 3 — Proposta + confirmação (decisão do engenheiro)**
- IA lista os documentos a emitir com áreas e valores
- Engenheiro confirma, remove, adiciona ou ajusta com linguagem natural
- Após confirmação → gera o JSON

**Vantagem**: Elimina a adivinhação de 36 tipos → seleção de 10 categorias → IA trabalha com contexto correto → pareceres certeiros.

### D3 — Problemas a resolver (todos os cinco)
1. Cálculos errados ou ausentes (TO, CA, TP, multas Art. 79 + LC 267 Art. 39)
2. Considerandos genéricos sem fato concreto
3. Campos JSON ausentes ou com valor nulo sem necessidade
4. Conclusões vagas sem dispositivo legal
5. Lógica de exceções não aplicada (decadência, lote ≤ 220m²)

### D4 — Formato dos considerandos: narrativo + legal junto
Cada considerando deve conter **três camadas obrigatórias**:
1. **Fato**: o que foi verificado no processo (medição, data, área, etc.)
2. **Dispositivo legal específico**: artigo + inciso + parágrafo com transcrição literal parcial
3. **Cálculo explícito** (quando aplicável): valores passo a passo, não só resultado final

Exemplo aceito:
> "Que a edificação possui área construída de 187,50 m² sobre terreno de 350,00 m², resultando em Taxa de Ocupação de 53,57% (187,50/350,00 × 100), dentro do limite de 60% previsto no Art. 9º, inciso I, Tabela 1 da LC 267/2019 para a Zona ZUR1."

### D5 — Gabarito nos dois lugares
O parecer manual de referência do engenheiro deve ser inserido:
- **No prompt** (`01_GEM_INSTRUCOES.md` ou arquivo dedicado) como exemplo few-shot com marcação `### EXEMPLO DE PARECER COMPLETO`
- **Em `0_Modelos_Prontos/`** como `MODELO_GABARITO_Alvara_Regularizacao.json` (ou similar), servindo de referência canônica para o motor Python

### D6 — Tipos de documento prioritários (ordem)
1. `alvará_regularização` — mais frequente, mais complexo (cálculos + multas)
2. `alvará_aprovação` — alto volume
3. `habitese_multa` — combina habite-se + cálculo de multa

> Modelos para estes 3 tipos devem ser criados/revisados primeiro. Os demais tipos aproveitam os padrões estabelecidos.

### D7 — Cálculos obrigatórios por tipo
| Tipo | Cálculos obrigatórios |
|------|----------------------|
| alvará_regularização | TO, CA, TP, multa Art. 79 Lei 1.544/86, multa Art. 39 LC 267/2019 |
| alvará_aprovação | TO, CA, TP (verificação prévia) |
| habitese_multa | TO, CA, TP (como construído), multa Art. 79, multa Art. 39 |

### D8 — Exceções legais obrigatórias (checklist explícito na IA)
A IA deve verificar e declarar explicitamente:
- **Decadência**: Art. 150 §4º CTN — se a obra tem 5+ anos sem autuação, multa Art. 79 é indevida
- **Lote ≤ 220m²**: §13 Art. 9º LC 267/2019 — afastamentos pelo Código Civil, não pela LC 267

---

## Inputs Necessários (pré-execução)

### I1 — Parecer manual de referência ✅ CONCLUÍDO
3 pareceres reais fornecidos pelo engenheiro em 2026-05-02:
- **Gabarito A**: Processo 545/2026 — Regularização com decadência parcial (ZUR03, 254,13m²)
- **Gabarito B**: Processo 108/2026 — Alvará de Construção projeto novo (ZUR-3, 59,10m²)
- **Gabarito C**: Processo 12329/2025 — Reforma, demolição e ampliação (ZUR3, 246,22m²)
- **Arquivos criados**: `3_Treinar_Inteligencia/04_GABARITO_PARECER.md` + `0_Modelos_Prontos/MODELO_GABARITO_Alvara_Regularizacao.json`

---

## Deferred Ideas (fora do escopo desta fase)
- Geoprocessamento e cruzamento com mapa de zoneamento (→ v3.0, Phase 8)
- OCR de alta fidelidade para PDFs escaneados (→ Phase 7)
- Automação total sem confirmação humana

---

## Files Created / Modified — STATUS FINAL

| Arquivo | Status |
|---------|--------|
| `3_Treinar_Inteligencia/00_INSTRUCAO_SISTEMA_GEMINI.md` | ✅ Reescrito v5.0 — Wizard de 4 Passos completo |
| `3_Treinar_Inteligencia/01_GEM_INSTRUCOES.md` | ✅ Reescrito — trigger de sessão simplificado |
| `3_Treinar_Inteligencia/04_GABARITO_PARECER.md` | ✅ Criado — 3 pareceres reais como few-shot |
| `3_Treinar_Inteligencia/05_MAPA_INTELIGENCIA.md` | ✅ Criado — árvore de decisão + cálculos |
| `3_Treinar_Inteligencia/06_BLOCOS_CONSIDERANDOS.md` | ✅ Criado — templates com 3 camadas |
| `3_Treinar_Inteligencia/07_COMO_USAR_NO_GEMINI.md` | ✅ Criado — guia operacional completo |
| `0_Modelos_Prontos/MODELO_GABARITO_Alvara_Regularizacao.json` | ✅ Criado — gabarito JSON canônico (processo 545/2026) |
| `0_Modelos_Prontos/MODELO_01_Alvara_Aprovacao.json` | ✅ Reescrito — gabarito completo (processo 108/2026) |
| `0_Modelos_Prontos/MODELO_14_Habitese_Multa.json` | ✅ Criado — habite-se com infração de TP + multa paga |
| `0_Modelos_Prontos/MODELO_15_Reforma_Ampliacao.json` | ✅ Criado — reforma+demolição+ampliação (processo 12329/2025) |
| `0_Modelos_Prontos/MODELO_08_Alvara_MCMV.json` | ✅ Revisado |
| `0_Modelos_Prontos/MODELO_09_Alvara_Construcao_Comercial.json` | ✅ Revisado |

---

## Success Criteria
- Parecer gerado para `alvará_regularização` inclui cálculos TO, CA, TP e dupla multa (Art. 79 + Art. 39), com valores passo a passo
- Cada considerando cita artigo específico e transcreve o cálculo
- Exceções (decadência, lote ≤ 220m²) são verificadas e declaradas antes de aplicar multa
- IA sugere lista de documentos antes de gerar JSON
- Gabarito manual do engenheiro está inserido como few-shot no prompt
