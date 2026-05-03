# GUIA DE CONFIGURAÇÃO E USO — GEM SMOSU no Gemini
## O que copiar, onde colar e como operar o Wizard de 4 Passos

---

## VISÃO GERAL

O sistema funciona em dois momentos distintos:

| Momento | O que fazer | Frequência |
|---------|------------|-----------|
| **Configuração inicial** | Criar o GEM e carregar os arquivos de referência | Uma vez |
| **Uso diário** | Abrir o GEM, anexar PDFs e colar o trigger | A cada novo processo |

---

## PARTE 1 — CONFIGURAÇÃO INICIAL DO GEM (UMA VEZ)

### Passo A — Criar ou editar o GEM no Gemini

1. Acesse **gemini.google.com** → clique em **"Gems"** no menu lateral → **"Novo Gem"**
   (ou edite um GEM já existente chamado "SMOSU" / "Engenheiro Analista")

2. Dê o nome: **GEM SMOSU — Engenheiro Analista**

### Passo B — Colar as Instruções do Sistema

No campo **"Instruções"** (ou "Instruções do sistema") do GEM:

> **Cole o conteúdo COMPLETO do arquivo:**
> `Sistema/inteligencia/00_INSTRUCAO_SISTEMA_GEMINI.md`

Este arquivo contém toda a personalidade, o protocolo Wizard de 4 Passos, as tabelas de zoneamento, as fórmulas de multa e as regras de qualidade dos pareceres.

### Passo C — Carregar os arquivos de referência

No campo **"Conhecimento"** (ou "Files") do GEM, faça upload dos seguintes arquivos:

| Arquivo | Função no GEM |
|---------|--------------|
| `Sistema/inteligencia/05_GABARITO_PARECER.md` | 3 pareceres reais como exemplo few-shot de qualidade |
| `Sistema/inteligencia/06_MAPA_INTELIGENCIA.md` | Árvore de decisão + cálculos + exceções legais |
| `Sistema/inteligencia/07_BLOCOS_CONSIDERANDOS.md` | Templates de considerandos com 3 camadas |
| `Sistema/modelos/MODELO_GABARITO_Alvara_Regularizacao.json` | Gabarito canônico de regularização |
| `Sistema/modelos/MODELO_01_Alvara_Aprovacao.json` | Gabarito de aprovação de projeto novo |
| `Sistema/modelos/MODELO_14_Habitese_Multa.json` | Gabarito de habite-se com multa |
| `Sistema/modelos/MODELO_15_Reforma_Ampliacao.json` | Gabarito de reforma + ampliação |

> **Opcional mas recomendado**: carregar também os outros `MODELO_*.json` para casos menos frequentes.

### Passo D — Salvar o GEM

Clique em **"Salvar"**. A configuração é permanente — não precisa repetir.

---

## PARTE 2 — USO DIÁRIO (A CADA NOVO PROCESSO)

### Passo 1 — Abrir nova conversa com o GEM

Clique no GEM configurado → **"Nova conversa"**

### Passo 2 — Anexar os PDFs do processo

Antes de digitar qualquer coisa, anexe **todos** os arquivos do processo:

| Documento | Obrigatório? |
|-----------|-------------|
| Requerimento / capa do processo | Sim |
| Matrícula do imóvel (SRI) | Sim |
| Projeto arquitetônico (DWG/PDF) ou As-Built | Sim |
| ART / RRT / TRT do responsável técnico | Sim |
| Parecer fiscal (vistoria) | Sim |
| Alvará anterior (se houver) | Quando aplicável |
| Comprovante de pagamento (DAM/boleto) | Quando houver multa paga |
| Planta cadastral municipal antiga | Quando invocar decadência |

### Passo 3 — Colar o trigger de sessão

Após anexar os PDFs, cole o seguinte texto (conteúdo de `01_GEM_INSTRUCOES.md`):

```
Engenheiro Analista, acabei de enviar os arquivos de um processo administrativo.

Execute o Wizard de 4 Passos definido nas suas Instruções de Sistema:

PASSO 1 → Triagem rápida + Menu de 10 categorias com sua sugestão
PASSO 2 → Disambiguação (se a categoria pedir)
PASSO 3 → Análise + Proposta de documentos a emitir
PASSO 4 → Geração do JSON (somente após eu confirmar)

Regras:
- Vá direto ao PASSO 1 sem pedir confirmação prévia
- Liste o que identificou em cada arquivo (5-10 segundos de leitura)
- Apresente sua sugestão de categoria com motivo curto
- Espere minha resposta antes de avançar para o próximo passo
- NUNCA gere o JSON sem o meu "confirma" / "pode gerar" / "ok"

Considerandos: cada um deve ter as 3 camadas (Fato + Artigo + Cálculo). Use 07_BLOCOS_CONSIDERANDOS.md como ponto de partida.

Padrão de qualidade: os 3 gabaritos em 05_GABARITO_PARECER.md são a referência.

Pronto. Pode começar.
```

### Passo 4 — Seguir o Wizard

O GEM responde automaticamente com o **PASSO 1**. A partir daí:

| O GEM apresenta | Você faz |
|----------------|---------|
| Menu de 10 categorias + sua sugestão | Confirma a categoria OU escolhe outra |
| Perguntas de disambiguação (ex: "residencial ou comercial?") | Responde em 1-2 palavras |
| Proposta visual dos documentos a emitir com áreas | Confirma, remove ou ajusta |
| Mensagem "Aguardando confirmação para gerar o JSON" | Digita: **confirma** |
| JSON completo | Copia e salva em `Entrada/` |

---

## PARTE 3 — FLUXO COMPLETO (EXEMPLO PRÁTICO)

```
Você:  [Anexa 5 PDFs] + cola o trigger

GEM:   ──────────────────────────────────────────
       PASSO 1 — TRIAGEM RÁPIDA

       Arquivos identificados:
       • Requerimento: processo 1847/2026, Sr. José da Silva
       • Matrícula nº 15823 — lote 08, quadra 12 (ZUR3)
       • Projeto As-Built (data de hoje)
       • TRT nº CFT2605XXXXX (execução)
       • Parecer fiscal: "obra concluída e habitável"

       ┌──────────────────────────────────────────────┐
       │ CATEGORIAS DE PROCESSO                       │
       │ 1. Aprovação de Projeto Novo                 │
       │ 2. Regularização (obra sem alvará)           │ ←
       │ 3. Habite-se — obra conforme                 │
       │ 4. Habite-se + Multa por infração            │
       │ 5. Reforma / Ampliação                       │
       │ 6. Certidão de Número / Localização          │
       │ 7. MCMV / Habitação Social                   │
       │ 8. Uso Comercial / Industrial                │
       │ 9. Desmembramento / Retificação              │
       │ 10. Outro / Comunicado / Ofício              │
       │                                              │
       │ MINHA SUGESTÃO: opção 2 — Regularização      │
       │ Motivo: As-Built + laudo + sem alvará prévio │
       └──────────────────────────────────────────────┘

Você:  confirma opção 2

GEM:   PASSO 2 — DISAMBIGUAÇÃO
       Residencial ou comercial?

Você:  residencial

GEM:   PASSO 3 — ANÁLISE E PROPOSTA
       [Extrai índices, calcula TO/CA/TP, verifica decadência]

       ╔══════════════════════════════════════════════╗
       ║ PROPOSTA DE DOCUMENTOS A EMITIR             ║
       ╠══════════════════════════════════════════════╣
       ║ 1. Alvará de Regularização — 187,50m²       ║
       ║ 2. Certidão de Decadência — 99,08m²         ║
       ║ 3. Carta de Habite-se — 187,50m²            ║
       ║ 4. Carta de Averbação — 118,50m² (acréscimo)║
       ╚══════════════════════════════════════════════╝

       Aguardando sua confirmação para gerar o JSON.

Você:  confirma

GEM:   [Gera o JSON completo]
```

---

## PARTE 4 — DICAS DE OPERAÇÃO

### Ajustando a proposta antes de confirmar
Se o GEM propôs algo errado no PASSO 3, corrija antes de confirmar:
- "Remova o item 2 (Certidão de Decadência)"
- "Troque o habite-se por 2ª via"
- "A área da averbação é 94,50m², não 118,50m²"

### Corrigindo durante o JSON
Se o JSON tiver algum campo errado, diga:
- "Corrija o campo `area_total_construida` para 203,40m²"
- "O fiscal responsável é Rogério Firmino Barros, mat. 30880745-1"
- "Adicione um considerando sobre o CEI nº XXXXX"

### Modo Livre (sem wizard)
Para casos que não seguem o fluxo padrão, basta dizer:
- "Modo livre — preciso de um ofício ao Meio Ambiente"
- "Modo livre — gere um memorando interno sobre..."

### Quando o GEM travar ou dar resposta genérica
1. Verifique se os arquivos foram anexados corretamente
2. Diga: "Recomece o PASSO 1 lendo os arquivos novamente"
3. Em último caso: inicie nova conversa e repita o processo

---

## RESUMO RÁPIDO (COLA NA PAREDE)

```
CONFIGURAÇÃO (uma vez):
  GEM > Instruções: cole 00_INSTRUCAO_SISTEMA_GEMINI.md
  GEM > Conhecimento: suba 05, 06, 07 e os MODELO_*.json

DIA A DIA:
  1. Abrir o GEM
  2. Anexar todos os PDFs do processo
  3. Colar o trigger de 01_GEM_INSTRUCOES.md
  4. Seguir o Wizard (confirma as categorias e proposta)
  5. Copiar o JSON → salvar em Entrada/
  6. Rodar GERAR_DOCUMENTOS.bat
```
