# Base de Conhecimento — Guia de Separação

## Visão Geral

O projeto possui **duas** localizações de conhecimento com propósitos distintos:

```text
Sistema/
├── base_conhecimento/         ← CORPUS JURÍDICO E TÉCNICO
│   ├── decreto_4149_2019.md   ← Textos legais na íntegra
│   ├── codex_legal.json       ← Índice jurídico estruturado
│   ├── geo_oliveira.json      ← Base geográfica (bairros, zoneamento)
│   ├── prompts/               ← Prompts de IA para análise
│   └── ...                    ← 39 documentos no total
│
└── inteligencia/
    └── Knowledge/             ← INSTRUÇÕES DO SIA (Sistema Interativo)
        ├── 00_SISTEMA_INTERATIVO.md  ← Prompt master do Gemini
        ├── 01_LEIS.md                ← Referência legal condensada
        ├── 02_GABARITOS_E_ESTILO.md  ← Guia de estilo de redação
        ├── 03_RETROALIMENTACAO.md    ← Histórico de aprendizados
        ├── 04_MANUAL_OPERACAO.md     ← Manual de operação do sistema
        ├── 05_CHECKLIST_DOCUMENTOS.md ← Checklist de documentação
        └── TRIGGER.md               ← Trigger de ativação do SIA
```

## Regras de Separação

### `base_conhecimento/` — Corpus Bruto
- **O que é:** Fonte de verdade jurídica e técnica. Textos legais, raciocínios, regras de cálculo.
- **Quem usa:** Ferramentas MCP (busca semântica via FAISS), IA durante análise, engenheiro humano.
- **Como cresce:** Adicionando novos textos de leis, decretos, raciocínios técnicos.
- **Não deve conter:** Instruções para a IA, prompts de sistema, gabaritos de estilo.

### `inteligencia/Knowledge/` — Instruções do SIA
- **O que é:** Manual de operação da IA. Define *como* o Gemini deve se comportar, que estilo usar, que checklist seguir.
- **Quem usa:** Exclusivamente o Gemini/Claude durante sessões interativas de análise.
- **Como cresce:** Atualizando instruções, adicionando gabaritos, retroalimentando com aprendizados.
- **Não deve conter:** Textos legais na íntegra (referenciar `base_conhecimento/` ao invés).

## Quando Adicionar Conteúdo

| Tipo de conteúdo | Destino |
|------------------|---------|
| Nova lei ou decreto | `base_conhecimento/` |
| Novo raciocínio técnico | `base_conhecimento/` |
| Dados geográficos | `base_conhecimento/geo_oliveira.json` |
| Prompt de IA | `base_conhecimento/prompts/` |
| Instrução de comportamento do Gemini | `inteligencia/Knowledge/` |
| Gabarito de estilo/redação | `inteligencia/Knowledge/02_GABARITOS_E_ESTILO.md` |
| Aprendizado de caso real | `inteligencia/Knowledge/03_RETROALIMENTACAO.md` |

---
*Documentação criada: 2026-05-06*
