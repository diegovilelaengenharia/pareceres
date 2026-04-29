# Guia de Estilo Narrativo — Pareceres Técnicos SMOSU
*Extraído da análise do Processo 6100/2025 — base para a IA redigir com precisão técnica e linguagem institucional*

> **Instrução para o GEM:** Este guia define como redigir cada seção de um parecer técnico.
> Siga os modelos de frase abaixo como se fossem molduras. Substitua os placeholders pelos
> fatos do processo. Nunca simplifique ou informe sem citar o instrumento legal correspondente.

---

## 1. PRINCÍPIOS GERAIS DE REDAÇÃO

- **Linguagem:** Formal, impessoal, técnica e objetiva. Nunca use coloquialismo.
- **Voz:** Preferencialmente passiva ou impessoal: "foi emitida", "atesta-se que", "constatou-se".
- **Tempo verbal:** Pretérito perfeito para fatos já ocorridos; presente para declarações em vigor.
- **Negrito:** Usar **apenas** em dados críticos — números de documentos, áreas em m², valores em R$, artigos de lei, nomes de profissionais/partes. Nunca negrito em texto narrativo comum.
- **Numerais:** Escrever por extenso entre parênteses quando relevante para segurança jurídica:
  - Área: **154,08m²** (cento e cinquenta e quatro metros e oito centímetros quadrados) — em certidões
  - Valor: R$ 1.281,32 (hum mil duzentos e oitenta e um reais e trinta e dois centavos) — em certidões
  - Para pareceres internos, a versão numérica com destaque em negrito é suficiente
- **Datas:** No corpo do parecer usar "dd/mm/yyyy". No cabeçalho formal usar "dd de mês de yyyy".
- **Áreas:** Sempre com vírgula decimal e "m²" junto: **154,08m²** — nunca "154.08 m²" nem "154m²".

---

## 2. ESTRUTURA CANÔNICA DO PARECER TÉCNICO

```
[CABEÇALHO INSTITUCIONAL]
[IDENTIFICAÇÃO: Processo nº / Requerente / Assunto]
[ABERTURA — "A SMOSU, no uso de suas atribuições..."]
[CONSIDERANDOS — lista de fatos técnicos e legais]
[FUNDAMENTAÇÃO LEGAL — artigos aplicados ao caso]
[CONCLUSÃO — despacho final]
[DOCUMENTOS A EMITIR — lista com observações]
[ASSINATURA — Responsável pelo Setor Técnico]
```

---

## 3. MODELOS DE FRASE POR TIPO DE CONSIDERANDO

### 3.1 Identificação do Imóvel (SEMPRE o primeiro considerando)
```
a requerente é proprietária do imóvel registrado sob **Matrícula nº [X]** do Serviço Registral 
de Imóveis (SRI), com área de terreno de **[X]m²** e testada de **[X]m**, situado na [endereço 
completo], Oliveira/MG, com Inscrição Cadastral [X], no qual não constava averbação da 
totalidade da área construída;
```
- Sempre mencionar: matrícula, área do terreno, testada, endereço completo, inscrição cadastral.
- Encerrar com o motivo da abertura do processo ("não constava averbação", "pretende ampliar", etc.).

### 3.2 Reconhecimento de Área com Decadência (quando aplicável)
```
a edificação [uso: residencial unifamiliar / comercial / misto] possui **[X]m²** regularizados 
por **Habite-se nº [X]/[ano]**, datado de [dd/mm/yyyy], expedido pelo Processo nº [X]/[ano], 
comprovando a decadência desta área, construída há mais de 05 (cinco) anos, nos termos do 
Art. 150, § 4º do Código Tributário Nacional;
```
- Fundamentar sempre no CTN. Jamais omitir o número do Habite-se anterior e o processo de origem.

### 3.3 Vistoria e Parecer Fiscal
```
o parecer fiscal emitido pelos Agentes **[Nome do Fiscal 1]**, Matrícula [X], e **[Nome do Fiscal 2]**, 
Matrícula [X], em [dd/mm/yyyy], atesta que a área construída total de **[X]m²** — [descrição 
dos pavimentos: ex. "distribuída em dois pavimentos, sendo o inferior com [X]m² e o superior 
com [X]m²"] — confere com o Projeto As Built apresentado, com Coeficiente de Aproveitamento 
(CA) de **[X]**, Taxa de Ocupação (TO) de **[X]%** e taxa de permeabilidade de **[X]%**, 
declarando a edificação finalizada e habitável;
```
- Identificar TODOS os fiscais (nome completo + matrícula).
- Sempre incluir: área total, distribuição de pavimentos (se houver), os três indicadores urbanísticos.

### 3.4 Responsabilidade Técnica (ART / RRT / TRT)

> **Atenção:** Este considerando é **obrigatório** em todo processo de regularização As-Built. Não jogar o número do documento técnico apenas em `extras_extraidos` — ele deve figurar explicitamente no corpo do parecer.

**Para ART (Engenheiro Civil — CREA):**
```
para o projeto foi emitida a Anotação de Responsabilidade Técnica (ART) **nº [X]** para as 
atividades de [descrição das atividades cobertas pela ART], pelo Engenheiro Civil 
**[Nome Completo]**, CREA/MG [nº do registro], cujo laudo técnico atesta condições adequadas 
de segurança, estabilidade e salubridade da edificação, em conformidade com a ABNT NBR 14.645:2001;
```

**Para RRT (Arquiteto e Urbanista — CAU):**
```
para o projeto foi emitido o Registro de Responsabilidade Técnica (RRT) **nº [X]** para as 
atividades de [descrição], pelo Arquiteto e Urbanista **[Nome Completo]**, CAU [nº do registro], 
cujo laudo técnico atesta condições adequadas de segurança, estabilidade e salubridade da 
edificação, em conformidade com a ABNT NBR 14.645:2001;
```

**Para TRT (Técnico em Edificações — CFT/CRT):**
```
para o projeto as built e Laudo Técnico foi emitido o Termo de Responsabilidade Técnica (TRT) 
**nº [CFT/CRT número]** para as atividades de [descrição], pelo Técnico em Edificações 
**[Nome Completo]**, CFT/CRT [nº do registro], cujo laudo técnico atesta condições adequadas 
de segurança, estabilidade e salubridade da edificação;
```

- Para As-Built: sempre incluir a menção ao laudo técnico e à ABNT NBR 14.645:2001 (exceto TRT, que não cita a norma).
- Para projetos novos: omitir a menção ao laudo.
- O número do TRT/ART/RRT **deve constar no `paragrafo_abertura`** quando for o único instrumento técnico do processo (não há Habite-se anterior).

### 3.5 Legislação Observada e Zoneamento

> **Como identificar o zoneamento:** Consultar `bairros_zoneamento_ipm.md` pelo nome do bairro. O campo `[zoneamento]` é sempre o código da LC 267/2019 (ex: ZUR 3, ZUR 2, ZC1). **Nunca usar a cor do Espelho Cadastral do IPTU** (ex: OCRE, AMARELO) — essas cores são faixas tributárias, não zonas urbanísticas.

> **Este considerando é obrigatório em todo parecer técnico.** Sempre incluir o Decreto 4.149/2019 além das duas leis principais.

```
para a análise técnica, foram observadas as legislações municipais vigentes, em especial o 
**Decreto nº 4.149/2019** (Procedimentos para Aprovação de Projetos), o **Código de Obras 
do Município** (**Lei nº 1.544/86**) e a **Lei de Uso e Ocupação do Solo** (**Lei Complementar 
nº 267/2019**), sendo aplicado o Art. 15 desta última, que prevê o reconhecimento de edificações 
com ocupação existente anterior à sua publicação; e que o imóvel está inserido na zona 
**[zoneamento]**, conforme classificação da referida Lei Complementar;
```
- O trecho "Art. 15 — reconhecimento de edificações existentes" é específico para As-Built/regularização.
- Para novos projetos, substituir pelo artigo pertinente ao tipo de uso e zoneamento.
- O **Decreto 4.149/2019** deve ser sempre o primeiro instrumento citado — ele rege os procedimentos administrativos da SMOSU.

### 3.6 Abertura Irregular na Divisa (janela/porta < 1,50m)
```
consta no projeto a existência de abertura ([tipo: janela / porta / basculante]) posicionada 
a distância inferior a 1,50m da divisa, em desconformidade com o **Art. 43 da Lei nº 1.544/86**; 
contudo, foi apresentado e aceito **Termo de Anuência** devidamente assinado pelo proprietário 
do imóvel confrontante, **[Nome do Confrontante]** (CPF: [X]), autorizando a permanência da 
abertura, em conformidade com o **Art. 1.301 do Código Civil**;
```
- Citar nome e CPF do confrontante anuente — isso é juridicamente necessário.
- Nunca omitir a base legal dupla: Art. 43 Lei 1.544/86 + Art. 1.301 CC.

### 3.7 Quitação de Taxas e Multas (DAMs)
```
a requerente comprovou o recolhimento de todas as taxas e multas exigidas no Comunicado 
emitido em [dd/mm/yyyy], conforme guias de pagamento DAM apresentadas em [dd/mm/yyyy], 
a saber: [listar cada item com valor]:
  — Taxa de Habite-se (R$ [X]);
  — Taxa de Aprovação de Projeto referente a [X]m² (R$ [X]);
  — Multa por construir sem licença — [X]m², Art. 79, Lei nº 1.544/86 (R$ [X]);
  — Multa por quebra de parâmetros urbanísticos — [X]m², Arts. 38 e 39, Lei nº 267/2019 (R$ [X]);
totalizando **R$ [total]** em regularizações fiscais.
```
- Nunca omitir o detalhamento item a item. O total em negrito.
- A data do Comunicado e a data de apresentação dos DAMs são campos distintos — nunca confundir.

---

## 4. ESTRUTURA DA FUNDAMENTAÇÃO LEGAL

Cada item da `fundamentacao_legal` deve seguir o padrão:
```
**[Instrumento Legal — Nome Abreviado]:** [Como o artigo se aplica ao caso específico.]
```

> **Atenção — itens obrigatórios para `alvara_regularizacao`:**
> 1. **Sempre** incluir o Art. 79 da Lei 1.544/86 + Arts. 38 e 39 da LC 267/2019 na fundamentação, mesmo que a multa seja dispensada por decadência. Indicar explicitamente o motivo da dispensa quando aplicável.
> 2. **Sempre** incluir o Art. 150, §4º do CTN quando houver área decadente.
> 3. Incluir Art. 43 da Lei 1.544/86 c/c Art. 1.301 do CC apenas quando houver abertura irregular na divisa.

**Modelo de fundamentação para regularização completa (referência — Processo 6100/2025):**
- `__Art. 150, § 4º do Código Tributário Nacional (Lei nº 5.172/1966)__: Se a lei não fixar prazo à homologação, será ele de 5 (cinco) anos, a contar da ocorrência do fato gerador. Aplica-se ao caso para fins de reconhecimento da decadência da área de [X]m², construída há mais de 5 anos.`
- `__Art. 79 da Lei nº 1.544/86 e Arts. 38 e 39 da Lei Complementar nº 267/2019__: Fundamentam a emissão do Alvará de Regularização e a aplicação de multas por construção sem licença e por infração de parâmetros urbanísticos (Taxa de Ocupação e Permeabilidade).`
- `__Art. 43 da Lei nº 1.544/86 c/c Art. 1.301 do Código Civil__: Resguardado mediante apresentação de Termo de Anuência assinado pelo proprietário confrontante para a manutenção de abertura posicionada a menos de 1,50m da divisa.`

**Modelo quando a multa Art. 79 é dispensada por decadência:**
- `__Art. 79 da Lei nº 1.544/86__: Aplicável à construção sem licença. A incidência da penalidade sobre a área de [X]m² fica afastada em razão da decadência administrativa comprovada (Art. 150, §4º do CTN), restando a multa exigível apenas sobre eventual área de acréscimo sem comprovação de 5 anos.`

---

## 5. MODELO DE CONCLUSÃO

```
Diante do exposto, visto que a requerente sanou todas as pendências apontadas, apresentou 
documentação técnica completa e comprovou o recolhimento das taxas e multas devidas, 
conclui-se que a regularização da edificação atende aos requisitos técnicos e legais 
aplicáveis, podendo ser emitidos os seguintes documentos:
```

Para processos em que há pendências ainda não resolvidas, usar:
```
Diante do exposto, conclui-se que o processo encontra-se condicionado ao saneamento das 
pendências abaixo relacionadas, devendo ser apresentada a documentação complementar no 
prazo de 30 (trinta) dias:
```

---

## 6. DOCUMENTOS A EMITIR — PADRÃO DE DESCRIÇÃO

Cada item da lista `documentos_emitir` deve ser descrito com precisão:

| Documento | Modelo de Descrição |
|---|---|
| Alvará de Construção | `Alvará de Construção nº [X]/[ano] — regularização de edificação [uso] com área total de [X]m²` |
| Habite-se | `Habite-se [Total / Parcial] nº [X]/[ano] — área total construída de [X]m² ([existente X]m² + acréscimo [X]m²)` |
| Certidão de Decadência | `Certidão de Decadência — [X]m²`, obs: `comprovados pelo Habite-se nº [X], datado de [dd/mm/yyyy], para fins de comprovação perante a Receita Federal do Brasil, nos termos do Art. 150, § 4º do CTN.` |
| Certidão de Averbação | `Certidão de Averbação — imóvel [uso] com [X]m² construídos`, obs: `Valor total do imóvel de R$ [X] ([por extenso]), conforme Laudo de Avaliação da Comissão de Avaliação da Prefeitura Municipal de Oliveira, datado de [dd/mm/yyyy]; Alvará de Construção: [dd/mm/yyyy]; Data do Habite-se: [dd/mm/yyyy].` |
| 2ª Via de Habite-se | `2ª Via do Habite-se nº [X]/[ano]`, obs: `Para arquivo da requerente, referente ao processo nº [X]/[ano].` |

---

## 7. ERROS DE ESTILO A EVITAR

| Errado | Correto |
|---|---|
| "foi verificado que a casa está ok" | "a edificação apresenta condições adequadas de segurança, estabilidade e salubridade" |
| "o morador pagou a multa" | "a requerente comprovou o recolhimento das taxas e multas devidas" |
| "área de 154m²" | "área de **154,08m²**" (sempre com casas decimais e negrito) |
| "conforme a lei" | "conforme o **Art. X da Lei nº X/XXXX** ([Nome da Lei])" |
| "a janela é irregular" | "abertura posicionada a distância inferior a 1,50m da divisa, em desconformidade com o Art. 43 da Lei nº 1.544/86" |
| "o fiscal aprovou" | "o parecer fiscal emitido pelo Agente [Nome], Matrícula [X], em [data], atesta que..." |
| "pode ser liberado" | "conclui-se que a regularização atende aos requisitos técnicos e legais aplicáveis" |
| "taxa de R$ 700" | "Multa por quebra de parâmetros urbanísticos — 54,50m², Arts. 38 e 39, Lei nº 267/2019 (R$ 700,33)" |

---

## 8. FLUXO CRONOLÓGICO DO PROCESSO (checklist para GEM verificar completude)

Para saber se o processo está completo para emissão dos documentos finais, verificar:
1. ✅ Requerimento inicial com documentos pessoais, matrícula e IPTU
2. ✅ Vistoria fiscal inicial → se houve divergência, exigência de As-Built
3. ✅ Juntada do Projeto As-Built + ART + Laudo Técnico pelo responsável técnico
4. ✅ Vistoria fiscal de confirmação (agentes atestam que o As-Built bate com o existente)
5. ✅ Parecer técnico com cálculo de áreas e infrações → Comunicado de Pendências
6. ✅ DAMs quitados apresentados pelo requerente
7. ✅ Parecer final favorável → emissão dos documentos

Se qualquer etapa estiver faltando → modo `MODO_CONDICIONADO` ou `comunicado_pendencia`.
