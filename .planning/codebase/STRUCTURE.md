# Codebase Structure

**Analysis Date:** 2026-05-01

## Directory Layout

```text
[project-root]/
├── 0_Modelos_Prontos/       # Modelos Word (.docx) com placeholders
├── 1_Colar_JSON_Aqui/       # Pasta de entrada para arquivos JSON
├── 2_Documentos_Prontos/    # Pasta de saída para documentos gerados
├── 3_Treinar_Inteligencia/   # Instruções e contextos para IA (GSD2)
├── _Sistema_Interno/
│   ├── 01_Motor_Python/     # Núcleo do motor de geração
│   │   ├── geradores/       # Lógica específica por tipo de documento
│   │   ├── logos/           # Imagens institucionais para o cabeçalho
│   │   └── templates/       # Templates HTML para preview
│   └── 03_Retroalimentacao/ # Base de conhecimento e histórico
├── .gemini/
│   └── plans/               # Planejamento GSD2 (Roadmap, States, Phases)
└── GERAR_DOCUMENTOS.bat     # Atalho para execução pelo usuário
```

## Directory Purposes

**_Sistema_Interno/01_Motor_Python/:**
- Purpose: Contém toda a lógica executável do sistema.
- Contains: Scripts Python, arquivos de configuração e utilitários.
- Key files: `compilador.py`, `config.py`, `logger.py`.

**0_Modelos_Prontos/:**
- Purpose: Repositório de templates oficiais em formato Word.
- Contains: Arquivos `.docx` que servem de base para a geração.

**1_Colar_JSON_Aqui/:**
- Purpose: Interface de entrada de dados para o usuário.
- Contains: Arquivos JSON exportados pelo agente de triagem ou preenchidos manualmente.

**.gemini/plans/:**
- Purpose: Governança do projeto seguindo a metodologia GSD2.
- Contains: Documentos de arquitetura, roadmaps e histórico de fases.

## Key File Locations

**Entry Points:**
- `_Sistema_Interno/01_Motor_Python/compilador.py`: Ponto de entrada principal do motor.
- `GERAR_DOCUMENTOS.bat`: Interface simplificada para o usuário final.

**Configuration:**
- `_Sistema_Interno/01_Motor_Python/config.py`: Definições globais de caminhos, estilos e tipos.

**Core Logic:**
- `_Sistema_Interno/01_Motor_Python/calculadora_indices.py`: Lógica matemática urbana.
- `_Sistema_Interno/01_Motor_Python/geradores/`: Implementações de preenchimento.

**Testing:**
- `_Sistema_Interno/01_Motor_Python/run_tests.py`: Suite de testes automatizados.

## Naming Conventions

**Files:**
- Python: `snake_case.py` (ex: `analisador_pdf.py`)
- JSON: `PROCESSO_ANO.json` ou `NOME.json`

**Directories:**
- Prefixo numérico para ordem de importância/fluxo: `0_...`, `1_...`.

## Where to Add New Code

**New Document Type:**
1. Adicionar template `.docx` em `0_Modelos_Prontos/`.
2. Mapear o tipo em `config.py` (`TIPOS_DOCUMENTO`).
3. Se necessário, criar/ajustar gerador em `geradores/`.

**New Business Rule:**
- Criar novo módulo em `_Sistema_Interno/01_Motor_Python/` e importar no `compilador.py`.

**Utilities:**
- Adicionar em `_Sistema_Interno/01_Motor_Python/componentes.py` se for relacionado a Word ou em novo arquivo utilitário.

## Special Directories

**.gemini/:**
- Purpose: Metadados e planos do projeto.
- Committed: Sim.

---

*Structure analysis: 2026-05-01*
