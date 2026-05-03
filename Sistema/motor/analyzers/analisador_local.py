import os
import sys
import glob
import time
import json

# Bibliotecas para o Roteador
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    from docling.document_converter import DocumentConverter
    HAS_DOCLING = True
except ImportError:
    HAS_DOCLING = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from core.config import PASTA_ENTRADA

# ═══════════════════════════════════════════════════════════
#  LÓGICA DO ROTEADOR (CLASSIFICAÇÃO)
# ═══════════════════════════════════════════════════════════

def classificar_pagina(page_text):
    """Identifica o tipo de documento baseado em palavras-chave específicas da SMOSU."""
    text = page_text.upper()
    
    # ── Categorias SMOSU Especializadas ──
    if "CERTIDÃO DE AVERBAÇÃO" in text: return "CERTIDAO_AVERBACAO"
    if "CARTA DE HABITE-SE" in text: return "HABITE_SE"
    if "ALVARÁ DE CONSTRUÇÃO" in text: return "ALVARA_CONSTRUCAO"
    if "CERTIDÃO DE DECADÊNCIA" in text: return "CERTIDAO_DECADENCIA"
    if "LAUDO DE AVALIAÇÃO" in text: return "LAUDO_AVALIACAO"
    if "PLANTA CADASTRAL" in text: return "PLANTA_CADASTRAL"
    if "TRIAGEM - SMOSU" in text: return "TRIAGEM"
    if "COMUNICADO" in text and "PENDÊNCIA" in text: return "PENDENCIA"
    if "PARECER TÉCNICO" in text and "THAMIRES" in text: return "PARECER_THAMIRES"
    if "CARTEIRA DE IDENTIDADE" in text or "POLÍCIA CIVIL" in text: return "IDENTIDADE"
    if "PIX REALIZADO" in text or "COMPROVANTE DE PAGAMENTO" in text: return "COMPROVANTE_PAGAMENTO"
    
    # ── Categorias Base ──
    if "ESPELHO CADASTRAL" in text or "CADASTRO IMOBILIÁRIO" in text: return "IPTU"
    if "ANOTAÇÃO DE RESPONSABILIDADE TÉCNICA" in text or "ART OBRA / SERVIÇO" in text: return "ART"
    if "DOCUMENTO DE ARRECADAÇÃO MUNICIPAL" in text or "DAM" in text: return "GUIA_PAGAMENTO"
    if "PARECER FISCAL" in text: return "PARECER_FISCAL"
    if "LAUDO TÉCNICO" in text: return "LAUDO_ENGENHEIRO"
    
    return "GENERICO"

# ═══════════════════════════════════════════════════════════
#  EXTRAÇÕES ESPECIALIZADAS
# ═══════════════════════════════════════════════════════════

def extrair_iptu_especifico(page):
    """Extração via coordenadas/tabelas para o Espelho do IPTU."""
    tables = page.extract_tables()
    data = []
    for table in tables:
        for row in table:
            row_clean = [str(c).replace('\n', ' ').strip() for c in row if c]
            if row_clean:
                data.append(" | ".join(row_clean))
    return "\n".join(data)

def extrair_art_especifico(page):
    """Extração focada nos blocos da ART do CREA-MG."""
    return page.extract_text() or ""

def extrair_dam_especifico(page):
    """Extração cirúrgica para DAM: Contribuinte, Valor, Vencimento, Multa e Autenticação."""
    text = page.extract_text() or ""
    linhas = text.split("\n")
    
    extraido = {
        "contribuinte": "Não encontrado",
        "cpf_cnpj": "Não encontrado",
        "sacado": "Não encontrado",
        "valor_total": "Não encontrado",
        "vencimento": "Não encontrado",
        "observacoes": "Não encontrado",
        "autenticacao": "Não encontrada"
    }
    
    for i, linha in enumerate(linhas):
        l_up = linha.upper()
        if "CONTRIBUINTE" in l_up or "NOME" in l_up:
            extraido["contribuinte"] = linha.split(":")[-1].strip()
        if "SACADO" in l_up:
            extraido["sacado"] = linha.split(":")[-1].strip()
        if "CPF" in l_up or "CNPJ" in l_up:
            extraido["cpf_cnpj"] = linha.split(":")[-1].strip()
        if "(=)" in l_up or "VALOR TOTAL" in l_up:
            extraido["valor_total"] = linha.split(")")[-1].strip()
        if "VENCIMENTO" in l_up:
            extraido["vencimento"] = linha.split(":")[-1].strip() or linha.split(" ")[-1].strip()
        if "OBSERVAÇÕES" in l_up or "HISTÓRICO" in l_up or "DESCRIÇÃO" in l_up:
            obs = linha.split(":")[-1].strip()
            if not obs and i + 1 < len(linhas):
                obs = linhas[i+1].strip()
            extraido["observacoes"] = obs
        if "AUTENTICAÇÃO" in l_up or "COMPROVANTE" in l_up or "PAGAMENTO" in l_up or "QUITAÇÃO" in l_up:
            extraido["autenticacao"] = "SINALIZADO NO DOCUMENTO"

    return (
        f"--- DADOS TÉCNICOS DA GUIA (DAM) ---\n"
        f"CONTRIBUINTE/SACADO: {extraido['contribuinte']} / {extraido['sacado']}\n"
        f"CPF/CNPJ: {extraido['cpf_cnpj']}\n"
        f"VALOR TOTAL: {extraido['valor_total']}\n"
        f"VENCIMENTO: {extraido['vencimento']}\n"
        f"OBSERVAÇÕES (MULTA/TAXA): {extraido['observacoes']}\n"
        f"STATUS PAGAMENTO: {extraido['autenticacao']}\n"
        f"------------------------------------"
    )

def extrair_comprovante_especifico(page):
    """Extrai dados do comprovante para bater com o boleto."""
    text = page.extract_text() or ""
    return f"--- DADOS DO COMPROVANTE ---\n{text[:1000]}\n----------------------------"

# ═══════════════════════════════════════════════════════════
#  ORQUESTRADOR HÍBRIDO
# ═══════════════════════════════════════════════════════════

def extrair_selo_projeto(page):
    """Extrai texto apenas do quadrante inferior direito (Selo/Carimbo)."""
    # Define a região do selo (geralmente os últimos 25% da largura e altura)
    width = float(page.width)
    height = float(page.height)
    
    # Bbox: (x0, y0, x1, y1) -> top-left to bottom-right
    # Vamos pegar a metade inferior (y0=height/2) e a metade direita (x0=width/2)
    region = (width * 0.5, height * 0.5, width, height)
    
    selo_page = page.within_bbox(region)
    text = selo_page.extract_text() or ""
    
    # Também tenta extrair tabelas nessa região (comum em quadros de áreas)
    tables = selo_page.extract_tables()
    table_data = []
    for table in tables:
        for row in table:
            row_clean = [str(c).replace('\n', ' ').strip() for c in row if c]
            if row_clean: table_data.append(" | ".join(row_clean))
            
    return (
        f"--- DADOS EXTRAÍDOS DO SELO DO PROJETO ---\n"
        f"TEXTO DETECTADO:\n{text[:1000]}\n"
        f"TABELAS NO SELO:\n{'\n'.join(table_data)}\n"
        f"-------------------------------------------"
    )

def analisar_processo_inteligente(pdf_path):
    """Orquestrador v5.2 com extração de Selo de Projetos."""
    if not HAS_PDFPLUMBER:
        print("[!] Instale pdfplumber: pip install pdfplumber")
        return None

    print(f"  [ROTEADOR] Analisando estrutura completa v5.2: {os.path.basename(pdf_path)}")
    extração_final = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text_preview = page.extract_text() or ""
            tipo = classificar_pagina(text_preview)
            
            # Filtro de Tamanho para RAM + Extração de Selo
            width_mm = float(page.width) * 0.352778
            if width_mm > 450:
                print(f"    - Pág {i}: Planta Gigante -> Extraindo apenas o Selo")
                content = extrair_selo_projeto(page)
                extração_final.append(f"## PÁGINA {i} [TIPO: PLANTA/PROJETO] (Extração de Selo)\n{content}\n")
                continue

            print(f"    - Pág {i}: {tipo}")
            
            header = f"## PÁGINA {i} [TIPO: {tipo}]"
            
            if tipo == "IPTU":
                content = extrair_iptu_especifico(page)
            elif tipo == "GUIA_PAGAMENTO":
                content = extrair_dam_especifico(page)
            elif tipo == "COMPROVANTE_PAGAMENTO":
                content = extrair_comprovante_especifico(page)
            elif tipo in ["ART", "PARECER_FISCAL", "LAUDO_ENGENHEIRO", "CERTIDAO_DECADENCIA", 
                         "PARECER_THAMIRES", "TRIAGEM", "CERTIDAO_AVERBACAO", "HABITE_SE", 
                         "ALVARA_CONSTRUCAO", "LAUDO_AVALIACAO", "PENDENCIA"]:
                # Documentos técnicos: preserva o texto digital completo
                content = text_preview
            elif tipo == "IDENTIDADE":
                # Apenas os primeiros dados para evitar LGPD/ruído de foto
                content = text_preview[:500]
            else:
                content = text_preview[:1500] 

            extração_final.append(f"{header}\n{content}\n")

    return "\n\n".join(extração_final)

def processar_pasta_inteligente():
    """Varre a pasta de entrada com a nova lógica de roteamento v5.1."""
    pdfs = glob.glob(os.path.join(PASTA_ENTRADA, "*.pdf"))
    if not pdfs:
        print(f"[!] Nenhum PDF encontrado em: {PASTA_ENTRADA}")
        return

    for pdf_path in pdfs:
        nome_base = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(PASTA_ENTRADA, f"{nome_base}_ROTEADO.md")
        
        print(f"\n{'=' * 62}")
        print(f"  PROCESSAMENTO INTELIGENTE v5.1: {os.path.basename(pdf_path)}")
        print(f"{'=' * 62}")

        conteudo = analisar_processo_inteligente(pdf_path)
        if conteudo:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"  [OK] Extração estruturada salva: {os.path.basename(output_path)}")

if __name__ == "__main__":
    processar_pasta_inteligente()

