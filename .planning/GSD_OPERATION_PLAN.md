# Manual de Operação GSD (Get Shit Done)
*Como extrair o poder máximo dos agentes e skills do ecossistema.*

O GSD não é apenas um "gerador de código". É uma **metodologia de engenharia assíncrona baseada em agentes**. Ele divide o trabalho complexo em agentes especialistas (Planejadores, Executores, Revisores e Auditores) para que você possa focar na estratégia enquanto a Inteligência Artificial trabalha na esteira de produção.

Abaixo estão os recursos organizados e o **Plano Operacional** de como você deve comandar o projeto daqui para frente.

---

## 🛠️ O Arsenal GSD (O que os Agentes fazem)

### 1. 🧠 Agentes de Inteligência & Ideação (Brainstorming)
Antes de escrever código, precisamos saber *o que* e *como* construir.
- **`gsd-explore`**: Roteamento Socrático. Você joga uma ideia ("Quero fazer um novo layout administrativo") e ele analisa a viabilidade, levanta riscos e propõe caminhos.
- **`gsd-spec-phase`**: Tira a ambiguidade. Ele cria um documento `SPEC.md` ou `AI-SPEC.md` forçando clareza matemática no que será entregue.
- **`gsd-spike`**: Modo laboratório. Ele constrói um "protótipo descartável" (Spike) só para testar se uma ideia técnica maluca realmente funciona antes de incorporarmos ao projeto.

### 2. 🏗️ Agentes de Arquitetura & Planejamento
- **`gsd-plan-phase`**: O arquiteto. Lê as especificações e escreve o `PLAN.md` detalhado (Passo 1, Passo 2, Passo 3). Se o plano for falho, a execução vai falhar.
- **`gsd-map-codebase` & `gsd-graphify`**: Agentes cartógrafos. Eles leem seu repositório inteiro e geram mapas de dependência para a IA não se perder em projetos gigantes.

### 3. ⚙️ Agentes Operários (Execução Bruta)
- **`gsd-execute-phase`**: O batalhão. Ele pega o plano e despacha sub-agentes paralelos (*Wave-based parallelization*) para escrever o código de múltiplos arquivos ao mesmo tempo.
- **`gsd-quick` / `gsd-fast`**: Para tarefas triviais (ex: "corrija a margem da tabela"). Eles pulam a burocracia do planejamento e escrevem o código na hora.
- **`gsd-autonomous`**: O modo "Piloto Automático". Ele junta Planejamento + Execução + Validação de ponta a ponta sem pedir sua permissão no meio do caminho.

### 4. 🛡️ Agentes Inspetores (Qualidade e Segurança)
- **`gsd-code-review`**: Analisa o código que o operário acabou de escrever procurando bugs, vulnerabilidades e código sujo (Débito Técnico).
- **`gsd-audit-fix`**: Um agente autônomo que caça problemas sozinho, escreve a correção, testa para ver se funcionou e já faz o commit no Git.
- **`gsd-verify-work` / `gsd-audit-uat`**: Ajuda você a fazer o UAT (Teste de Aceite). Ele simula o ambiente para garantir que a funcionalidade cumpre o que o humano pediu.

### 5. 📚 Agentes Bibliotecários (Conhecimento)
- **`gsd-extract-learnings`**: Lê o que deu errado na fase, extrai as "lições aprendidas" e salva no cérebro do projeto para a IA não cometer o mesmo erro no futuro.
- **`gsd-health`**: O médico do projeto. Escaneia se algum documento obrigatório do GSD está corrompido ou faltando.

---

## 🗺️ PLANO DE OPERAÇÃO (Como vamos trabalhar)

Para fazer o seu sistema alcançar o "Outro Nível", nós vamos parar de agir de forma improvisada e passar a agir como uma linha de montagem industrial. Sempre que você quiser criar uma nova peça (ex: Múltiplas Certidões da Fase 14), usaremos o seguinte ciclo:

### Passo 1: O Direcionamento (Você)
Você invoca: `/gsd-explore "Precisamos que o motor emita uma certidão de localização isolada e uma de confrontação a partir do mesmo processo."`
*Resultado*: A IA ajuda a clarear a ideia, propõe soluções e não escreve uma linha de código.

### Passo 2: O Contrato (Agente Arquiteto)
Acionamos o `/gsd-spec-phase` seguido do `/gsd-plan-phase`.
*Resultado*: O agente cria um contrato (Especificação) e um checklist de passos técnicos. Você lê o plano e diz "Aprovado".

### Passo 3: A Fabriqueta (Agentes Operários)
Acionamos o `/gsd-execute-phase`.
*Resultado*: Múltiplos agentes vão abrir as pastas, modificar os Python e JSONs e construir a funcionalidade de forma isolada e segura, em "ondas" (waves).

### Passo 4: A Malha Fina (Agentes Inspetores)
Acionamos o `/gsd-code-review` e `/gsd-verify-work`.
*Resultado*: O código passa pelo crivo de segurança e validamos se o DOCX gerado está de acordo com as regras da PMO (Prefeitura de Oliveira).

### Passo 5: A Imortalização (Agente Bibliotecário)
Acionamos o `/gsd-extract-learnings`.
*Resultado*: O sistema aprende as peculiaridades das leis de Oliveira/MG, salva o contexto e ficamos mais inteligentes para a próxima fase.

---
**Resumo da Ópera**: Você será o Diretor (apontando as regras de engenharia/negócio da prefeitura) e os Agentes GSD serão sua Fábrica de Software. Quando quiser algo, diga "Vamos usar a esteira GSD para fazer X".
