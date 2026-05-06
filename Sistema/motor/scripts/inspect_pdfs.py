import fitz # PyMuPDF
import sys
import os
import glob

def inspect_pdf(path):
    if not os.path.exists(path):
        print(f"Error: File not found: {path}")
        return
    print(f"\n--- 🔍 Inspecting: {path} ---")
    try:
        doc = fitz.open(path)
        print(f"📄 Total Pages: {len(doc)}")
        for i in range(min(3, len(doc))):
            page = doc[i]
            text = page.get_text()
            print(f"  Page {i+1}: {'Image/Scanned' if len(text.strip()) < 50 else 'Text Layer Detected'} ({len(text)} chars)")
            if len(text.strip()) > 50:
                print(f"  Snippet: {text[:300].replace('\n', ' ')}...")
        doc.close()
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if os.path.isdir(target):
            pdfs = glob.glob(os.path.join(target, "*.pdf"))
            print(f"Found {len(pdfs)} PDFs in directory.")
            for p in pdfs:
                inspect_pdf(p)
        else:
            inspect_pdf(target)
    else:
        print("Usage: python inspect_pdfs.py <path_to_pdf_or_directory>")
