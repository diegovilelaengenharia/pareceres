# Plano de Atualização: Wizard e Inteligência GEM v3.0

## 1. Objetivo
Tornar o Sistema Interativo (GEM Gemini) mais inteligente e capaz de produzir pareceres técnicos mais completos e bem fundamentados. O sistema adotará uma abordagem de "Contexto Dinâmico + Análise de Mérito" e oferecerá "Revisão Interativa", permitindo ajustes finos sem perder a finalidade central e o rigor técnico.

## 2. Fase 1: Atualização do Wizard (Painel UI)
A interface web (`painel_gem.html` e `painel_gem.py`) será expandida para coletar e apresentar informações mais ricas:
- **Campo de Contexto Extra:** Adição de uma área de texto "Observações do Engenheiro" onde o usuário poderá inserir diretrizes manuais e apontamentos específicos que a IA deve considerar.
- **Checklists de Foco Especial:** Adição de opções selecionáveis (ex: "Avaliar Acessibilidade", "Avaliar Impacto de Vizinhança", "Analisar Mitigações de Risco") que modificarão o prompt dinamicamente.
- **Tela de Revisão Interativa:** Antes de consolidar o DOCX/PDF, o Wizard exibirá o "Raciocínio da IA" (Chain of Thought) e a prévia estruturada do texto gerado. O engenheiro terá um botão/campo para pedir pequenos ajustes ("Refine o considerando X", "Adicione a lei Y") diretamente nessa tela.

## 3. Fase 2: Expansão da Inteligência (Knowledge & Prompts)
A base de conhecimento (`Sistema/inteligencia/Knowledge/`) e os prompts do motor serão atualizados para produzir pareceres robustos:
- **Análise de Mérito Técnico:** Atualização em `00_SISTEMA_INTERATIVO.md` e nos prompts base para que a IA não apenas cite a lei, mas gere um parágrafo (ou seção) de "Análise de Mérito", explicando detalhadamente o *porquê* da conformidade ou irregularidade do projeto.
- **Integração do Contexto:** A IA passará a consumir as "Observações do Engenheiro" fornecidas no Wizard, incorporando-as organicamente na redação final (ao invés de apenas anexá-las como notas).
- **Gabaritos Aprimorados:** Atualização do `02_GABARITOS_E_ESTILO.md` para contemplar estruturas de texto que incluam mitigações de risco e recomendações técnicas, elevando a qualidade do documento final sem torná-lo prolixo.

## 4. Fase 3: Integração e Testes
- Conectar o novo fluxo de revisão do UI ao motor (`Sistema/motor/core/base_engine.py` e `painel_gem.py`), mantendo a estabilidade das operações em lote.
- Realizar testes com processos modelo que exijam "Contexto Extra" para verificar se a IA responde adequadamente e se a "Análise de Mérito" aparece com precisão no documento final.

## 5. Critérios de Sucesso
1. O Wizard coleta com sucesso observações manuais e passa para o modelo LLM.
2. O usuário consegue revisar a prévia da resposta da IA e solicitar um re-processamento de ajuste fino na interface antes de salvar.
3. Os pareceres gerados contêm explicações mais profundas ("Análise de Mérito") e incorporam as diretrizes extras de forma idiomática e técnica.