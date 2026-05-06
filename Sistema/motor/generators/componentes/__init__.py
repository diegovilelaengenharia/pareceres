"""
Pacote componentes — re-exporta todas as funções públicas para compatibilidade retroativa.

Consumidores existentes (geradores_core.py, compilador_livre.py, etc.) que usam:
    from generators.componentes import build_corpo
continuam funcionando sem nenhuma alteração.
"""
from generators.componentes.tabelas import (
    build_titulo,
    build_identificacao,
    build_destinatario,
    build_dados_carimbo,
    build_partes_envolvidas,
    build_historico_cronologico,
)
from generators.componentes.corpo import build_corpo, _ensure_list
from generators.componentes.conclusao import (
    build_conclusao_e_docs,
    build_conclusao_simples,
    add_doc_item,
)
from generators.componentes.assinatura import build_assinatura
from generators.componentes.comunicado import build_comunicado_pendencia
from generators.componentes.calculo import build_memoria_calculo

__all__ = [
    "build_titulo", "build_identificacao", "build_destinatario",
    "build_dados_carimbo", "build_corpo",
    "build_conclusao_e_docs", "build_conclusao_simples", "build_assinatura",
    "build_comunicado_pendencia",
    "build_partes_envolvidas", "build_historico_cronologico",
    "build_memoria_calculo", "_ensure_list", "add_doc_item",
]
