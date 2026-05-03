<!-- refreshed: 2026-05-01 -->
# Architecture

**Analysis Date:** 2026-05-01

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                      Interface de Usuário                   │
│         `GERAR_DOCUMENTOS.bat` / CLI python                 │
└──────────────────┬──────────────────┬───────────────────────┘
                   │                  │
                   ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    Orquestrador Central                     │
│               `_Sistema_Interno/01_Motor_Python/compilador.py`│
└────────┬──────────────────┬──────────────────┬──────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   Validadores    │ │   Processadores  │ │    Geradores     │
│ `consistencia.py`│ │ `calculadora.py` │ │ `geradores/*.py` │
│ `inspetor.py`    │ │ `alertas.py`      │ │ `componentes.py` │
└────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                  │                     │
         ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                Camada de Persistência e Saída               │
│         `0_Modelos_Prontos/` (Entrada de Template)          │
│         `2_Documentos_Prontos/` (Saída DOCX)                │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| Orquestrador | Gerenciamento do fluxo de vida do processo e despacho | `_Sistema_Interno/01_Motor_Python/compilador.py` |
| Configurações | Centralização de paths, estilos e mapeamentos | `_Sistema_Interno/01_Motor_Python/config.py` |
| Calculadora | Cálculos de índices urbanísticos e áreas | `_Sistema_Interno/01_Motor_Python/calculadora_indices.py` |
| Inspetor | Verificação de conformidade documental | `_Sistema_Interno/01_Motor_Python/inspetor_documental.py` |
| Geradores | Lógica específica de preenchimento de templates | `_Sistema_Interno/01_Motor_Python/geradores/` |
| Visualizador | Geração de preview HTML antes da finalização | `_Sistema_Interno/01_Motor_Python/preview_html.py` |

## Pattern Overview

**Overall:** Orchestrator-Worker (Dispatcher)

**Key Characteristics:**
- **Decoupling**: The main engine doesn't know the specifics of each document type; it delegates to generators.
- **Centralized Config**: All environment-dependent data (paths) is in one file.
- **Validation First**: Documents are only generated if the data passes consistency checks.

## Layers

**Input Layer:**
- Purpose: Entry point for user data.
- Location: `1_Colar_JSON_Aqui/`
- Contains: JSON files.
- Depends on: None.
- Used by: Orchestrator.

**Logic Layer:**
- Purpose: Analysis and validation.
- Location: `_Sistema_Interno/01_Motor_Python/`
- Contains: Validation and calculation modules.
- Depends on: `config.py`.
- Used by: Orchestrator.

**Generation Layer:**
- Purpose: Template filling and Word export.
- Location: `_Sistema_Interno/01_Motor_Python/geradores/`
- Contains: Generator classes/functions.
- Depends on: `python-docx`.
- Used by: Orchestrator.

## Data Flow

### Primary Request Path (DOCX Generation)

1. **Entry**: User runs `GERAR_DOCUMENTOS.bat` or `python compilador.py`.
2. **Scan**: `compilador.py` scans `1_Colar_JSON_Aqui/` for JSON files.
3. **Validate**: Each JSON is passed through `consistencia.py` and `inspetor_documental.py`.
4. **Calculate**: `calculadora_indices.py` computes totals and indices.
5. **Preview**: `preview_html.py` generates an HTML view.
6. **Generate**: If approved, the corresponding generator in `geradores/` is called.
7. **Output**: Result is saved to `2_Documentos_Prontos/`.

**State Management:**
- State is stateless per run; information is passed via dictionaries/JSON between modules.

## Architectural Constraints

- **Threading**: Single-threaded (Synchronous processing).
- **Global state**: Avoided; most modules use function calls. `config.py` acts as a global immutable (mostly) state for settings.
- **Circular imports**: Handled by separating logic from orchestration.

## Anti-Patterns

### Hardcoded Paths (Mitigated)

**What happens**: Previously, paths were hardcoded to specific user directories.
**Why it's wrong**: Broken portability.
**Do this instead**: Use `config.py` with relative path resolution (`os.path.abspath(__file__)`).

## Error Handling

**Strategy**: Stop-on-error for validation, logging for execution.

**Patterns**:
- Try-Except blocks in `compilador.py` catching generator exceptions.
- Logging via `logger.py` to `motor.log`.

---

*Architecture analysis: 2026-05-01*
