"""
Modo PDF LOCAL — sem API, sem IA externa.
Fluxo: PDF na pasta → extrai texto → abre no Bloco de Notas →
       usuário usa Gemini/Claude Code para gerar JSON →
       salva JSON → compila DOCX com preview.
"""

import os
import sys
import glob
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from config import PASTA_ENTRADA


def _aguardar_json(pdfs_originais: list[str]) -> list[str]:
    """
    Aguarda o usuário colocar o(s) JSON(s) na pasta de entrada.
    Retorna lista dos JSONs encontrados que não existiam antes.
    """
    # JSONs que já existiam antes (ignorar)
    jsons_antes = set(glob.glob(os.path.join(PASTA_ENTRADA, "*.json")))
    nomes_pdfs  = {os.path.splitext(os.path.basename(p))[0] for p in pdfs_originais}

    print()
    print("─" * 62)
    print("  AGUARDANDO O JSON...")
    print("─" * 62)
    print()
    print("  Passos:")
    print("  1. Use o texto extraído acima com o Gemini ou Claude Code")
    print("  2. Peça para gerar o JSON estruturado do processo")
    print("  3. Salve o JSON em:")
    print(f"     {PASTA_ENTRADA}")
    print()
    print("  Quando o JSON estiver salvo na pasta, pressione ENTER.")
    print("  Para sair sem compilar, digite S + ENTER.")
    print()

    while True:
        resp = input("  [ENTER para verificar / S para sair]: ").strip().upper()
        if resp == "S":
            return []

        jsons_agora = set(glob.glob(os.path.join(PASTA_ENTRADA, "*.json")))
        novos = jsons_agora - jsons_antes

        if novos:
            print(f"\n  [OK] {len(novos)} JSON(s) encontrado(s):")
            for j in novos:
                print(f"    • {os.path.basename(j)}")
            return list(novos)

        # Também aceitar JSONs com o mesmo nome do PDF
        todos = list(jsons_agora)
        if todos:
            print(f"\n  JSONs disponíveis na pasta:")
            for i, j in enumerate(todos, 1):
                print(f"    [{i}] {os.path.basename(j)}")
            resp2 = input(f"\n  Usar estes JSONs? [S/N]: ").strip().upper()
            if resp2 == "S":
                return todos

        print("  [!] Nenhum JSON novo encontrado. Tente novamente.")


def main():
    print()
    print("=" * 62)
    print("  MODO PDF LOCAL — Extração de texto + Geração via Gemini")
    print("=" * 62)
    print()

    # ── Verificar PDFs ────────────────────────────────────────────────────────
    pdfs = glob.glob(os.path.join(PASTA_ENTRADA, "*.pdf"))

    if not pdfs:
        print("[!] Nenhum arquivo .pdf encontrado em:")
        print(f"    {PASTA_ENTRADA}")
        print()
        print("  Cole o PDF do processo nessa pasta e tente novamente.")
        input("\n  Pressione ENTER para sair.")
        return

    print(f"  PDFs encontrados: {len(pdfs)}")
    for p in pdfs:
        print(f"    • {os.path.basename(p)}")
    print()

    # ── Passo 1: Extrair texto dos PDFs ─────────────────────────────────────
    print("─" * 62)
    print("  PASSO 1/3 — Extraindo texto dos PDFs")
    print("─" * 62)
    print()

    from extrator_pdf import processar_pdfs
    txts = processar_pdfs(PASTA_ENTRADA)

    if txts:
        resp = input("\n  Abrir o(s) arquivo(s) de texto no Bloco de Notas? [S/N]: ").strip().upper()
        if resp == "S":
            for txt in txts:
                try:
                    subprocess.Popen(["notepad.exe", txt])
                except Exception:
                    pass
    else:
        print()
        print("  [!] Não foi possível extrair texto automaticamente.")
        print("  Provavelmente o PDF é uma imagem escaneada.")
        print()
        print("  Alternativa: anexe o PDF diretamente no Gemini e peça o JSON.")

    # ── Passo 2: Aguardar JSON do usuário ────────────────────────────────────
    print()
    print("─" * 62)
    print("  PASSO 2/3 — Cole o JSON gerado na pasta de entrada")
    print("─" * 62)

    jsons = _aguardar_json(pdfs)

    if not jsons:
        print("\n  [!] Operação cancelada.")
        input("  Pressione ENTER para sair.")
        return

    # ── Passo 3: Preview + compilação ────────────────────────────────────────
    print()
    print("─" * 62)
    print("  PASSO 3/3 — Preview e geração do DOCX")
    print("─" * 62)
    print()

    from compilador import main as compilar
    sys.argv = [sys.argv[0]]
    compilar()


if __name__ == "__main__":
    main()
