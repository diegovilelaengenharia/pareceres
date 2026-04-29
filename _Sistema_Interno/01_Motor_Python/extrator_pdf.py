"""
Extrator de texto de PDFs — sem API, sem IA externa.
Usa pdfplumber (preferido) ou pypdf como fallback.
Salva o texto extraído como .txt legível na mesma pasta do PDF.
"""

import os
import sys
import glob

SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT  = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PASTA_ENTRADA = os.path.join(PROJECT_ROOT, "1_Colar_JSON_Aqui")
PASTA_MODELOS = os.path.join(PROJECT_ROOT, "0_Modelos_Prontos")


# ── Extração ──────────────────────────────────────────────────────────────────

def _extrair_com_pdfplumber(pdf_path: str) -> str:
    import pdfplumber
    paginas = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, pagina in enumerate(pdf.pages, 1):
            texto = pagina.extract_text() or ""
            if texto.strip():
                paginas.append(f"── PÁGINA {i} {'─'*40}\n{texto}")
    return "\n\n".join(paginas)


def _extrair_com_pypdf(pdf_path: str) -> str:
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    paginas = []
    for i, pagina in enumerate(reader.pages, 1):
        texto = pagina.extract_text() or ""
        if texto.strip():
            paginas.append(f"── PÁGINA {i} {'─'*40}\n{texto}")
    return "\n\n".join(paginas)


def extrair_texto(pdf_path: str) -> tuple[str | None, str]:
    """
    Tenta extrair texto do PDF.
    Retorna (texto, metodo_usado) ou (None, mensagem_de_erro).
    """
    nome = os.path.basename(pdf_path)

    # Tenta pdfplumber primeiro (melhor qualidade, preserva layout)
    try:
        import pdfplumber
        texto = _extrair_com_pdfplumber(pdf_path)
        if texto.strip():
            return texto, "pdfplumber"
        # pdfplumber funcionou mas retornou vazio (PDF de imagem)
        return None, "pdf_escaneado"
    except ImportError:
        pass  # biblioteca não instalada, tentar próxima
    except Exception as e:
        print(f"  [!] pdfplumber falhou: {e}")

    # Fallback: pypdf
    try:
        from pypdf import PdfReader
        texto = _extrair_com_pypdf(pdf_path)
        if texto.strip():
            return texto, "pypdf"
        return None, "pdf_escaneado"
    except ImportError:
        return None, "sem_biblioteca"
    except Exception as e:
        return None, f"erro: {e}"


def _detectar_tipo_processo(nome_arquivo: str) -> str | None:
    """Sugere o tipo_relatorio baseado no nome do arquivo PDF."""
    nome = nome_arquivo.lower()
    mapeamento = {
        "regulariz": "alvara_regularizacao",
        "as-built":  "alvara_regularizacao",
        "asbuilt":   "alvara_regularizacao",
        "aprovacao": "alvara_aprovacao",
        "habitese":  "habitese_comum",
        "habite-se": "habitese_comum",
        "localizacao": "certidao_localizacao",
        "decadencia":  "certidao_decadencia",
        "pendencia":   "comunicado_pendencia",
        "oficio":      "oficio_meio_ambiente",
        "memorando":   "memorando",
        "mcmv":        "alvara_mcmv",
        "comercial":   "alvara_construcao_comercial",
    }
    for chave, tipo in mapeamento.items():
        if chave in nome:
            return tipo
    return None


def _cabecalho_txt(nome_pdf: str, metodo: str) -> str:
    return (
        f"{'='*64}\n"
        f"  TEXTO EXTRAÍDO DO PDF — {nome_pdf}\n"
        f"  Método: {metodo}\n"
        f"{'='*64}\n\n"
        f"COMO USAR ESTE ARQUIVO:\n"
        f"\n"
        f"  OPÇÃO A — Via Gemini (gemini.google.com):\n"
        f"    1. Abra o Gemini e cole as instruções de 3_Treinar_Inteligencia/\n"
        f"    2. Em seguida cole o texto abaixo\n"
        f"    3. Peça: 'Gere o JSON estruturado para este processo'\n"
        f"    4. Salve o JSON em 1_Colar_JSON_Aqui/\n"
        f"\n"
        f"  OPÇÃO B — Via Claude Code (este chat):\n"
        f"    1. Copie o texto abaixo e cole no chat\n"
        f"    2. Peça: 'Gere o JSON GEM para este processo'\n"
        f"    3. Salve o JSON em 1_Colar_JSON_Aqui/\n"
        f"\n"
        f"  OPÇÃO C — Manual:\n"
        f"    1. Abra um modelo da pasta 0_Modelos_Prontos/\n"
        f"    2. Preencha os campos usando este texto como referência\n"
        f"\n"
        f"{'='*64}\n"
        f"  TEXTO DO PROCESSO:\n"
        f"{'='*64}\n\n"
    )


# ── Processamento em lote ─────────────────────────────────────────────────────

def processar_pdfs(pasta: str = PASTA_ENTRADA) -> list[str]:
    """
    Varre a pasta por PDFs, extrai texto de cada um e salva como .txt.
    Retorna lista de caminhos .txt gerados com sucesso.
    """
    pdfs = glob.glob(os.path.join(pasta, "*.pdf"))
    if not pdfs:
        return []

    txts_gerados = []

    for pdf_path in pdfs:
        nome_base = os.path.splitext(os.path.basename(pdf_path))[0]
        txt_path  = os.path.join(pasta, f"{nome_base}_TEXTO_EXTRAIDO.txt")

        print(f"\n  ── PDF: {os.path.basename(pdf_path)}")

        texto, metodo = extrair_texto(pdf_path)

        if metodo == "sem_biblioteca":
            print(f"  [!] Nenhuma biblioteca de PDF instalada.")
            print(f"      Execute: pip install pdfplumber")
            continue

        if metodo == "pdf_escaneado":
            print(f"  [!] PDF sem texto selecionável (imagem escaneada).")
            print(f"      Solução: use o Gemini com o PDF anexado diretamente.")
            # Criar arquivo de aviso mesmo assim
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(
                    f"AVISO: Este PDF é composto por imagens escaneadas.\n"
                    f"Não é possível extrair texto automaticamente.\n\n"
                    f"ALTERNATIVA: Acesse gemini.google.com, anexe o PDF original\n"
                    f"e use as instruções de 3_Treinar_Inteligencia/01_GEM_INSTRUCOES.md\n"
                )
            print(f"  [>] Arquivo de aviso criado: {os.path.basename(txt_path)}")
            txts_gerados.append(txt_path)
            continue

        if texto and metodo.startswith("erro"):
            print(f"  [ERRO] {metodo}")
            continue

        # Sucesso — salvar texto
        conteudo = _cabecalho_txt(os.path.basename(pdf_path), metodo) + texto
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(conteudo)

        tipo_sugerido = _detectar_tipo_processo(nome_base)
        tipo_str = f" (tipo sugerido: {tipo_sugerido})" if tipo_sugerido else ""
        print(f"  [OK] Texto extraído com {metodo}{tipo_str}")
        print(f"  [OK] Salvo: {os.path.basename(txt_path)}")
        txts_gerados.append(txt_path)

    return txts_gerados


# ── Interface de linha de comando ─────────────────────────────────────────────

def main():
    import subprocess

    print()
    print("=" * 62)
    print("  EXTRATOR DE TEXTO — PDF local (sem API, sem IA)")
    print("=" * 62)
    print()

    # Verificar dependências
    tem_pdfplumber = False
    tem_pypdf      = False
    try:
        import pdfplumber; tem_pdfplumber = True
    except ImportError:
        pass
    try:
        from pypdf import PdfReader; tem_pypdf = True
    except ImportError:
        pass

    if not tem_pdfplumber and not tem_pypdf:
        print("  [!] Nenhuma biblioteca de leitura de PDF instalada.")
        print()
        print("  Instale uma das opções abaixo:")
        print("    pip install pdfplumber     (recomendado — melhor qualidade)")
        print("    pip install pypdf          (alternativa mais leve)")
        print()
        resp = input("  Deseja instalar pdfplumber agora? [S/N]: ").strip().upper()
        if resp == "S":
            print()
            subprocess.run([sys.executable, "-m", "pip", "install", "pdfplumber"])
            print()
        else:
            input("  Pressione ENTER para sair.")
            return

    pdfs = glob.glob(os.path.join(PASTA_ENTRADA, "*.pdf"))
    if not pdfs:
        print(f"  [!] Nenhum arquivo .pdf encontrado em:")
        print(f"      {PASTA_ENTRADA}")
        print()
        print("  Coloque o(s) PDF(s) do processo nessa pasta e tente novamente.")
        input("\n  Pressione ENTER para sair.")
        return

    print(f"  PDFs encontrados: {len(pdfs)}")
    for p in pdfs:
        print(f"    • {os.path.basename(p)}")
    print()

    txts = processar_pdfs()

    if not txts:
        print()
        print("  [!] Nenhum texto extraído. Verifique os avisos acima.")
        input("\n  Pressione ENTER para sair.")
        return

    print()
    print(f"  {len(txts)} arquivo(s) de texto gerado(s).")
    print()
    print("─" * 62)
    print("  PRÓXIMOS PASSOS:")
    print("─" * 62)
    print()
    print("  1. Leia o arquivo _TEXTO_EXTRAIDO.txt gerado")
    print("  2. Escolha uma das opções:")
    print()
    print("     A) Cole o texto no Gemini + instruções GEM → receba o JSON")
    print("     B) Cole o texto aqui no Claude Code → peça o JSON")
    print("     C) Preencha um modelo manualmente da pasta 0_Modelos_Prontos/")
    print()
    print("  3. Salve o JSON em 1_Colar_JSON_Aqui/")
    print("  4. Volte ao menu e use [1] MOTOR para gerar o DOCX")
    print()

    resp = input("  Abrir os arquivos de texto no Bloco de Notas? [S/N]: ").strip().upper()
    if resp == "S":
        for txt in txts:
            try:
                subprocess.Popen(["notepad.exe", txt])
            except Exception:
                pass
        print("  [OK] Arquivos abertos.")

    print()
    input("  Pressione ENTER para sair.")


if __name__ == "__main__":
    main()
