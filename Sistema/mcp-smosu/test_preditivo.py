import sys
import os

# Adiciona o diretório atual ao path para importar tools
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tools

def test_preditivo():
    print("="*60)
    print("Testando Inteligência Preditiva (Fase 4)")
    print("="*60)
    
    # Cenário 1: Regularização na ZUR3
    print("\nCenário 1: Regularização na ZUR3")
    res1 = tools.prever_pendencias_recorrentes("Regularização As-Built", zona="ZUR3")
    print(res1)
    
    # Cenário 2: Aprovação de Lote Pequeno
    print("\nCenário 2: Aprovação de Lote Pequeno (150m²)")
    res2 = tools.prever_pendencias_recorrentes("Aprovação de Projeto Novo", area_terreno=150)
    print(res2)
    
    # Cenário 3: Reforma Comercial
    print("\nCenário 3: Reforma Comercial")
    res3 = tools.prever_pendencias_recorrentes("Reforma de Galpão", zona="ZC")
    print(res3)

if __name__ == "__main__":
    test_preditivo()
