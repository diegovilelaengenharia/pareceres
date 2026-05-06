# Plano de Implementação: Novas Funções MCP SMOSU

## Objetivo
Adicionar 9 novas ferramentas ao servidor MCP `smosu-conhecimento` (7 originais do plano + 2 extras aprovadas), aprimorando a capacidade de cálculo, validação, extração de metadados e análise processual. Além de correções na base de conhecimento.

## Key Files & Context
- `Sistema/mcp-smosu/server.py`: Endpoint do servidor MCP.
- `Sistema/mcp-smosu/tools.py`: Lógica principal das ferramentas.
- `Sistema/base_conhecimento/checklist_documentos.json`: Novo arquivo de regras de documentação.
- `Sistema/base_conhecimento/raciocinio_parametros_e_multas.md`: Correção do URM.
- `Sistema/base_conhecimento/casos_treinamento.jsonl`: Criação de histórico de treinamento.

## Implementation Steps

### 1. Atualizar Base de Conhecimento
- Corrigir o URM 2026 para R$ 102,42 em `raciocinio_parametros_e_multas.md`.
- Criar `casos_treinamento.jsonl` com no mínimo 3 exemplos estruturados.
- Criar `checklist_documentos.json` com os requisitos bloqueantes, obrigatórios e condicionais (Aprovação, Regularização, Habite-se, Reforma).

### 2. Implementar Funções em `tools.py`
Adicionar as seguintes funções:
1. `calcular_multas_processo`: Cálculo de áreas para Art. 79 e Art. 39.
2. `validar_checklist_documentos`: Leitura de `checklist_documentos.json` e batimento de regras.
3. `analisar_decadencia`: Avaliação do CTN Art. 150 §4º (prazo > 5 anos x provas).
4. `gerar_memoria_calculo_indices`: Montar as equações matemáticas para compor o parecer.
5. `consultar_documentos_emitir`: Basear no `checklist_documentos.json` e diretrizes para emitir ofícios, certidões e alvarás adequados.
6. `verificar_excecoes_lote_pequeno`: Testar limite ≤220m² conforme Art 9º §13 LC 267.
7. `buscar_logradouro_oficial`: Procurar histórico de logradouros por nome nos arquivos txt/md.
8. `identificar_conflitos_processuais` (Novo): Analisar inconsistências entre SRI e Cadastro PMO, além de checar restrições de APP/Tombamento e inferir necessidades (ex: `Certidão de Localização Corretiva`, ofícios CODEMA/IEPHA).
9. `estruturar_historico_cronologico` (Novo): Organizar fatos passados em um array cronológico válido para o JSON (com os tipos de evento padrão: abertura_processo, vistoria_fiscal, etc).

### 3. Registrar Funções no Servidor
- Expor as 9 funções em `server.py` utilizando o decorador `@mcp.tool()` com descrições detalhadas.

### 4. Restart e Verificação
- Garantir que não haja quebras de sintaxe ou de tipagem no `tools.py` ou `server.py`.
- O servidor MCP precisa reiniciar e carregar as novas ferramentas corretamente.

## Verification & Testing
- Revisar a sintaxe dos arquivos Python (`python -m py_compile`).
- Garantir que as funções que precisam de `os.path` busquem seus JSONs locais corretamente.