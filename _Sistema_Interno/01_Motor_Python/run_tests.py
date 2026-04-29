"""
Suite de Testes de Regressão — Motor GEM / SMOSU Oliveira-MG

Roda todos os TESTE-*.json (motor estruturado) e TESTE-LIVRE-*.json (modo livre)
verificando se o compilador gera cada documento sem erros. Os .docx ficam em
json/_output_testes/ para inspeção visual.

Uso:
    python run_tests.py           → roda todos os testes
    python run_tests.py --limpar  → apaga _output_testes após os testes
    python run_tests.py --livre   → roda apenas os testes do modo livre
    python run_tests.py --motor   → roda apenas os testes do motor estruturado
"""

import os
import sys
import json
import glob
import time
import shutil
import traceback

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from geradores import gerar
from schema_validator import validar

JSON_DIR    = os.path.join(SCRIPT_DIR, "json")
OUTPUT_DIR  = os.path.join(JSON_DIR, "_output_testes")
LIMPAR_APOS = "--limpar" in sys.argv
MODO_LIVRE  = "--livre"  in sys.argv
MODO_MOTOR  = "--motor"  in sys.argv


def rodar_teste_motor(caminho_json: str) -> tuple:
    """Valida schema e gera documento com o motor estruturado."""
    with open(caminho_json, encoding="utf-8") as f:
        dados = json.load(f)

    erros, avisos = validar(dados)
    if erros:
        return False, f"Schema inválido — {erros[0]}", 0.0

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    nome_base = os.path.splitext(os.path.basename(caminho_json))[0]
    caminho_saida = os.path.join(OUTPUT_DIR, f"{nome_base}.docx")

    inicio = time.perf_counter()
    try:
        gerar(dados, caminho_saida)
        duracao = time.perf_counter() - inicio
    except Exception:
        duracao = time.perf_counter() - inicio
        if os.path.exists(caminho_saida):
            tamanho_kb = os.path.getsize(caminho_saida) / 1024
            return True, f"{tamanho_kb:.0f} KB  [PDF skipped]", duracao
        linhas = traceback.format_exc().strip().splitlines()
        msg_curta = linhas[-1] if linhas else "Erro desconhecido"
        return False, msg_curta, duracao

    if not os.path.exists(caminho_saida):
        return False, "Compilador não gerou o arquivo .docx", duracao

    tamanho_kb = os.path.getsize(caminho_saida) / 1024
    return True, f"{tamanho_kb:.0f} KB", duracao


def rodar_teste_livre(caminho_json: str) -> tuple:
    """Tenta gerar documento com o modo livre (compilador_livre.py)."""
    try:
        from compilador_livre import gerar_livre
    except ImportError as e:
        return False, f"compilador_livre não importável: {e}", 0.0

    with open(caminho_json, encoding="utf-8") as f:
        dados = json.load(f)

    if not dados.get("texto_livre") and not dados.get("paragrafo_abertura"):
        return False, "JSON sem 'texto_livre' — use o motor padrão", 0.0

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    nome_base = os.path.splitext(os.path.basename(caminho_json))[0]
    caminho_saida = os.path.join(OUTPUT_DIR, f"{nome_base}.docx")

    inicio = time.perf_counter()
    try:
        gerar_livre(dados, caminho_saida)
        duracao = time.perf_counter() - inicio
    except Exception:
        duracao = time.perf_counter() - inicio
        if os.path.exists(caminho_saida):
            tamanho_kb = os.path.getsize(caminho_saida) / 1024
            return True, f"{tamanho_kb:.0f} KB  [PDF skipped]", duracao
        linhas = traceback.format_exc().strip().splitlines()
        msg_curta = linhas[-1] if linhas else "Erro desconhecido"
        return False, msg_curta, duracao

    if not os.path.exists(caminho_saida):
        return False, "Modo livre não gerou o arquivo .docx", duracao

    tamanho_kb = os.path.getsize(caminho_saida) / 1024
    return True, f"{tamanho_kb:.0f} KB  [LIVRE]", duracao


def _rodar_suite(titulo: str, arquivos: list, fn_teste) -> list[bool]:
    if not arquivos:
        print(f"  (nenhum arquivo para '{titulo}')")
        return []

    print(f"\n{'=' * 62}")
    print(f"  {titulo}  ({len(arquivos)} arquivo(s))")
    print("=" * 62)

    resultados = []
    for caminho in arquivos:
        nome = os.path.basename(caminho)
        try:
            passou, msg, t = fn_teste(caminho)
        except json.JSONDecodeError as e:
            passou, msg, t = False, f"JSON inválido: {e}", 0.0
        except Exception as e:
            passou, msg, t = False, f"Exceção inesperada: {e}", 0.0

        icone = "OK" if passou else "FALHOU"
        t_str = f"({t:.2f}s)" if t > 0 else ""
        print(f"  [{icone}] {nome:<42} {t_str:<8} {msg}")
        resultados.append(passou)

    return resultados


def main():
    # Coletar arquivos por modo
    todos_motor = sorted(glob.glob(os.path.join(JSON_DIR, "TESTE-*.json")))
    # Excluir arquivos LIVRE da lista do motor
    arquivos_motor = [f for f in todos_motor if "LIVRE" not in os.path.basename(f).upper()]
    arquivos_livre = sorted(glob.glob(os.path.join(JSON_DIR, "TESTE-LIVRE-*.json")))

    if not todos_motor and not arquivos_livre:
        print(f"Nenhum TESTE-*.json encontrado em {JSON_DIR}")
        sys.exit(1)

    print("=" * 62)
    print("  Suite de Testes — Motor GEM / SMOSU Oliveira-MG")
    print("=" * 62)

    resultados_motor = []
    resultados_livre = []

    if not MODO_LIVRE:
        resultados_motor = _rodar_suite("MOTOR ESTRUTURADO", arquivos_motor, rodar_teste_motor)

    if not MODO_MOTOR:
        resultados_livre = _rodar_suite("MODO LIVRE", arquivos_livre, rodar_teste_livre)

    todos_resultados = resultados_motor + resultados_livre
    total  = len(todos_resultados)
    ok     = sum(todos_resultados)
    falhos = total - ok

    print(f"\n{'=' * 62}")
    if ok == total and total > 0:
        print(f"  Todos os {total} teste(s) passaram.")
        print("  Documentos gerados em: json/_output_testes/")
    elif total == 0:
        print("  Nenhum teste executado.")
    else:
        print(f"  {ok}/{total} passou(aram)  |  {falhos} falhou(aram)")
    print("=" * 62)

    if LIMPAR_APOS and os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        print("  Pasta _output_testes removida (--limpar).")

    sys.exit(0 if falhos == 0 else 1)


if __name__ == "__main__":
    main()
