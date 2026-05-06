# MANUAL DE OPERAÇÃO GEM SMOSU — Versão 2.0 (Maio/2026)

Sistema de Geração Automatizada de Pareceres Técnicos  
SMOSU — Secretaria Municipal de Obras e Serviços Urbanos de Oliveira/MG  
Responsável: Eng. Diego Tarcísio Nunes Vilela — CREA 235.474/D

---

## 1. VISÃO GERAL DO SISTEMA

O **GEM SMOSU** é um sistema de geração automatizada de pareceres técnicos municipais composto por três camadas:

| Camada | Componente | Função |
|--------|-----------|--------|
| **Inteligência** | Gemini Gem (SIA v1.1) | Análise interativa, extração de dados, geração de texto |
| **Motor** | Python (`Sistema/motor/`) | Compilação de DOCX/PDF a partir do JSON do Gemini |
| **Ferramentas** | Servidor MCP (`Sistema/mcp-smosu/`) | Cálculos determinísticos: índices, multas, logradouros |

### Fluxo de Trabalho Padrão

```
PDF do Processo
      ↓
  Gemini Gem (SIA v1.1)
  — análise fase a fase —
  — chamadas MCP obrigatórias —
  — gera JSON estruturado —
      ↓
  Motor Python (gerar.py)
  — compila DOCX + PDF —
      ↓
  Pasta Saída / Assinatura
```

---

## 2. CONFIGURAÇÃO DO AMBIENTE (PASSO A PASSO)

### Passo 1: Servidor MCP

O servidor MCP é **obrigatório** para cálculos determinísticos:

```
python Sistema/mcp-smosu/server.py
```

Confirme que as ferramentas estão ativas verificando o output:

```
[MCP] Server running — 17 tools available
```

Se o servidor não iniciar, verifique:
- Python 3.10+ instalado
- Dependências: `pip install -r Sistema/mcp-smosu/requirements.txt`
- Arquivo `decreto_4149_2019.md` presente em `Sistema/base_conhecimento/`

### Passo 2: Configuração do Gemini Gem (SIA v1.1)

**System Instructions:** Copie o conteúdo de `Sistema/inteligencia/Knowledge/00_SISTEMA_INTERATIVO.md` nas System Instructions do Gem.

**Knowledge Files (obrigatórios — subir no Gem):**

| # | Arquivo | Conteúdo |
|---|---------|---------|
| 1 | `base_conhecimento/lc_267_2019_uso_ocupacao.md` | Zonas, TO/CA/TP por zona |
| 2 | `base_conhecimento/lei_1544_1986_codigo_obras.md` | Art. 79 (multas), prazos |
| 3 | `inteligencia/Knowledge/02_GABARITOS_E_ESTILO.md` | Gabaritos de texto dos pareceres |
| 4 | `inteligencia/Knowledge/03_RETROALIMENTACAO.md` | Lições aprendidas em processos reais |
| 5 | `inteligencia/Knowledge/05_CHECKLIST_DOCUMENTOS.md` | Documentos exigidos por tipo de processo |
| 6 | `base_conhecimento/estilo_narrativo_pareceres.md` | Estilo de redação do Eng. Diego |

### Passo 3: Painel de Geração

Para gerar documentos via interface visual:

```
python Sistema/motor/ui/painel_gem.py
```

---

## 3. O SIA — SISTEMA INTERATIVO DE ANÁLISE (v1.1)

O SIA é o protocolo de análise em 6 fases que governa como o Gemini processa cada processo.

### Fases e Ferramentas MCP Obrigatórias

| Fase | Descrição | Ferramentas MCP |
|------|-----------|----------------|
| **0** | Menu inicial — seleção de tipo | — |
| **1** | Triagem documental | `validar_checklist_documentos`, `buscar_diretriz_processo` |
| **2** | Identificação do imóvel | `buscar_logradouro_oficial`, `consultar_indices_urbanisticos` |
| **3** | Análise técnica | `validar_parametros_projeto`, `gerar_memoria_calculo_indices`, `analisar_decadencia` |
| **4** | Multas e sanções | `calcular_multas_processo` |
| **5** | Roteamento de documentos | `consultar_documentos_emitir`, `estruturar_historico_cronologico` |

### Protocolo de Rigor Técnico (MCP)

O SIA v1.1 proíbe **cálculos manuais**. As seguintes operações são sempre delegadas ao MCP:

- **Áreas e índices (TO, TP, CA):** Somente via `gerar_memoria_calculo_indices`
- **Multas:** Somente via `calcular_multas_processo`
- **Logradouros:** Somente via `buscar_logradouro_oficial`
- **Decadência:** Somente via `analisar_decadencia`

Se o servidor MCP estiver offline, o SIA entra em **modo degradado** (aviso explícito) e exige que o engenheiro preencha os campos manualmente.

---

## 4. O JSON — ESTRUTURA DE DADOS

O Gemini gera um JSON estruturado que o motor transforma em DOCX. Campos principais:

### Campos Obrigatórios (todos os tipos)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `tipo_relatorio` | string | ID técnico do tipo de documento (ver config.py) |
| `numero_processo` | string | Ex: `"1234/2026"` |
| `data_processo` | string | Ex: `"06/05/2026"` |
| `requerente` | string | Nome completo do requerente |
| `logradouro` | string | Nome oficial da rua (validado pelo MCP) |
| `considerandos` | lista de strings | Cada item é um parágrafo "Considerando que..." |

### Campos Técnicos (para pareceres com Alvará)

| Campo | Tipo | Obrigatoriedade | Base Legal |
|-------|------|-----------------|------------|
| `area_terreno` | string | Obrigatório | Art. 11, Dec. 4.149/2019 |
| `area_total_construida` | string | Obrigatório | Art. 11, Dec. 4.149/2019 |
| `taxa_ocupacao` | string | Obrigatório | Art. 11, Dec. 4.149/2019 |
| `taxa_permeabilidade` | string | Obrigatório | Art. 11, Dec. 4.149/2019 |
| `coef_aproveitamento` | string | Obrigatório | Art. 11, Dec. 4.149/2019 |
| `zona_uso` | string | Obrigatório | Lei nº 267/2019 |
| `art_rrt` | string | Obrigatório | Art. 5º, IV, Dec. 4.149/2019 |
| `memoria_de_calculo` | string | Recomendado | Boa prática técnica |

> **Formato de `memoria_de_calculo`:** Texto corrido com quebras de linha `\n`. Inclua operações como `TO = 120,50 / 360,00 = 33,47%`.

### Campos de Histórico e Partes (Art. 11, Dec. 4.149/2019)

**`historico_cronologico`** — lista de objetos:
```json
[
  {"data": "15/03/2026", "evento": "Descrição do evento", "referencia": "fls. 01-05"},
  {"data": "06/05/2026", "evento": "Análise técnica concluída", "referencia": "fls. 40-41"}
]
```

**`partes_envolvidas`** — objeto estruturado:
```json
{
  "requerente": {"nome": "João da Silva", "cpf": "123.456.789-00"},
  "responsavel_tecnico": {"nome": "Maria Arquiteta", "registro": "CAU A123-4/MG"},
  "agentes_fiscais": ["Fiscal A (Mat. 001)", "Fiscal B (Mat. 002)"],
  "assinante_parecer": {"nome": "Diego Vilela", "cargo": "Engenheiro Civil / SMOSU"}
}
```

---

## 5. CONFORMIDADE COM O DECRETO 4.149/2019

O sistema valida automaticamente os seguintes requisitos:

| Artigo | Requisito | Validação Automática |
|--------|-----------|---------------------|
| Art. 4º | Documentos para Alvará de Construção | `validar_checklist_documentos` |
| Art. 5º | Documentos para Habite-se | `validar_checklist_documentos` |
| Art. 5º, VI | RT obrigatório no Habite-se | Schema validator |
| Art. 6º | Documentos para Alvará de Regularização | `validar_checklist_documentos` |
| Art. 7º | Certidão Imobiliária validade 30 dias | `validar_checklist_documentos` |
| Art. 8º | Prazo de 15 dias para regularização | Comunicado de Pendência |
| Art. 11 | Dados técnicos no parecer (TO, CA, TP) | Schema validator + Motor |

O `schema_validator.py` emite aviso de **"Não conformidade com Decreto 4.149/2019"** quando campos obrigatórios do Art. 11 estão ausentes em pareceres técnicos.

---

## 6. TIPOS DE DOCUMENTO DISPONÍVEIS

| ID (`tipo_relatorio`) | Nome | Categoria |
|-----------------------|------|-----------|
| `alvara_aprovacao` | Parecer + Alvará de Construção | `parecer_tecnico` |
| `alvara_regularizacao` | Parecer + Alvará de Regularização | `parecer_tecnico` |
| `alvara_construcao_comercial` | Alvará Comercial | `parecer_tecnico` |
| `alvara_mcmv` | MCMV — Minha Casa Minha Vida | `parecer_tecnico` |
| `habitese_comum` | Habite-se e Averbação | `parecer_simples` |
| `certidoes_separadas_localizacao_confrontacao` | Certidões Separadas | `parecer_administrativo` |
| `comunicado_pendencia` | Comunicado de Pendência Documental | `comunicado_pendencia` |
| `parecer_tecnico` | Parecer Técnico Genérico | `parecer_tecnico` |

---

## 7. AUDITORIA DE QUALIDADE (GOLDEN DATASET)

O sistema inclui um conjunto de dados de referência para auditoria de fidelidade:

```
python Sistema/motor/scripts/validador_fidelidade.py --all
```

Casos incluídos:
- `alvara_ouro.json` — Alvará de Aprovação complexo (11 campos verificados)
- `habitese_ouro.json` — Habite-se com histórico de 5 eventos
- `pendencia_ouro.json` — Comunicado de Pendência com 3 pendências

O validador compara os dados do JSON de entrada com o texto extraído do DOCX gerado, garantindo fidelidade de 100% nos campos críticos.

---

## 8. PROTOCOLOS DE ANÁLISE JURÍDICA

### 8.1 Decadência Administrativa (Art. 150 §4º CTN)
- **Decadência Total:** Obra irregular > 5 anos (comprovada por Planta Cadastral antiga) sem averbação no SRI.
- **Decadência Parcial:** Decadência incide apenas sobre a parte irregular; o que está averbado é regular.
- **Proibição:** Nunca conceder decadência para áreas já constantes na Matrícula.

### 8.2 Cadeia Dominial e Titularidade
- **Promissário Comprador:** Aceitar se o Contrato de C&V estiver anexado.
- **Troca de Requerente no Trâmite:** Manter histórico e emitir no nome do proprietário/comprador final.

### 8.3 Lotes Pequenos (≤ 220m²)
- Afastamentos do Código Civil (1,50m), mas TO e TP **continuam obrigatórias** conforme a zona.

### 8.4 Restrições Ambientais e Patrimoniais
- **APP:** Citar Lei 3.971/2023 e exigir recuo mínimo do CODEMA.
- **IEPHA (ZC-2):** Bloqueio absoluto até Nota Técnica do IEPHA.

---

*Manual v2.0 — 06/05/2026 — SMOSU — Sistema GEM v2.0*
