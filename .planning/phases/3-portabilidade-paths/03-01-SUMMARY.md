---
plan: 03-01
phase: 3-portabilidade-paths
status: complete
completed: 2026-05-01
commits: 3f7d772, dccc0d0, 1815c2d, 1917b72
---

# Summary: 03-01 — Centralizar Constantes de Pasta

## O que foi feito

Centralização completa dos nomes das 4 pastas do projeto em `config.py` como fonte única de verdade. Antes, strings como `"1_Colar_JSON_Aqui"` e `"2_Documentos_Prontos"` apareciam duplicadas em 8+ arquivos.

**Task 1 — config.py:** Adicionadas 5 constantes na seção CAMINHOS:
- `PROJECT_ROOT` — pasta raiz `02. Pareceres/`
- `PASTA_ENTRADA` — `1_Colar_JSON_Aqui/`
- `PASTA_SAIDA` — `2_Documentos_Prontos/`
- `PASTA_MODELOS` — `0_Modelos_Prontos/`
- `PASTA_TREINO` — `3_Treinar_Inteligencia/`

**Task 2 — compilador.py:** Import de `PASTA_ENTRADA` adicionado; linha de path hardcoded substituída. Comentário atualizado.

**Task 3 — geradores/__init__.py:** `PASTA_SAIDA` e `PASTA_MODELOS` importados de config; variável local `root_dir` removida.

**Task 4 — 9 módulos restantes:**
- `analisador_pdf.py` — já usava config; docstring atualizada
- `extrator_pdf.py` — adicionados `PASTA_MODELOS`, `PASTA_TREINO`; 6 strings literais em texto de instrução substituídas por `os.path.basename(PASTA_*)`
- `modo_pdf.py` — `PROJECT_ROOT` local removido; importa `PASTA_ENTRADA` de config
- `painel_gem.py` — 3 strings no banner do terminal substituídas por `os.path.basename(PASTA_*)`
- `compilador_livre.py` — `PASTA_ENTRADA` e `PASTA_SAIDA` importados; 2 construções de path e 1 print corrigidos
- `preview_html.py` — bloco `__main__` reescrito para importar `PASTA_ENTRADA` de config
- `refinador.py` — `PROJECT_ROOT` e `PASTA_ENTRADA` locais removidos; importa de config
- `schema_validator.py` — docstring de uso atualizada
- `compilador.py` — comentário atualizado

## Verificação

- `py_compile`: OK em todos os 10 arquivos modificados
- `python -c "from config import PASTA_ENTRADA, PASTA_SAIDA, PASTA_MODELOS, PASTA_TREINO; print('OK')"`: OK
- `run_tests.py --motor`: **5/5 testes passaram** (erros de PDF via Word COM são pré-existentes e não relacionados)
- `grep` para strings literais de pasta (excluindo config.py): **zero resultados**

## Self-Check: PASSED

## key-files.created
- (nenhum arquivo novo — refatoração pura)

## key-files.modified
- `_Sistema_Interno/01_Motor_Python/config.py`
- `_Sistema_Interno/01_Motor_Python/compilador.py`
- `_Sistema_Interno/01_Motor_Python/geradores/__init__.py`
- `_Sistema_Interno/01_Motor_Python/analisador_pdf.py`
- `_Sistema_Interno/01_Motor_Python/extrator_pdf.py`
- `_Sistema_Interno/01_Motor_Python/modo_pdf.py`
- `_Sistema_Interno/01_Motor_Python/painel_gem.py`
- `_Sistema_Interno/01_Motor_Python/compilador_livre.py`
- `_Sistema_Interno/01_Motor_Python/preview_html.py`
- `_Sistema_Interno/01_Motor_Python/refinador.py`
- `_Sistema_Interno/01_Motor_Python/schema_validator.py`

## Desvios

**Escopo expandido:** `schema_validator.py` e `analisador_pdf.py` não estavam na lista original do Task 4, mas tinham strings literais que seriam capturadas pela verificação grep. Incluídos para garantir que a acceptance criteria (zero resultados) fosse cumprida.

**Strings em texto de instrução ao usuário:** Para arquivos como `extrator_pdf.py` e `painel_gem.py`, as strings de pasta estavam em texto exibido ao usuário (banner, instruções). Foram substituídas usando `os.path.basename(PASTA_*)` para manter o comportamento dinâmico correto caso as pastas sejam renomeadas.
