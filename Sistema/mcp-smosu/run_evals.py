import xml.etree.ElementTree as ET
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    evals_path = os.path.join(SCRIPT_DIR, "evals.xml")
    if not os.path.exists(evals_path):
        print("Arquivo evals.xml não encontrado!")
        return

    try:
        tree = ET.parse(evals_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Erro ao fazer o parse do evals.xml: {e}")
        return

    print("="*60)
    print("Iniciando Runner de Avaliações (Evals) do MCP-SMOSU")
    print("="*60)
    
    total = 0
    for eval_node in root.findall('eval'):
        eval_id = eval_node.get('id')
        question = eval_node.find('question').text
        expected = eval_node.find('expected').text
        
        print(f"\n[Eval #{eval_id}]")
        print(f"Pergunta: {question.strip()}")
        print(f"Ação/Chamada Esperada: {expected.strip()}")
        print("-" * 60)
        total += 1
        
    print(f"\nTotal de {total} evals listados.")
    print("Para avaliação fim-a-fim completa, conecte este script a um modelo judger (LLM).")

if __name__ == '__main__':
    main()