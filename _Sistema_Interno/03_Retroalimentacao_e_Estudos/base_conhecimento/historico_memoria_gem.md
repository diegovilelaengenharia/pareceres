# Histórico e Memória de Contexto do GEM (SMOSU Oliveira/MG)

> **Instrução para o GEM:** Este arquivo é atualizado automaticamente por `registrar_aprendizado.py`
> após cada parecer processado. Use-o como **few-shot learning**: ao analisar um novo processo,
> identifique casos similares abaixo e replique o padrão de argumentação, ajustando apenas os
> fatos específicos (endereço, área, profissional, datas).

---

## 📊 Estatísticas da Base (atualizado automaticamente)

| Indicador | Valor |
|-----------|-------|
| Total de casos registrados | 5 |
| Tipos mais frequentes | `alvara_regularizacao`, `habitese_multa` |
| Flags mais comuns | `DECADENCIA_CTN`, `MULTA_ART79`, `BAIXA_ALVARA_ANTIGO`, `QUEBRA_TP` |

---

## 🏆 Casos de Referência (Aprendizados Fundamentais)

### CASO-1 — Regularização As Built com Decadência, Multa Art. 79 e Anuência de Lindeiro
- **Processo:** 6100/2025 | **Tipo:** `alvara_regularizacao`
- **Zona:** ZUR 3 (conforme LC 267/2019 — Bairro Acácio Ribeiro, Cód. IPM 922) | **Terreno:** 180,00m² | **Construído total:** 154,08m²
- **Bairro:** Acácio Ribeiro | **Endereço:** Rua Coronel Teodorinho, nº 15 | **Requerente:** Maria Aparecida Silva Vasconcelos
- **Flags:** `ISENCAO_LOTE_PEQUENO` | `MULTA_ART79` | `MULTA_ART39` | `DECADENCIA_CTN` | `ABERTURA_DIVISA`
- **Composição de áreas:**
  - 82,58m² — área com decadência reconhecida (comprovada pelo Habite-se nº 928/2010, Proc. 4620/2010)
  - 71,50m² — área de acréscimo irregular (< 5 anos) → Multa Art. 79
  - 54,50m² — área que violou TO (29,21m² excedente) + permeabilidade (25,29m² insuficiente) → Multa Art. 39
- **Decisão correta:**
  - Decadência do Art. 150, §4º CTN reconhecida para 82,58m² (Habite-se anterior como prova).
  - Multa Art. 79 (obra sem licença): R$ 193,77 sobre 71,50m².
  - Multa Arts. 38 e 39 (quebra de parâmetros): R$ 700,33 sobre 54,50m² — **APLICADA mesmo com lote ≤ 220m²**.
  - Art. 15 da LC 267/2019 usado como fundamento para PERMITIR a regularização (reconhecimento de edificação com ocupação anterior à publicação da lei), **não como isenção de multa**.
  - Janela irregular (< 1,50m da divisa): resolvida com Termo de Anuência do confrontante (Art. 43 Lei 1.544/86 c/c Art. 1.301 Código Civil).
  - Total de regularizações fiscais: **R$ 1.281,32** (Taxa Habite-se R$ 81,20 + Taxa Aprovação R$ 306,02 + Multa Art. 79 R$ 193,77 + Multa Arts. 38/39 R$ 700,33).
- **Documentos emitidos:** Alvará de Construção nº 313/2025 | Habite-se Total nº 273/2025 (154,08m²) | Certidão de Decadência (82,58m²) | 2ª Via Habite-se nº 928/2010 | Certidão de Averbação (valor: R$ 265.163,44).
- **⚠️ LIÇÃO-CHAVE — CORRIGE ERRO ANTERIOR:** Terreno ≤ 220m² NÃO isenta da multa do Art. 39 em regularizações As-Built. A exceção do Art. 15 da LC 267/2019 serve para HABILITAR a regularização de edificações existentes, não para perdoar infrações já cometidas. A multa compensatória Art. 38/39 DEVE ser cobrada sobre a área que violou TO ou permeabilidade, independente do tamanho do lote, quando se tratar de regularização (As-Built). A isenção de TO/permeabilidade do Art. 15 aplica-se apenas a **novos projetos de aprovação** em lotes ≤ 220m².

---

### CASO-2 — APP Urbana como Condicionante Ambiental
- **Processo:** N/D | **Tipo:** `alvara_aprovacao` / `habitese_comum`
- **Flags:** `QUESTAO_AMBIENTAL`
- **Situação:** Imóvel próximo a ribeirão ou zona de proteção ambiental (APP). A planta ou as anotações do fiscal indicavam curso d'água.
- **Decisão correta:**
  - O parecer aprovou o processo tecnicamente, MAS condicionou a emissão ao `oficio_meio_ambiente`.
  - Em `documentos_emitir`, adicionado: *"Ofício à Secretaria de Meio Ambiente — análise e chancela do CODEMA (Condicionante ao Alvará)"*.
- **Lição-chave:** Sempre que houver menção a rio, ribeirão, mata ciliar, APP ou "zona azul" na planta ou anotações do fiscal → emitir `oficio_meio_ambiente` como condicionante paralela obrigatória.

---

---

### CASO-3 — Espólio + Alvará Antigo + Decomposição de Múltiplas Infrações
- **Processo:** 1205/2026 | **Tipo:** `habitese_multa` / `alvara_regularizacao`
- **Requerente:** Espólio de José Diniz de Oliveira | **Representante:** Edwar (procurador, por procuração da viúva Margarida)
- **Flags:** `ESPOLIO` | `BAIXA_ALVARA_ANTIGO` | `DECOMPOSICAO_MULTAS` | `INFRACAO_RECUO` | `DECADENCIA_CTN`
- **Alvará apenso:** Alvará nº 36/2000 (76,65m²) — existia mas nunca teve Habite-se.
- **Área final regularizada:** 171,74m²
- **Decomposição de infrações:**
  - 95,09m² → Multa Art. 79 (171,74 − 76,65 = área ampliada sem licença, < 5 anos)
  - [área específica] → Multa Art. 80 (obra diverge do projeto aprovado)
  - 4,87m² → Multa LC 267/2019 (depósito construído no recuo/afastamento lateral)
- **Decadência:** Comprovada por Planta Cadastral física do Município, Julho/2002. `meio_comprobatorio_decadencia: "Planta Cadastral do Município datada de julho/2002"`
- **Decisão correta:**
  - Processo bloqueado na Triagem por falta de representação legal do espólio — só liberou após juntada da Procuração.
  - Cada infração calculada e descrita separadamente no Comunicado de Pendência.
  - Parecer Final ordenou: *"Dar Baixa na CEI: Alvará de Construção nº 36/2000"*.
  - Avaliação financeira (R$ 165.806,93) gerada pela Comissão de Avaliação para fins de ITBI — **NÃO incluída** nas certidões emitidas (conforme Ofício 01/2026/CA).
- **⚠️ LIÇÃO-CHAVE 1 — ESPÓLIO:** A análise de mérito (técnica, urbanística) só começa após confirmação da representação legal. Sem Certidão de Óbito + Termo de Inventariante ou Procuração → emitir comunicado de pendência exclusivo para documentação de espólio, antes de qualquer outra avaliação.
- **⚠️ LIÇÃO-CHAVE 2 — VALOR DO IMÓVEL:** Avaliações financeiras para ITBI são internas e NÃO compõem as certidões de regularização física (Habite-se, Alvará, Certidão de Averbação). Nunca incluir valor do imóvel nesses documentos.
- **⚠️ LIÇÃO-CHAVE 3 — DECOMPOSIÇÃO:** Cada infração tem lei própria, metragem própria e multa própria. Discriminar sempre — o Comunicado de Pendência deve listar cada parcela individualmente.

---

---

### CASO-4 — Permeabilidade Zero + Divergência Cadastral de Bairro + CNO/CEI
- **Processo:** 190/2026 | **Tipo:** `habitese_multa` / `alvara_regularizacao`
- **Bairro físico (prefeitura):** Do Rosário | **Bairro na matrícula (SRI):** Boa Vista ← divergência
- **Terreno:** 174,70m² | **Alvará apenso:** Alvará nº 4176/2012 (74,98m²)
- **Área final as-built:** 117,09m² | **Ampliação irregular:** 42,11m²
- **Flags:** `PERMEABILIDADE_ZERO` | `DIVERGENCIA_CADASTRAL_BAIRRO` | `BAIXA_ALVARA_ANTIGO` | `DECOMPOSICAO_MULTAS` | `MULTA_ART79` | `MULTA_ART80`
- **Parâmetros críticos:** TO = 75,16% | **Permeabilidade = 0,00%** (impermeabilização total do lote)
- **Tramitação:** 09/01/2026 a 09/04/2026 (3 meses). Bloqueio inicial na triagem (14/01) por CND faltante + comprovantes; correção de projeto em 20/03; documentos corrigidos e multas pagas ao final de março.
- **Decomposição de multas (5 cobranças):**
  - Taxa de Habite-se: R$ 85,00
  - Taxa de Aprovação (42,11m²): R$ 188,67
  - Multa Art. 80 (obra em desacordo com projeto): R$ 102,42
  - Multa Art. 79 (42,11m² sem licença): R$ 42,95
  - Multa LC 267/2019 (permeabilidade 0%): R$ 591,18 ← **maior parcela (~59% do total)**
  - **TOTAL: R$ 1.010,22**
- **Evento especial — Divergência Cadastral:** Matrícula 29.543 (SRI) apontava Bairro Boa Vista, mas o imóvel é fisicamente no Bairro Do Rosário (confirmado in loco e pelo cadastro imobiliário municipal) → emitida **Certidão de Localização** para garantir segurança jurídica da averbação.
- **Evento especial — CNO/CEI:** Em vez de dar baixa interna no alvará antigo, a prefeitura emitiu comunicado transferindo ao proprietário a responsabilidade pela baixa do CNO/CEI junto à Receita Federal — blindando o município após substituição do alvará.
- **Documentos emitidos:** Alvará nº 059/2026 | Habite-se nº 061/2026 | Certidão de Localização | Certidão de Averbação
- **⚠️ LIÇÃO-CHAVE 1 — PERMEABILIDADE ZERO:** Quando TP = 0%, a multa da LC 267/2019 domina o custo total (~60%). Citar expressamente no parecer que a impermeabilização total transfere o ônus da drenagem pluvial ao sistema público, justificando a severidade da penalidade.
- **⚠️ LIÇÃO-CHAVE 2 — DIVERGÊNCIA CADASTRAL:** Quando a matrícula do cartório indica bairro diferente do cadastro municipal → emitir Certidão de Localização. Nunca corrigir a matrícula diretamente — isso é competência do cartório.
- **⚠️ LIÇÃO-CHAVE 3 — CNO/CEI:** Quando há substituição de alvará antigo por novo, a prefeitura pode transferir ao proprietário a responsabilidade de dar baixa no CNO/CEI na Receita Federal via comunicado. Isso é mais seguro juridicamente do que a prefeitura fazer a baixa internamente.

---

---

### CASO-5 — Regularização com TRT + Alvará Antigo (CEI) + CPF Invertido + Decadência por Espelho BCI
- **Processo:** 8901/2025 | **Tipo:** `alvara_regularizacao`
- **Requerente:** LUIS MARCOS DE OLIVEIRA | **Proprietários:** Edna Maria Henrique Oliveira e Luis Marcos de Oliveira
- **Endereço:** Rua Goiás, nº 725, Bairro Do Rosário | **Zona:** ZUR-3
- **Terreno:** 234,00m² | **Área regularizada:** 160,12m² | **Matrícula SRI:** 10.748
- **Responsável Técnico:** Sidney Cesar Caminha — **TRT nº CFT2605691319** (Técnico em Edificações, CFT/CRT)
- **Fiscais:** Wallace Alencar Martins Silveira (Mat. 306017-9), Silvania F. Santos Pedrosa (Mat. 3083160-1), Marlei Henrique de Oliveira (Mat. 3087661-8) — vistoria em 16/04/2026
- **Flags:** `TRT_CFT` | `ALVARA_ANTIGO_CEI` | `CPF_INVERTIDO` | `DECADENCIA_BCI` | `QUEBRA_TO` | `QUEBRA_TP`
- **Parâmetros:** TO = 76,38% (excede 70%), TP = 12,98% (abaixo de 20%), CA = 0,68 (atende)
- **Decadência:** Comprovada por Espelho Cadastral Municipal (BCI) com data de cadastro em 06/03/2017. Área decadente: **159,30m²**
- **Alvará anterior:** nº 300/1995 (94,80m²) — deverá ser dado baixa/cancelado junto ao CNO/CEI da Receita Federal
- **Situação especial — CPF Invertido:** Os CPFs dos proprietários estavam invertidos nas pranchas do projeto e no TRT. Exige retificação formal do TRT e dos carimbos antes da emissão dos documentos.
- **Situação especial — Taxa de Habite-se:** Balcão havia equivocadamente dispensado a taxa de habite-se alegando decadência. A decadência afasta apenas multas punitivas (Art. 79), nunca taxas de expediente e serviço municipal.
- **Documentos emitidos (condicionados):** Alvará de Regularização (160,12m²) | Cancelamento/Baixa CEI Alvará 300/1995 | Carta de Habite-se (160,12m²) | Certidão de Averbação (160,12m²) | Certidão de Decadência (159,30m²)
- **⚠️ LIÇÃO-CHAVE 1 — TRT NO PARECER:** Quando o responsável técnico é Técnico em Edificações (CFT/CRT), o documento é **TRT** (não ART nem RRT). O número do TRT deve aparecer: (a) no `paragrafo_abertura` junto ao nome do profissional; (b) em um considerando específico citando as atividades cobertas. Nunca jogar só em `extras_extraidos`.
- **⚠️ LIÇÃO-CHAVE 2 — DECRETO 4.149/2019 NO CONSIDERANDO DE LEGISLAÇÃO:** O considerando de legislação observada deve citar o **Decreto 4.149/2019** como primeiro instrumento, antes da Lei 1.544/86 e da LC 267/2019. Modelo: *"para a análise técnica, foram observadas as legislações municipais vigentes, em especial o Decreto nº 4.149/2019 (Procedimentos para Aprovação de Projetos), o Código de Obras do Município (Lei nº 1.544/86) e a Lei de Uso e Ocupação do Solo (Lei Complementar nº 267/2019)..."*
- **⚠️ LIÇÃO-CHAVE 3 — ART. 79 NA FUNDAMENTAÇÃO LEGAL:** O Art. 79 da Lei 1.544/86 deve SEMPRE aparecer na `fundamentacao_legal`, mesmo quando dispensado por decadência — neste caso, explicar que a penalidade fica afastada pela decadência do Art. 150, §4º CTN.
- **⚠️ LIÇÃO-CHAVE 4 — ESPELHO BCI COMO PROVA DE DECADÊNCIA:** O cadastro retroativo no Espelho Cadastral Municipal (BCI/IPM) é prova administrativa hábil para comprovar a decadência quando não há Habite-se anterior. Citar a data específica de cadastro no BCI como "prova administrativa inequívoca".
- **⚠️ LIÇÃO-CHAVE 5 — CEI/CNO COM ALVARÁ ANTIGO:** Quando existe alvará anterior com CEI/CNO vinculado, a prefeitura deve emitir documento de cancelamento/baixa e orientar o proprietário a providenciar a baixa junto à Receita Federal. Mesma situação do CASO-4.

---

## 📋 Casos Registrados em Produção

*(Seção alimentada automaticamente por `registrar_aprendizado.py`)*
