import pdfplumber
import sys
import os

def extract_text(pdf_path):
    print(f"--- Extracting: {pdf_path} ---")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        return f"Error: {e}"

files = [
    "LEGISLAÇÕES PARA TREINAR E REVISAR/Obras/LEI Nº 4.071, DE 11 DE JUNHO DE 2025.pdf",
    "LEGISLAÇÕES PARA TREINAR E REVISAR/Obras/Multas e Taxas de 2025.pdf",
    "LEGISLAÇÕES PARA TREINAR E REVISAR/Obras/IEPHA/PTE145_2013_Oliveira_Centro Historico_Setorizacao_areas_de_protecao_2025.pdf"
]

for f in files:
    if os.path.exists(f):
        print(extract_text(f))
        print("\n" + "="*50 + "\n")
    else:
        print(f"File not found: {f}")

