import fitz # PyMuPDF
import sys

def inspect_pdf(path):
    print(f"--- Inspecting: {path} ---")
    doc = fitz.open(path)
    print(f"Pages: {len(doc)}")
    for i in range(min(5, len(doc))):
        page = doc[i]
        text = page.get_text()
        print(f"Page {i+1} text length: {len(text)}")
        if len(text) > 0:
            print(f"Sample text: {text[:200]}...")
        else:
            print("No text found (likely scanned image).")
    doc.close()

files = [
    "LEGISLAÇÕES PARA TREINAR E REVISAR/Obras/Multas e Taxas de 2025.pdf",
    "LEGISLAÇÕES PARA TREINAR E REVISAR/Obras/IEPHA/PTE145_2013_Oliveira_Centro Historico_Setorizacao_areas_de_protecao_2025.pdf"
]

for f in files:
    inspect_pdf(f)

