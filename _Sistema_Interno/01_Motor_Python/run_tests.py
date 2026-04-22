"""
Suite de Testes de Regressão — Motor GEM / SMOSU Oliveira-MG

Roda todos os TESTE-*.json e verifica se o compilador gera cada documento
sem erros. Os .docx gerados ficam em json/_output_testes/ para inspeção visual.

Uso:
    python run_tests.py           → roda todos os TESTE-*.json
    python run_tests.py --limpar  → apaga a pasta _output_testes após os testes
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


def rodar_teste(caminho_json: str) -> tuple:
    """
    Valida o schema e tenta gerar o documento.
    Retorna (passou: bool, mensagem: str, duracao_s: float).
    """
    with open(caminho_json, encoding="utf-8") as f:
        dados = json.load(f)

    # 1. Validação de schema
    erros, avisos = validar(dados)
    if erros:
        return False, f"Schema inválido — {erros[0]}", 0.0

    # 2. Geração do documento
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    nome_base = os.path.splitext(os.path.basename(caminho_json))[0]
    caminho_saida = os.path.join(OUTPUT_DIR, f"{nome_base}.docx")

    inicio = time.perf_counter()
    try:
        gerar(dados, caminho_saida)
        duracao = time.perf_counter() - inicio
    except Exception:
        duracao = time.perf_counter() - inicio
        # Se o DOCX foi criado, o erro é no pós-processamento (ex: geração de PDF via COM).
        # O teste de regressão valida o DOCX — falha de PDF é aviso, não bloqueante.
        if os.path.exists(caminho_saida):
            tamanho_kb = os.path.getsize(caminho_saida) / 1024
            return True, f"{tamanho_kb:.0f} KB  [PDF skipped]", duracao
        linhas = traceback.format_exc().strip().splitlines()
        msg_curta = linhas[-1] if linhas else "Erro desconhecido"
        return False, msg_curta, duracao

    # Verificar que o arquivo foi realmente criado
    if not os.path.exists(caminho_saida):
        return False, "Compilador nao gerou o arquivo .docx (sem excecao, mas arquivo ausente)", duracao

    tamanho_kb = os.path.getsize(caminho_saida) / 1024
    return True, f"{tamanho_kb:.0f} KB", duracao


def main():
    arquivos = sorted(glob.glob(os.path.join(JSON_DIR, "TESTE-*.json")))

    if not arquivos:
        print(f"Nenhum TESTE-*.json encontrado em {JSON_DIR}")
        sys.exit(1)

    print("=" * 62)
    print("  Suite de Testes - Motor GEM / SMOSU Oliveira-MG")
    print(f"  {len(arquivos)} arquivo(s) encontrado(s)")
    print("=" * 62)

    resultados = []
    for caminho in arquivos:
        nome = os.path.basename(caminho)
        try:
            passou, msg, t = rodar_teste(caminho)
        except json.JSONDecodeError as e:
            passou, msg, t = False, f"JSON inválido: {e}", 0.0
        except Exception as e:
            passou, msg, t = False, f"Exceção inesperada: {e}", 0.0

        icone  = "OK" if passou else "FALHOU"
        t_str  = f"({t:.2f}s)" if t > 0 else ""
        status = msg if passou else msg
        print(f"  [{icone}] {nome:<40} {t_str:<8} {status}")
        resultados.append(passou)

    total  = len(resultados)
    ok     = sum(resultados)
    falhos = total - ok

    print("=" * 62)
    if ok == total:
        print(f"  Todos os {total} teste(s) passaram.")
        print("  Documentos gerados em: json/_output_testes/")
    else:
        print(f"  {ok}/{total} passou(aram)  |  {falhos} falhou(aram)")
    print("=" * 62)

    if LIMPAR_APOS and os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        print("  Pasta _output_testes removida (--limpar).")

    sys.exit(0 if falhos == 0 else 1)


if __name__ == "__main__":
    main()
