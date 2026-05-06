"""
Motor de Treinamento Contínuo — GEM SMOSU
=========================================
Analisa extrações híbridas e converte em 'Conhecimento de Caso' para a base.
"""

import os
import sys
import json
import re
from pathlib import Path

# Ajustar sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_ROOT = os.path.dirname(SCRIPT_DIR)
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from core.logger import log_ok, log_warn, log_err, log_info
from core.config import PASTA_BASE_CONHECIMENTO

TRAINING_FILE = Path(PASTA_BASE_CONHECIMENTO) / "casos_treinamento.jsonl"

def extrair_padroes(texto: str) -> dict:
    """Extrai padrões técnicos e descobre potenciais novas variáveis."""
    # Variáveis conhecidas (Legacy)
    dados = {
        "numero_processo": re.search(r"(?:Processo|Proc\.)\s*(?:nº|Nº)?\s*(\d+[/.-]\d+)", texto, re.I),
        "zoneamento": re.search(r"(ZUR\s*[123]|ZCRE|ZAE\s*[1234]|ZC|ZIND)", texto),
        "area": re.search(r"(?:Área|area|metragem)\s*(?:total)?\s*(?:de)?\s*(\d+[.,]\d+)\s*m²", texto, re.I),
        "leis": list(set(re.findall(r"(?:Lei|Decreto|LC)\s*(?:nº|Nº)?\s*(\d+(?:\.\d+)?(?:/\d+)?)", texto))),
        "bairro": re.search(r"Bairro\s*:?\s*([A-ZÀ-Úa-zà-ú\s0-9]+)", texto, re.I),
    }
    
    # --- DESCOBERTA DE NOVAS VARIÁVEIS (Inovação) ---
    # Busca por termos que seguem padrões de 'Chave: Valor' ainda não mapeados
    novos_termos = re.findall(r"([A-ZÀ-Ú][a-zà-ú\s]{3,20}):\s*([A-ZÀ-Úa-zà-ú0-9\s/.,º°-]{2,50})", texto)
    dados["descobertas"] = [f"{k.strip()}: {v.strip()}" for k, v in novos_termos if k.lower() not in ["bairro", "logradouro", "requerente", "assunto"]]

    # Busca por cláusulas de 'Observação' ou 'Notas' que podem conter regras novas
    notas_especiais = re.findall(r"(?:Obs|Nota|Importante):\s*([^\n.]{10,200})", texto, re.I)
    dados["clausulas_potenciais"] = list(set(notas_especiais))

    # Limpar resultados do regex
    for k, v in dados.items():
        if hasattr(v, "group"):
            dados[k] = v.group(1).strip()
        elif isinstance(v, list):
            pass
        else:
            dados[k] = None
            
    return dados

def registrar_insight(pdf_name: str, padroes: dict):
    """Registra novos termos e ideias em um arquivo de insights para o engenheiro."""
    INSIGHTS_FILE = Path(PASTA_BASE_CONHECIMENTO) / "LAB_INSIGHTS.md"
    
    if not padroes.get("descobertas") and not padroes.get("clausulas_potenciais"):
        return

    entry = [
        f"### 💡 Insight extraído de: {pdf_name}",
        "#### Novas Variáveis Detectadas:",
        *[f"- `{t}`" for t in padroes.get("descobertas", [])[:10]],
        "#### Cláusulas de Interesse (Regras de Negócio):",
        *[f"- {c}" for c in padroes.get("clausulas_potenciais", [])[:5]],
        "\n---\n"
    ]
    
    with open(INSIGHTS_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(entry) + "\n")

def registrar_treinamento(pdf_name: str, texto: str):
    """Registra o caso na base de treinamento e gera insights."""
    padroes = extrair_padroes(texto)
    registrar_insight(pdf_name, padroes)
    
    registro = {
        "arquivo": pdf_name,
        "data_treino": Path(pdf_name).stat().st_mtime if Path(pdf_name).exists() else 0,
        "contexto_resumido": texto[:1000].replace("\n", " "), 
        "padroes_detectados": padroes
    }
    
    try:
        with open(TRAINING_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        log_ok(f"Treinamento registrado para {pdf_name}")
        return True
    except Exception as e:
        log_err(f"Falha ao registrar treino: {e}")
        return False

def treinar_pasta(pasta_entrada: str):
    """Treina o sistema com todos os textos extraídos na pasta."""
    txts = list(Path(pasta_entrada).glob("*_TEXTO_EXTRAIDO.txt"))
    if not txts:
        log_warn("Nenhum arquivo de texto extraído encontrado para treinamento.")
        return
        
    log_info(f"Iniciando treinamento com {len(txts)} casos...")
    for txt in txts:
        with open(txt, "r", encoding="utf-8") as f:
            content = f.read()
        registrar_treinamento(txt.name, content)
    log_ok("Treinamento concluído.")

if __name__ == "__main__":
    from core.config import PASTA_ENTRADA
    treinar_pasta(PASTA_ENTRADA)
