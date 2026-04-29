# Ciclo de Retroalimentação Contínua (Self-Healing Workflow)

Este documento estabelece o pacto de inteligência contínua entre o Engenheiro (Usuário) e a Inteligência Artificial (Antigravity). O sistema de Pareceres e Alvarás em Oliveira/MG é vivo e deve evoluir a cada falha ou ambiguidade identificada.

## 🔄 O Loop de Evolução

Sempre que o usuário trouxer um **JSON defeituoso**, com **informações genéricas/inventadas**, ou que o **compilador travar** devido a chaves ausentes, o Antigravity não deve apenas "corrigir o erro pontual". Ele executará a seguinte análise de triagem profunda:

### Passo 1: Diagnóstico da Anomalia
1. A falha foi de **alucinação**? (O GEM inventou uma regra que não existe?)
2. A falha foi de **omissão**? (O GEM deixou de aplicar uma multa ou parâmetro que deveria?)
3. A falha foi **estrutural**? (Ele quebrou o esquema exigido no `04_Caderno_Modelos_Finais_Secretaria.txt`?)

### Passo 2: Ação de Contenção (Fix Imediato)
- Ajustar o JSON manualmente para que o usuário possa gerar o documento do processo do dia sem bloqueios.

### Passo 3: Cura Estrutural (Retroalimentação do Motor)
Baseado no diagnóstico, a IA editará proativamente o "Cérebro" do sistema:
- **Se a alucinação ocorreu por ausência de instrução:** A IA vai editar o `codex_legal.json` criando uma exceção ou regra fixa clara.
- **Se o GEM se comportou mal interpretando texto livre:** A I.A vai refatorar o `01_Instrucao_Principal.txt` inserindo diretrizes rígidas (ex: "Não assuma X se Y não for declarado").
- **Se o código Python de compilação não capturou o erro elegantemente:** A I.A vai editar o `_engine/geradores/__init__.py` ou os `componentes.py` para tornar a arquitetura blindada contra aquele tipo de formato de dados incorreto.

## 💡 Princípio Operacional: Nunca errar o mesmo erro duas vezes.
Com esta diretriz, o sistema deixa de ser apenas um "gerador de relatórios" e passa a ser um ecossistema que aprende com a vivência prática da Secretaria Municipal de Obras e Serviços Urbanos (SMOSU). A cada falha reportada da Fiscalização ou do GEM, o código principal será instantaneamente refinado e submetido ao Repositório Remoto (`push`).

---

## 📋 Registro de Evoluções Aplicadas

### [2026-04-21] Processo 12329/2025 — Kessia Maria Candido Salviano

**Problema identificado:** O GEM produzia análises brilhantes no chat (Fase 1), mas ao empacotar no JSON (Fase 2), os textos ficavam genéricos e "pobres" — sem citações de lei, sem narrativa documental, sem argumentação técnica.

**Diagnóstico:** Omissão nas instruções. Os prompts não exigiam explicitamente que a qualidade textual fosse mantida dentro do JSON. O GEM tratava o JSON como "formulário de dados" e não como "parecer oficial".

**Correções aplicadas (21/04/2026):**

1. **Prompts do GEM reescritos do zero** (`GEM_INSTRUCOES_COMPLETAS.txt`):
   - Arquivo único consolidado substituindo os fragmentos antigos.
   - Regra de Ouro: liberdade total de redação formal, mas dados/fatos são sagrados e imutáveis.
   - Orientações de escopo para cada campo de texto (considerandos, fundamentação, conclusão).
   - Exemplo real do Processo 6100 como régua de qualidade mínima.

2. **Engine Python (`componentes.py`) — formatação visual:**
   - Negrito em **todos** os valores das tabelas de identificação e carimbo técnico.
   - Card de documentos emitir: fonte do título aumentada de 9pt → 11pt, observações de 9pt → 10pt.
   - Espaçamento maior entre o cabeçalho e o título "PARECER SETOR TÉCNICO".
   - Espaçamento maior entre a tabela de identificação e "DADOS TÉCNICOS".
   - Bug fix: `build_conclusao_e_docs` usava `add_run` simples → trocado para `rich_segments` para processar `**negrito**` e `__itálico__` na conclusão.

3. **Padrão de citação de leis no JSON:**
   - Legislações devem ser citadas com marcadores `__itálico__` (ex: `__Art. 15 da LC 267/2019__`).
   - RRTs simplificados: usar apenas o número curto (ex: `15541842`), não o código completo do sistema CAU.
   - Referências cruzadas: quando uma lei é citada nos considerandos, deve reaparecer na fundamentação legal com explicação detalhada da sua aplicação ao caso concreto.
   - `data_processo` deve estar por extenso ("18 de dezembro de 2025"), não abreviado ("18/12/2025").

4. **Prompts secundários atualizados:**
   - `01_Instrucao_Principal.txt`: adicionada diretriz de "Riqueza Textual no JSON (CRÍTICO)".
   - `05_Prompt_Chat_de_Inicializacao.txt`: adicionada regra 4 na Fase Dois exigindo citações e narrativa.
   - `prompt_modelo.md`: diretriz de riqueza textual integrada nas regras de formatação.

### [2026-04-22] Processo 10654/2025 — João Batista da Costa (Comunicado e Parecer)

**Problemas identificados:**
1. A IA usou `__` (itálico) com a intenção de gerar **negrito** nos itens do Comunicado de Pendência. No engine Python (`componentes.py`), a função `rich_segments` requer explicitamente `**` para renderizar negrito.
2. O texto do Comunicado de Pendência gerado inicialmente pela IA era muito técnico ("multa por extrapolação de índices urbanísticos").
3. As infrações de TO e TP (LC 267/2019) foram separadas em dois itens diferentes de pendência.
4. Diagramação no documento gerado: O título `CONCLUSÃO TÉCNICA:\n` em um parágrafo justificado forçava o Word a esticar a palavra por toda a linha.
5. A seção "Emissão de Documentos" ficava solta na mesma página da conclusão.

**Correções aplicadas (22/04/2026):**

1. **Engine Python (`componentes.py`):**
   - **Correção de Justificação:** Títulos `CONCLUSÃO TÉCNICA:` agora possuem um parágrafo isolado com alinhamento à esquerda, impedindo o esticamento bizarro da fonte quando estava no mesmo parágrafo justificado.
   - **Quebra de Página Automática:** Inserida a propriedade `page_break_before = True` no título "Emissão de Documentos:", garantindo que os cards de documentos sejam sempre plotados em uma folha nova e limpa.
   - **Padronização Visual:** Fixado tamanho 11pt para todos os textos da conclusão (títulos, bullet points e observações).

2. **Padrão de Geração de JSON (Retroalimentação do Prompt):**
   - **Comunicados de Pendência (Linguagem):** O GEM deve adotar uma linguagem simplificada e mais acessível ao cidadão/requerente, evitando jargões excessivos ("espaço de terra livre" ao invés de apenas "taxa de permeabilidade"), sendo direto nas instruções.
   - **Negrito Obrigatório:** Sempre utilizar duplo asterisco `**texto**` (e não sublinhado `__`) para destacar em negrito os itens de pendência dentro do JSON, garantindo que o `rich_segments` leia a formatação corretamente.
   - **Unificação de Multas:** Multas de mesma natureza legal (Excesso de Ocupação e Déficit de Permeabilidade pela LC 267/2019) devem ser agrupadas no Comunicado como uma única pendência de "Multas Urbanísticas Acumulativas", deixando claro seu caráter simultâneo.

### [2026-04-22] Processo 1065/2026 — Edimirce Eduardo de Oliveira (Parecer e Comunicado)

**Problemas identificados:**
1. Os documentos (especialmente o parecer e o comunicado inicial gerados pelo GEM) correram o risco de se tornarem demasiadamente simplificados na tentativa de clareza, perdendo a riqueza técnica e a "identidade institucional" característica dos pareceres modelo da prefeitura.
2. O detalhamento das multas cumulativas não estava claro quanto à origem (diferença entre o apresentado e o alvará aprovado anteriormente, e falta de licença sobre a mesma área).

**Correções aplicadas:**
1. **Identidade Institucional da Escrita:** Retificou-se a instrução para garantir que o GEM mantenha o tom formal, professoral e detalhado. A simplificação no Comunicado não significa "empobrecimento" textual; os textos devem ser fáceis de entender, mas sem perder o embasamento legal robusto (cite as leis, explique o que cada taxa reprovada significa). 
2. **Explicação Didática de Multas:** Sempre especificar no Comunicado de Pendência a origem das multas de forma completa. Ex: detalhar que há cobrança simultânea de taxa de aprovação (pela diferença de área) e multa por edificar sem licença, ambas sobre a mesma infração, amparadas pela Lei 267 e somadas cumulativamente. Os valores e porcentuais divergentes (ex: TO em 87,05% e TP em 1,87%) devem figurar explicitamente na comunicação ao cidadão.

---

### [2026-04-22] Reforma Estrutural dos Prompts — Liberdade Analítica + Extração Máxima

**Problema identificado:**
O GEM gerava pareceres truncados porque os prompts impunham quotas numéricas rígidas (mínimo 5 considerandos, mínimo 3 fundamentações, mínimo 100 palavras na conclusão). Isso forçava textos genéricos em processos simples e cortes indevidos em processos complexos.

**Correções aplicadas:**

1. **Arquivos reformulados:**
   - `01_Instrucao_Principal.txt`: Reescrito. Quotas removidas. Profundidade nasce do caso, não de regras fixas.
   - `05_Prompt_Chat_de_Inicializacao.txt`: Reescrito. Simplificado, sem checklists rígidos.
   - `03_Banco_de_Historico.txt`: Atualizado com 4 processos modelo. Diretriz mudada de "REPLIQUE" para "INSPIRE-SE".
   - `GEM_INSTRUCOES_COMPLETAS.txt`: Checklist numérico removido. Revisão qualitativa referenciada nos pareceres modelo.

2. **Nova funcionalidade — Chave `extras_extraidos`:**
   - GEM coleta o MÁXIMO de dados do PDF (fiscais e matrículas funcionais, alvarás anteriores, valores pagos, confrontantes, observações manuscritas, etc.) na chave livre `"extras_extraidos"`.
   - O engenheiro (Antigravity) faz a triagem ao receber o JSON, decide o que incorporar ao sistema e retroalimenta.
   - Ciclo: GEM extrai → Antigravity tria → sistema evolui.

**Princípio consolidado:**
> A qualidade é medida pela fidelidade aos fatos e riqueza narrativa — não por contagem de itens. Processos simples = parecer objetivo. Processos complexos = parecer extenso.

---

### [2026-04-23] Processo 1065/2026 — Edimirce Eduardo de Oliveira (Revisão Final pelo Engenheiro)

**Revisão humana aplicada após geração automática. Diferenças identificadas:**

#### 1. Número do RRT — Formato Simplificado
- **Gerado pela IA:** `RRT nº SI16568585100CT001` (código completo do sistema CAU)
- **Corrigido pelo Engenheiro:** `RRT nº 16568585` (número simplificado)
- **Regra aprendida:** Em considerandos e no corpo do parecer, usar **apenas os 8 primeiros dígitos numéricos do RRT**, suprimindo os prefixos/sufixos de sistema (ex: `SI`, `100CT001`). A chave `art_rrt_numero` no JSON também deve guardar o número simplificado.

#### 2. Considerandos — Remoção de Redundância Técnica
- **Gerado pela IA:** Incluía considerando explicando que, "por instrução técnica, não obstante o Art. 15 da LC 267/2019 para lotes pequenos, foram identificadas infrações por TO > 70% e TP < 20%..."
- **Corrigido pelo Engenheiro:** Esse considerando foi **removido**. As multas de TO e TP já são justificadas na Fundamentação Legal (Arts. 38 e 39 LC 267/2019), sendo desnecessário repeti-las nos considerandos.
- **Regra aprendida:** Os **considerandos** devem registrar fatos do processo (quem é, o que foi feito, quem assina, o que falta). A **fundamentação legal** é o lugar para explicar as infrações e os dispositivos aplicáveis. Não duplicar.

#### 3. Documentos a Emitir — Lista Expandida com Comunicados Específicos
- **Gerado pela IA:** 3 documentos (Alvará, Habite-se, Certidão de Averbação)
- **Corrigido pelo Engenheiro:** 5 documentos:
  1. **Alvará de Regularização (As Built) — 152,64m²** — com obs. legal completa citando Art. 79 Lei 1.544/1986 e Arts. 38 e 39 LC 267/2019
  2. **Comunicado de Baixa de CEI** — informando o nº do alvará anterior cancelado (4845/2013 / 69,51m²)
  3. **Comunicado de Decadência** — registrando formalmente que não há decadência por Planta Cadastral ou Habite-se
  4. **Carta de Habite-se — 152,64m²** — sem obs. adicional
  5. **Certidão de Averbação de Área — 152,64m²** — incluir a área no próprio título
- **Regra aprendida:** Em processos de regularização As Built com alvará anterior, **sempre gerar**:
  - `Comunicado de Baixa de CEI` (para extinguir o alvará/CEI original)
  - `Comunicado de Decadência` (registrando se há ou não decadência, conforme análise do arquivo municipal)
  - A obs. do Alvará de Regularização deve citar explicitamente as leis que fundamentam a regularização (não apenas "substituição ao licenciamento de 2013")

#### 4. Observações dos Documentos — Linguagem Institucional
- **Regra aprendida:** A obs. do Alvará deve ter linguagem de fundamentação legal, no estilo:
  > *"Alvará emitido para regularização de imóvel edificado em desacordo com projeto aprovado pela prefeitura, mediante o cumprimento do Art. 79 da Lei 1.544 de 1986 e Art. 38, 39 da Lei 267 de 2019."*
- A obs. do Comunicado de Baixa de CEI deve referenciar o alvará sendo cancelado:
  > *"Alvará de Construção nº [NÚMERO] para uma área de [ÁREA]."*
- A obs. do Comunicado de Decadência deve ter linguagem afirmativa ou negativa clara:
  > *"Conforme analise em arquivo municipal, o imóvel não possui decadência por Planta Cadastral ou Habite-se."*

#### 5. Anotações na Tabela de Dados Técnicos
- **Padrão aprendido:** Quando TO ou TP estão fora dos limites normativos mas há multa aplicada (regularização com penalidade), os campos da tabela de cabeçalho devem ter a anotação `(conferir zoneamento)` ao lado do valor.
- Quando o lote se enquadra na exceção de lote pequeno (≤ 220m²), o campo `Área Terreno` deve exibir `(exceção da lei)` ao lado da metragem.
- Esses sufixos textuais devem ser incluídos diretamente no valor do campo no JSON quando aplicáveis (ex: `"area_terreno": "144,38m² (exceção da lei)"`).

