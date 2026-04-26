# Fluxo de Tramitação de Processos — Lógica Institucional SMOSU

> **Instrução para o GEM:** Este arquivo descreve como a prefeitura de Oliveira-MG
> "pensa" e movimenta um processo internamente. Use-o para determinar o **Destino**
> correto de cada documento gerado e para antecipar loops de correção antes de
> propor o tipo de parecer.

---

## Setores da SMOSU (Obras) e suas funções

| Setor | Função principal |
|---|---|
| **PROTOCOLO** | Recebimento inicial do requerimento + documentos básicos |
| **FISCALIZAÇÃO (OBRAS)** | Vistoria física do imóvel; investigação de processos apensos |
| **TRIAGEM (OBRAS)** | Verificação superficial de documentos obrigatórios por decreto |
| **ENTREGA DE DOCUMENTOS (OBRAS)** | Balcão de espera — cidadão anexa faltantes ou paga guias |
| **ANÁLISE (OBRAS)** | Análise técnica: zoneamento, TO, TP, CA, multas, enquadramento legal |
| **CONFECÇÃO DE DOCUMENTOS (OBRAS)** | Redação e impressão de pareceres, comunicados, alvarás, certidões |
| **DESENHISTA PLANTA CADASTRAL (OBRAS)** | Atualização do mapa cadastral da cidade com as áreas aprovadas |
| **CADASTRO IMOBILIÁRIO** | Atualização do cadastro tributário do imóvel (vinculado ao IPTU) |

---

## Fluxo Padrão de Tramitação (Habite-se / Regularização)

### Fase 1 — Protocolo e Vistoria Física

```
PROTOCOLO
  └─► FISCALIZAÇÃO (1ª passagem)
        Artefato: Parecer Fiscal atestando existência e habitabilidade
        └─► TRIAGEM
```

**Documentos que o cidadão deve apresentar no protocolo:**
- Requerimento
- RG do requerente
- Comprovante de endereço
- Matrícula do imóvel

**Atenção — Espólio:** SE o proprietário registrado for falecido (espólio), a Triagem exige adicionalmente:
- Certidão de Óbito
- Termo de Inventariante **ou** Procuração de herdeiro/representante legal
→ Sem esses, o processo retorna ao balcão (ENTREGA DE DOCUMENTOS) independentemente de qualquer outra análise.

---

### Fase 2 — Triagem Documental (1º Loop possível)

```
TRIAGEM
  ├─► [OK] Todos os documentos básicos presentes
  │         └─► ANÁLISE (prossegue)
  │
  └─► [BLOQUEIO] Faltam documentos primários (ART/RRT, comprovante Taxa Habite-se, etc.)
            └─► ENTREGA DE DOCUMENTOS (aguarda o cidadão/RT juntar os faltantes)
                  └─► [após juntada] ANÁLISE
```

**Documentos primários que travam na Triagem (exigidos por decreto):**
- ART ou RRT do responsável técnico
- As-Built assinado (planta da situação atual)
- Laudo técnico
- Comprovante de pagamento da Taxa de Habite-se (guia PIX/DAM)

---

### Fase 3 — Análise Técnica e Cobranças (2º Loop possível)

```
ANÁLISE (1ª passagem)
  Ação: verificar leis, zoneamento, TO, TP, CA, multas, irregularidades
  └─► CONFECÇÃO DE DOCUMENTOS
        Artefato: Comunicado de Pendência (cobrança de taxas + multas + ajustes de projeto)
        └─► ENTREGA DE DOCUMENTOS (aguarda pagamentos e/ou correções)
              └─► [após pagamento] ANÁLISE (2ª passagem — parecer final)
```

**Evento especial — Processo Físico Apenso:**
> Durante a espera na Fase 3, a Fiscalização pode localizar no arquivo físico um
> processo antigo vinculado ao mesmo lote (ex: alvará anterior). Quando isso ocorre:
> - A Fiscalização emite parecer informando a anexação do processo apenso.
> - A Análise recalcula as multas com base nas áreas já licenciadas no passado.
> - Um novo Comunicado de Pendência (ajustado) substitui o anterior.
> - Apenas a **diferença de área** (área atual − área já licenciada) é multada.

**Evento especial — Divergência Cadastral de Bairro:**
> Quando a matrícula no SRI (Serviço Registral de Imóveis/cartório) registra um bairro
> diferente do que consta no cadastro imobiliário municipal (IPM/IPTU) e no levantamento in loco:
> - Emitir **Certidão de Localização** atestando a localização real conforme os registros municipais.
> - Não tentar corrigir a matrícula — isso é competência exclusiva do cartório.
> - Incluir a Certidão de Localização na lista de `documentos_emitir` do JSON.

**Evento especial — Baixa de Alvará Antigo Sem Habite-se:**
> Se existir alvará anterior vinculado ao lote que nunca recebeu Habite-se, o Parecer
> Técnico Final deve incluir instrução explícita para "Dar Baixa" nesse documento
> (ex: *"Cancelar/dar baixa no Alvará de Construção nº XX/AAAA — CEI"*) a fim de
> evitar duplicidade no sistema da prefeitura.

---

### Fase 4 — Parecer Final, Emissão, Cadastro e Arquivo

```
ANÁLISE (2ª passagem)
  Artefato: Parecer Técnico Final (deferimento, ordenando emissão de certidões)
  └─► CONFECÇÃO DE DOCUMENTOS (2ª passagem)
        Artefatos: Alvará + Carta de Habite-se + Certidão de Decadência + Certidão de Averbação
        └─► DESENHISTA PLANTA CADASTRAL
              Artefatos: Planta Cadastral (.pdf + .dwg) com áreas aprovadas atualizadas
              └─► CADASTRO IMOBILIÁRIO
                    Ação: Atualização do cadastro tributário do imóvel (área, valor venal, IPTU)
                    └─► ARQUIVO (processo encerrado + retirada dos documentos pelo cidadão)
```

---

## Regra de Decisão de Tipo de Documento e Destino

O GEM deve aplicar esta árvore para determinar qual documento gerar e para onde ele vai:

### Nó 0 — O requerente é espólio?
**SE** o proprietário registrado for falecido **→** verificar se constam no processo:
- Certidão de Óbito **E**
- Termo de Inventariante **OU** Procuração de representante legal habilitado

**SE** qualquer um desses documentos estiver faltando **→**
- Tipo de documento: **Comunicado de Pendência (Espólio)**
- Destino: **ENTREGA DE DOCUMENTOS**
- Campos obrigatórios no JSON: `tipo_requerente: "Espólio"`, `nome_espolio`, `nome_representante_legal`

---

### Nó 1 — Falta documento primário obrigatório?
**SE** faltar ART/RRT, As-Built, Laudo Técnico ou comprovante de taxa **→**
- Tipo de documento: **Parecer de Triagem (INDEFERIDO)**
- Destino: **ENTREGA DE DOCUMENTOS**

---

### Nó 2 — Há multa a pagar, divergência no projeto ou ajuste pendente?
**SE** o processo passou da Triagem mas o engenheiro identificou infrações, diferença de área ou erro no projeto **→**
- Tipo de documento: **Comunicado de Pendência**
- Destino: **ENTREGA DE DOCUMENTOS**
- **Regra de decomposição:** discriminar cada infração individualmente com sua metragem exata (ver seção abaixo).
- Obs.: se um processo apenso foi descoberto após o 1º Comunicado, emitir um **2º Comunicado (Ajustado)** recalculando apenas a diferença de área.

---

### Nó 3 — Tudo pago e projeto correto?
**SE** todas as taxas foram pagas, multas quitadas e o projeto está sem pendências **→**
- Tipo de documento: **Parecer Técnico de Deferimento**
- Destino: **CONFECÇÃO DE DOCUMENTOS**
- **Sequência obrigatória pós-emissão:** CONFECÇÃO → DESENHISTA PLANTA CADASTRAL → **CADASTRO IMOBILIÁRIO** → ARQUIVO.
- **SE** houver alvará antigo sem Habite-se vinculado ao lote → incluir instrução de "Dar Baixa" no corpo do parecer.

---

## Regra de Decomposição de Infrações

Nunca tratar irregularidades como um bloco único. Cada infração tem lei própria, metragem própria e multa própria. Calcular e descrever separadamente:

| Tipo de Infração | Lei base | Variável |
|---|---|---|
| Área ampliada sem licença (< 5 anos) | Art. 79 Lei 1.544/86 | `area_ampliada_sem_licenca` |
| Área em desacordo com projeto aprovado | Art. 80 Lei 1.544/86 | `area_em_desacordo_projeto` |
| Área que violou TO ou TP | Arts. 38 e 39 LC 267/2019 | `area_infracao_parametros` |
| Área construída em recuo/afastamento | LC 267/2019 (limitações de uso) | `area_infracao_recuo` |

Fórmula de composição:
```
area_total_irregular = area_ampliada_sem_licenca + area_em_desacordo_projeto + area_infracao_parametros + area_infracao_recuo
```
Cada parcela deve aparecer explicitamente no Comunicado de Pendência com sua metragem e base legal.

---

## Cardápio de Meios de Prova para Decadência Administrativa

A IA deve selecionar e citar o meio comprobatório disponível no processo:

| Meio de Prova | Como citar |
|---|---|
| Habite-se anterior | *"conforme Habite-se nº XXX/AAAA (Proc. NNNNN/AAAA)"* |
| Inclusão no espelho IPTU/cadastro tributário | *"data de inclusão no espelho cadastral tributário municipal — AAAA"* |
| Ortofoto ou imagem de satélite | *"Ortofoto de satélite de AAAA constante nos autos"* |
| Planta Cadastral física do município | *"Planta Cadastral do Município datada de mês/AAAA, constante nos autos"* |
| Escritura ou certidão cartorial com data | *"Escritura Pública de AAAA / Certidão de Registro de Imóveis de AAAA"* |

Variável JSON: `meio_comprobatorio_decadencia` — preencher com o meio disponível.

---

## Casos de Referência

### Caso 1 — Processo 441/2026
**Descrição:** Habite-se com processo apenso (Proc. 699/2004, alvará de 470m²) descoberto durante a tramitação.

**Sequência real de tramitação:**
1. PROTOCOLO → FISCALIZAÇÃO (confirmou obra pronta)
2. FISCALIZAÇÃO → TRIAGEM → **BLOQUEIO** (faltavam ART/RRT e comprovante de taxa)
3. TRIAGEM → ENTREGA DE DOCUMENTOS (RT juntou As-Built, Laudo, RRT, PIX)
4. ENTREGA DE DOCUMENTOS → ANÁLISE (1ª) → CONFECÇÃO (**Comunicado 1**: multa sobre 545,52m² + correção no selo)
5. CONFECÇÃO → ENTREGA DE DOCUMENTOS (aguardando pagamento)
6. **Evento:** FISCALIZAÇÃO encontrou Proc. 699/2004 no arquivo físico (alvará de 470m²)
7. FISCALIZAÇÃO emitiu parecer de anexação → CONFECÇÃO emitiu **Comunicado 2 (Ajustado)**: multa recalculada apenas sobre a diferença de 75,52m² (545,52 − 470,00)
8. Pagamento efetuado → ANÁLISE (2ª) → Parecer Final de Deferimento
9. CONFECÇÃO → emitiu Alvará + Habite-se + Certidão Decadência + Certidão Averbação
10. DESENHISTA PLANTA CADASTRAL → atualizou mapa (arquivos PDF + DWG)
11. CADASTRO IMOBILIÁRIO → atualização tributária
12. ARQUIVO → retirada pelo cidadão

**Lição principal:** Nunca assumir que o primeiro Comunicado de Pendência é definitivo. A existência de processo apenso com área já licenciada no passado **zera a multa sobre essa área** e exige recálculo.

---

### Caso 2 — Processo 1205/2026
**Descrição:** Espólio + alvará antigo sem Habite-se (Alvará nº 36/2000, 76,65m²) + múltiplas infrações decompostas.

**Particularidades:**
- Proprietário original (José Diniz de Oliveira) falecido → representado por procurador dos herdeiros (Edwar, com procuração da viúva Margarida).
- Alvará Nº 36/2000 (76,65m²) existia mas nunca teve Habite-se → área já licenciada desconta da multa Art. 79.
- Área final: 171,74m². Infrações decompostas em 3 fatias:
  - 95,09m² → Multa Art. 79 (área ampliada sem licença = 171,74 − 76,65)
  - [área em desacordo com projeto] → Multa Art. 80 (obra diverge do projeto aprovado)
  - 4,87m² → Multa LC 267/2019 (depósito construído no recuo/afastamento lateral)
- Decadência comprovada por Planta Cadastral física do município (Julho/2002).
- Parecer Final incluiu instrução de baixa: *"Dar Baixa na CEI: Alvará de Construção nº 36/2000"*.

**Lição principal:** Espólio exige representação legal antes de qualquer análise de mérito. Infrações devem ser cirurgicamente decompostas — cada metro quadrado tem sua lei e sua conta.
