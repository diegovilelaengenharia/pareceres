"""
Gerador Automático de Documentos – Prefeitura de Oliveira / SMOSU
Orquestrador principal – despacha para os geradores especializados.

Uso: python _engine\\compilador.py dados.json [saida.docx]
"""

import sys
import json
import os

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

    # Ler JSON de entrada
    try:
        with open(args[0], encoding="utf-8") as f:
            dados = json.load(f)
        print(f"[>] Lendo arquivo: {args[0]}")
    except FileNotFoundError:
        print(f"[!] Não encontrado: {args[0]}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[!] JSON inválido: {e}")
        sys.exit(1)

    # Verificar marcadores de segurança
    json_str = json.dumps(dados)
    if "⚠️ VERIFICAR" in json_str:
        print("\n" + "="*70)
        print("  [AVISO]: O JSON contém marcações de incerteza do GEM.")
        print("="*70)
        print("    Para forçar o GEM a re-avaliar as folhas e corrigir as suas")
        print("    próprias dúvidas, copie e envie a ele a mensagem abaixo:\n")
        print("    'Gem, você marcou dados como '⚠️ VERIFICAR'. Releia os anexos")
        print("    com mais atenção e tente cruzar os dados pra ter a certeza.'")
        print("="*70 + "\n")

    # Gerar documento
    caminho_saida = args[1] if len(args) > 1 else None
    gerar(dados, caminho_saida)


if __name__ == "__main__":
    main()