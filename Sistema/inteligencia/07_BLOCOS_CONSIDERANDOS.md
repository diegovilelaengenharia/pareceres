# BLOCOS DE CONSIDERANDOS — GEM SMOSU
## Templates com 3 camadas: Fato + Artigo + Cálculo

> **Regra de ouro**: Cada considerando deve responder:
> - **O QUÊ** foi verificado (fato do processo)
> - **QUAL LEI** rege aquilo (artigo específico)
> - **QUANTO** dá (cálculo explícito, quando houver)

---

## CATEGORIA A — REGULARIZAÇÃO (`alvara_regularizacao`)

### [REG-01] Documentos de propriedade *(obrigatório)*
```
"Que o requerente apresentou Título de Propriedade com MATRÍCULA DE INTEIRO TEOR sob nº
[matricula_sri] ([descrição: Lote X, Quadra Y, com área de Z m²]) e Inscrição Cadastral
[inscricao_municipal], comprovando a regularidade dominial do imóvel, conforme exigido pelo
Art. 1º do Decreto Municipal nº 4.149/2019."
```
> Variantes: se o requerente é comprador com contrato → "comprovado por COMPROMISSO
> PARTICULAR DE COMPRA E VENDA em nome do requerente, com Inscrição Cadastral [X]."

---

### [REG-02] Responsabilidade técnica *(obrigatório)*
```
"Que para o projeto As-Built e Laudo Técnico (Data: [data_laudo]), foi emitido o
[Termo de Responsabilidade Técnica TRT / Anotação de Responsabilidade Técnica ART /
Registro de Responsabilidade Técnica RRT] nº [art_rrt] pelo profissional
[profissional_nome] ([profissional_registro]), atendendo ao requisito de responsabilidade
técnica previsto no Art. 48 da Lei Municipal nº 1.544/86."
```

---

### [REG-03] Índices urbanísticos com cálculos *(obrigatório)*
```
"Que o imóvel está inserido no Zoneamento [zona_uso], sendo verificados os índices
urbanísticos conforme Tabela 1 do Art. 9º da Lei Complementar nº 267/2019:
Taxa de Ocupação de [taxa_ocupacao] (= [area_projecao]/[area_terreno]×100) [abaixo/dentro]
do limite de [limite_TO_zona]%;
Coeficiente de Aproveitamento de [coef_aproveitamento] (= [area_total_construida]/[area_terreno])
[abaixo/dentro] do limite de [limite_CA_zona];
Taxa de Permeabilidade de [taxa_permeabilidade] (= [area_permeavel]/[area_terreno]×100)
[acima/dentro] do mínimo de [minimo_TP_zona]%."
```

---

### [REG-04] Decomposição das áreas — área já averbada *(obrigatório quando há AV-X)*
```
"Que a análise documental demonstra que o imóvel possui área existente já regularizada de
[area_ja_averbada], conforme [averbação / Certidão de Habite-se] [area_averbada_anterior_av]
datada de [area_averbada_anterior_data]. Tendo em vista que o levantamento do projeto
As-Built constatou área total de [area_total_construida], a diferença aferida de
[area_acrescimo] (= [area_total_construida] − [area_ja_averbada]) configura-se como área
edificada sem licença prévia da Prefeitura, sobre a qual incidem as penalidades previstas
no Art. 79 da Lei nº 1.544/86 e Arts. 38-39 da LC nº 267/2019."
```

---

### [REG-05] Decadência administrativa *(obrigatório quando comprovada)*
```
"Que, nos termos do Art. 150, §4º do Código Tributário Nacional (decadência
administrativa), a [Planta Cadastral Municipal datada de / Habite-se nº X de / IPTU de]
[data_referencia_decadencia] atesta a existência consolidada de [area_decadencia] de área
construída no lote há mais de 5 (cinco) anos sem autuação fiscal, configurando a decadência
do direito de lançamento das penalidades tributárias sobre esta parcela, que será objeto
de Certidão de Decadência específica."
```
> **Regra**: só usar quando a área NÃO está averbada na matrícula. Se já está averbada (AV-X),
> usar o bloco REG-04 e NÃO emitir certidão de decadência para essa parte.

---

### [REG-06] Sem histórico de licença *(condicional — quando o fiscal não encontrou alvará)*
```
"Que mediante a vistoria fiscal, constatou-se não ter sido encontrado alvará, habite-se ou
projeto anterior do imóvel em questão nos arquivos da Prefeitura, configurando edificação
realizada integralmente sem licença prévia, nos termos do Art. 79 da Lei nº 1.544/86."
```

---

### [REG-07] Legislação aplicável *(encerramento — obrigatório)*
```
"Que o setor técnico salienta que a análise se ateve à Legislação: Decreto 4.149 de
19/12/2019, Código de Obras do Município de Oliveira (Lei nº 1.544, de 04 de março de 1986)
e Lei de Uso e Ocupação do Solo (Lei Complementar nº 267, de 11/11/2019)."
```

---

## CATEGORIA B — OBRA NOVA (`alvara_aprovacao`)

### [APR-01] Situação da obra — vistoria fiscal *(obrigatório)*
```
"Que de acordo com o PARECER FISCAL emitido por [agentes_fiscais], a construção não foi
iniciada[, sendo tirado o nº [numero_porta]] [na data de [data_vistoria_fiscal]]."
```
> Variante com número: "...não foi iniciada, sendo tirado o nº [numero_porta]."
> Variante sem número: "...não foi iniciada." (omitir a parte do número)

---

### [APR-02] Documentos de propriedade *(obrigatório)*
```
"Que o requerente apresentou título de propriedade através de [MATRÍCULA DE INTEIRO TEOR
com registro nº [matricula_sri] do SRI / COMPROMISSO PARTICULAR DE COMPRA E VENDA] e
INSCRIÇÃO IMOBILIÁRIA [inscricao_municipal]."
```

---

### [APR-03] Responsabilidade técnica *(obrigatório)*
```
"Que para o PROJETO apresentado, foi emitido o [Termo de Responsabilidade Técnica TRT /
Anotação de Responsabilidade Técnica ART / Registro de Responsabilidade Técnica RRT]
nº [art_rrt] para as atividades de [art_atividade: Projeto e Execução Arquitetônica,
Instalação Hidráulica, Impermeabilização, etc.] pelo [Engenheiro Civil / Arquiteto e
Urbanista / Técnico em Edificações] [profissional_nome], [profissional_registro]."
```

---

### [APR-04] Índices urbanísticos *(obrigatório — mesmo formato REG-03)*
```
[Usar o mesmo bloco REG-03, adaptado para o projeto proposto]
```
> Adicionar: "deverá atender à taxa de permeabilidade mínima de [minimo_TP_zona]% do
> referido terreno, que corresponde a [TP_minima_m2]m² (o projeto prevê [area_permeavel]m²)."

---

### [APR-05] Legislação aplicável *(encerramento — obrigatório)*
```
"Que a análise desta secretaria se ateve ao Código de Obras do Município de Oliveira
(Lei nº 1544, de 04 de Março de 1986), à Lei de Uso e Ocupação do Solo
(Lei nº 267, de 11 de Outubro de 2019) e ao Decreto nº 4.149 de 19 de dezembro de 2019."
```

---

## CATEGORIA C — HABITE-SE SIMPLES (`habitese_comum`)

### [HAB-01] Referência ao alvará *(obrigatório)*
```
"Que a obra foi licenciada pelo Alvará de Construção nº [numero_alvara_emitido], emitido
em [data_alvara_emitido], para área de [area_total_construida]."
```

### [HAB-02] Parecer fiscal — conclusão *(obrigatório)*
```
"Que de acordo com o PARECER FISCAL emitido por [agentes_fiscais], a obra se encontra
concluída e em condições de habitabilidade, conferindo com o projeto aprovado."
```

### [HAB-03] Documentos de propriedade *(obrigatório)*
```
[Usar APR-02]
```

### [HAB-04] Legislação *(encerramento)*
```
[Usar APR-05]
```

---

## CATEGORIA D — HABITE-SE COM MULTA (`habitese_multa`)

### [HBM-01 a 04]
Usar os mesmos blocos HAB-01 a 04.

### [HBM-05] Infração detectada *(obrigatório — específico desta categoria)*
```
"Que o PARECER FISCAL identificou que não foi respeitada a [taxa de permeabilidade mínima /
Taxa de Ocupação máxima] aprovada em projeto: o projeto previa [valor_previsto]
([area_prevista]m²) e o realizado foi de [valor_realizado] ([area_realizada]m²), resultando
em [déficit de Xm² de área permeável / excesso de Y% na Taxa de Ocupação], configurando
infração ao Art. [79 da Lei nº 1.544/86 / 38-39 da LC nº 267/2019]."
```

### [HBM-06] Pagamento da multa *(obrigatório)*
```
"Que o requerente efetuou o pagamento da multa referente à infração constatada, conforme
[guia de recolhimento nº X / DAM nº X] quitado em [data_pagamento], no valor de
R$ [valor_multa]."
```

---

## CATEGORIA E — REFORMA/AMPLIAÇÃO (`alvara_reforma_demolicao_ampliacao`)

### [RFA-01] Situação da obra *(obrigatório)*
```
"Que de acordo com o PARECER FISCAL emitido por [agentes_fiscais], a construção ainda não
foi iniciada."
```

### [RFA-02] Composição da área *(obrigatório)*
```
"Que o terreno está registrado sob Matrícula nº [matricula_sri] em nome do(a) requerente
(com área averbada de [area_ja_averbada]) e possui Inscrição Cadastral [inscricao_municipal]."
```

### [RFA-03] Responsabilidade técnica *(obrigatório)*
```
"Que para o projeto, foram apresentados a [ART/RRT] nº [art_rrt] referente à atividade
de [art_atividade: Projeto Arquitetônico de Reforma], e [SE houver execução separada]
o respectivo [ART/RRT] nº [art_rrt_execucao] contemplando a atividade de Execução de Obra,
ambos de responsabilidade do(a) [título: Arquiteta e Urbanista / Engenheiro Civil]
[profissional_nome], [profissional_registro], englobando a área da ampliação de [area_ampliacao]."
```

### [RFA-04] Legislação *(encerramento)*
```
[Usar APR-05]
```

---

## VERIFICAÇÕES DE EXCEÇÃO (aplicar em qualquer categoria)

### [EXC-01] Lote ≤ 220m² *(condicional)*
```
"Que o lote possui área de [area_terreno], sendo inferior ao limite de 220,00m²,
aplicando-se a exceção prevista no §13 do Art. 9º da Lei Complementar nº 267/2019,
que remete os afastamentos laterais e de fundos ao Código Civil (Art. 1.301 — mínimo
de 1,50m), em substituição às faixas previstas na Tabela 1 da mesma lei."
```

### [EXC-02] IEPHA / Área tombada *(condicional)*
```
"Que o imóvel encontra-se em área de entorno do tombamento do Centro Histórico de
Oliveira (desde 31/10/2013), sendo submetido à análise e aprovação do IEPHA —
Instituto Estadual do Patrimônio Histórico e Artístico de Minas Gerais, conforme
exigência legal; sendo apresentada a Nota Técnica nº [nota_tecnica_iepha]."
```

### [EXC-03] Abertura na divisa *(condicional)*
```
"Que o projeto prevê abertura (janela/porta) a menos de 1,50m da divisa com o imóvel
[lindeiro], condicionando a aprovação à apresentação de Termo de Anuência assinado pelo
proprietário lindeiro [confrontante_anuente_nome], nos termos do Art. 43 da Lei nº 1.544/86
c/c Art. 1.301 do Código Civil."
```

### [EXC-04] APP / Curso d'água *(condicional — emitir ofício paralelo)*
```
"Que o imóvel confronta-se com [córrego/nascente/área de preservação permanente —
APP], devendo o processo ser encaminhado ao CODEMA para análise ambiental prévia, nos
termos da Lei Federal nº 12.651/2012 (Código Florestal) e legislação municipal."
```

### [EXC-05] Processo judicial vinculado *(condicional)*
```
"Que o imóvel está sujeito a processo judicial nº [processo_judicial_vinculado],
[cujos autos foram apensados ao presente processo / sendo a regularização condicionada
ao trâmite judicial], devendo os documentos emitidos ser utilizados exclusivamente
para os fins do referido processo."
```

---

## REGRAS DE CONSTRUÇÃO DOS CONSIDERANDOS

### O que SEMPRE fazer:
1. Começar com "Que..." (padrão jurídico)
2. Citar o artigo de lei **dentro** do considerando, não depois
3. Escrever o cálculo no formato: "(= X/Y×100)" junto com o resultado
4. Para multas: citar a faixa do escalonamento + a conta completa
5. Ordem: documentação → vistoria → índices → exceções/agravantes → legislação geral

### O que NUNCA fazer:
- Considerando genérico sem dado do processo ("Que a obra está concluída") → sempre inserir o número real
- Citação legal sem artigo específico ("conforme a legislação") → sempre citar o artigo
- Cálculo omitido ("TO = 63,32%") → sempre mostrar a conta: "(= 227,96/360,00×100)"
- "Considerando que" como frase completa → deve ter conteúdo substantivo

### Quantidade por tipo:
- Regularização: 4–7 considerandos (obrigatórios + condicionais)
- Aprovação (obra nova): 3–5 considerandos
- Habite-se simples: 3–4 considerandos
- Habite-se com multa: 5–6 considerandos
- Reforma/ampliação: 3–4 considerandos
