import os
import sys
from typing import List, Dict
from mcp.server.fastmcp import FastMCP
import tools

# Initialize FastMCP server
mcp = FastMCP("SMOSU Conhecimento")

@mcp.tool()
def prever_pendencias_recorrentes(tipo_processo: str, zona: str = None, area_terreno: float = None) -> str:
    """
    Analisa o perfil do projeto e prevê pendências ou multas comuns baseadas no histórico de Oliveira/MG.
    Use no início da análise para antecipar problemas (ex: falta de RT de execução, multas do Art. 79 ou Art. 39).
    """
    return tools.prever_pendencias_recorrentes(tipo_processo, zona, area_terreno)

@mcp.tool()
def buscar_conceito_legal(query: str) -> str:
    """
    Realiza uma busca semântica por conceito na base de leis e manuais.
    Use quando você não souber a palavra exata da lei, mas souber o conceito (ex: 'vagas para carros' em vez de 'estacionamento').
    """
    return tools.buscar_conceito_legal(query)

@mcp.tool()
def validar_parametros_projeto(
    area_terreno: float, 
    area_ocupada: float, 
    area_construida_total: float, 
    zona: str,
    area_permeavel: float = 0
) -> str:
    """
    Calcula e valida automaticamente os índices urbanísticos do projeto (TO, CA, TP) contra os limites da zona informada.
    Útil para verificar se um projeto atende à LC 267/2019.
    """
    return tools.validar_parametros_projeto(area_terreno, area_ocupada, area_construida_total, zona, area_permeavel)

@mcp.tool()
def consultar_codex_legal(termo_busca: str) -> str:
    """
    Busca estruturada no arquivo codex_legal.json.
    Use esta ferramenta para encontrar artigos, incisos e alíneas exatas das leis do município (Código de Obras, Plano Diretor, Uso e Ocupação).
    """
    return tools.consultar_codex_legal(termo_busca)

@mcp.tool()
def consultar_indices_urbanisticos(zona_ou_bairro: str) -> str:
    """
    Busca na base estruturada geo_oliveira.json os índices urbanísticos (Taxa de Ocupação, Coeficiente de Aproveitamento, Recuos, etc).
    Passe o nome do bairro ou a sigla da zona (ex: 'ZCS', 'Bairro Centro').
    """
    return tools.consultar_indices_urbanisticos(zona_ou_bairro)

@mcp.tool()
def buscar_diretriz_processo(tipo_processo: str) -> str:
    """
    Retorna o raciocínio e o fluxo de trabalho exigido para aprovar ou regularizar um tipo específico de projeto.
    Use quando tiver dúvidas sobre 'como' analisar um processo (ex: 'regularização as-built', 'alvará de aprovação').
    """
    return tools.buscar_diretriz_processo(tipo_processo)

@mcp.tool()
def pesquisa_livre_leis_txt(palavra_chave: str) -> str:
    """
    Varre todos os arquivos de texto (.md e .txt) na base de conhecimento buscando o termo.
    Use como último recurso se as ferramentas estruturadas não retornarem o que você precisa.
    """
    return tools.pesquisa_livre_leis_txt(palavra_chave)

@mcp.tool()
def consultar_historico_treinamento(termo_busca: str) -> str:
    """
    Busca casos similares na base de treinamento (casos_treinamento.jsonl).
    Retorna padrões detectados em processos anteriores (zoneamento, leis, áreas, bairros).
    Use para aprender com a experiência acumulada do sistema.
    """
    return tools.consultar_historico_treinamento(termo_busca)

@mcp.tool()
def calcular_multas_processo(
    area_irregular: float,
    zona: str,
    area_terreno: float,
    area_ocupada: float,
    area_permeavel: float,
    tem_decadencia: bool = False
) -> str:
    """
    Calcula com precisão todas as multas aplicáveis (Art. 79 Lei 1.544 + Art. 39 LC 267/2019).
    Retorna valor final, base legal e memória de cálculo formatada para o parecer.
    """
    return tools.calcular_multas_processo(area_irregular, zona, area_terreno, area_ocupada, area_permeavel, tem_decadencia)

@mcp.tool()
def validar_checklist_documentos(tipo_processo: str, documentos_apresentados: str) -> str:
    """
    Recebe o tipo de processo e retorna o checklist de documentos obrigatórios com status baseado no Decreto 4.149/2019.
    Use para identificar pendências de documentos logo no início da análise.
    """
    return tools.validar_checklist_documentos(tipo_processo, documentos_apresentados)

@mcp.tool()
def analisar_decadencia(ano_construcao: int, tipo_prova: str, area_total: float, area_averbada: float = 0.0) -> str:
    """
    Análise jurídica precisa sobre decadência fiscal (CTN Art. 150 §4º).
    Informa se a multa do Art. 79 é aplicável ou se a área já está consolidada (>5 anos).
    """
    return tools.analisar_decadencia(ano_construcao, tipo_prova, area_total, area_averbada)

@mcp.tool()
def gerar_memoria_calculo_indices(
    area_terreno: float,
    area_coberta: float,
    area_construida_total: float,
    area_permeavel: float,
    zona: str,
    area_garagem_descoberta: float = 0.0
) -> str:
    """
    Gera a memória de cálculo completa dos índices urbanísticos (TO, CA, TP).
    O resultado é formatado para ser colado diretamente no campo 'memoria_de_calculo' do parecer técnico.
    """
    return tools.gerar_memoria_calculo_indices(area_terreno, area_coberta, area_construida_total, area_permeavel, zona, area_garagem_descoberta)

@mcp.tool()
def consultar_documentos_emitir(
    tipo_processo: str,
    resultado_analise: str,
    tem_decadencia: bool = False,
    tem_divergencia_cadastral: bool = False
) -> str:
    """
    Retorna a lista exata e ordenada de documentos oficiais a emitir (Alvarás, Habite-se, Certidões) baseada no desfecho da análise.
    """
    return tools.consultar_documentos_emitir(tipo_processo, resultado_analise, tem_decadencia, tem_divergencia_cadastral)

@mcp.tool()
def verificar_excecoes_lote_pequeno(area_terreno: float, tipo_processo: str, zona: str) -> str:
    """
    Verifica se o lote (<= 220m²) possui isenções de TO ou Afastamentos conforme o Art. 9º §13 da LC 267/2019.
    Essencial para evitar exigências indevidas em lotes populares.
    """
    return tools.verificar_excecoes_lote_pequeno(area_terreno, tipo_processo, zona)

@mcp.tool()
def buscar_logradouro_oficial(nome_rua: str) -> str:
    """
    Verifica o nome oficial de uma rua/logradouro conforme Decretos de Denominação, evitando nomes desatualizados no documento final.
    """
    return tools.buscar_logradouro_oficial(nome_rua)

@mcp.tool()
def identificar_conflitos_processuais(
    bairro_sri: str,
    bairro_pmo: str,
    tem_app: bool = False,
    tem_tombamento: bool = False,
    divergencia_area_pct: float = 0.0
) -> str:
    """
    Identifica conflitos entre Matrícula (SRI) e Cadastro (PMO), restrições de APP ou IEPHA.
    Sugere automaticamente a emissão de Certidões de Localização Corretiva ou Ofícios.
    """
    return tools.identificar_conflitos_processuais(bairro_sri, bairro_pmo, tem_app, tem_tombamento, divergencia_area_pct)

@mcp.tool()
def estruturar_historico_cronologico(eventos_raw: List[Dict[str, str]]) -> str:
    """
    Organiza uma lista de eventos brutos (data e descrição) no formato 'historico_cronologico' exigido pelo JSON do parecer.
    Padroniza os tipos de evento (abertura_processo, vistoria_fiscal, etc).
    """
    return tools.estruturar_historico_cronologico(eventos_raw)

@mcp.tool()
def buscar_modelo_parecer(contexto_caso: str) -> str:
    """
    Busca os melhores modelos de parecer/certidão baseados no contexto do caso (ex: 'habite-se multa permeável').
    Retorna os 3 modelos mais similares do catálogo da SMOSU.
    """
    return tools.buscar_modelo_parecer(contexto_caso)

if __name__ == "__main__":
    # MCP servers on stdio are common for local integrations
    mcp.run()
