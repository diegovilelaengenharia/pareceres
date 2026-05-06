import pytest
import os
import json
import shutil
import tempfile
from unittest.mock import patch, MagicMock

# Ajustar sys.path para importar os módulos do motor
import sys
_MOTOR_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _MOTOR_DIR not in sys.path:
    sys.path.insert(0, _MOTOR_DIR)

from generators import geradores_core
from core import config

@pytest.fixture
def mock_dados_parecer():
    """Mock de dados JSON para um parecer técnico."""
    return {
        "tipo_relatorio": "alvara_regularizacao",
        "numero_processo": "123/2026",
        "requerente": "João da Silva",
        "assunto": "Regularização de Edificação",
        "logradouro": "Rua das Flores, 10",
        "bairro": "Centro",
        "area_terreno": "250,00m²",
        "area_total_construida": "180,00m²",
        "taxa_ocupacao": "72,00%",
        "taxa_permeabilidade": "15,00%",
        "considerandos": ["O imóvel possui habite-se anterior.", "A área ampliada cumpre os afastamentos."],
        "fundamentacao_legal": ["Art. 10 da Lei 123"],
        "conclusao": "Aprovação recomendada.",
        "memoria_de_calculo": "Área Base: 100m2 + Ampliação: 80m2 = 180m2"
    }

@pytest.fixture
def temp_output_dir():
    """Cria um diretório temporário para as saídas de teste."""
    tmp = tempfile.mkdtemp()
    # Patch direto no módulo que usa a variável
    with patch('generators.geradores_core.PASTA_SAIDA', tmp):
        yield tmp
    shutil.rmtree(tmp)

def test_gerar_docx_integracao(mock_dados_parecer, temp_output_dir):
    """Teste de integração: gera um DOCX real a partir de um mock JSON."""

    # Mockar a geração de PDF para não depender de Word/LibreOffice no ambiente de teste
    with patch('generators.geradores_core._gerar_pdf') as mock_pdf:
        caminho = geradores_core.gerar(mock_dados_parecer)

        assert os.path.exists(caminho)
        assert caminho.endswith(".docx")
        assert "João Da Silva" in caminho  # Nome real conforme o mock
        mock_pdf.assert_called_once()
def test_gerar_parecer_simples(temp_output_dir):
    """Testa a geração de um parecer simples."""
    dados = {
        "tipo_relatorio": "certidao_localizacao",
        "numero_processo": "456/2026",
        "requerente": "Maria Oliveira",
        "paragrafo_abertura": "Trata-se de solicitação de certidão.",
        "considerandos": "Documentação ok.",
        "conclusao": "Certidão emitida.",
        "memoria_de_calculo": "Cálculo simples."
    }

    with patch('generators.geradores_core._gerar_pdf'):
        caminho = geradores_core.gerar(dados)
        assert os.path.exists(caminho)
        assert "Certidao Localizacao - 456-2026" in caminho

def test_schema_resilience(temp_output_dir):
    """Testa se o motor lida com campos aninhados (resiliência)."""
    dados = {
        "tipo_relatorio": "oficio_meio_ambiente",
        "campos_obrigatorios": {
            "numero_processo": "789/2026",
            "destinatario_titulo": "Ilmo. Sr. Secretário"
        },
        "assunto": "Informação técnica",
        "paragrafo_abertura": "Segue informação..."
    }

    with patch('generators.geradores_core._gerar_pdf'):
        caminho = geradores_core.gerar(dados)
        assert os.path.exists(caminho)
        assert "Oficio Meio Ambiente" in caminho
def test_error_missing_type():
    """Garante que falha se não houver tipo_relatorio."""
    with pytest.raises(ValueError, match="tipo_relatorio"):
        geradores_core.gerar({"numero_processo": "1"})

if __name__ == "__main__":
    pytest.main([__file__])
