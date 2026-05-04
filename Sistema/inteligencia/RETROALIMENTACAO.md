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

## Versão 9.0 — 04/05/2026 — Sistema Interativo de Análise (SIA)

### Mudança Estrutural: De Pipeline a Diálogo

**Problema identificado:** O fluxo TRIGGER → Wizard avançava rápido demais sem possibilidade de intervenção. O engenheiro só via o resultado final (JSON), sem chance de corrigir dados extraídos erroneamente durante as fases intermediárias (identificação, cálculo de índices, multas).

**Solução implementada:**

1. **Novo `SIA_v1.0.md`** — substituiu o `01_SUPER_PROMPT_RESEARCH.md` como system instruction principal. Implementa 6 fases sequenciais com checkpoints obrigatórios. Nenhuma fase avança sem aprovação explícita do engenheiro.

2. **`GABARITOS.md` criado** — 5 templates estruturais (Regularização com Multa, com Decadência, Aprovação, Comunicado de Pendência, Habite-se). Estrutura 3 camadas obrigatória: Fato → Artigo → Cálculo.

3. **7 ferramentas MCP implementadas e corrigidas:**
   - `calcular_multas_processo` — Art. 79 + Art. 39, URM 2026 = R$ 102,42
   - `validar_checklist_documentos` — Decreto 4.149/2019
   - `analisar_decadencia` — CTN Art. 150 §4º
   - `gerar_memoria_calculo_indices` — TO/CA/TP formatado
   - `consultar_documentos_emitir` — **CORRIGIDO**: agora inclui Baixa CEI e Comunicado Decadência obrigatórios em regularizações
   - `verificar_excecoes_lote_pequeno` — **CORRIGIDO**: TO e TP continuam obrigatórios mesmo em lotes ≤ 220m²; só afastamentos são flexibilizados
   - `buscar_logradouro_oficial` — **MELHORADO**: detecta palavras-chave de renomeação e ativa flag MUDANCA_DENOMINACAO

4. **Comandos globais do SIA** — o engenheiro pode digitar `voltar`, `pular`, `editar [campo]: [valor]`, `explicar`, `adicionar`, `remover`, `recomeçar` a qualquer momento.

5. **Gatilhos automáticos** — 10 flags detectados automaticamente: APP_URBANA, IEPHA_OBRIGATORIO, ADENSAMENTO_CRITICO, CONFLITO_SRI_PMO, NOTA_DEVOLUTIVA, MUDANCA_DENOMINACAO, RETIFICACAO_ART, CONDOMINIO, TROCA_REQUERENTE, DECADENCIA_PARCIAL.

**Regra consolidada v9.0:**
> O JSON só é gerado na Fase 6, após todas as 5 fases anteriores serem aprovadas pelo engenheiro. A `memoria_de_calculo` é sempre preenchida pela ferramenta `gerar_memoria_calculo_indices` antes da geração do JSON.

---

## Versão 8.0 — 03/05/2026

### Novas Diretrizes:
1. **memoria_de_calculo OBRIGATÓRIA:** Nunca emitir parecer com campo vazio. Usar saída de `gerar_memoria_calculo_indices` diretamente. O motor Python agora renderiza este campo em uma seção dedicada.
   
2. **Consulta sequencial MCP:** Sempre executar na ordem: (1) indices_urbanisticos → (2) validar_parametros → (3) calcular_multas → (4) analisar_decadencia.

3. **GABARITOS.md integrado:** Todo parecer deve derivar de um template do GABARITOS.md, adaptando para o caso concreto sem alterar a estrutura dos considerandos (3 camadas: Fato + Artigo + Cálculo).

4. **Análise Temporal e Partes:** Os campos `historico_cronologico` e `partes_envolvidas` são agora obrigatórios para garantir a rastreabilidade forense do processo.

5. **URM 2026 CORRETA:** R$ 102,42 (corrigido de R$ 4,10 errado em algumas referências antigas).

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

---

### [2026-05-03] Processo 1125/2026 — Nelson Colhado Junior (Complexidade Ambiental e Patrimonial)

**Problemas identificados:** Processos que envolvem divisa com córregos (APP) e áreas de tombamento (IEPHA) exigem uma narrativa muito mais cautelosa nos considerandos, citando órgãos externos que não pertencem à SMOSU (CODEMA e IEPHA).

**Diagnóstico:** O sistema precisa de "gatilhos" claros para processos em Áreas Urbanas Consolidadas. A simples menção a "córrego" ou "nascente" deve disparar a exigência de recuos específicos e anuências ambientais.

**Correções e Lições Aplicadas:**

1. **Protocolo de APP em Área Consolidada:** Quando detectada divisa com curso d'água, o parecer deve citar a **Lei Municipal nº 3.971/2023** e a **Lei Federal nº 12.651/2012**. O recuo deve seguir o que for determinado pelo CODEMA (neste caso, 10 metros lineares).
2. **Servidões de Utilidade Pública:** Áreas de servidão do SAAE (AV-2 na matrícula) devem ser subtraídas da área edificável, mas computadas na Taxa de Permeabilidade.
3. **Trava do IEPHA:** Para imóveis no Centro (ZC-2), a Nota Técnica do IEPHA é um bloqueador absoluto. O sistema deve sugerir automaticamente um `comunicado_pendencia` se esse documento não estiver no PDF.
4. **Soma de Áreas (Novo + Existente):** Em lotes que já possuem edificação regular (80,07m²) e solicitam nova obra (171,56m²), o cálculo de TO e CA deve ser SEMPRE a soma das duas, para evitar que o lote seja superlotado além do limite da zona.

### [2026-05-03] Processo 1169/2026 — Wander Furtado Alves (Confrontantes e Logradouros)

**Problemas identificados:** Frequentemente, o nome da rua no projeto ("Rua E") diverge do nome oficial atualizado ("Rua Zizinha Rabelo Costa"). Se o sistema não capturar essa transição, a certidão de número sai com o endereço desatualizado.

**Diagnóstico:** A extração forense deve sempre buscar por "antiga Rua X" ou decretos de denominação (como o **Decreto 3.207/2013** citado neste processo).

**Correções e Lições Aplicadas:**

1.  **Mapeamento de Confrontantes:** O sistema agora extrai a tabela de vizinhos (Frente, Lados e Fundos) diretamente do memorial ou da matrícula. Isso permite que a **Certidão de Localização** seja gerada com 100% de precisão sem intervenção manual.
2.  **Protocolo de Denominação:** Se houver menção a "antiga rua" ou "Loteamento X", o sistema deve gerar automaticamente a flag `MUDANCA_DENOMINACAO_LOGRADOURO` e sugerir a emissão da **Certidão de Nome de Rua**.
3. **Garagem Descoberta (Memória de Cálculo):** Reafirmamos que áreas de garagem sem estrutura não computam no CA, mas devem constar na TO (se houver projeção/piso impermeável) e ser descritas no campo de observação do alvará.

### [2026-05-03] Processo 1526/2026 — Marileia Pedrosa Pereira (Conflito Cadastral SRI vs PMO)

**Problemas identificados:** O Cartório (SRI) recusou a averbação (Nota Devolutiva) porque o bairro na matrícula era "Aparecida" e no Habite-se saiu "Jardim dos Bandeirantes".

**Diagnóstico:** Divergências entre o registro histórico do Cartório e a base tributária/geo da Prefeitura são comuns em áreas de transição ou novos loteamentos.

**Correções e Lições Aplicadas:**

1.  **Gatilho de Nota Devolutiva:** Sempre que o PDF contiver uma "Nota Devolutiva" do SRI, o sistema deve priorizar a extração do motivo da recusa.
2.  **Certidão de Localização Corretiva:** Nestes casos, o parecer não deve apenas deferir o Habite-se, mas exigir a emissão de uma **Certidão de Localização** específica que ateste: "O imóvel situado na Rua X, embora conste como Bairro A na matrícula, localiza-se tecnicamente no Bairro B conforme legislação municipal vigente".
3. **Cruzamento de Inscrição:** A Inscrição Municipal (01.02.051...) é a âncora de verdade. Se o bairro nela divergir da matrícula, o sistema deve levantar a "Flag" de potencial conflito antes mesmo do engenheiro emitir o documento.

### [2026-05-03] Processo 6161/2025 — Gustavo Moreira (Reforma em Unidade Autônoma / Condomínio)

**Problemas identificados:** Em reformas de salas ou apartamentos, o sistema pode se confundir entre os índices do edifício todo (CA de 8,18) e a área da unidade (104,03m²).

**Diagnóstico:** Reformas internas não alteram TO ou CA global, mas exigem verificação se a unidade está regularizada na matrícula mãe.

**Correções e Lições Aplicadas:**

1.  **Distinção de Áreas:** O sistema agora diferencia "Área Privativa" (uso exclusivo) de "Área Comum" (proporção do terreno/edifício). O Alvará de Reforma deve citar apenas a área privativa da unidade autônoma.
2.  **Referência ao Habite-se Global:** Sempre que houver reforma em prédio, o sistema deve buscar o **número do Habite-se original do edifício** (ex: 226/2022) para garantir que a unidade existe legalmente antes da reforma.
3. **RRT de Projeto vs Execução:** Em condomínios, a exigência de RRTs separadas para projeto e execução é rígida devido ao impacto em outras unidades. O sistema deve validar se ambos os códigos de RRT foram extraídos.

### [2026-05-03] Processo 8235/2025 — Antônio César Vieites (Infração de TP e Multas Cumulativas)

**Problemas identificados:** Imóvel com Taxa de Permeabilidade zerada (0,00%) e ampliação clandestina de 116,74m². O requerente tentou decadência para área que já estava averbada.

**Diagnóstico:** Este é um caso de "Infração Combinada". Quando a TP é zerada, a multa do Art. 39 da Lei 267/2019 atinge seu patamar mais alto de gravidade.

**Correções e Lições Aplicadas:**

1.  **Lógica de Decadência Negativa:** Se a área já consta na Matrícula (averbada), ela é considerada regular. Não se emite Certidão de Decadência para áreas regulares; a decadência serve apenas para anistiar multas de áreas irregulares antigas. O sistema deve travar pedidos de decadência para áreas averbadas.
2.  **Multas Cumulativas (Art. 79 + Art. 39):** O sistema aprendeu que as multas são somadas. A multa por "Construir sem Licença" (Art. 79) incide sobre o m² do acréscimo. A multa por "Infração Urbanística" (Art. 39) incide sobre a quebra dos índices (TO/TP). No caso de TP 0%, o cálculo deve ser explícito na memória de cálculo.
3. **Identificação de Processos Anteriores:** A extração capturou os processos de 1997 e 1998. O sistema deve sempre buscar por números de processos antigos para montar a árvore genealógica do imóvel.

### [2026-05-03] Processo 9542/2025 — Guilherme Claret (Decadência Parcial e Adensamento Crítico)

**Problemas identificados:** Coexistência de área regular (87,04m² de 2014) e acréscimo irregular (97,79m²). O adensamento no lote de 146,29m² chegou a TO 86,17% e TP 0,34%.

**Diagnóstico:** Este caso exige a separação clara entre o que é "Direito Adquirido/Consolidado" e o que é "Infração Atual".

**Correções e Lições Aplicadas:**

1.  **Protocolo de Decadência Parcial:** O sistema aprendeu que um único imóvel pode ter três estados de área:
    - Área Averba (Regular)
    - Área Decadente (Irregular mas consolidada > 5 anos)
    - Área Infracionada (Irregular < 5 anos sujeita a multa)
2.  **Multas em Lotes Adensados:** Em casos de TO > 80% e TP quase nula (< 1%), as multas da Lei 267/2019 devem ser aplicadas com rigor máximo. O sistema deve sugerir a flag `ADENSAMENTO_CRITICO`.
3. **Rastreabilidade de Alvarás Antigos:** A identificação do Alvará 5415/2014 e Habite-se 3068/2014 foi vital para conceder a decadência parcial. O sistema deve sempre cruzar dados com o histórico de Habite-se emitidos na última década.

### [2026-05-03] Processo 10016/2025 — Lorena Necesio Pio (Troca de Titularidade e Substituição de ART)

**Problemas identificados:** O processo iniciou em nome de uma pessoa e terminou em nome de outra. Além disso, a ART original continha um erro de digitação e foi substituída.

**Diagnóstico:** Mudanças administrativas durante o trâmite (comprador assumindo o processo do vendedor) e erros materiais em documentos técnicos são frequentes.

**Correções e Lições Aplicadas:**

1.  **Protocolo de Troca de Requerente:** O sistema deve identificar no campo `requerente` o nome final (Lorena), mas mencionar nos `considerandos` o vínculo inicial (Compromisso de Compra e Venda) para manter a rastreabilidade jurídica.
2.  **Rastreio de ART Substituta:** Se houver menção a "em substituição à ART X", o sistema deve capturar ambos os números para garantir que o setor de fiscalização não aceite o documento antigo e inválido. A flag `RETIFICACAO_ART` deve ser ativada.
3.  **Memória de Áreas (Útil vs Construída):** Reafirma-se o padrão: garagens descobertas não computam para fins de taxa de alvará (área coberta), mas integram o "Parecer Narrativo" para descrever a totalidade do uso do solo.

---

### [2026-05-03] Upgrade de Análise Temporal — Campos `historico_cronologico` e `partes_envolvidas`

**Problema identificado:** O GEM analisava os processos de forma estática — dados dispersos em `extras_extraidos` (fiscais, datas, alvarás anteriores) sem narrativa cronológica. O engenheiro precisava solicitar explicitamente "analise de forma temporal" a cada novo processo. O documento final não refletia a sequência lógica dos fatos.

**Diagnóstico:** Omissão estrutural. O sistema não possuía campos formais para linha do tempo nem para identificação estruturada de todas as partes. A análise temporal era comportamento ad-hoc, não padrão.

**Correções aplicadas (30/04/2026):**

1. **Novo campo `historico_cronologico`** — Array obrigatório em pareceres técnicos:
   - Cada evento tem: `data`, `evento`, `tipo`, `referencia`, `agentes` (para vistorias)
   - Tipos padronizados: `abertura_processo`, `vistoria_fiscal`, `habite_se`, `alvara`, `comunicado_pendencia`, `quitacao_dam`, `documento_municipal`, `embargo`, `certidao`, `averbacao`, `apensamento`
   - Ordem cronológica do mais antigo ao mais recente — do registro original da matrícula ao parecer atual
   - O compilador Python gera automaticamente uma tabela visual "HISTÓRICO CRONOLÓGICO DO PROCESSO" no DOCX

2. **Novo campo `partes_envolvidas`** — Objeto obrigatório em pareceres técnicos:
   - `requerente` com campo `qualidade` (proprietário, procurador, comprador, etc.)
   - `proprietario` (apenas se diferente do requerente)
   - `responsavel_tecnico` com `conselho`, `tipo_rt` e `numero_rt` simplificado
   - `agentes_fiscais` como array com nome + matrícula funcional de cada fiscal
   - `assinante_parecer` (sempre Diego Tarcísio / CREA 235.474/D)
   - O compilador gera tabela "PARTES E RESPONSÁVEIS DO PROCESSO" no DOCX

3. **`prompt_modelo.md` atualizado** — Seção "Análise Temporal Obrigatória (SEMPRE)" adicionada. O comportamento temporal agora é **padrão**, não precisa ser solicitado.

4. **`cobertura_considerandos.py` atualizado** — Novo tema `cronologia` adicionado como recomendado. O relatório pré-voo avisa quando os considerandos não mencionam datas/sequência histórica.

5. **Instruções de treinamento atualizadas** — `00_INSTRUCAO_SISTEMA_GEMINI.md` e `01_GEM_INSTRUCOES.md` atualizados com os dois novos campos como obrigatórios no checklist pré-entrega do JSON.

**Regra consolidada:**
> Ao analisar qualquer processo como engenheiro civil: primeiro monte a linha do tempo (do mais antigo ao mais recente), depois redija os considerandos seguindo essa ordem cronológica. Os campos `historico_cronologico` e `partes_envolvidas` devem estar presentes em todos os pareceres técnicos.

#### 5. Anotações na Tabela de Dados Técnicos
- **Padrão aprendido:** Quando TO ou TP estão fora dos limites normativos mas há multa aplicada (regularização com penalidade), os campos da tabela de cabeçalho devem ter a anotação `(conferir zoneamento)` ao lado do valor.
- Quando o lote se enquadra na exceção de lote pequeno (≤ 220m²), o campo `Área Terreno` deve exibir `(exceção da lei)` ao lado da metragem.
- Esses sufixos textuais devem ser incluídos diretamente no valor do campo no JSON quando aplicáveis (ex: `"area_terreno": "144,38m² (exceção da lei)"`).

