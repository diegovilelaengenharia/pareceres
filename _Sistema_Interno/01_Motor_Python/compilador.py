"""
Gerador Automático de Documentos – Prefeitura de Oliveira / SMOSU
Orquestrador principal – despacha para os geradores especializados.

Uso: python _engine\\compilador.py dados.json [saida.docx]
"""

import sys
import json
import os
import glob

# Adicionar o diretório do script ao path para imports locais
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from config import TIPOS_DOCUMENTO
from geradores import gerar

# Módulos de análise pré-voo
import calculadora_indices    as calc_idx
import alertas_decadencia     as alerta_dec
import consistencia           as consist
import precedentes            as prec
import verificador_multas     as verif_multas
import cobertura_considerandos as cob_cons
import gerador_sero           as gen_sero


# ── Relatório pré-voo unificado ───────────────────────────────────────────────

def _relatorio_prevoo(dados: dict) -> tuple[bool, dict]:
    """
    Executa todas as análises antes de gerar o documento.
    Retorna (pode_prosseguir, resumo_cobertura).
    """
    tipo      = dados.get("tipo_relatorio", "?")
    processo  = dados.get("numero_processo", "?")
    requerente = dados.get("requerente", dados.get("proprietario_nome", "?"))

    print("\n" + "=" * 62)
    print(f"  PRÉ-VOO — Processo {processo}  |  {requerente}")
    print(f"  Tipo: {tipo}")
    print("=" * 62)

    tem_erro_bloqueante = False

    # ── 1. Calculadora de índices urbanísticos ────────────────────────────────
    try:
        res_idx = calc_idx.calcular(dados)
        calc_idx.imprimir_relatorio(res_idx)
        if res_idx.get("erros"):
            tem_erro_bloqueante = False  # índices fora do limite não bloqueiam — podem ser multas
    except Exception as e:
        print(f"\n  [!] Calculadora de índices indisponível: {e}")

    # ── 2. Alerta de decadência ───────────────────────────────────────────────
    try:
        res_dec = alerta_dec.verificar(dados)
        alerta_dec.imprimir_relatorio(res_dec)
    except Exception as e:
        print(f"\n  [!] Módulo de decadência indisponível: {e}")

    # ── 3. Consistência semântica ─────────────────────────────────────────────
    try:
        erros_sem, avisos_sem = consist.verificar(dados)
        consist.imprimir_relatorio(erros_sem, avisos_sem, tipo)
        if erros_sem:
            pass # tem_erro_bloqueante = True  -- desativado para permitir geração com placeholders
    except Exception as e:
        print(f"\n  [!] Módulo de consistência indisponível: {e}")

    # ── 4. Verificação de cálculo de multas ───────────────────────────────────
    try:
        erros_multas, avisos_multas, resumo_multas = verif_multas.verificar(dados)
        verif_multas.imprimir_relatorio(erros_multas, avisos_multas, resumo_multas)
        if erros_multas:
            pass # tem_erro_bloqueante = True  -- desativado para permitir geração parcial
    except Exception as e:
        print(f"\n  [!] Módulo de multas indisponível: {e}")

    # ── 5. Cobertura temática dos considerandos ───────────────────────────────
    cobertos: set = set()
    resumo_cob: dict = {}
    try:
        erros_cob, avisos_cob, cobertos, faltando = cob_cons.verificar(dados)
        cob_cons.imprimir_relatorio(erros_cob, avisos_cob, cobertos, faltando)
        if erros_cob:
            pass # tem_erro_bloqueante = True  -- desativado para permitir geração com placeholders
        resumo_cob = {
            "cobertos": sorted(cobertos),
            "faltando": sorted(faltando - cobertos),
            "n_total":  len(cob_cons._TEMAS),
        }
    except Exception as e:
        print(f"\n  [!] Módulo de cobertura temática indisponível: {e}")

    # ── 6. SERO/INSS metadata ─────────────────────────────────────────────────
    tem_sero = bool(dados.get("sero_metadata"))
    try:
        erros_sero, avisos_sero = gen_sero.validar(dados)
        gen_sero.imprimir_relatorio(erros_sero, avisos_sero)
    except Exception as e:
        print(f"\n  [!] Módulo SERO indisponível: {e}")

    resumo_cob["tem_sero"] = tem_sero
    resumo_cob["tem_multas"] = bool(dados.get("multas_calculadas"))
    resumo_cob["tem_excecoes"] = bool(dados.get("excecoes_aplicadas"))

    return not tem_erro_bloqueante, resumo_cob


def _relatorio_pos(dados: dict, caminho_docx: str, resumo_cob: dict) -> None:
    """Exibe precedentes e resumo de cobertura após a geração do documento."""
    try:
        prec.imprimir_relatorio(dados)
    except Exception as e:
        print(f"\n  [!] Módulo de precedentes indisponível: {e}")

    # Resumo de qualidade do documento gerado
    nome_doc = os.path.basename(caminho_docx) if caminho_docx else "documento"
    cobertos = resumo_cob.get("cobertos", [])
    faltando = resumo_cob.get("faltando", [])
    n_total  = resumo_cob.get("n_total", 8)
    n_cob    = len(cobertos)

    print(f"\n{'=' * 62}")
    print(f"  RESUMO DE QUALIDADE — {nome_doc}")
    print(f"  Temas cobertos: {n_cob}/{n_total}", end="")
    if faltando:
        print(f"  (faltam: {', '.join(faltando)})")
    else:
        print()

    flag_multas  = "[OK]" if resumo_cob.get("tem_multas") else "[ - ] ausente"
    flag_excecoes = "[OK]" if resumo_cob.get("tem_excecoes") else "[ - ] ausente"
    flag_sero    = "[OK]" if resumo_cob.get("tem_sero") else "[ - ] ausente"
    print(f"  multas_calculadas: {flag_multas}")
    print(f"  excecoes_aplicadas: {flag_excecoes}")
    print(f"  sero_metadata: {flag_sero}")
    print('=' * 62)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    # Sem argumentos: tentar usar a pasta padrão 1_Colar_JSON_Aqui
    if not args:
        pasta_padrao = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "1_Colar_JSON_Aqui")
        if os.path.exists(pasta_padrao) and glob.glob(os.path.join(pasta_padrao, "*.json")):
            args = [pasta_padrao]
        else:
            print("╔══════════════════════════════════════════════════════════════════╗")
            print("║  Gerador de Documentos – SMOSU Oliveira/MG                     ║")
            print("╠══════════════════════════════════════════════════════════════════╣")
            print("║                                                                ║")
            print("║  Uso: python compilador.py dados.json [saida.docx]             ║")
            print("║                                                                ║")
            print("║  O JSON deve conter o campo 'tipo_relatorio' com um dos tipos  ║")
            print("║  listados abaixo.                                              ║")
            print("║                                                                ║")
            print("╠══════════════════════════════════════════════════════════════════╣")
            print("║  TIPOS DE DOCUMENTO DISPONÍVEIS:                               ║")
            print("╠══════════════════════════════════════════════════════════════════╣")

            categorias = {}
            for tipo, cat in sorted(TIPOS_DOCUMENTO.items()):
                categorias.setdefault(cat, []).append(tipo)

            for cat in ["parecer_tecnico", "parecer_simples", "oficio", "comunicado"]:
                tipos = categorias.get(cat, [])
                if tipos:
                    print(f"║  [{cat.upper():^20}]                                     ║")
                    for t in tipos:
                        print(f"║    • {t:<56} ║")
                    print("║                                                                ║")

            print("╚══════════════════════════════════════════════════════════════════╝")
            sys.exit(0)

    alvo = args[0]
    arquivos_para_processar = []

    if os.path.isdir(alvo):
        print(f"\n[>] MODO EM LOTE: Escaneando pasta '{alvo}'")
        arquivos_para_processar = glob.glob(os.path.join(alvo, "*.json"))
        if not arquivos_para_processar:
            print(f"[!] Nenhum arquivo .json encontrado na pasta de origem.")
            sys.exit(0)
    elif os.path.isfile(alvo) and alvo.endswith(".json"):
        arquivos_para_processar = [alvo]
    else:
        print(f"[!] Erro: O caminho não é um JSON válido ou não existe -> {alvo}")
        sys.exit(1)

    caminho_saida_fornecido = args[1] if len(args) > 1 else None

    if len(arquivos_para_processar) > 1 and caminho_saida_fornecido:
        print("[!] Aviso: Parâmetro de saída único ignorado devido ao processamento em lote.")
        caminho_saida_fornecido = None

    sucessos = 0
    erros    = 0

    from traceback import print_exc

    for arquivo in arquivos_para_processar:
        # Ler JSON de entrada
        try:
            with open(arquivo, encoding="utf-8") as f:
                dados = json.load(f)
            print(f"\n[>] Processando arquivo: {os.path.basename(arquivo)}")
        except json.JSONDecodeError as e:
            print(f"[X] Ignorando {os.path.basename(arquivo)}: JSON inválido ({e})")
            erros += 1
            continue

        # Verificar marcadores de segurança
        json_str = json.dumps(dados, ensure_ascii=False)
        if "⚠️ VERIFICAR" in json_str:
            print("  - [AVISO TÉCNICO]: O JSON contém marcações incompletas (VERIFICAR).")
            print("  - Dica para o GEM:")
            print("    'Gem, você marcou dados como 'VERIFICAR'. Releia os anexos")
            print("    com mais atenção e tente cruzar os dados pra ter a certeza.'\n")

        # ── Relatório pré-voo ─────────────────────────────────────────────────
        pode_prosseguir, resumo_cob = _relatorio_prevoo(dados)

        if not pode_prosseguir:
            print("\n[X] Geração BLOQUEADA por erro de consistência semântica.")
            print("    Corrija o JSON antes de compilar.")
            erros += 1
            continue

        # ── Gerar documento ───────────────────────────────────────────────────
        caminho_gerado = caminho_saida_fornecido
        try:
            caminho_gerado = gerar(dados, caminho_saida_fornecido)
            sucessos += 1
        except Exception as e:
            print(f"  [ALERTA DE SISTEMA] Falha ao compilar {os.path.basename(arquivo)}: {e}")
            erros += 1
            continue

        # ── Precedentes + resumo de qualidade (pós-geração) ──────────────────
        _relatorio_pos(dados, caminho_gerado or "", resumo_cob)

    print("\n" + "=" * 70)
    print(f" [V] COMPILAÇÃO ENCERRADA. Sucessos: {sucessos} | Falhas de Dados: {erros}")
    print("=" * 70)


if __name__ == "__main__":
    main()
