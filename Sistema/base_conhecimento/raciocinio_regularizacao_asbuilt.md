# CADEIA DE RACIOCÍNIO DA ANALISTA — REGULARIZAÇÃO AS-BUILT
## Documento de Treinamento GEM — Processo 190/2026 (Dirceu) como Caso Base

*Versão: 1.0 | Engenheiro: Diego Tarcísio Nunes Vilela | SMOSU — Oliveira/MG*

---

> **PROPÓSITO:** Este documento captura o modelo mental completo de um analista experiente ao processar uma regularização As-Built. Não é uma lista de regras — é o raciocínio vivo. Use-o para **pensar**, não para preencher campos.

---

## PARTE 1 — O QUE É UMA REGULARIZAÇÃO AS-BUILT?

A regularização As-Built surge quando um imóvel foi construído ou ampliado sem a devida licença, ou com execução divergente do projeto aprovado. O processo existe para trazer essa edificação à legalidade, mediante o cumprimento de penalidades pecuniárias previstas em lei.

**A pergunta central que guia toda a análise:**
> *"O que foi construído vs. o que estava licenciado — e o que deve ser feito para legalizar a diferença?"*

Há dois cenários:
1. **Sem alvará algum:** Toda a área construída é irregular.
2. **Com alvará parcial (o caso mais comum):** O imóvel tem histórico de licenciamento, mas foi ampliado sem atualização — como no Processo 190/2026 (Dirceu): Alvará 4176/2012 para 74,98m², mas construção real de 117,09m².

---

## PARTE 2 — A CADEIA DE RACIOCÍNIO PASSO A PASSO

### PASSO 1 — TRIAGEM DOCUMENTAL: O QUE TEM E O QUE FALTA?

**O que o analista busca primeiro:**
Antes de qualquer cálculo, o analista realiza o inventário dos documentos. Para regularização As-Built, os dois **bloqueadores absolutos** são:
- ART/RRT do projeto As-Built (do levantamento)
- Guia paga da Taxa de Habite-se

Se QUALQUER UM desses dois estiver ausente → **INDEFERIR** imediatamente com comunicado de pendências. O processo não avança.

**Caso real (Processo 190):** Na triagem inicial, a CND do imóvel e a taxa de Habite-se estavam ausentes. O processo foi paralisado em TRIAGEM. O requerente retornou em 04/02/2026 com os documentos faltantes → processo avançou.

**Raciocínio do analista neste momento:**
> *"Tenho ART do as-built? Tenho taxa paga? Tenho laudo técnico? Se sim nos três: posso analisar. Se não: comunicado e aguardo."*

---

### PASSO 2 — LEITURA DO PARECER FISCAL: A REALIDADE DO TERRENO

O parecer fiscal é o documento que ancora toda a análise na realidade física. O analista lê com atenção:
- Endereço exato (e se bate com a documentação)
- Área do terreno confirmada in loco
- Área construída confirmada in loco
- Se confere com o projeto apresentado
- Se a construção está finalizada e é habitável

**Caso real (Processo 190):**
> *"Feito levantamento in loco, na Rua Alagoas, 740, Bairro Rosário. Área total do terreno: 174,70m² e área construída: 117,09m². Confere com o projeto apresentado. Construção finalizada. Habitável."*

**Raciocínio do analista:**
> *"O fiscal confirmou os números. Posso usar 117,09m² como área real e 174,70m² como área do terreno. Agora preciso confrontar com o que estava licenciado."*

---

### PASSO 3 — IDENTIFICAÇÃO DA ÁREA IRREGULAR

**Fórmula mental do analista:**

```
Área Total As-Built     = Área confirmada pelo laudo + fiscal
Área Licenciada (anterior) = Área do alvará mais recente
─────────────────────────────────────────────────────────
Área Irregular (ampliação sem licença) = As-Built - Licenciada
```

**Caso real (Processo 190):**
- As-Built: 117,09m²
- Licenciada: 74,98m² (Alvará 4176/2012)
- Irregular: **42,11m²**

**Pontos de atenção críticos:**
1. **Existe alvará anterior?** Verificar no histórico do processo, na matrícula ou nos documentos apresentados.
2. **Existe averbação na matrícula?** Se o imóvel nunca foi averbado, toda a área é "nova" administrativamente, mesmo que o alvará exista — como no Processo 190, onde havia alvará de 2012 mas sem averbação.
3. **Existe Habite-se anterior?** Um Habite-se parcial pode indicar área regularizada em momento anterior.

---

### PASSO 4 — VERIFICAÇÃO DOS ÍNDICES URBANÍSTICOS

O analista calcula TO, CA e TP para dois fins:
1. **Confirmar se há violação** → se sim, aplica multa LC 267/2019
2. **Registrar no parecer** → consta na memória de cálculo e no JSON

**Memorial padrão:**
```
TO = Área_coberta / Área_terreno × 100
CA = Área_total_construída / Área_terreno
TP = Área_permeável / Área_terreno × 100
```

**Caso real (Processo 190) — Zona ZUR03:**
- TO = 117,09 / 174,70 × 100 = **75,16%** → excede limite ZUR03
- CA = 117,09 / 174,70 = **0,67**
- TP = 0,00% → déficit total (sem área permeável)

**Raciocínio do analista sobre a zona:**
> *"Qual é o zoneamento? Verifica no espelho cadastral ou na inscrição imobiliária. ZUR03 permite TO máximo de X% e TP mínimo de 20%. Se estou acima do TO ou abaixo do TP → infração LC 267 → multa Art. 39."*

**Atenção especial para lotes ≤ 220m²:**
Mesmo em lotes pequenos, a isenção do Art. 15 (LC 267/2019) aplica-se **apenas para novos projetos**. Em regularizações As-Built, a multa dos Arts. 38/39 SEMPRE incide se houver violação de TO ou TP. (Confirmado nos Processos 6100 e 190.)

---

### PASSO 5 — VERIFICAÇÃO DA DECADÊNCIA

A pergunta da decadência é SEMPRE feita antes de aplicar qualquer multa do Art. 79:

> *"Há prova de que essa área existe há mais de 5 anos?"*

**Evidências aceitas (em ordem de força):**
1. Espelho Cadastral Municipal com data de inclusão > 5 anos
2. Habite-se parcial anterior há mais de 5 anos
3. Ortofoto ou imagem de satélite datada há mais de 5 anos
4. Laudo de engenharia com data da construção documentada

**Caso real (Processo 190):**
- Alvará original é de 2012, mas refere-se à área base (74,98m²)
- A **ampliação** de 42,11m² não tem data comprovada
- Não há ortofoto, espelho com data anterior nem Habite-se parcial
- **Conclusão: Decadência NÃO aplicável à ampliação**

**Se houvesse decadência:**
> *"A área decadente ficaria isenta da multa Art. 79 (construir sem licença). As multas LC 267 ainda incidem, pois são de zoneamento, não de obra."*

---

### PASSO 6 — CÁLCULO DAS MULTAS

O analista aplica **cumulativamente** as multas de fontes legais distintas:

#### Multa 1 — Art. 79 Inciso I (Construir Sem Licença)
Incide sobre a **área irregular** (ampliação sem alvará).

| Faixa de área irregular | % do VRM por m² |
|-------------------------|-----------------|
| Até 60m²                | 1%              |
| 61 a 75m²               | 3%              |
| 76 a 100m²              | 4%              |
| Acima de 100m²          | 5%              |

> VRM 2026 = R$ 102,42

**Caso real (Processo 190):** 42,11m² × 1% × R$ 102,42 = **R$ 43,13**

#### Multa 2 — Art. 79 Inciso II (Desacordo com Projeto Aprovado)
Incide sempre que há alvará anterior e a obra divergiu do projeto aprovado.
- **Valor:** 100% do VRM = **R$ 102,42** (valor fixo, não por m²)

#### Multa 3 — Arts. 38/39 LC 267/2019 (Quebra de Parâmetros Urbanísticos)
Incide sobre a área irregular quando TO excede o limite ou TP está abaixo do mínimo.

| Faixa (cumulativa) | Proporção |
|--------------------|-----------|
| Até 40m²           | 1× taxa de aprovação (R$ 4,48/m²) |
| 40,01 a 80m²       | 3× taxa de aprovação (R$ 13,45/m²) |
| 80,01 a 100m²      | 6× taxa de aprovação (R$ 28,00/m²) |
| Acima de 100m²     | 10× taxa de aprovação (R$ 44,86/m²) |

> As faixas são **acumulativas** — calcula-se cada faixa separadamente.

**Atenção:** Se houve violação de **TO e de TP** ao mesmo tempo → a multa Art. 39 é aplicada **duas vezes** (uma para cada parâmetro violado), conforme jurisprudência administrativa local.

#### Taxa de Aprovação
Separada das multas — é a taxa pelo serviço de análise e aprovação do projeto:
- Valor 2026: R$ 4,48/m² sobre a área irregular

---

### PASSO 7 — MONTAGEM DO PARECER TÉCNICO DO SETOR

Após toda a análise, o analista redige o Parecer Técnico. Estrutura obrigatória:

1. **Cabeçalho:** Número do processo, nome do requerente
2. **Contexto:** O que foi solicitado, onde está o imóvel, área total, zone
3. **Documentação apresentada:** Matrícula, ART/RRT, laudo técnico, parecer fiscal
4. **Histórico de licenciamento:** Alvará anterior, área licenciada, situação de averbação
5. **Constatação:** Diferença entre área licenciada e as-built = área irregular
6. **Decisão:** "Diante disso, aprovado e verificado o laudo técnico..."
7. **Documentos a emitir:** Lista com as observações específicas de cada um

**O campo "Observação" do Alvará é fundamental — deve conter:**
> "Alvará emitido para substituição do Alvará nº [ANTERIOR] (emitido em [DATA], área de [Xm²]) e regularização de imóvel edificado com ampliação não licenciada de área de [Ym²], totalizando área total de [Zm²], mediante o cumprimento do Art. 79 da Lei 1.544 de 1986 e Art. 38, 39 da Lei 267 de 2019."

---

### PASSO 8 — VERIFICAÇÃO DE DIVERGÊNCIAS CADASTRAIS

**Divergência de bairro (padrão recorrente):**
O SRI (Serviço de Registro de Imóveis) frequentemente registra bairros com nomes diferentes do cadastro municipal. O analista verifica:
- Bairro na matrícula/SRI ≠ Bairro no espelho cadastral municipal?
- Se sim → **Certidão de Localização** deve ser emitida

**Caso real (Processo 190):**
- SRI registrava: **Bairro Boa Vista**
- Cadastro municipal: **Bairro do Rosário**
- Solução: Certidão de Localização assinada pelo Engenheiro e pelo Secretário

---

### PASSO 9 — DOCUMENTOS A EMITIR (SEQUÊNCIA PADRÃO)

Para regularização As-Built típica, a sequência de documentos é:

| Documento | Condição de emissão |
|-----------|---------------------|
| Alvará de Regularização | Sempre — com observação detalhada |
| Carta de Habite-se | Sempre — área total as-built |
| Certidão de Averbação | Sempre — com dados do novo alvará |
| Certidão de Localização | Se houver divergência de bairro entre SRI e cadastro municipal |
| Comunicado de Baixa de CEI | Se existia alvará anterior com CEI ativa |
| Comunicado de Decadência | Se decadência foi reconhecida |

---

### PASSO 10 — TRAMITAÇÃO APÓS O PARECER

Após emissão do parecer favorável, o processo segue:

```
ANÁLISE (OBRAS)
     ↓  [Parecer Técnico do Setor assinado]
CONFECÇÃO DE DOCUMENTOS (OBRAS)
     ↓  [Alvará, Habite-se, Averbação, Certidões confeccionadas]
ENTREGA DE DOCUMENTOS (OBRAS)
     ↓  [Documentos entregues ao requerente]
DESENHISTA PLANTA CADASTRAL
     ↓  [Planta cadastral atualizada — arquivo PDF + DWG]
ENTREGA DE DOCUMENTOS
     ↓  [Desenho finalizado, retorna]
CADASTRO IMOBILIÁRIO
     ↓  [Inscrição cadastral atualizada, área registrada]
FAZENDA
     ↓  [Processo colocado na pilha — atualização fiscal/IPTU]
ENTREGA DE DOCUMENTOS
     ↓  [Processo retorna com informações de cadastro]
ARQUIVO GERAL
     ↓  [Encerramento — Data de Arquivamento]
```

---

## PARTE 3 — PADRÕES CRÍTICOS IDENTIFICADOS NOS PROCESSOS REAIS

### Padrão 1: Alvará sem Averbação
> *"Processo 190 — Alvará de 2012 existe, mas a matrícula nunca foi averbada. O analista trata como se a área toda fosse nova para fins de averbação, mas usa o alvará como referência para identificar qual parte é 'original licenciada' e qual é 'ampliação irregular'."*

### Padrão 2: Bairro Divergente (SRI vs. Cadastro Municipal)
> *"Frequente em Oliveira/MG. O SRI usa denominações diferentes das adotadas pelo cadastro imobiliário municipal. Sempre verificar se os bairros conferem. Se não — emitir Certidão de Localização. Não impede o processo, mas o documenta corretamente."*

### Padrão 3: CEI ativa em Alvará Antigo
> *"Se o alvará original tinha CEI (Cadastro Específico do INSS) ativa, e o novo alvará substitui o anterior, o requerente é responsável por solicitar a baixa da CEI junto à Receita Federal. Emitir Comunicado de Baixa de CEI sempre que houver Alvará anterior no sistema anterior."*

### Padrão 4: Decadência Parcial
> *"É possível que apenas parte da área seja decadente. Ex.: área base licenciada em 2012 e ampliação de 2019 (> 5 anos). Nesse caso, a área decadente fica isenta da multa Art. 79, mas a área não decadente paga normalmente. A multa LC 267 incide sobre toda a área em violação, independentemente de decadência."*

### Padrão 5: Lote ≤ 220m² em Regularização
> *"Não confundir com alvará de aprovação. Em alvará de aprovação/ampliação nova, lote ≤ 220m² tem isenção de TO e TP (Art. 15 LC 267). Em REGULARIZAÇÃO AS-BUILT, o Art. 15 é usado apenas para habilitar a análise do imóvel existente — mas a multa dos Arts. 38/39 SEMPRE incide se houver violação. Processo 6100 (terreno 180m²) confirmou isso."*

### Padrão 6: Sem Responsável Técnico para Execução
> *"Em regularizações, frequentemente o próprio proprietário aparece como responsável pela execução. Isso é aceito. O ART/RRT exigido é do projeto As-Built e do Laudo Técnico — não da execução propriamente dita."*

---

## PARTE 4 — VERIFICAÇÕES LEGAIS (CHECKLIST DO ANALISTA)

Antes de emitir o parecer favorável, o analista mentalmente percorre:

```
□ Fiscalização confirmou área as-built? ✔/✘
□ Laudo técnico de estabilidade está OK? ✔/✘
□ ART/RRT do as-built cobre projeto E laudo? ✔/✘
□ Taxa de Habite-se paga? ✔/✘
□ Há alvará anterior? → Identificar área base vs. ampliação
□ Há averbação na matrícula? → Se não, alertar no parecer
□ Há Habite-se anterior? → Pode indicar área regularizada
□ Decadência aplicável (> 5 anos com prova)? ✔/✘
□ Lote ≤ 220m²? → Habilitar Art. 15, mas cobrar multa Art. 39
□ TO excede limite? → Multa Art. 38/39 LC 267
□ TP abaixo do mínimo? → Multa Art. 39 LC 267 (separada)
□ Abertura na divisa (< 1,50m)? → Anuência do lindeiro
□ APP ou curso d'água próximo? → Licença ambiental/CODEMA
□ Bairro SRI ≠ Bairro cadastro municipal? → Certidão Localização
□ CEI ativa em alvará anterior? → Comunicado Baixa CEI
```

---

## PARTE 5 — O QUE O ANALISTA NUNCA FAZ

- **Nunca aplica isenção de multa Art. 79 em regularização**, mesmo com Art. 15 LC 267 (a isenção é de parâmetros urbanísticos em novos projetos, não de multas por obra ilegal)
- **Nunca emite Habite-se sem Laudo Técnico** em regularização (o laudo atesta a segurança estrutural, elétrica e hidráulica da edificação existente)
- **Nunca usa o nome de bairro do SRI como definitivo** — sempre confronta com o cadastro imobiliário municipal
- **Nunca confunde o CPF do engenheiro (ART)** com o CPF do proprietário
- **Nunca calcula multa LC 267 sobre a área total** — incide sobre a área em infração (o delta entre o que foi construído e o que o parâmetro permitia)
- **Nunca avança o processo sem os dois bloqueadores**: ART do as-built e taxa de Habite-se paga

---

## PARTE 6 — MEMÓRIA DE CÁLCULO MODELO (PROCESSO 190 COMO EXEMPLO)

```
PROCESSO 190/2026 — DIRCEU LOPES DE OLIVEIRA
Rua Alagoas, 740 — Bairro do Rosário — ZUR03
Terreno: 174,70m² | As-Built: 117,09m²
Alvará anterior: 4176/2012 (74,98m²) | Ampliação irregular: 42,11m²

ÍNDICES URBANÍSTICOS:
• TO = 117,09 / 174,70 × 100 = 75,16% → EXCEDE ZUR03
• CA = 117,09 / 174,70 = 0,67
• TP = 0 / 174,70 × 100 = 0,00% → DÉFICIT

DECADÊNCIA: Não aplicável (sem prova de > 5 anos para a ampliação)

TAXA DE APROVAÇÃO (área irregular):
• 42,11m² × R$ 4,48/m² = R$ 188,65

MULTA ART. 79, I (Construir sem licença, faixa até 60m²):
• 42,11m² × 1% × R$ 102,42 = R$ 43,13

MULTA ART. 79, II (Desacordo com projeto aprovado):
• 100% VRM = R$ 102,42 (valor fixo)

MULTA ART. 39 LC 267 — VIOLAÇÃO DE TO:
• 40m² × R$ 4,48 (1×) = R$ 179,20
• 2,11m² × R$ 13,45 (3×) = R$ 28,38
• Subtotal TO: R$ 207,58

MULTA ART. 39 LC 267 — VIOLAÇÃO DE TP:
• Idem: R$ 207,58

TOTAL ESTIMADO: R$ 188,65 + R$ 43,13 + R$ 102,42 + R$ 207,58 + R$ 207,58 = R$ 749,36
(+ Taxa de Habite-se R$ 85,00)
```

---

*GEM SMOSU — Base de Conhecimento | Gerado com base no Processo 190/2026*
*Referência cruzada: processo_190_Dirceu.json, padroes_recorrentes.md, tabela_valores_e_regras_2025.md*
