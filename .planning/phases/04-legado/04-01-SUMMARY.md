---
phase: 04-legado
plan: 01
subsystem: Motor Python
tags: [refactor, technical-debt, cleanup]
requirements: [FR-02, NFR-01]
tech_stack: [python, docx]
key_files:
  - _Sistema_Interno/01_Motor_Python/config.py
  - _Sistema_Interno/01_Motor_Python/geradores/__init__.py
  - _Sistema_Interno/01_Motor_Python/compilador.py
  - _Sistema_Interno/01_Motor_Python/json/processo_1065_2026.json
  - _Sistema_Interno/01_Motor_Python/json/processo_6100_Maria.json
decisions:
  - Removidos fallbacks de compatibilidade para forçar o uso de IDs técnicos estritos.
  - Implementada validação de presença do campo 'tipo_relatorio' no gerador base.
  - Substituídas heurísticas de sanitização de strings por checagem direta no mapa de tipos.
metrics:
  duration: 15m
  completed_date: "2025-05-15T14:30:00Z"
---

# Phase 04 Plan 01: Saneamento de IDs e Limpeza de Legado - Summary

Este plano eliminou a dívida técnica relacionada ao despacho de documentos, movendo o sistema de um modelo baseado em strings descritivas flexíveis para um modelo de IDs técnicos estritos.

## Key Changes

### 1. Migração de Dados e Config
- Removido o alias `"regularizacao"` do `config.py`.
- Atualizados os arquivos de teste `processo_1065_2026.json` e `processo_6100_Maria.json` para usar o ID canônico `"alvara_regularizacao"`.

### 2. Fortalecimento do Despacho (geradores/__init__.py)
- A função `gerar()` agora exige explicitamente o campo `"tipo_relatorio"`, lançando `ValueError` caso esteja ausente.
- Removido o default inseguro que assumia `"regularizacao"`.
- Melhoria nas mensagens de erro quando um tipo de documento não é encontrado no `config.py`.

### 3. Simplificação do Orquestrador (compilador.py)
- Removida a lógica que tentava identificar tipos de documentos contendo espaços ou traços.
- Implementada validação robusta contra o dicionário `TIPOS_DOCUMENTO`.
- Adicionado log de erro detalhado para IDs técnicos inválidos em documentos secundários (`documentos_emitir`).

## Deviations from Plan

Nenhuma - o plano foi executado exatamente como escrito.

## Verification Results

- **Suite de Testes:** `python run_tests.py --motor` executado com 100% de sucesso (5 testes).
- **Teste de Falha Controlada:** Verificado que tipos inexistentes geram erros legíveis e bloqueiam a compilação de forma segura.

## Self-Check: PASSED
- [x] Aliases removidos do config.py.
- [x] JSONs de teste atualizados.
- [x] Validação de tipo obrigatório implementada.
- [x] Heurísticas de string removidas do compilador.
- [x] Commits atômicos realizados para cada tarefa.
