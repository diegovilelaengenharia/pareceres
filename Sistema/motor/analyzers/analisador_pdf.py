"""
Analisador de PDFs via Claude API.
Envia o PDF para claude-sonnet-4-6, extrai o JSON estruturado e salva na pasta de entrada.
"""

import os
import sys
import json
import base64
import re
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from core.config import PASTA_ENTRADA, PASTA_TREINO as PASTA_INSTRUCOES

INSTRUCOES_PRINCIPAL = os.path.join(PASTA_INSTRUCOES, "TRIGGER.md")
INSTRUCOES_REFERENCIA = os.path.join(PASTA_INSTRUCOES, "REFERENCIA.md")


def _ler_instrucoes() -> str:
    partes = []
    for caminho in [INSTRUCOES_PRINCIPAL, INSTRUCOES_REFERENCIA]:
        if os.path.exists(caminho):
            try:
                with open(caminho, encoding="utf-8") as f:
                    partes.append(f.read())
            except Exception:
                pass
    return "\n\n---\n\n".join(partes) if partes else (
        "Você é o Engenheiro Analista Sênior da SMOSU — Prefeitura de Oliveira/MG. "
        "Analise o processo e gere o JSON estruturado completo."
    )


def _extrair_json(texto: str) -> dict | None:
    """Extrai o bloco JSON da resposta da API."""
    # Tenta bloco ```json ... ```
    match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', texto)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Tenta o maior { ... } da resposta
    match = re.search(r'\{[\s\S]*\}', texto)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def analisar_pdf(pdf_path: str) -> dict:
    """
    Envia o PDF para a Claude API e retorna o JSON extraído.
    Lança RuntimeError se não conseguir extrair JSON válido.
    """
    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "Biblioteca 'anthropic' não instalada.\n"
            "  Execute: pip install anthropic"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "Variável de ambiente ANTHROPIC_API_KEY não definida.\n"
            "  Defina a chave antes de rodar: set ANTHROPIC_API_KEY=sk-ant-..."
        )

    print(f"  [API] Lendo PDF: {os.path.basename(pdf_path)}")
    pdf_bytes = open(pdf_path, "rb").read()
    pdf_b64   = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    instrucoes = _ler_instrucoes()

    print("  [API] Enviando para Claude API (claude-sonnet-4-6)...")
    client = anthropic.Anthropic(api_key=api_key)

    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        system=instrucoes,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_b64,
                        },
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "type": "text",
                        "text": (
                            "Analise este processo administrativo completo e emita:\n"
                            "1. Uma análise narrativa em Markdown (obrigatória)\n"
                            "2. O JSON estruturado completo em bloco ```json\n\n"
                            "Siga rigorosamente as instruções do sistema. "
                            "Não pule a análise narrativa antes do JSON."
                        ),
                    },
                ],
            }
        ],
    )

    resposta = msg.content[0].text
    print("  [API] Resposta recebida. Extraindo JSON...")

    dados = _extrair_json(resposta)
    if dados is None:
        # Salvar resposta bruta para diagnóstico
        bruto_path = pdf_path.replace(".pdf", "_resposta_bruta.txt")
        with open(bruto_path, "w", encoding="utf-8") as f:
            f.write(resposta)
        raise RuntimeError(
            f"Não foi possível extrair JSON válido da resposta da API.\n"
            f"  Resposta bruta salva em: {os.path.basename(bruto_path)}"
        )

    return dados, resposta


def processar_pdfs_na_pasta() -> list[str]:
    """
    Varre PASTA_ENTRADA por PDFs, analisa cada um e salva o JSON.
    Retorna lista de caminhos JSON gerados.
    """
    pdfs = glob.glob(os.path.join(PASTA_ENTRADA, "*.pdf"))
    if not pdfs:
        print(f"[!] Nenhum arquivo .pdf encontrado em: {PASTA_ENTRADA}")
        return []

    jsons_gerados = []
    for pdf_path in pdfs:
        nome_base = os.path.splitext(os.path.basename(pdf_path))[0]
        json_path = os.path.join(PASTA_ENTRADA, f"{nome_base}.json")

        print(f"\n{'=' * 62}")
        print(f"  ANALISANDO PDF: {os.path.basename(pdf_path)}")
        print(f"{'=' * 62}")

        try:
            dados, resposta_bruta = analisar_pdf(pdf_path)

            # Salvar JSON extraído
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)

            # Salvar análise narrativa para referência
            analise_path = json_path.replace(".json", "_analise_claude.md")
            with open(analise_path, "w", encoding="utf-8") as f:
                f.write(resposta_bruta)

            print(f"  [OK] JSON salvo: {os.path.basename(json_path)}")
            print(f"  [OK] Análise salva: {os.path.basename(analise_path)}")
            jsons_gerados.append(json_path)

        except RuntimeError as e:
            print(f"  [ERRO] {e}")
        except Exception as e:
            print(f"  [ERRO INESPERADO] {e}")

    return jsons_gerados


if __name__ == "__main__":
    jsons = processar_pdfs_na_pasta()
    if jsons:
        print(f"\n[>] {len(jsons)} JSON(s) gerado(s). Pronto para compilar.")
    else:
        print("\n[!] Nenhum JSON gerado.")

