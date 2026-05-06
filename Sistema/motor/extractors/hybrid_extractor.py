"""
Motor de Extração Híbrida de Alta Fidelidade — GEM SMOSU
========================================================
Combina PyMuPDF, pdfplumber e Docling para extração máxima de dados.
"""

import os
import sys
import logging
from pathlib import Path

# Ajustar sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_ROOT = os.path.dirname(SCRIPT_DIR)
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from core.logger import log_ok, log_warn, log_err, log_info

# Suprimir logs
logging.getLogger("docling").setLevel(logging.ERROR)

class HybridExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.nome_arquivo = os.path.basename(pdf_path)
        self.resultados = {
            "pymupdf": "",
            "pdfplumber": "",
            "docling": "",
            "metodo_principal": ""
        }

    def extrair_pymupdf(self):
        """Extração ultra-rápida e precisa para texto digital."""
        try:
            import fitz
            doc = fitz.open(self.pdf_path)
            texto = ""
            for i, page in enumerate(doc):
                texto += f"\n── PÁGINA {i+1} (PyMuPDF) ──\n"
                texto += page.get_text("text")
            self.resultados["pymupdf"] = texto
            return True
        except Exception as e:
            log_warn(f"PyMuPDF falhou: {e}")
            return False

    def extrair_pdfplumber(self):
        """Bom para tabelas simples e alinhamento de texto."""
        try:
            import pdfplumber
            texto = ""
            with pdfplumber.open(self.pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    texto += f"\n── PÁGINA {i+1} (pdfplumber) ──\n"
                    # Tenta extrair tabelas se houver
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            texto += "\n[TABELA DETECTADA]\n"
                            for row in table:
                                texto += " | ".join([str(cell or "") for cell in row]) + "\n"
                    
                    texto += page.extract_text() or ""
            self.resultados["pdfplumber"] = texto
            return True
        except Exception as e:
            log_warn(f"pdfplumber falhou: {e}")
            return False

    def extrair_docling(self):
        """O 'estado da arte' para estrutura e OCR de alta qualidade."""
        try:
            from docling.document_converter import DocumentConverter
            converter = DocumentConverter()
            result = converter.convert(self.pdf_path)
            self.resultados["docling"] = result.document.export_to_markdown()
            return True
        except Exception as e:
            log_err(f"Docling falhou (bad_alloc ou erro crítico): {e}")
            return False

    def fusion(self):
        """
        Lógica de Fusão Híbrida:
        Prioriza Docling (Markdown) para estrutura.
        Complementa com PyMuPDF para garantir que nenhum texto digital "invisível" foi perdido.
        """
        log_info(f"Executando fusão híbrida para {self.nome_arquivo}...")
        
        # Executa extrações em paralelo (ou sequência rápida)
        self.extrair_pymupdf()
        
        # Se for um PDF digital com muito texto, o PyMuPDF será ótimo.
        # Se for escaneado, o PyMuPDF virá vazio.
        is_scanned = len(self.resultados["pymupdf"].strip()) < 100
        
        if is_scanned:
            log_info("  [!] Detectado PDF escaneado ou com pouco texto digital. Usando OCR pesado.")
            if self.extrair_docling():
                self.resultados["metodo_principal"] = "Docling (OCR)"
                return self.resultados["docling"]
            else:
                log_err("  [!] OCR pesado falhou. Tentando fallback para pdfplumber...")
                self.extrair_pdfplumber()
                self.resultados["metodo_principal"] = "pdfplumber (Fallback)"
                return self.resultados["pdfplumber"]
        else:
            log_info("  [OK] PDF digital detectado.")
            # Tenta Docling para pegar a estrutura (Markdown é melhor para o Gemini)
            if self.extrair_docling():
                log_ok("  [OK] Estrutura Markdown obtida com Docling.")
                self.resultados["metodo_principal"] = "Híbrido (Docling + PyMuPDF)"
                # Concatenamos para garantir redundância em dados críticos (como números de processo)
                return f"{self.resultados['docling']}\n\n--- COMPLEMENTO TEXTUAL (PyMuPDF) ---\n{self.resultados['pymupdf']}"
            else:
                log_warn("  [!] Docling falhou no digital. Usando PyMuPDF puro.")
                self.resultados["metodo_principal"] = "PyMuPDF"
                return self.resultados["pymupdf"]

def processar_hibrido(pdf_path: str, txt_path: str):
    extractor = HybridExtractor(pdf_path)
    texto_final = extractor.fusion()
    
    cabecalho = (
        f"{'='*64}\n"
        f"  EXTRAÇÃO HÍBRIDA DE ALTA FIDELIDADE — GEM SMOSU\n"
        f"  Arquivo: {os.path.basename(pdf_path)}\n"
        f"  Motor Principal: {extractor.resultados['metodo_principal']}\n"
        f"{'='*64}\n\n"
    )
    
    try:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(cabecalho + texto_final)
        log_ok(f"Extração híbrida concluída: {os.path.basename(txt_path)}")
        return True
    except Exception as e:
        log_err(f"Erro ao salvar: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        processar_hibrido(sys.argv[1], sys.argv[1].replace(".pdf", "_HIBRIDO.txt"))
    else:
        print("Uso: python hybrid_extractor.py arquivo.pdf")
