"""
Motor de OCR de Alta Fidelidade — Motor GEM / SMOSU Oliveira-MG
Utiliza Docling (IBM) para extração estruturada de PDFs.

Este módulo é o coração da Fase 07, permitindo extrair texto de PDFs 
complexos e escaneados com preservação de layout.
"""

import os
import sys
import logging
from pathlib import Path

# Ajustar sys.path para o motor
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_ROOT = os.path.dirname(SCRIPT_DIR)
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from core.logger import log_ok, log_warn, log_err, log_info

# Suprimir logs verbosos do docling/onnx
logging.getLogger("docling").setLevel(logging.ERROR)
logging.getLogger("onnxruntime").setLevel(logging.ERROR)

def extrair_fiel(pdf_path: str) -> str:
    """
    Extrai texto do PDF usando Docling. 
    Ideal para documentos com tabelas, colunas ou escaneados.
    """
    try:
        from docling.datamodel.base_models import InputFormat
        from docling.document_converter import DocumentConverter
        
        converter = DocumentConverter()
        result = converter.convert(pdf_path)
        
        # Exporta para Markdown para preservar estrutura (tabelas, títulos)
        return result.document.export_to_markdown()
    except Exception as e:
        log_err(f"Falha no OCR Docling: {e}")
        return ""

def processar_ocr_local(pdf_path: str, txt_path: str) -> bool:
    """
    Executa o fluxo de OCR e salva em arquivo.
    """
    log_info(f"Iniciando OCR de alta fidelidade: {os.path.basename(pdf_path)}")
    
    texto = extrair_fiel(pdf_path)
    
    if not texto.strip():
        log_err("OCR resultou em texto vazio.")
        return False
        
    try:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(texto)
        log_ok(f"Texto extraído e salvo: {os.path.basename(txt_path)}")
        return True
    except Exception as e:
        log_err(f"Erro ao salvar arquivo de texto: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        out = path.replace(".pdf", "_OCR.txt")
        processar_ocr_local(path, out)
    else:
        print("Uso: python ocr_engine.py arquivo.pdf")
