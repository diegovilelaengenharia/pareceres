# MAPA DE INTELIGÊNCIA GEM — SMOSU Oliveira/MG
## Como ler os documentos do processo e direcionar ao parecer correto

> **Princípio**: A IA lê os PDFs → identifica os documentos presentes → deduz o tipo de processo → propõe a lista de documentos a emitir → **o engenheiro confirma** antes de gerar o JSON.

---

## PARTE 1 — SINAIS DE ENTRADA: O QUE CADA DOCUMENTO INDICA

### DOCUMENTOS DE ENTRADA E O QUE REVELAM

| Documento Encontrado no Processo | O que indica |
|----------------------------------|-------------|
| **Projeto Arquitetônico** (novo, sem "As Built") | Obra futura — processo de APROVAÇÃO |
| **Projeto As-Built** ("como construído") | Obra já executada — REGULARIZAÇÃO ou HABITE-SE |
| **Laudo Técnico** | Obra já concluída — sempre acompanha As-Built → REGULARIZAÇÃO ou HABITE-SE |
| **ART/RRT/TRT de Projeto** | Projeto ainda não executado |
| **ART/RRT/TRT de As-Built + Laudo** | Obra já construída sem alvará → REGULARIZAÇÃO |
| **ART/RRT/TRT de Execução** | Obra em andamento ou concluída com alvará prévio |
| **Cópia do Alvará de Construção** anterior | Existe licença prévia → HABITE-SE ou REFORMA/AMPLIAÇÃO |
| **Matrícula/SRI com Averbação (AV-X)** de área | Área já regularizada consta no cartório |
| **Planta Cadastral Municipal** com data antiga | Evidência de existência → base para DECADÊNCIA |
| **Fiscal diz "obra concluída e habitável"** | Emitir Habite-se |
| **Fiscal diz "obra não iniciada"** | Alvará de construção novo |
| **Contrato MCMV / Caixa Econômica** | `alvara_mcmv` |
| **Levantamento Topográfico Georreferenciado** | `certidao_desmembramento` ou `certidao_retificacao_area` |
| **Pedido simples de certidão** (sem projeto) | Certidão de localização/número/nome de rua |

---

## PARTE 2 — ÁRVORE DE DECISÃO (Fase Zero)

### PASSO 1 — Verificar se a documentação básica está completa

```
Bloqueador absoluto (→ comunicado_pendencia):
  - Falta projeto arquitetônico (DWG ou PDF)?
  - Falta ART/RRT/TRT do responsável técnico?
  - Taxa de licença não quitada?
  - 3+ documentos críticos ausentes?
```

> Se algum bloqueador estiver presente: **parar aqui**, propor `comunicado_pendencia`.
> Se tudo OK: seguir para PASSO 2.

---

### PASSO 2 — Qual o estado da obra?

```
A → OBRA AINDA NÃO EXISTE (projeto novo para construir)
    ↓ → Ir para GRUPO A: Alvarás de Construção

B → OBRA JÁ EXISTE, SEM ALVARÁ PRÉVIO (irregular)
    ↓ → Ir para GRUPO B: Regularização

C → OBRA JÁ EXISTE, COM ALVARÁ PRÉVIO (e está concluída)
    ↓ → Ir para GRUPO C: Habite-se

D → OBRA EXISTENTE COM ALVARÁ PRÉVIO que precisa de mudança
    ↓ → Ir para GRUPO D: Reforma / Ampliação / Mudanças

E → PEDIDO DE CERTIDÃO APENAS (sem obra envolvida)
    ↓ → Ir para GRUPO E: Certidões Simples

F → SITUAÇÃO ESPECIAL
    ↓ → Ir para GRUPO F: Ofícios / Comunicados / Casos Especiais
```

---

### GRUPO A — Alvarás de Construção (obra ainda não existe)

| Condição adicional | Tipo de Processo | Documentos a Emitir |
|-------------------|------------------|---------------------|
| Residencial unifamiliar, qualquer área, uso padrão | `alvara_aprovacao` | Alvará de Construção (1 ano) + Certidão de Número + Certidão de Localização |
| Programa MCMV / CEF / contrato habitacional | `alvara_mcmv` | Alvará Habitacional + Certidão de Número |
| Uso comercial (loja, escritório, serviço) | `alvara_construcao_comercial` | Alvará Comercial (1 ano) |
| Galpão / depósito / indústria | `alvara_galpao_comercial` | Alvará Galpão (1 ano) |
| Mudança de projeto já aprovado | `alvara_substituicao_projeto` | Alvará com Novo Projeto |

**Variáveis-chave a extrair do PDF:**
- `numero_processo`, `data_processo`, `requerente`
- `area_terreno`, `area_total_construida`, `taxa_ocupacao`, `coef_aproveitamento`, `taxa_permeabilidade`
- `zona_uso` (verificar pelo bairro na tabela de zoneamento)
- `art_rrt` (número da ART/RRT/TRT)
- `profissional_nome` (nome do engenheiro/arquiteto/técnico)
- `logradouro`, `bairro`, `inscricao_municipal`
- `numero_porta` (se o fiscal tirou o número — vai para Certidão de Número)
- `categoria_uso` (para alvarás comerciais)

**Cálculos obrigatórios a apresentar:**
```
TO = área_projeção / área_terreno × 100
CA = área_total_construída / área_terreno
TP = área_permeável / área_terreno × 100
Verificar: TO ≤ limite_zona | CA ≤ limite_zona | TP ≥ mínimo_zona
TP_mínima_m2 = área_terreno × (TP_mínima_zona / 100)
```

---

### GRUPO B — Regularização (obra existe sem alvará prévio)

> **Sinal principal**: Projeto As-Built + Laudo Técnico + Fiscal diz "concluída e habitável" **sem** apresentação de alvará anterior.

| Condição adicional | Tipo | Documentos a Emitir |
|-------------------|------|---------------------|
| Padrão | `alvara_regularizacao` | Alvará de Regularização + Habite-se + Certidão de Averbação |
| + Área com >5 anos (planta cadastral antiga) | `alvara_regularizacao` | + **Certidão de Decadência** paralela |
| + Área já averbada no SRI (AV-X matrícula) | `alvara_regularizacao` | + **Não** emitir certidão de decadência para parte já averbada |
| Processo envolve múltiplas unidades | `regularizacao_complexa_multipla` | Múltiplos habite-se / averbações individuais |

**Variáveis-chave a extrair:**
- Tudo do Grupo A, mais:
- `area_ja_averbada` — área que já consta na matrícula (ex: "69,00m² — AV-5/1999")
- `area_averbada_anterior_av` — número da averbação (ex: "AV-5")
- `area_averbada_anterior_data` — data da averbação (ex: "07/05/1999")
- `area_acrescimo` — área nova sem licença (= total - já averbada)
- `area_decadencia` — área com evidência de >5 anos (ex: planta cadastral Ago/2002)
- `area_decadencia_prova` — documento que comprova (ex: "Planta Cadastral Municipal de Agosto/2002")
- `area_decadencia_data` — data do documento comprobatório
- `agentes_fiscais` — nomes e matrículas dos fiscais que fizeram a vistoria

**Cálculos obrigatórios:**
```
TO, CA, TP (igual Grupo A)
área_acrescimo = area_total_construida − area_ja_averbada
area_sujeita_multa_art79 = area_acrescimo − area_decadencia (se houver)

MULTA ART. 79 (Lei 1.544/86) — por m² da área irregular:
  Até 60m²:    1% da URM/m² × área
  61–120m²:    2% da URM/m² × área
  121–240m²:   3% da URM/m² × área
  241–360m²:   4% da URM/m² × área
  Acima 360m²: 5% da URM/m² × área
  (URM = R$ 4,10; VRM = R$ 102,42)

MULTA ART. 39 (LC 267/2019) — por quebra de TO ou TP:
  Até 60m²:    1× taxa do alvará
  61–120m²:    2× taxa do alvará
  ...até 10× acima de 360m²
  (As duas multas são CUMULATIVAS se houver quebra de TO/TP)
```

**Regra de Decadência:**
```
SE planta_cadastral_data < hoje - 5 anos:
  → área mostrada no documento está dispensada de multa Art. 79
  → emitir Certidão de Decadência para essa área
  → base legal: Art. 150, §4º CTN

SE area_ja_averbada > 0 (consta na matrícula via AV-X):
  → NÃO emitir Certidão de Decadência para essa parte
  → emitir apenas Certidão de Averbação do acréscimo
```

---

### GRUPO C — Habite-se (obra existe, com alvará prévio, concluída)

> **Sinal principal**: Cópia do Alvará de Construção (anterior) + Fiscal diz "concluída e habitável" conforme o alvará.

| Condição | Tipo | Documentos a Emitir |
|----------|------|---------------------|
| Obra conforme alvará, sem infração | `habitese_comum` | Carta de Habite-se + Certidão de Averbação |
| Infração detectada (quebra de TP, TO, etc.) | `habitese_multa` | Habite-se + Notificação de Multa |
| Edifício com múltiplas unidades/matrículas | `habitese_condominio` | Habite-se por unidade |
| Obra inclui ampliação não licenciada | `habitese_inclusao_area` | Habite-se + regularização da ampliação |
| Reemissão de habite-se anterior | `habitese_2via` | 2ª Via do Habite-se |

**Variáveis-chave:**
- `numero_alvara_emitido` (número do alvará original)
- `data_alvara_emitido` (data de emissão do alvará)
- Índices como construído (TO, CA, TP reais)
- Se `habitese_multa`: identificar qual infração e calcular multa

---

### GRUPO D — Reforma / Ampliação / Mudanças (obra existente com alvará)

> **Sinal principal**: Cópia do Habite-se/Alvará anterior + Projeto de alteração.

| Condição | Tipo | Documentos a Emitir |
|----------|------|---------------------|
| Apenas reforma interna (sem demolição/ampliação) | `alvara_reforma` | Alvará de Reforma (1 ano) |
| Apenas ampliação (acréscimo sem demolição) | `alvara_ampliacao` | Alvará de Ampliação (1 ano) |
| Reforma + demolição parcial + ampliação | `alvara_reforma_demolicao_ampliacao` | Alvará Múltiplo (1 ano) |
| Alvará vencido, mesma obra | `alvara_renovacao` | Alvará Renovado (+ 1 ano) |
| Cancelamento por desistência | `alvara_cancelamento` | Termo de Cancelamento |
| Novo proprietário, obra em andamento | `alvara_substituicao_titular` | Alvará com Novo Titular |
| Novo Engenheiro/RT, mesma obra | `alvara_troca_responsavel_tecnico` | Alvará com Novo RT |

**Variáveis específicas para reforma/ampliação:**
```
area_averbada_anterior = área já existente e averbada
area_demolicao = área que será derrubada (se houver)
area_ampliacao = área nova que será construída
area_total_construida = area_averbada_anterior - area_demolicao + area_ampliacao
(verificar que a conta fecha exatamente)
```

---

### GRUPO E — Certidões Simples (sem obra envolvida)

| Pedido do Requerente | Tipo | Documentos a Emitir |
|---------------------|------|---------------------|
| "onde fica o imóvel / confrontações" | `certidao_localizacao` | Certidão de Localização |
| "nome oficial da rua" | `certidao_nome_rua` | Certidão Toponímica |
| "número SAAE/CEMIG" (residencial) | `certidao_numero_2via` | Certidão de Número |
| "número SAAE/CEMIG" (comercial) | `certidao_numero_comercial` | Certidão de Número Comercial |
| "localização + número + rua juntos" | `certidao_conjunta` | Certidão Conjunta |
| "construção tem mais de 5 anos" | `certidao_averbacao_decadencia` | Certidão de Decadência |
| Divisão de lote | `certidao_desmembramento` | Certidão de Desmembramento |
| Correção de área no cartório | `certidao_retificacao_area` | Certidão de Retificação |
| Confirmar zona de uso (ZUE) | `certidao_zue` | Certidão de Zoneamento |
| Demolitação concluída | `certidao_demolicao` | Certidão de Conclusão de Demolição |

---

### GRUPO F — Situações Especiais

| Situação | Ação |
|----------|------|
| Documentação incompleta (falta bloqueante) | `comunicado_pendencia` — retorna ao balcão |
| Indeferimento por inconformidade | `comunicado_indeferimento` |
| APP, córrego, vegetação nativa detectados | `oficio_meio_ambiente` (em paralelo com o parecer principal) |
| Usucapião / retificação judicial | `parecer_juridico` |
| Obra flagrada irregular, embargo | `oficio_juridico_embargo` |
| Comunicação interna entre setores | `memorando` |
| Pedido de desapropriação | `oficio_decreto_utilidade` |

---

## PARTE 3 — DOCUMENTOS PARALELOS (emitidos junto com o principal)

Além do documento principal, a IA deve propor automaticamente:

| Situação Detectada | Documento Paralelo |
|-------------------|--------------------|
| Área comprovadamente >5 anos sem averbação | `certidao_averbacao_decadencia` |
| Terreno confinante com APP/córrego/nascente | `oficio_meio_ambiente` |
| Projeto novo → fiscal tirou número predial | `certidao_numero_2via` (ou `certidao_numero_comercial`) |
| Aprovação/regularização → localização precisa | `certidao_localizacao` |
| Imóvel em área de tombamento (IEPHA) | Nota no parecer + aguardar Nota Técnica IEPHA |
| Abertura <1,50m da divisa | Condicionante: Termo de Anuência (Art. 43 Lei 1.544/86) |

---

## PARTE 4 — TABELA DE ZONEAMENTO (LC 267/2019)

Use o bairro informado para determinar a zona. Parâmetros por zona:

| Zona | TO máx. | CA máx. | TP mín. | Recuo frontal | Obs. |
|------|---------|---------|---------|---------------|------|
| ZUR1 | 60% | 1,5 | 20% | 5,00m | Baixa densidade |
| ZUR2 | 70% | 2,5 | 20% | 5,00m | |
| ZUR3 | 70% | 3,5 | 20% | 5,00m | Centro expandido |
| ZC1 | 80% | 4,0 | 15% | 0 | Área central |
| ZC2 | 80% | 5,0 | 15% | 0 | |
| ZAE1–4 | 70% | variável | 20% | variável | Atividade econômica |
| ZIND | 70% | 2,0 | 20% | 10,00m | Industrial |
| ZEIS | 60% | 1,0 | 20% | 2,00m | Interesse social |
| OCRE | 40% | 0,4 | 40% | 15,00m | Proteção ambiental |

**Exceção lote ≤ 220m²** (Art. 9º §13 LC 267/2019): afastamentos laterais e de fundos pelo Código Civil (1,50m), não pela LC 267. TP e TO continuam obrigatórias.

---

## PARTE 5 — VARIÁVEIS CANÔNICAS (nomes exatos para o JSON)

### Tier A — Obrigatórios em TODOS os documentos
```
tipo_relatorio         → valor exato da tabela de tipos (ex: "alvara_aprovacao")
numero_processo        → "545/2026" (nunca "processo nº 545")
data_processo          → "15 de janeiro de 2026" (extenso, nunca DD/MM/AAAA)
requerente             → "NOME COMPLETO EM MAIÚSCULAS"
inscricao_municipal    → "01.03.119.0276.001"
```

### Tier B — Obrigatórios nos Pareceres Técnicos
```
assunto                → "Regularização de Edificação" (texto curto)
logradouro             → "Rua Quinze de Novembro, nº 720"
bairro                 → "Do Rosário"
area_terreno           → "360,00m²" (com m², vírgula decimal)
area_total_construida  → "254,13m²"
taxa_ocupacao          → "63,32%"
coef_aproveitamento    → "0,706" (número, não %)
taxa_permeabilidade    → "20,59%"
zona_uso               → "ZUR03" (sigla exata)
profissional_nome      → "Wdson Willian de Oliveira Belmiro"
art_rrt                → "CFT2605342989" (número, sem prefixo "TRT nº")
paragrafo_abertura     → texto narrativo completo
considerandos          → array de strings (cada um = um parágrafo)
fundamentacao_legal    → array de strings com __negrito__ para o nome da lei
conclusao              → texto com **negrito** para a palavra FAVORÁVEL/DESFAVORÁVEL
documentos_emitir      → array de {tipo, obs}
memoria_de_calculo     → cálculos passo a passo em texto
```

### Tier C — Opcionais por tipo
```
area_ja_averbada              → "69,00m²" (regularização: área já no SRI)
area_averbada_anterior_av     → "AV-5" (número da averbação anterior)
area_averbada_anterior_data   → "07/05/1999" (data da averbação anterior)
area_acrescimo                → "185,13m²" (área sem licença)
area_decadencia               → "99,08m²" (área decadente)
area_decadencia_prova         → "Planta Cadastral Municipal de Agosto/2002"
area_decadencia_data          → "Agosto/2002"
area_demolicao                → "0,94m²" (reforma/ampliação)
area_ampliacao                → "194,62m²" (reforma/ampliação)
agentes_fiscais               → "Wallace Alencar Martins Silveira e Marlei Henrique de Oliveira"
matricula_sri                 → "11.769"
proprietario                  → nome se diferente do requerente
lote                          → "17"
quadra                        → "40"
categoria_uso                 → "UR 1" (para comercial/especial)
pavimentos_descricao          → "dois pavimentos: inferior 120m² e superior 134,13m²"
```

### Campos PROIBIDOS (nunca usar)
```
parecer_tecnico | legislacao_aplicada | condicionantes | resultado_final
documentos_analisados | status | observacoes_gerais | resumo | analise
irregularidades | tipo_documento | categoria | tipo (como campo)
```

---

## PARTE 6 — FORMATO DOS CONSIDERANDOS (padrão narrativo + legal)

Cada considerando deve ter **três camadas**:

```
CAMADA 1 — Fato verificado no processo
CAMADA 2 — Dispositivo legal específico (artigo + inciso + parágrafo)
CAMADA 3 — Cálculo explícito (quando aplicável)
```

### Exemplos corretos (extraídos dos gabaritos reais):

**Considerando de índices urbanísticos:**
> "Que o imóvel está inserido no Zoneamento ZUR03, sendo verificados os índices urbanísticos conforme Tabela 1 do Art. 9º da LC 267/2019: Taxa de Ocupação de 63,32% (= 227,96/360,00×100) abaixo do limite de 70%; Coeficiente de Aproveitamento de 0,706 (= 254,13/360,00) abaixo do limite de 3,5; Taxa de Permeabilidade de 20,59% (= 74,14/360,00×100) acima do mínimo de 20%."

**Considerando de decadência:**
> "Que, nos termos do Art. 150, §4º do Código Tributário Nacional, a Planta Cadastral Municipal datada de Agosto de 2002 atesta a existência consolidada de 99,08m² de área construída no lote há mais de 5 (cinco) anos sem autuação fiscal, configurando a decadência do direito de lançamento das penalidades para esta parcela."

**Considerando de responsabilidade técnica:**
> "Que para o projeto As-Built e Laudo Técnico (Data: 08/01/2026), foi emitido o Termo de Responsabilidade Técnica TRT nº CFT2605342989 pelo profissional Wdson Willian de Oliveira Belmiro, atendendo ao requisito de responsabilidade técnica previsto no Art. 48 da Lei Municipal nº 1.544/86."

### Considerandos obrigatórios por tipo:

**Para alvara_regularizacao:**
1. Documentos de propriedade (matrícula, inscrição)
2. Responsabilidade técnica (ART/TRT do As-Built + Laudo)
3. Índices urbanísticos (TO, CA, TP com cálculos)
4. Decomposição das áreas (existente averbada + acréscimo)
5. Decadência (se houver — citar documento + data + área)
6. Situações especiais (IEPHA, anuência, etc.) — condicional

**Para alvara_aprovacao:**
1. Situação da obra (fiscal: "não iniciada")
2. Documentos de propriedade
3. Responsabilidade técnica (ART/TRT de projeto)
4. Índices urbanísticos verificados

---

## PARTE 7 — PERGUNTAS DE CONFIRMAÇÃO AO ENGENHEIRO

Antes de gerar o JSON, a IA deve confirmar com o engenheiro:

### Para qualquer processo:
```
"Identifiquei o processo como: [TIPO]. Proposta de documentos a emitir:
  1. [documento 1]
  2. [documento 2]
  3. [documento 3] (se aplicável)

Confirma? Alguma correção?"
```

### Para regularização:
```
"Área total: XXX m². Área já averbada: XXX m² (AV-X/AAAA). Acréscimo: XXX m².
Decadência detectada: XXX m² (Planta Cadastral Mês/Ano — mais de 5 anos).
Área sujeita à multa Art. 79: XXX m².
Confirma esses valores?"
```

### Para habite-se:
```
"Alvará original nº XXX/AAAA. Obra concluída e habitável conforme parecer fiscal.
[SE infração] Infração detectada: quebra de TP (prevista XXX m², realizado XXX m²).
Confirma a situação?"
```

### Para certidão de número:
```
"Fiscal retirou o número XXX (SAAE/CEMIG). Emitir Certidão de Número?
Também emitir Certidão de Localização junto? (comum em aprovações)"
```

---

## PARTE 8 — CASOS ESPECIAIS E ARMADILHAS

### Armadilha 1: Área já averbada vs. Decadência
- **AV-X na matrícula** = área já regularizada → NÃO é decadência → NÃO emitir Certidão de Decadência para essa parte
- **Planta Cadastral antiga** (sem averbação) = evidência de existência → É decadência → Emitir Certidão de Decadência

### Armadilha 2: Fiscal diz "habitável" sem alvará prévio
- Se não existe cópia de alvará de construção → é REGULARIZAÇÃO (não habite-se simples)
- Sempre perguntar: "tem alvará de construção anterior?"

### Armadilha 3: TRT vs. ART vs. RRT
- **TRT** (CFT): emitido por Técnico em Edificações
- **ART** (CREA): emitido por Engenheiro Civil
- **RRT** (CAU): emitido por Arquiteto
- Todos têm o mesmo peso legal para o processo. Usar o nome correto no parecer.

### Armadilha 4: Garagem descoberta sem estrutura
- Não computa no CA (Coeficiente de Aproveitamento)
- Pode ou não computar na TO (depende de projeção)
- Deve ser mencionada no alvará de construção

### Armadilha 5: Lote ≤ 220m²
- Exceção de afastamentos pelo Código Civil (1,50m)
- **NÃO** isenta de TO e TP — esses continuam obrigatórios pela LC 267/2019
- Art. 9º §13 LC 267/2019

### Armadilha 6: Imóvel tombado / IEPHA
- Qualquer imóvel no Centro Histórico de Oliveira (tombamento desde 31/10/2013)
- Precisa Nota Técnica do IEPHA antes de emitir alvará
- Citar no parecer: "sujeito à análise prévia do IEPHA"

### Armadilha 7: Processo judicial vinculado
- Alguns processos têm liminar judicial (ex: usucapião pendente)
- Mencionar o processo judicial no parecer
- Campo: `processo_judicial_vinculado`

---

## PARTE 9 — ESCALONAMENTO DE MULTAS (referência rápida)

### Multa Art. 79 — Lei 1.544/86 (construção sem licença)

| Faixa de Área | Taxa | Base |
|---------------|------|------|
| Até 60,00 m² | 1% da URM/m² | = R$ 0,041/m² |
| 60,01 – 120,00 m² | 2% da URM/m² | = R$ 0,082/m² |
| 120,01 – 240,00 m² | 3% da URM/m² | = R$ 0,123/m² |
| 240,01 – 360,00 m² | 4% da URM/m² | = R$ 0,164/m² |
| Acima de 360,00 m² | 5% da URM/m² | = R$ 0,205/m² |

**URM = R$ 4,10** | **VRM = R$ 102,42**

> Exemplo: área de 86,05m² (faixa de 60,01–120m²) = 86,05 × 2% × R$ 4,10 = R$ 7,06

### Multa Art. 39 — LC 267/2019 (quebra de TO ou TP)

| Faixa de Área | Multiplicador |
|---------------|--------------|
| Até 60,00 m² | 1× taxa do alvará |
| 60,01 – 120,00 m² | 2× taxa do alvará |
| 120,01 – 240,00 m² | 4× taxa do alvará |
| 240,01 – 360,00 m² | 6× taxa do alvará |
| Acima de 360,00 m² | 10× taxa do alvará |

> As duas multas (Art. 79 + Art. 39) são **CUMULATIVAS** quando há quebra de parâmetro.

---

## PARTE 10 — CHECKLIST FINAL ANTES DE GERAR O JSON

```
□ tipo_relatorio identificado e confirmado pelo engenheiro
□ numero_processo e data_processo extraídos corretamente
□ requerente em MAIÚSCULAS
□ inscricao_municipal com pontuação correta (XX.XX.XXX.XXXX.XXX)
□ area_terreno, area_total_construida preenchidos com "m²"
□ taxa_ocupacao, taxa_permeabilidade com "%"
□ coef_aproveitamento sem "%"
□ TO, CA, TP calculados e verificados contra os limites da zona
□ art_rrt com número correto (sem "nº")
□ Considerandos com 3 camadas: fato + artigo + cálculo
□ documentos_emitir com tipo e obs preenchidos
□ memoria_de_calculo com todos os passos numéricos
□ Para regularização: area_acrescimo calculada e conferida
□ Para regularização: decadência verificada (há ou não há)
□ Para regularização: documentos paralelos (habite-se, averbação, decadência)
□ Nenhum campo proibido presente no JSON
□ Nenhum campo com valor nulo desnecessário (omitir em vez de null)
```
