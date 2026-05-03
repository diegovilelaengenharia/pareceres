"""
Detector de Dessincronização de Templates — Motor GEM / SMOSU Oliveira-MG

Este script audita os modelos JSON públicos (0_Modelos_Prontos/) contra 
o validador de schema interno e os templates técnicos do sistema.

Garante que o que o usuário vê (modelos) é exatamente o que o motor espera.
"""

import json
import os
import sys
import glob

# Ajustar sys.path para encontrar os subpacotes do motor
# O script está em _Sistema_Interno/01_Motor_Python/scripts/
# A raiz do motor é _Sistema_Interno/01_Motor_Python/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_ROOT = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(ENGINE_ROOT))

if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

from core.schema_validator import validar
from core.logger import log_ok, log_warn, log_err, log_info

def carregar_json(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

def check_templates():
    PASTA_MODELOS = os.path.join(PROJECT_ROOT, "Modelos")
    PASTA_TEMPLATES = os.path.join(ENGINE_ROOT, "templates")
    
    if not os.path.exists(PASTA_MODELOS):
        log_err(f"Pasta de modelos não encontrada: {PASTA_MODELOS}")
        return False

    modelos = glob.glob(os.path.join(PASTA_MODELOS, "MODELO_*.json"))
    if not modelos:
        log_warn(f"Nenhum arquivo MODELO_*.json encontrado em {PASTA_MODELOS}")
        return True

    sucesso_geral = True
    
    print("\n" + "="*60)
    print("  AUDITORIA DE MODELOS PÚBLICOS vs MOTOR INTERNO")
    print("="*60)

    for path_modelo in sorted(modelos):
        nome_modelo = os.path.basename(path_modelo)
        dados = carregar_json(path_modelo)
        
        if dados is None:
            log_err(f"[{nome_modelo}] Falha ao ler ou JSON inválido.")
            sucesso_geral = False
            continue

        tipo = dados.get("tipo_relatorio")
        if not tipo:
            log_err(f"[{nome_modelo}] Chave 'tipo_relatorio' ausente.")
            sucesso_geral = False
            continue

        # 1. Validar contra o Schema Validator
        erros, avisos = validar(dados)
        
        # 2. Validar contra o Template JSON específico (campos_obrigatorios)
        path_template = os.path.join(PASTA_TEMPLATES, f"{tipo}.json")
        if os.path.exists(path_template):
            template_dados = carregar_json(path_template)
            if template_dados and "campos_obrigatorios" in template_dados:
                obrigatorios = template_dados["campos_obrigatorios"]
                for campo in obrigatorios:
                    if campo not in dados:
                        erros.append(f"Campo exigido pelo template técnico '{tipo}.json' ausente no modelo: '{campo}'")

        if erros:
            log_err(f"[FALHA] {nome_modelo} ({tipo})")
            for e in erros:
                print(f"   ❌ {e}")
            sucesso_geral = False
        elif avisos:
            log_warn(f"[AVISO] {nome_modelo} ({tipo})")
            for a in avisos:
                print(f"   ⚠️ {a}")
        else:
            log_ok(f"[OK]    {nome_modelo} ({tipo})")

    print("="*60)
    if sucesso_geral:
        log_ok("Auditoria concluída: Modelos públicos sincronizados.")
    else:
        log_err("Auditoria falhou: Modelos públicos precisam de atualização.")
    print("="*60 + "\n")

    return sucesso_geral

if __name__ == "__main__":
    if not check_templates():
        sys.exit(1)
    sys.exit(0)
