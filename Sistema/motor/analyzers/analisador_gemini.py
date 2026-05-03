"""
Analisador de PDFs via Gemini API (Google Generative AI).
Envia o PDF para o modelo Gemini 1.5 Pro/Flash, extrai o JSON estruturado 
e salva na pasta de entrada, permitindo análise de documentos complexos e escaneados.
"""

import os
import sys
import json
import re
import glob
import time

# Tenta importar a biblioteca oficial do Google
try:
    import google.generativeai as genai
except ImportError:
    genai = None

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
    match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', texto)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    match = re.search(r'\{[\s\S]*\}', texto)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def analisar_pdf_gemini(pdf_path: str, model_name: str = "gemini-1.5-pro") -> tuple[dict, str]:
    """
    Envia o PDF para a Gemini API e retorna o JSON extraído e a resposta completa.
    """
    if genai is None:
        raise RuntimeError(
            "Biblioteca 'google-generativeai' não instalada.\n"
            "  Execute: pip install google-generativeai"
        )

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "Variável de ambiente GEMINI_API_KEY não definida.\n"
            "  Defina a chave antes de rodar: set GEMINI_API_KEY=AIza..."
        )

    genai.configure(api_key=api_key)

    print(f"  [GEMINI] Carregando PDF: {os.path.basename(pdf_path)}")
    
    # Upload do arquivo para a API do Gemini (suporta PDFs nativamente)
    sample_file = genai.upload_file(path=pdf_path, display_name=os.path.basename(pdf_path))
    
    # Aguarda o processamento do arquivo
    while sample_file.state.name == "PROCESSING":
        time.sleep(2)
        sample_file = genai.get_file(sample_file.name)

    if sample_file.state.name == "FAILED":
        raise RuntimeError(f"Falha no processamento do arquivo pela API: {sample_file.state.name}")

    instrucoes = _ler_instrucoes()

    print(f"  [GEMINI] Analisando com {model_name}...")
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=instrucoes
    )

    prompt = (
        "Analise este processo administrativo completo e emita:\n"
        "1. Uma análise narrativa em Markdown (obrigatória)\n"
        "2. O JSON estruturado completo em bloco ```json\n\n"
        "Siga rigorosamente as instruções do sistema. "
        "Não pule a análise narrativa antes do JSON."
    )

    response = model.generate_content([sample_file, prompt])
    
    # Limpeza: Deleta o arquivo da nuvem após o processamento
    genai.delete_file(sample_file.name)

    resposta = response.text
    print("  [GEMINI] Resposta recebida. Extraindo JSON...")

    dados = _extrair_json(resposta)
    if dados is None:
        bruto_path = pdf_path.replace(".pdf", "_resposta_gemini_bruta.txt")
        with open(bruto_path, "w", encoding="utf-8") as f:
            f.write(resposta)
        raise RuntimeError(
            f"Não foi possível extrair JSON válido da resposta do Gemini.\n"
            f"  Resposta bruta salva em: {os.path.basename(bruto_path)}"
        )

    return dados, resposta


def processar_pdfs_na_pasta() -> list[str]:
    """
    Varre PASTA_ENTRADA por PDFs, analisa cada um e salva o JSON.
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
        print(f"  ANALISANDO PDF COM GEMINI: {os.path.basename(pdf_path)}")
        print(f"{'=' * 62}")

        try:
            # Tenta com o Flash 2.0 por ser mais robusto/atual
            dados, resposta_bruta = analisar_pdf_gemini(pdf_path, model_name="gemini-2.0-flash")

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)

            analise_path = json_path.replace(".json", "_analise_gemini.md")
            with open(analise_path, "w", encoding="utf-8") as f:
                f.write(resposta_bruta)

            print(f"  [OK] JSON salvo: {os.path.basename(json_path)}")
            print(f"  [OK] Análise salva: {os.path.basename(analise_path)}")
            jsons_gerados.append(json_path)

        except Exception as e:
            print(f"  [ERRO] {e}")

    return jsons_gerados


if __name__ == "__main__":
    jsons = processar_pdfs_na_pasta()
    if jsons:
        print(f"\n[>] {len(jsons)} JSON(s) gerado(s) via Gemini OCR. Pronto para compilar.")
    else:
        print("\n[!] Nenhum JSON gerado.")

