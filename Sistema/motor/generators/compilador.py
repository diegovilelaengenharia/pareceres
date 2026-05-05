"""
Compilador central do sistema de geração de documentos SMOSU.
Lê arquivos JSON da pasta de entrada, aplica regras de pré-voo e orquestra os geradores DOCX.
"""

import os
import sys
import json
import glob
from docx import Document

# Adiciona o diretório atual e o diretório motor ao sys.path para importações
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOTOR_DIR = os.path.dirname(SCRIPT_DIR)

if MOTOR_DIR not in sys.path:
    sys.path.insert(0, MOTOR_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Importações do Motor
from core.config import PASTA_ENTRADA, PASTA_SAIDA, TIPOS_DOCUMENTO
from geradores_core import gerar

# Módulos de Análise e Especialidade
from utils import calculadora_indices   as calc_ind
from utils import alertas_decadencia     as decadencia
from utils import verificador_multas     as verif_multas
from utils import cobertura_considerandos as cob_cons
import gerador_sero           as gen_sero
from analyzers import inspetor_documental    as insp_doc

from core.logger import _OK, _WARN, _ERR, _INFO, log_ok, log_warn, log_err, log_info, _BLUE, _RESET


# ── Relatório pré-voo unificado ───────────────────────────────────────────────

def _relatorio_prevoo(dados: dict) -> tuple[bool, dict]:
    """
    Realiza todas as validações técnicas e cálculos urbanísticos antes da geração do DOCX.
    
    Args:
        dados: Dicionário com os dados do processo.
        
    Returns:
        Uma tupla (sucesso, resumo_cobertura).
    """
    print(f"\n{'=' * 62}")
    print(f"  PRÉ-VOO — Processo {dados.get('numero_processo', '?')}  |  {dados.get('requerente_nome', '?')}")
    print(f"  Tipo: {dados.get('tipo_relatorio', '?')}")
    print(f"{'=' * 62}")

    # 1. Cálculos Urbanísticos
    res_indices = calc_ind.calcular(dados)
    calc_ind.imprimir_relatorio(res_indices)

    # 2. Decadência Tributária
    res_decadencia = decadencia.verificar(dados)
    decadencia.imprimir_relatorio(res_decadencia)

    # 3. Verificação Semântica (Consistência)
    from core import consistencia
    err_cons, av_cons = consistencia.verificar(dados)
    consistencia.imprimir_relatorio(err_cons, av_cons, dados.get("tipo_relatorio", ""))

    # 4. Cobertura de Considerandos
    err_cob, av_cob, cob_ok, cob_falt = cob_cons.verificar(dados)
    cob_cons.imprimir_relatorio(err_cob, av_cob, cob_ok, cob_falt)

    # Retorna o resumo para uso no relatório pós-voo
    resumo_cob = {"alertas": err_cob + av_cob}
    return True, resumo_cob


def _relatorio_pos(dados: dict, caminho_doc: str, resumo_cob: dict):
    """
    Exibe informações e recomendações complementares após a geração bem-sucedida.
    
    Args:
        dados: Dados do processo.
        caminho_doc: Caminho do arquivo gerado.
        resumo_cob: Dados do relatório de cobertura.
    """
    print(f"\n{_BLUE}{'─' * 62}{_RESET}")
    
    # Link para Sero (se aplicável)
    if "alvara" in dados.get("tipo_relatorio", "") or "habitese" in dados.get("tipo_relatorio", ""):
        gen_sero.gerar_obs_sero(dados)

    print(f"{_BLUE}{'─' * 62}{_RESET}")


# ── Fluxo Principal ───────────────────────────────────────────────────────────

def main():
    """Ponto de entrada do compilador. Processa todos os arquivos JSON na pasta de entrada."""
    # Lista arquivos JSON na pasta de entrada
    arquivos = glob.glob(os.path.join(PASTA_ENTRADA, "*.json"))
    
    if not arquivos:
        print(f"\n  {_WARN}Nenhum arquivo JSON encontrado em: {PASTA_ENTRADA}")
        return

    print(f"\n[>] MODO EM LOTE: Escaneando pasta '{PASTA_ENTRADA}'")

    sucessos = 0
    erros = 0

    for arquivo in arquivos:
        # Ignora arquivos de esquema ou internos
        if "_esquema" in arquivo or "matriz_" in arquivo:
            continue

        print(f"\n[>] Processando arquivo: {os.path.basename(arquivo)}")
        
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except Exception as e:
            print(f"  {_ERR}Erro ao ler JSON: {e}")
            erros += 1
            continue

        # ── Suporte a Bundling (Emissão Múltipla) ──────────────────────────────
        # Se for o tipo mestre e não houver lista explícita, injeta o padrão
        if dados.get("tipo_relatorio") == "certidoes_separadas_localizacao_confrontacao":
            if not dados.get("documentos_emitir"):
                dados["documentos_emitir"] = ["parecer_tecnico", "certidao_localizacao", "certidao_confrontacao"]

        # ── Pré-voo ───────────────────────────────────────────────────────────
        sucesso_pre, resumo_cob = _relatorio_prevoo(dados)
        
        if not sucesso_pre:
            print(f"  {_WARN}Pré-voo reprovado para {os.path.basename(arquivo)}. Pulando...")
            continue

        # ── Preview HTML (se não estiver em modo silencioso) ──────────────────
        modo_sem_preview = "--sem-preview" in sys.argv
        if not modo_sem_preview:
            try:
                from ui.preview_html import gerar_preview
                alertas_html = resumo_cob.get("alertas", [])
                print(f"\n  {_INFO}Abrindo preview HTML no navegador...")
                gerar_preview(dados, alertas=alertas_html)

                print()
                print("  ─────────────────────────────────────────────────────")
                print("  Revise o preview no navegador e responda:")
                print("  [ENTER]  → Confirmar e gerar o DOCX")
                print("  [N]      → Cancelar este documento")
                print("  ─────────────────────────────────────────────────────")
                resp = input("  Sua escolha: ").strip().upper()
                if resp == "N":
                    print(f"  {_WARN}Documento cancelado pelo usuário.")
                    continue
            except Exception as e:
                print(f"  {_WARN}Preview indisponível: {e}")

        # ── Gerar documento ───────────────────────────────────────────────────
        caminho_saida_fornecido = dados.get("_caminho_saida")
        caminho_gerado = caminho_saida_fornecido
        try:
            pecas_selecionadas = dados.get("documentos_emitir", [])
            if pecas_selecionadas and isinstance(pecas_selecionadas, list):
                print(f"  {_INFO}Gerando MÚLTIPLAS PEÇAS ({len(pecas_selecionadas)})")
                for item in pecas_selecionadas:
                    # Suporte para string (novo padrão do painel) ou dict (padrão antigo do Gemini)
                    peca = item if isinstance(item, str) else item.get("tipo", "")
                    if not peca: continue
                    
                    dados_temp = dados.copy()
                    
                    # Validar se o ID técnico é reconhecido pelo motor
                    if peca not in TIPOS_DOCUMENTO:
                        print(f"  {_ERR}ID técnico inválido em documentos_emitir: {peca}")
                        continue
                        
                    dados_temp["tipo_relatorio"] = peca
                    
                    try:
                        caminho_peca = gerar(dados_temp, caminho_saida_fornecido)
                        print(f"  {_OK}Peça gerada: {os.path.basename(caminho_peca)}")
                        sucessos += 1
                    except Exception as e_peca:
                        print(f"  {_ERR}Erro na peça {peca}: {e_peca}")
                        erros += 1
            else:
                caminho_gerado = gerar(dados, caminho_saida_fornecido)
                print(f"  {_OK}DOCX gerado: {os.path.basename(caminho_gerado or arquivo)}")
                sucessos += 1
        except Exception as e:
            print(f"  {_ERR}Falha ao compilar {os.path.basename(arquivo)}: {e}")
            erros += 1
            continue

        # ── Precedentes + resumo de qualidade (pós-geração) ──────────────────
        _relatorio_pos(dados, caminho_gerado or "", resumo_cob)

    print(f"\n{'=' * 62}")
    print(f"  CONCLUÍDO: {sucessos} sucessos, {erros} erros.")
    print(f"{'=' * 62}\n")


if __name__ == "__main__":
    main()
