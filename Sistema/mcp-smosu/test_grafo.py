import sys
import os

# Adiciona o diretório atual ao path para importar tools
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tools

def test_grafo():
    print("="*60)
    print("Testando Grafo de Dependências Legais (Fase 3)")
    print("="*60)
    
    # Busca por uma lei que tem correlações
    print("\nBusca: 'LC 267/2019'")
    res1 = tools.consultar_codex_legal("LC 267/2019")
    print(res1)
    
    # Busca por outra lei
    print("\nBusca: 'Lei 1.544/86'")
    res2 = tools.consultar_codex_legal("Lei 1.544/86")
    print(res2)

if __name__ == "__main__":
    test_grafo()
