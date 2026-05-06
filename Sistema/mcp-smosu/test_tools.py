import pytest
import os
import json
from unittest.mock import patch, mock_open

# O import do tools vai considerar que o arquivo `tools.py` está no mesmo diretório
# Se houver problema de path, nós adicionamos sys.path
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tools

@pytest.fixture
def mock_base_conhecimento_dir():
    # Cria uma pasta temporária simulada ou usa um mock patch para o BASE_CONHECIMENTO_DIR
    return "/mock/base_conhecimento"

def test_load_json_inexistente():
    """Garante que a rotina lida bem com a falta de arquivos JSON, retornando None."""
    with patch('os.path.exists', return_value=False):
        resultado = tools._load_json("arquivo_fantasma.json")
        assert resultado is None

def test_consultar_codex_legal_inexistente():
    """Garante resposta elegante quando o codex legal não existir."""
    with patch('tools._load_json', return_value=None):
        resposta = tools.consultar_codex_legal("ZCS")
        assert "Erro: Arquivo codex_legal.json não encontrado" in resposta

def test_consultar_codex_legal_sucesso():
    """Garante que o codex retorna corretamente um bairro cadastrado."""
    mock_data = {
        "parametros_zonais": {
            "ZCS": {
                "Taxa de Ocupacao": "70%",
                "Coeficiente": "3"
            }
        }
    }
    with patch('tools._load_json', return_value=mock_data):
        resposta = tools.consultar_codex_legal("ZCS")
        assert "Parâmetros da Zona ZCS" in resposta
        assert "70%" in resposta

def test_consultar_indices_urbanisticos_sucesso():
    """Testa a busca de índices por zona ou bairro."""
    mock_data = {
        "Zona Comercial": {"TO": "80%"},
        "Bairro Centro": {"TO": "90%"}
    }
    with patch('tools._load_json', return_value=mock_data):
        resposta = tools.consultar_indices_urbanisticos("Centro")
        assert "Bairro Centro" in resposta
        assert "90%" in resposta

def test_consultar_indices_urbanisticos_nao_encontrado():
    """Testa quando a zona ou bairro não está no geo_oliveira."""
    mock_data = {"Bairro Rural": {"TO": "10%"}}
    with patch('tools._load_json', return_value=mock_data):
        resposta = tools.consultar_indices_urbanisticos("Centro")
        assert "Não foram encontrados dados urbanísticos" in resposta

@patch('glob.glob')
@patch('builtins.open', new_callable=mock_open, read_data="Raciocínio para aprovação de asbuilt...")
def test_buscar_diretriz_processo_sucesso(mock_file, mock_glob):
    """Testa a leitura de diretriz (markdown)."""
    mock_glob.return_value = ['/mock/base/raciocinio_regularizacao_asbuilt.md']
    resposta = tools.buscar_diretriz_processo("regularizacao")
    assert "Diretriz:" in resposta
    assert "asbuilt" in resposta

@patch('glob.glob')
@patch('builtins.open', new_callable=mock_open, read_data="Raciocínio para aprovação de asbuilt...")
def test_pesquisa_livre_leis_txt_sucesso(mock_file, mock_glob):
    """Testa pesquisa livre em texto."""
    mock_glob.return_value = ['/mock/base/leis_municipais.md']
    resposta = tools.pesquisa_livre_leis_txt("aprovação")
    assert "Resultados da Pesquisa Livre" in resposta
    assert "aprovação" in resposta

def test_pesquisa_livre_leis_txt_nao_encontrado():
    """Testa pesquisa livre quando a palavra não existe."""
    with patch('glob.glob', return_value=[]):
        resposta = tools.pesquisa_livre_leis_txt("termo_absurdo_123")
        assert "não foi encontrada" in resposta

@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data='{"arquivo": "proc_123", "padroes_detectados": {"numero_processo": "123", "zoneamento": "ZCS", "area": "200", "bairro": "Centro", "leis": ["Lei 1"]}}\n')
def test_consultar_historico_treinamento_sucesso(mock_file, mock_exists):
    """Testa leitura de jsonl no histórico de treinamento."""
    resposta = tools.consultar_historico_treinamento("ZCS")
    assert "Casos Similares Encontrados" in resposta
    assert "Proc: 123" in resposta
    assert "Zona: ZCS" in resposta

def test_calcular_multas_processo():
    """Testa o cálculo de multas (Art. 79 e Art. 39)."""
    mock_codex = {
        "parametros_zonais": {
            "ZUR3": {"to_max_pct": 70, "tp_min_pct": 20}
        }
    }
    with patch('tools._load_json', return_value=mock_codex):
        # Caso com multa Art. 79 e violação de TO/TP
        resposta = tools.calcular_multas_processo(
            area_irregular=154.08,
            zona="ZUR3",
            area_terreno=180.0,
            area_ocupada=154.08, # TO = 85.6% > 70%
            area_permeavel=0.0,    # TP = 0% < 20%
            tem_decadencia=False
        )
        assert "MULTA ART. 79" in resposta
        assert "MULTA ART. 39" in resposta
        assert "VIOLAÇÃO" in resposta
        assert "TOTAL GERAL ESTIMADO" in resposta

def test_validar_checklist_documentos():
    """Testa o validador de checklists."""
    mock_checklist = {
        "regularizacao": {
            "obrigatorios_bloqueantes": ["ART de execução"],
            "obrigatorios": ["Requerimento"],
            "base_legal": "Decreto 4149"
        }
    }
    with patch('tools._load_json', return_value=mock_checklist):
        # Caso com pendência
        resposta = tools.validar_checklist_documentos("regularizacao", "Requerimento assinado")
        assert "PROCESSO BLOQUEADO" in resposta
        assert "BLOQUEIO: ART de execução" in resposta
        
        # Caso completo
        resposta = tools.validar_checklist_documentos("regularizacao", "ART de execução, Requerimento")
        assert "APROVADO PARA ANÁLISE" in resposta

def test_analisar_decadencia():
    """Testa análise de decadência."""
    # Caso comprovado
    resposta = tools.analisar_decadencia(2010, "matricula", 200.0)
    assert "DECADÊNCIA COMPROVADA" in resposta
    assert "ISENTO" in resposta
    
    # Caso não comprovado (prova inválida)
    resposta = tools.analisar_decadencia(2010, "nenhuma", 200.0)
    assert "DECADÊNCIA NÃO COMPROVÁVEL" in resposta

def test_gerar_memoria_calculo_indices():
    """Testa geração de texto de memória de cálculo."""
    resposta = tools.gerar_memoria_calculo_indices(180.0, 120.0, 240.0, 36.0, "ZUR3")
    assert "Memória de Cálculo (ZUR3)" in resposta
    assert "66.67%" in resposta # TO
    assert "1.333" in resposta  # CA
    assert "20.00%" in resposta # TP

def test_consultar_documentos_emitir():
    """Testa sugestão de documentos."""
    resposta = tools.consultar_documentos_emitir("regularizacao", "aprovado_com_multa", tem_decadencia=True)
    assert "Alvará de Regularização" in resposta
    assert "Certidão de Decadência" in resposta

def test_verificar_excecoes_lote_pequeno():
    """Testa exceções para lotes <= 220m2."""
    # Lote pequeno em aprovação
    resposta = tools.verificar_excecoes_lote_pequeno(180.0, "aprovacao_novo", "ZUR3")
    assert "APLICA-SE A EXCEÇÃO" in resposta
    
    # Lote grande
    resposta = tools.verificar_excecoes_lote_pequeno(250.0, "aprovacao_novo", "ZUR3")
    assert "NÃO se enquadra" in resposta

def test_identificar_conflitos_processuais():
    """Testa identificação de conflitos."""
    resposta = tools.identificar_conflitos_processuais("Centro", "Aparecida", tem_app=True)
    assert "CONFLITO" in resposta
    assert "RESTRIÇÃO" in resposta
    assert "CODEMA" in resposta

def test_estruturar_historico_cronologico():
    """Testa estruturação de histórico."""
    eventos = [{"data": "01/01/2026", "txt": "Vistoria Fiscal"}]
    resposta = tools.estruturar_historico_cronologico(eventos)
    assert "vistoria_fiscal" in resposta
    assert "01/01/2026" in resposta
