# 📘 MANUAL DE OPERAÇÃO GEM SMOSU — Versão 7.0 (Maio/2026)

Este manual consolida os aprendizados de 10 processos reais de alta complexidade analisados em 03/05/2026. Ele deve ser a referência máxima para a configuração do Gemini Gem.

---

## 🏛️ 1. PROTOCOLOS DE ANÁLISE JURÍDICA

### 1.1 Decadência Administrativa (Art. 150 §4º CTN)
- **Decadência Total:** Obra irregular > 5 anos (comprovada por Planta Cadastral antiga) sem averbação no SRI.
- **Decadência Parcial:** Parte da obra é regular (averbada) e parte é irregular antiga (> 5 anos). A decadência incide **apenas** sobre a parte irregular.
- **Indeferimento de Decadência:** Nunca conceder decadência para áreas que já constam na Matrícula (averbadas). O que é averbado já é regular.

### 1.2 Cadeia Dominial e Titularidade
- **Contrato vs. Matrícula:** Aceitar pedidos em nome de promissários compradores, desde que o Contrato de Compra e Venda esteja anexado.
- **Troca de Requerente:** Se o processo mudar de dono no trâmite, manter o histórico e emitir o documento no nome do proprietário/comprador final.

---

## 🏗️ 2. REGRAS DE CÁLCULO E ÍNDICES URBANÍSTICOS

### 2.1 Adensamento Crítico
- **Gatilho:** TO > 80% ou TP < 1%.
- **Ação:** Ativar flag `ADENSAMENTO_CRITICO` e aplicar multas cumulativas (Art. 79 Lei 1544 + Art. 39 Lei 267).

### 2.2 Lotes Pequenos (≤ 220m²)
- **Regra:** Aplicam-se os afastamentos do Código Civil (1,50m), mas a TO e TP **continuam obrigatórias** conforme a zona.
- **Anotação:** No JSON, usar `"area_terreno": "XXX m² (exceção da lei)"`.

### 2.3 Áreas de Garagem Descoberta
- **Cálculo:** Não computam para Coeficiente de Aproveitamento (CA), mas devem constar na narrativa como "Área Útil" para transparência.

---

## 🌿 3. RESTRIÇÕES AMBIENTAIS E PATRIMONIAIS

### 3.1 Área Urbana Consolidada (APP)
- **Gatilho:** Lote em divisa com córrego ou nascente.
- **Ação:** Citar Lei 3.971/2023 e exigir recuo mínimo determinado pelo CODEMA (geralmente 10m).

### 3.2 IEPHA (Patrimônio Histórico)
- **Gatilho:** Imóvel em zona ZC-2 (Centro Histórico).
- **Ação:** Bloqueio absoluto até a apresentação de Nota Técnica do IEPHA.

---

## 📑 4. SANEAMENTO DE DIVERGÊNCIAS (SRI vs PMO)

### 4.1 Divergência de Bairro
- **Ação:** Emitir **Certidão de Localização Corretiva** justificando a transição de nomenclatura de bairros para evitar Notas Devolutivas do Cartório.

### 4.2 Divergência de Área de Terreno
- **Gatilho:** Diferença > 5% entre Matrícula e Realidade in loco.
- **Ação:** Bloquear aprovação e exigir **Retificação de Área no SRI** via comunicado.

---

## 🛠️ 5. CONFIGURAÇÃO DO GEMINI GEM (v9.0 — SIA)

### Passo 1: System Instructions
Copie o conteúdo de **`Sistema/inteligencia/SIA_v1.0.md`** nas System Instructions do Gemini Gem.

> O arquivo `01_SUPER_PROMPT_RESEARCH.md` foi aposentado — use apenas o SIA v1.0.

### Passo 2: Knowledge Files (Obrigatórios)
Suba estes 6 arquivos como base de "verdade" no Knowledge do Gem:
1. `base_conhecimento/lc_267_2019_uso_ocupacao.md` — Zonas, TO/CA/TP
2. `base_conhecimento/lei_1544_1986_codigo_obras.md` — Art. 79 (multas)
3. `inteligencia/GABARITOS.md` — Templates estruturais de parecer (**NOVO**)
4. `inteligencia/RETROALIMENTACAO.md` — Lições aprendidas em processos reais
5. `base_conhecimento/casos_treinamento.jsonl` — Histórico de processos modelo
6. `base_conhecimento/estilo_narrativo_pareceres.md` — Como o Eng. Diego escreve

### Passo 3: Servidor MCP
Certifique-se de que o servidor MCP está rodando:
```
python Sistema/mcp-smosu/server.py
```
O SIA depende das 15 ferramentas MCP para calcular multas, validar checklist e gerar memória de cálculo. Sem o servidor, as fases 1, 3, 4 e 5 funcionarão em modo degradado.

---
*Manual v9.0 — 04/05/2026 — SMOSU — Sistema Interativo de Análise (SIA)*
