# Coding Conventions

**Analysis Date:** 2026-05-01

## Naming Patterns

**Files:**
- snake_case.py (ex: `compilador.py`, `calculadora_indices.py`)

**Functions:**
- snake_case (ex: `_relatorio_prevoo`, `gerar_documento`)
- Funções internas/auxiliares frequentemente prefixadas com underscore `_`.

**Variables:**
- snake_case (ex: `tipo_relatorio`, `dados_processo`)
- Constantes em SCREAMING_SNAKE_CASE (especialmente em `config.py`).

**Types:**
- Tipagem Python 3.9+ (ex: `dict`, `list`, `tuple[bool, dict]`).

## Code Style

**Formatting:**
- Indentação de 4 espaços.
- Alinhamento vertical de atribuições em blocos (ex: em `config.py` e definições de variáveis em `compilador.py`).

**Linting:**
- Não detectado arquivo de configuração formal (ex: `.flake8` ou `pyproject.toml`), mas segue estilo PEP8 consistente.

## Import Organization

**Order:**
1. Standard Library imports (`sys`, `os`, `json`).
2. Local path adjustments (`sys.path.insert`).
3. Internal module imports (`from config import ...`).
4. Logic/Validation modules (`import calculadora_indices as calc_idx`).

**Path Aliases:**
- Uso frequente de aliases curtos para módulos internos (`calc_idx`, `alerta_dec`, `consist`).

## Error Handling

**Patterns:**
- Validação "Pre-Flight": O sistema executa uma bateria de testes antes de iniciar a geração.
- Uso de blocos `try-except` no orquestrador para capturar falhas nos geradores.
- Retorno de tuplas `(sucesso, dados)` para propagação de status.

## Logging

**Framework:** Custom logger (`_Sistema_Interno/01_Motor_Python/logger.py`)

**Patterns:**
- Uso de funções curtas prefixadas com underscore para logs coloridos: `_ok()`, `_warn()`, `_err()`, `_info()`.
- Logs persistentes no arquivo `motor.log`.

## Comments

**When to Comment:**
- Cabeçalhos de arquivos descrevendo o propósito.
- Docstrings em funções complexas.
- Divisores de seção visuais usando caracteres Unicode (ex: `── ... ──`).

**JSDoc/TSDoc:**
- Docstrings Python padrão (`""" ... """`).

## Function Design

**Size:** Funções variam de utilitários pequenos a orquestradores médios (30-50 linhas).

**Parameters:** Passagem de grandes dicionários de dados (`dados: dict`) é o padrão para evitar listas longas de argumentos.

**Return Values:** Frequentemente retorna tuplas para indicar status e dados resultantes.

---

*Convention analysis: 2026-05-01*
