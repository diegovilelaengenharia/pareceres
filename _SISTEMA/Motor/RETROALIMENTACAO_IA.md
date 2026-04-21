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
