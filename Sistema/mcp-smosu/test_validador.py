import sys
import os

# Adiciona o diretório atual ao path para importar tools
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tools

def test_validador():
    print("="*60)
    print("Testando Validador Automático (Fase 2)")
    print("="*60)
    
    # Cenário 1: Tudo OK na ZUR1
    print("\nCenário 1: ZUR1 dentro dos limites")
    res1 = tools.validar_parametros_projeto(
        area_terreno=300,
        area_ocupada=150,        # TO = 50% (Max 60%)
        area_construida_total=300, # CA = 1.0 (Max 1.5)
        zona="ZUR1",
        area_permeavel=80       # TP = 26% (Min 20%)
    )
    print(res1)
    
    # Cenário 2: Erro de TO e CA na ZC2
    print("\nCenário 2: ZC2 com infrações")
    res2 = tools.validar_parametros_projeto(
        area_terreno=200,
        area_ocupada=180,        # TO = 90% (Max 70%)
        area_construida_total=800, # CA = 4.0 (Max ~2.8 ou 3.5)
        zona="ZC2",
        area_permeavel=10        # TP = 5% (Min 20%)
    )
    print(res2)

if __name__ == "__main__":
    test_validador()
