# Testing Patterns

**Analysis Date:** 2026-05-06 (atualizado pós-Milestone v3.0)

## Test Framework

**Runner:**
- Custom test runner: `Sistema/motor/scripts/run_tests.py`
- Golden Dataset: `Sistema/motor/tests/golden_dataset/`
- Validador de Fidelidade: `Sistema/motor/scripts/validador_fidelidade.py`

**Assertion Library:**
- Checks condicionais built-in + validação de existência/tamanho de arquivos.
- MCP-SMOSU usa assertions próprias em `test_tools.py`.

**Run Commands:**
```bash
# A partir da raiz do projeto
python Sistema/motor/scripts/run_tests.py           # Todos os testes
python Sistema/motor/scripts/run_tests.py --limpar   # Testes + limpar outputs
python Sistema/motor/scripts/run_tests.py --motor    # Apenas motor estruturado
python Sistema/motor/scripts/run_tests.py --livre    # Apenas modo livre

# Validação de fidelidade (Golden Dataset)
python Sistema/motor/scripts/validador_fidelidade.py

# Testes do MCP-SMOSU
cd Sistema/mcp-smosu
python test_tools.py
```

## Test File Organization

**Location:**
- Test data: `Sistema/motor/json/` (matriz documental)
- Test outputs: `Sistema/motor/json/_output_testes/`
- Golden Dataset: `Sistema/motor/tests/golden_dataset/` (3 casos padrão-ouro)
- MCP tests: `Sistema/mcp-smosu/test_*.py`

**Naming:**
- `TESTE-[NOME].json`: Testes estruturados (motor).
- `TESTE-LIVRE-[NOME].json`: Testes em modo livre.
- `TESTE-INVALIDO-[NOME].json`: Testes negativos (rejeição esperada).

## Test Types

| Tipo | Cobertura | Ferramenta |
|------|-----------|------------|
| E2E (Motor) | JSON → DOCX completo | `run_tests.py` |
| Fidelidade | JSON ↔ DOCX (campos críticos) | `validador_fidelidade.py` |
| Dessincronização | Template ↔ Gerador | `template_checker.py` |
| MCP Tools | Ferramentas individuais | `test_tools.py` |
| Schema | Validação de tipos JSON | `schema_validator.py` |

## Common Patterns

**E2E Test Flow:**
1. Setup: `os.makedirs(OUTPUT_DIR, exist_ok=True)`
2. Execution: `gerar(dados)` — chama o pipeline completo
3. Assertion: Arquivo existe, tamanho > 0, sem exceções
4. Teardown: Remoção opcional via `--limpar`

**Golden Dataset Flow:**
1. Gerar DOCX a partir dos 3 JSONs padrão-ouro
2. Extrair texto do DOCX gerado
3. Verificar presença de campos críticos (número do processo, requerente, conclusão)
4. Score de fidelidade: 100% = todos os campos encontrados

---

*Testing analysis: 2026-05-06 (pós-Milestone v3.0)*
