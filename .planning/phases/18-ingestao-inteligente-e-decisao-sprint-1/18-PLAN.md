---
phase: 18
wave: 1
autonomous: false
files_modified:
  - Sistema/motor/analyzers/pdf_classifier.py
  - Sistema/motor/analyzers/decision_tree.py
  - Sistema/motor/generators/compilador.py
  - Sistema/motor/config.py
---

# Phase 18: Ingestão Inteligente e Decisão (Sprint 1)

## Objetivo
Implementar o classificador multimodal de PDFs (P1-A) para triagem inicial e a árvore de decisão automatizada (P3-A) para sugerir recomendações nos 5 processos mais comuns.

## Tarefas

<task type="execute">
<action>
Criar o módulo `Sistema/motor/analyzers/pdf_classifier.py`.
Implementar a classe `PDFClassifier` que utilize a SDK do Gemini para ler o arquivo PDF de entrada.
- Deve possuir um método `classify_pdf(pdf_path: str) -> dict`.
- O dict retornado deve conter a chave `tipo_processo` com valores limitados aos tipos conhecidos no `config.TIPOS_DOCUMENTO`.
- Deve usar o modo multimodal (System Instruction + `upload_file` ou passagem por bytes, dependendo da configuração Gemini do projeto).
- Tratar exceções de leitura ou falha de inferência com fallback para um tipo "desconhecido" ou solicitando intervenção.
</action>
<read_first>
- Sistema/motor/generators/enricher.py (para entender como o Gemini já é invocado)
- Sistema/motor/config.py (para listar as opções de tipos_documento que a IA pode retornar)
</read_first>
<acceptance_criteria>
- `pdf_classifier.py` contém a classe `PDFClassifier` com o método `classify_pdf`.
- O método é capaz de receber o caminho de um arquivo PDF e retornar o tipo correspondente mapeado.
</acceptance_criteria>
</task>

<task type="execute">
<action>
Criar o módulo `Sistema/motor/analyzers/decision_tree.py`.
Implementar um motor de regras de negócio `DecisionTree` com um método `evaluate(dados_extraidos: dict, tipo_processo: str) -> dict`.
- O motor deve focar nos 5 tipos: "alvara_aprovacao", "habitese_comum", "certidao_localizacao", "comunicado_pendencia", "regularizacao".
- Implementar as regras lógicas estritas (ex: `TO` extraído > `TO` permitido = PENDÊNCIA).
- Como ainda não há banco SQLite (isso será no Sprint 2), a regra por hora deve apenas avaliar a consistência dos dados internos do JSON vs parâmetros globais (ex: verificar se falta algum documento obrigatório sinalizado nos dados).
- O retorno deve ser um dicionário que contém a recomendação: `{"recomendacao": "APROVADO", "motivo": "Todos os parâmetros dentro dos limites."}`.
</action>
<read_first>
- Sistema/BASE_CONHECIMENTO_GUIA.md (para ler os critérios dos documentos)
- Sistema/motor/config.py
</read_first>
<acceptance_criteria>
- `decision_tree.py` contém a função de avaliação.
- Ela processa as condições de 5 tipos de processos e retorna uma recomendação formal (APROVADO, PENDENCIA, INDEFERIDO) e um motivo associado.
</acceptance_criteria>
</task>

<task type="execute">
<action>
Atualizar `Sistema/motor/generators/compilador.py` para integrar o novo fluxo de ingestão no modo de pré-voo.
- Adicionar argumento opcional `--pdf` ou detecção se a entrada não for JSON.
- Se a entrada for um PDF, instanciar o `PDFClassifier` primeiro, extrair o tipo.
- Logo após extrair os dados e formar o JSON base, passar pela `DecisionTree.evaluate()` antes de chamar os geradores DOCX.
- Injetar o resultado da `DecisionTree` dentro dos dados interpolados no DOCX, especificamente na conclusão do parecer técnico, anexando a recomendação automática.
</action>
<read_first>
- Sistema/motor/generators/compilador.py
- Sistema/motor/geradores_core.py
</read_first>
<acceptance_criteria>
- `compilador.py` importa e chama `PDFClassifier` e `DecisionTree`.
- A geração do relatório `Preview HTML` exibe a recomendação sugerida pela árvore de decisão.
</acceptance_criteria>
</task>

## Verification
- Ao processar um PDF de alvará usando `compilador.py --pdf arquivo.pdf`, o sistema deve classificar corretamente, aplicar a árvore de decisão, injetar a recomendação e gerar o DOCX sem falhas.
