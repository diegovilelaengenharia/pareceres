import sys
import os

# Adiciona o diretório atual ao path para importar tools
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tools

def test_semantic_search():
    print("="*60)
    print("Testando Busca Semântica (Fase 1)")
    print("="*60)
    
    queries = [
        "espaço para estacionar veículos",
        "construir em beira de rio",
        "como regularizar casa pronta"
    ]
    
    for q in queries:
        print(f"\nQuery: {q}")
        resultado = tools.buscar_conceito_legal(q, top_k=2)
        print(resultado)
        print("-" * 60)

if __name__ == "__main__":
    test_semantic_search()
