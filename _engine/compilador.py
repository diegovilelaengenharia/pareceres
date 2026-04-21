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


def main():
    args = sys.argv[1:]

    # Sem argumentos: mostrar ajuda
    if not args:
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

        # Agrupar por categoria
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
    erros = 0

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
        json_str = json.dumps(dados)
        if "⚠️ VERIFICAR" in json_str:
            print("  - [AVISO TÉCNICO]: O JSON contém marcações incompletas ('⚠️ VERIFICAR').")
            print("  - Dica para o GEM:")
            print("    'Gem, você marcou dados como '⚠️ VERIFICAR'. Releia os anexos")
            print("    com mais atenção e tente cruzar os dados pra ter a certeza.'\n")

        # Gerar documento
        try:
            gerar(dados, caminho_saida_fornecido)
            sucessos += 1
        except Exception as e:
            # Em modo lote, interceptar erro e continuar o loop sem crashar a prefeitura inteira
            print(f"  [ALERTA DE SISTEMA] Falha ao compilar {os.path.basename(arquivo)}: {e}")
            erros += 1
            
    print("\n" + "="*70)
    print(f" [V] COMPILAÇÃO ENCERRADA. Sucessos: {sucessos} | Falhas de Dados: {erros}")
    print("="*70)


if __name__ == "__main__":
    main()