# Plano de Atualização: Motor de Pareceres Robustos v2.0

## 1. Objetivo
Garantir que os pareceres gerados em DOCX/PDF reflitam com fidelidade absoluta a análise inteligente feita pelo GEM (IA), eliminando discrepâncias causadas por automações rígidas do motor e garantindo conformidade legal total (precedência do Decreto 4.149/2019).

## 2. Diagnóstico Atual
- O motor tenta injetar prefixos ("Considerando que") e marcadores ("[PREENCHER]") que corrompem a análise fluida da IA.
- A calculadora urbanística reprocessa dados, podendo causar divergências visuais.
- Templates rígidos ignoram se o GEM já forneceu um texto final superior.

## 3. Ações Estratégicas

### Fase 1: Inteligência e Prompts (Prioridade Total ao GEM)
- **Ação 1.1:** Atualizar os prompts base (`Sistema/base_conhecimento/prompts`) para que o GEM entregue os campos `paragrafo_abertura`, `considerandos` e `fundamentacao_legal` já formatados e robustos.
- **Ação 1.2:** Enquadrar a hierarquia legal: Decreto 4.149/2019 deve ser sempre o primeiro citado na fundamentação técnica.

### Fase 2: Refatoração do Motor (Surgical Update)
- **Ação 2.1: Desativar Injeção Forçada.** Modificar `componentes.py` para que a "Inteligência de Prefixo" seja opcional. Se o texto já começar com "Considerando" ou estiver em negrito/lista, o motor não mexerá.
- **Ação 2.2: Eliminar Marcadores Intrusivos.** Remover a injeção de `[PREENCHER]` em campos de texto se o GEM decidiu que aquele campo não era necessário para o caso específico.
- **Ação 2.3: Calculadora Silenciosa.** Manter a auditoria da calculadora de índices, mas impedir que ela altere os valores no dicionário de dados final (ela apenas reportará erros no log/preview).

### Fase 3: Design e Robustez (Pareceres Incríveis)
- **Ação 3.1: Tabelas Avançadas.** Ativar e estilizar os blocos de "Histórico Cronológico" e "Partes Envolvidas" no DOCX para dar um aspecto profissional de dossiê.
- **Ação 3.2: Estética DOCX.** Refinar margens, fontes (Cambria/Calibri) e cores institucionais (Azul SMOSU) nos componentes.

### Fase 4: Validação e Testes
- **Ação 4.1:** Criar um processo de teste (`Entrada/processo_teste_auditoria.json`) com uma análise densa e verificar se o DOCX gerado é idêntico em conteúdo e superior em forma.

## 4. Critérios de Sucesso
1. O texto do GEM no JSON é transportado integralmente para o DOCX sem "lixo" de automação.
2. A fundamentação legal segue a hierarquia correta.
3. O design do documento é robusto, organizado e visualmente impactante.
4. Geração de PDF funcionando sem erros de conversão.
