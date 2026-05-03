import os
import json
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_RETRO = os.path.join(os.path.dirname(SCRIPT_DIR), "03_Retroalimentacao_e_Estudos")
PASTA_HIST = os.path.join(PASTA_RETRO, "historico")
ARQUIVO_DECISOES = os.path.join(PASTA_HIST, "decisoes_triagem.jsonl")

def calcular_metricas():
    if not os.path.exists(ARQUIVO_DECISOES):
        return {
            "total_processos": 0,
            "score_medio": 0,
            "taxa_acerto_ia": 0,
            "top_condicionantes": []
        }
        
    total_processos = 0
    soma_score = 0
    acertos_ia = 0
    todas_condicionantes = []
    
    sugestoes_por_peca = Counter()
    aceitacoes_por_peca = Counter()
    
    with open(ARQUIVO_DECISOES, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            try:
                decisao = json.loads(linha)
                total_processos += 1
                soma_score += float(decisao.get("score", 0))
                
                sugeridas = set(decisao.get("pecas_sugeridas", []))
                aceitas = set(decisao.get("pecas_aceitas", []))
                
                for p in sugeridas:
                    sugestoes_por_peca[p] += 1
                    if p in aceitas:
                        aceitacoes_por_peca[p] += 1
                
                if aceitas and aceitas.issubset(sugeridas):
                    acertos_ia += 1
                    
                conds = decisao.get("condicionantes", [])
                todas_condicionantes.extend(conds)
                
            except Exception as e:
                pass
                
    if total_processos == 0:
        return {"total_processos": 0, "score_medio": 0, "taxa_acerto_ia": 0, "top_condicionantes": [], "taxas_rejeicao": {}}
        
    score_medio = round(soma_score / total_processos, 1)
    taxa_acerto_ia = round((acertos_ia / total_processos) * 100, 1)
    
    contagem_conds = Counter(todas_condicionantes)
    top_condicionantes = [{"texto": k, "qtd": v} for k, v in contagem_conds.most_common(5)]
    
    taxas_rejeicao = {}
    for p, total in sugestoes_por_peca.items():
        if total >= 3:
            rej = 1.0 - (aceitacoes_por_peca[p] / total)
            taxas_rejeicao[p] = round(rej * 100, 1)
    
    return {
        "total_processos": total_processos,
        "score_medio": score_medio,
        "taxa_acerto_ia": taxa_acerto_ia,
        "top_condicionantes": top_condicionantes,
        "taxas_rejeicao": taxas_rejeicao
    }

def exportar_relatorio():
    """Gera um relatório markdown formatado para ser colado no Gemini."""
    metricas = calcular_metricas()
    if metricas["total_processos"] == 0:
        return {"ok": False, "erro": "Sem processos analisados para gerar relatório."}
        
    relatorio = f"""# Relatório Semanal de Triagem e IA - SMOSU

## Resumo Geral
- **Total de Processos Analisados:** {metricas['total_processos']}
- **Score Médio de Saúde (Documentação):** {metricas['score_medio']}%
- **Taxa de Acerto da IA (Sugestões):** {metricas['taxa_acerto_ia']}%

## Padrões e Condicionantes Frequentes
Abaixo estão os erros e condicionantes técnicas mais recorrentes desta semana:
"""
    for c in metricas['top_condicionantes']:
        relatorio += f"- ({c['qtd']} processos) {c['texto']}\n"
        
    relatorio += """
## Instruções de Aprendizado (Para o Gemini)
Por favor, analise as condicionantes acima. Se um padrão se repete muito, você deve passar a inspecioná-lo de forma mais rígida durante a Fase Zero, exigindo a documentação correspondente com antecedência para evitar retrabalho.
"""
    
    arq_saida = os.path.join(PASTA_RETRO, "relatorio_semanal_treino.md")
    os.makedirs(os.path.dirname(arq_saida), exist_ok=True)
    with open(arq_saida, "w", encoding="utf-8") as f:
        f.write(relatorio)
        
    return {"ok": True, "caminho": arq_saida, "conteudo": relatorio}

if __name__ == "__main__":
    import pprint
    pprint.pprint(calcular_metricas())


