# Testing Patterns

**Analysis Date:** 2026-05-01

## Test Framework

**Runner:**
- Custom test runner: `run_tests.py`

**Assertion Library:**
- Built-in conditional checks (no formal framework like `pytest` or `unittest` yet, but plans for expansion).

**Run Commands:**
```bash
python _Sistema_Interno/01_Motor_Python/run_tests.py           # Run all tests
python _Sistema_Interno/01_Motor_Python/run_tests.py --limpar  # Run and clean outputs
python _Sistema_Interno/01_Motor_Python/run_tests.py --motor   # Structured motor only
python _Sistema_Interno/01_Motor_Python/run_tests.py --livre   # Free mode only
```

## Test File Organization

**Location:**
- Test data: `_Sistema_Interno/01_Motor_Python/json/`
- Test outputs: `_Sistema_Interno/01_Motor_Python/json/_output_testes/`

**Naming:**
- `TESTE-[NOME].json`: Structured tests.
- `TESTE-LIVRE-[NOME].json`: Free mode tests.
- `TESTE-INVALIDO-[NOME].json`: Negative tests (schema validation expected to fail).

## Test Structure

**Suite Organization:**
O `run_tests.py` descobre arquivos JSON por globbing e executa em loops baseados no prefixo do arquivo.

```python
def _rodar_suite(titulo, arquivos, fn_teste):
    # Loop over files
    for caminho in arquivos:
        passou, msg, t = fn_teste(caminho)
        # Log result
```

**Patterns:**
- **Setup**: `os.makedirs(OUTPUT_DIR, exist_ok=True)`
- **Execution**: Chama a função `gerar()` do motor ou `gerar_livre()`.
- **Teardown**: Remoção opcional da pasta de saída via flag `--limpar`.
- **Assertion**: Verifica existência do arquivo de saída, tamanho em KB e ausência de exceções.

## Mocking

**Framework:** None.

**What to Mock:**
- Não há mocking de IO ou bibliotecas externas. Os testes são de integração real (End-to-End para o motor).

**What NOT to Mock:**
- `python-docx` e `os.path` são usados diretamente para garantir que o documento final seja legível pelo Word.

## Fixtures and Factories

**Test Data:**
Arquivos JSON estáticos em `_Sistema_Interno/01_Motor_Python/json/`. Representam casos reais de uso (Alvarás, Certidões, etc.).

## Coverage

**Requirements:** None enforced.

**View Coverage:**
- Manual verification of generated files in `_output_testes/`.

## Test Types

**Unit Tests:**
- Validação de Schema (via `schema_validator.validar`).

**Integration Tests:**
- Fluxo completo do JSON até o DOCX final.

**E2E Tests:**
- `run_tests.py` cobre o fluxo completo do ponto de vista do motor.

## Common Patterns

**Async Testing:**
- N/A (System is synchronous).

**Error Testing:**
- Arquivos `TESTE-INVALIDO-*.json` verificam se o sistema rejeita corretamente dados malformados ou incompletos.

---

*Testing analysis: 2026-05-01*
