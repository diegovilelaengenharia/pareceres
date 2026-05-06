"""
DEPRECATED — Shim de compatibilidade (Fase 16: Refatoração do Gerador DOCX).

Este arquivo foi convertido em um shim de re-exportação. O código real agora
vive no pacote generators/componentes/ (módulos temáticos).

Imports existentes como:
    from generators.componentes import build_corpo
continuam funcionando normalmente através deste shim.

Para novos desenvolvimentos, importe diretamente do módulo temático:
    from generators.componentes.corpo import build_corpo
"""

# Re-exporta tudo do pacote componentes/ para compatibilidade retroativa.
# Qualquer import de 'from generators.componentes import X' continua funcionando.
from generators.componentes import (
    build_titulo,
    build_identificacao,
    build_destinatario,
    build_dados_carimbo,
    build_corpo,
    build_conclusao_e_docs,
    build_conclusao_simples,
    build_assinatura,
    build_comunicado_pendencia,
    build_partes_envolvidas,
    build_historico_cronologico,
    build_memoria_calculo,
)

__all__ = [
    "build_titulo", "build_identificacao", "build_destinatario",
    "build_dados_carimbo", "build_corpo",
    "build_conclusao_e_docs", "build_conclusao_simples", "build_assinatura",
    "build_comunicado_pendencia",
    "build_partes_envolvidas", "build_historico_cronologico",
    "build_memoria_calculo",
]
