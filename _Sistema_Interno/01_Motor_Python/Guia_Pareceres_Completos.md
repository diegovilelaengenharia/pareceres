# Diretrizes para Pareceres Técnicos Mais Completos

Para garantir que o seu motor de IA gere pareceres verdadeiramente completos e à prova de auditoria, você deve treinar o Gemini (seja nas instruções globais, seja no prompt que você cola) para que ele nunca seja superficial.

Aqui estão **5 Sugestões de Ouro** para você injetar nas instruções do seu Analista Gemini (no link fornecido) e melhorar imediatamente a qualidade das análises:

## 1. Exigir Raciocínio Explícito (Cadeia de Pensamento)
Em vez de pedir apenas que a IA preencha um modelo, ordene que ela **explique por que** está tomando uma decisão antes de gerar o resultado final.
* **Sugestão de Comando para a IA:** *"Antes de emitir o parecer, faça um raciocínio lógico em tópicos. Justifique cada infração ou taxa fora da norma com base nas Leis (ex: LC 267/2019 ou Lei 1.544/86). Se um índice estiver correto, declare explicitamente 'O índice X atende à norma Y'."*

## 2. Aprofundamento no "Considerando" (Modo Motor)
Os "Considerandos" costumam ser genéricos. Eles devem contar a história do processo.
* **Sugestão de Comando para a IA:** *"Sempre gere no mínimo 3 'Considerandos'. O primeiro deve referenciar o pedido inicial e a documentação apresentada; o segundo deve analisar o contexto urbanístico e a lei pertinente; e o terceiro deve focar na divergência (se houver) ou na conformidade do projeto em relação à legislação atual."*

## 3. Checklist Obrigatório de Componentes
O parecer nunca deve esquecer elementos básicos. Force a IA a fazer um "checklist mental".
* **Sugestão de Comando para a IA:** *"Seu parecer DEVE conter, obrigatoriamente: 
  1) Análise da Taxa de Ocupação e Permeabilidade (com números comparados aos limites legais).
  2) Situação da ART/RRT e do responsável técnico.
  3) Verificação de Decadência Tributária (se a obra for antiga).
  4) Existência de CNO/CEI. 
  Caso alguma informação falte nos dados extraídos, escreva expressamente no parecer: 'Ausência de informação sobre X, requer diligência'."*

## 4. Padronização Severa de Linguagem (Anti-Amadorismo)
IAs costumam usar palavras como "Infelizmente", "Eu acho", ou "Notei que".
* **Sugestão de Comando para a IA:** *"Aja como um Auditor Técnico da SMOSU. Use estritamente linguagem impessoal, técnica e administrativa em 3ª pessoa. NUNCA use saudações. Utilize termos como 'Constata-se', 'Verifica-se divergência', 'Em atenção ao exposto', 'Diante das prerrogativas legais'. Seja assertivo."*

## 5. Criação da Seção "Medidas Saneadoras" (O que fazer agora?)
Um parecer excelente não apenas aponta o erro, mas diz exatamente o que o requerente ou o setor deve fazer para arrumar.
* **Sugestão de Comando para a IA:** *"No final da sua análise ou despacho (especialmente no Modo Livre), inclua uma seção chamada 'Medidas Saneadoras' ou 'Encaminhamentos'. Liste em formato de 'bullet points' (tópicos) exatamente quais documentos o contribuinte deve anexar ou qual setor deve ser acionado (ex: Fiscalização, Tributação) para dar prosseguimento."*

## 6. Análise Temporal Obrigatória — Linha do Tempo como Estrutura do Parecer

Os considerandos mais fracos são aqueles que enumeram fatos sem sequência lógica. Os mais fortes narram o processo como uma história cronológica: o que existia antes, o que foi requerido, o que foi vistoriado, e qual é a situação atual.

* **Sugestão de Comando para a IA:** *"Antes de redigir qualquer considerando, monte mentalmente a linha do tempo completa do processo — do evento mais antigo (matrícula original, habite-se histórico, planta cadastral antiga, alvará anterior) ao mais recente (vistoria fiscal, quitação de DAMs, data atual). Os considerandos devem seguir esta ordem cronológica e cada fato relevante deve citar sua data e documento de origem."*

* **Campos novos obrigatórios no JSON (pareceres técnicos):**
  * **`historico_cronologico`** — array de eventos datados e ordenados, cada um com `data`, `evento`, `tipo` e `referencia`. O compilador Python gera automaticamente a tabela "HISTÓRICO CRONOLÓGICO DO PROCESSO" no documento Word.
  * **`partes_envolvidas`** — objeto estruturado com requerente (e sua qualidade: proprietário, procurador, comprador), responsável técnico (conselho + tipo de RT + número simplificado), fiscais vistoriadores (nome + matrícula funcional) e signatário do parecer. O compilador gera a tabela "PARTES E RESPONSÁVEIS DO PROCESSO".

* **Por que isso importa:** O documento final deve fazer sentido histórico. Um auditor externo lendo o parecer precisa entender o imóvel desde sua origem — o que foi licenciado, o que foi construído sem licença, o que foi comprovado por decadência, e como chegamos à situação atual. Sem a linha do tempo, o parecer é tecnicamente correto mas narrativamente vazio.

---

### Como aplicar isso hoje?
Abra o seu Analista Gemini no link: [https://gemini.google.com/gem/c0f3480899a2](https://gemini.google.com/gem/c0f3480899a2)

Vá nas **Instruções** dele e adicione um parágrafo como este:

> *"Você é um Auditor da SMOSU. Sempre que analisar um processo, exija completude. Sempre mencione os índices urbanísticos com base nas leis 1.544/86 e LC 267/2019. Crie 'Considerandos' ricos que contem a história documental do processo. Não deixe escapar nenhuma inconsistência de RRT ou CEI. Sempre conclua apontando exatamente os próximos passos ou pendências documentais."*
