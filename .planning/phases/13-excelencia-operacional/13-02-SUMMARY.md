---
phase: 13-excelencia-operacional
plan: 13-02
subsystem: motor-qualidade
tags: [golden-dataset, validacao-cruzada, fidelidade, auditoria]
dependency_graph:
  requires: [13-01]
  provides: [golden-dataset, validador-fidelidade]
  affects: [Sistema/motor/tests/golden_dataset, Sistema/motor/scripts/validador_fidelidade.py]
tech_stack:
  added: []
  patterns: [Golden Dataset, Cross-Validation, Fidelity Audit]
key_files:
  created:
    - Sistema/motor/tests/golden_dataset/alvara_ouro.json
    - Sistema/motor/tests/golden_dataset/habitese_ouro.json
    - Sistema/motor/tests/golden_dataset/pendencia_ouro.json
    - Sistema/motor/tests/golden_dataset/relatorio_auditoria.md
    - Sistema/motor/scripts/validador_fidelidade.py
  modified:
    - Sistema/motor/generators/componentes/comunicado.py
decisions:
  - Golden Dataset cobre os 3 principais casos de uso: Alvará de Aprovação, Habite-se Comum e Comunicado de Pendência.
  - Validador de fidelidade extrai texto do DOCX gerado e compara campos críticos (numéricos e de texto) com o JSON de entrada.
  - Bug corrigido em comunicado.py: COR_PENDENCIA_BORDA era string hex mas era usada como RGBColor em font.color.rgb.
metrics:
  duration: 30m
  completed_date: "2026-05-06"
---

# Phase 13 Plan 02: Golden Dataset e Validação Cruzada — Summary

Este plano estabeleceu o controle de qualidade rigoroso do motor através de um conjunto de dados de referência e uma ferramenta de validação cruzada automática.

## Principais Mudanças

### 1. Golden Dataset (3 casos padrão-ouro)
- **`alvara_ouro.json`**: Alvará de Aprovação com dados complexos — índices urbanísticos detalhados, memória de cálculo, 4 eventos no histórico, partes envolvidas completas (requerente, RT, fiscais, assinante), 3 documentos a emitir.
- **`habitese_ouro.json`**: Habite-se Comum com 5 eventos históricos, dados de vistoria dupla, observação fiscal específica.
- **`pendencia_ouro.json`**: Comunicado de Pendência com 3 itens de pendência documental fundamentados nos Arts. 5º e 6º do Decreto 4.149/2019.

### 2. Validador de Fidelidade (`validador_fidelidade.py`)
- Carrega cada JSON do Golden Dataset, gera o DOCX via motor, extrai todo o texto e compara.
- Campos numéricos verificados: `area_terreno`, `area_total_construida`, `taxa_ocupacao`, `taxa_permeabilidade`, `coef_aproveitamento`.
- Campos de texto verificados: `numero_processo`, `requerente`, `logradouro`, `numero_alvara`, `matricula_sri`, `inscricao_municipal`, `art_rrt`.
- Normalização inteligente: aceita variações de separador decimal (vírgula vs ponto) e sufixos (m², %).
- Gera `relatorio_auditoria.md` com tabela detalhada de resultados por caso.
- Suporta modos: `--all`, `--file <caminho>`, `--test-mode`.

### 3. Bug Corrigido: `comunicado.py` linha 143
- `r_bullet.font.color.rgb = COR_PENDENCIA_BORDA` causava `ValueError` porque `COR_PENDENCIA_BORDA` é string hex, não `RGBColor`.
- Corrigido para `RGBColor(0xF2, 0xC9, 0x4C)` inline.

## Resultado da Auditoria Final

| Caso | Tipo | Status | Campos |
|------|------|--------|--------|
| `alvara_ouro.json` | `alvara_aprovacao` | **PASS** | 11/11 MATCH |
| `habitese_ouro.json` | `habitese_comum` | **PASS** | 7/7 MATCH |
| `pendencia_ouro.json` | `comunicado_pendencia` | **PASS** | 3/3 MATCH |

**Fidelidade total: 100% — zero discrepâncias entre JSON de entrada e DOCX gerado.**

## Deviations from Plan
- Bug em `comunicado.py` identificado e corrigido durante a execução (não estava no escopo original mas foi necessário para viabilizar a geração do 3º caso).

## Self-Check: PASSED
- [x] Golden Dataset com 3 arquivos JSON de alta qualidade criados.
- [x] Validador de fidelidade operacional (`--all`, `--file`, `--test-mode`).
- [x] Auditoria concluída com 100% de fidelidade nos campos críticos.
- [x] Relatório `relatorio_auditoria.md` gerado no diretório do dataset.
