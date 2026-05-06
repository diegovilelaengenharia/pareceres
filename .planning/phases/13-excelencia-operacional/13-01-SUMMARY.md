---
phase: 13-excelencia-operacional
plan: 13-01
subsystem: motor-legal
tags: [templates, validation, decreto-4149, compliance]
dependency_graph:
  requires: []
  provides: [template-updates, legal-validation]
  affects: [Sistema/motor/templates, Sistema/motor/core/schema_validator.py]
tech_stack:
  added: []
  patterns: [JSON Schema Validation, Legal Compliance Enforcement]
key_files:
  created: []
  modified:
    - Sistema/motor/templates/alvara_aprovacao.json
    - Sistema/motor/templates/habitese_comum.json
    - Sistema/motor/templates/alvara_regularizacao.json
    - Sistema/motor/core/schema_validator.py
    - Sistema/inteligencia/Knowledge/05_CHECKLIST_DOCUMENTOS.md
decisions:
  - Adicionado suporte explícito aos campos 'historico_cronologico' e 'partes_envolvidas' em todos os templates principais.
  - Implementada validação de estrutura para o histórico cronológico (data, evento, referencia).
  - Injetados avisos de não conformidade com o Art. 11 do Decreto 4.149/2019 no validador de schema para índices urbanísticos ausentes.
metrics:
  duration: 45m
  completed_date: "2026-05-04"
---

# Phase 13 Plan 01: Alinhamento Legal e Templates Summary

Este plano alinhou a estrutura de dados do motor com as exigências legais do Decreto 4.149/2019, garantindo que os pareceres técnicos e checklists estejam em conformidade com a legislação municipal de Oliveira-MG.

## Principais Mudanças

### 1. Atualização de Templates JSON
- Os arquivos `alvara_aprovacao.json`, `habitese_comum.json` e `alvara_regularizacao.json` foram atualizados para incluir:
    - Descrições detalhadas para as chaves `historico_cronologico` e `partes_envolvidas`, referenciando o Art. 11 do Decreto 4.149/2019.
    - Confirmação de campos técnicos obrigatórios (`taxa_ocupacao`, `taxa_permeabilidade`, etc.) em pareceres técnicos.

### 2. Reforço no Validador de Schema (`schema_validator.py`)
- Adicionada verificação de conformidade com o Art. 11 do Decreto 4.149/2019 para categorias `parecer_tecnico`. O sistema agora emite avisos se `taxa_ocupacao`, `taxa_permeabilidade`, `coef_aproveitamento` ou `area_total_construida` estiverem ausentes.
- Implementada validação rigorosa para o campo `historico_cronologico`, exigindo a estrutura `{"data": "...", "evento": "...", "referencia": "..."}`.
- Corrigidos avisos de placeholder para serem mais descritivos quanto à criticidade (Tier A/B).

### 3. Alinhamento do Checklist de Documentos
- O arquivo `05_CHECKLIST_DOCUMENTOS.md` foi revisado e atualizado para refletir exatamente as exigências dos Artigos 4, 5, 6 e 7 do Decreto.
- Incluída a obrigatoriedade de Responsabilidade Técnica (RT) para Habite-se (Art. 5º, VI).
- Especificado o prazo de validade de 30 dias para Certidão Imobiliária em processos de Topografia (Art. 7º, IV).

### 4. Verificação de Cores Institucionais
- Confirmado que `Sistema/motor/core/config.py` utiliza o "Azul SMOSU" (`#1F3864`) conforme o padrão estabelecido.

## Deviations from Plan

Nenhuma - o plano foi executado exatamente como escrito, com a adição da verificação de cores solicitada pelo usuário no prompt inicial.

## Self-Check: PASSED
- [x] Templates atualizados com novas chaves e descrições legais.
- [x] Validador de schema detectando ausência de índices urbanísticos e erros de formatação no histórico.
- [x] Checklist de documentos 100% alinhado com o Decreto 4.149/2019.
- [x] Cores institucionais verificadas no `config.py`.

## TDD Gate Compliance
- N/A (Plano de execução, não TDD puro).
