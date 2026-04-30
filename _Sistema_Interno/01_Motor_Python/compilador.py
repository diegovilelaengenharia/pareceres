"""
Gerador Automático de Documentos – Prefeitura de Oliveira / SMOSU
Orquestrador principal – despacha para os geradores especializados.

Uso: python _engine\\compilador.py dados.json [saida.docx]
"""

import sys
import json
import os
import glob

# Adicionar o diretório do script ao path para imports locais
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from config import TIPOS_DOCUMENTO
from geradores import gerar

# Módulos de análise pré-voo
import calculadora_indices    as calc_idx
import alertas_decadencia     as alerta_dec
import consistencia           as consist
import precedentes            as prec
import verificador_multas     as verif_multas
import cobertura_considerandos as cob_cons
import gerador_sero           as gen_sero
import inspetor_documental    as insp_doc

# ── Cores do terminal (colorama) ──────────────────────────────────────────────
try:
    from colorama import init as _colorama_init, Fore, Style
    _colorama_init(autoreset=True)
    _OK    = Fore.GREEN  + Style.BRIGHT
    _WARN  = Fore.YELLOW + Style.BRIGHT
    _ERR   = Fore.RED    + Style.BRIGHT
    _INFO  = Fore.CYAN   + Style.BRIGHT
    _RESET = Style.RESET_ALL
    _BLUE  = Fore.BLUE   + Style.BRIGHT
except ImportError:
    _OK = _WARN = _ERR = _INFO = _RESET = _BLUE = ""

def _ok(msg):   return f"{_OK}[OK]{_RESET} {msg}"
def _warn(msg): return f"{_WARN}[WARN]{_RESET} {msg}"
def _err(msg):  return f"{_ERR}[ERR]{_RESET} {msg}"
def _info(msg): return f"{_INFO}[INFO]{_RESET} {msg}"


# ── Relatório pré-voo unificado ───────────────────────────────────────────────

def _relatorio_prevoo(dados: dict) -> tuple[bool, dict]:
    """
    Executa todas as análises antes de gerar o documento.
    Retorna (pode_prosseguir, resumo_cobertura).
    """
    tipo      = dados.get("tipo_relatorio", "?")
    processo  = dados.get("numero_processo", "?")
    requerente = dados.get("requerente", dados.get("proprietario_nome", "?"))

    print()
    print(f"{_BLUE}{'=' * 62}{_RESET}")
    print(f"{_BLUE}  PRÉ-VOO — Processo {processo}  |  {requerente}{_RESET}")
    print(f"{_BLUE}  Tipo: {tipo}{_RESET}")
    print(f"{_BLUE}{'=' * 62}{_RESET}")

    tem_erro_bloqueante = False
    alertas_prevoo: list = []  # coletados para o preview HTML

    # ── 1. Calculadora de índices urbanísticos ────────────────────────────────
    try:
        res_idx = calc_idx.calcular(dados)
        calc_idx.imprimir_relatorio(res_idx)
        for e in res_idx.get("erros", []):
            alertas_prevoo.append({"nivel": "erro", "msg": e})
            print(f"  {_err(e)}")
        for a in res_idx.get("avisos", []):
            alertas_prevoo.append({"nivel": "aviso", "msg": a})
    except Exception as e:
        print(f"  {_warn(f'Calculadora de índices indisponível: {e}')}")

    # ── 2. Alerta de decadência ───────────────────────────────────────────────
    try:
        res_dec = alerta_dec.verificar(dados)
        alerta_dec.imprimir_relatorio(res_dec)
        for a in res_dec.get("avisos", []):
            alertas_prevoo.append({"nivel": "aviso", "msg": a})
    except Exception as e:
        print(f"  {_warn(f'Módulo de decadência indisponível: {e}')}")

    # ── 3. Consistência semântica ─────────────────────────────────────────────
    try:
        erros_sem, avisos_sem = consist.verificar(dados)
        consist.imprimir_relatorio(erros_sem, avisos_sem, tipo)
        for e in erros_sem:
            alertas_prevoo.append({"nivel": "erro", "msg": e})
    except Exception as e:
        print(f"  {_warn(f'Módulo de consistência indisponível: {e}')}")

    # ── 3b. Inspeção Documental (Triagem Inteligente) ─────────────────────────
    try:
        if "analise_documental" in dados:
            res_insp = insp_doc.inspecionar(dados)
            insp_doc.imprimir_relatorio(res_insp, tipo)
            
            if res_insp.get("bloqueantes_faltando", 0) > 0:
                tem_erro_bloqueante = True
                for p in res_insp.get("pendencias", []):
                    if p.get("bloqueante"):
                        alertas_prevoo.append({"nivel": "erro", "msg": f"FALTA BLOQUEANTE: {p['documento']}"})
    except Exception as e:
        print(f"  {_warn(f'Módulo de inspeção documental indisponível: {e}')}")

    # ── 4. Verificação de cálculo de multas ───────────────────────────────────
    try:
        erros_multas, avisos_multas, resumo_multas = verif_multas.verificar(dados)
        verif_multas.imprimir_relatorio(erros_multas, avisos_multas, resumo_multas)
        for e in erros_multas:
            alertas_prevoo.append({"nivel": "erro", "msg": e})
    except Exception as e:
        print(f"  {_warn(f'Módulo de multas indisponível: {e}')}")

    # ── 5. Cobertura temática dos considerandos ───────────────────────────────
    cobertos: set = set()
    resumo_cob: dict = {}
    try:
        erros_cob, avisos_cob, cobertos, faltando = cob_cons.verificar(dados)
        cob_cons.imprimir_relatorio(erros_cob, avisos_cob, cobertos, faltando)
        resumo_cob = {
            "cobertos": sorted(cobertos),
            "faltando": sorted(faltando - cobertos),
            "n_total":  len(cob_cons._TEMAS),
        }
        for e in erros_cob:
            alertas_prevoo.append({"nivel": "aviso", "msg": e})
    except Exception as e:
        print(f"  {_warn(f'Módulo de cobertura temática indisponível: {e}')}")

    # ── 6. SERO/INSS metadata ─────────────────────────────────────────────────
    tem_sero = bool(dados.get("sero_metadata"))
    try:
        erros_sero, avisos_sero = gen_sero.validar(dados)
        gen_sero.imprimir_relatorio(erros_sero, avisos_sero)
    except Exception as e:
        print(f"  {_warn(f'Módulo SERO indisponível: {e}')}")

    resumo_cob["tem_sero"]        = tem_sero
    resumo_cob["tem_multas"]      = bool(dados.get("multas_calculadas"))
    resumo_cob["tem_excecoes"]    = bool(dados.get("excecoes_aplicadas"))
    resumo_cob["tem_historico"]   = bool(dados.get("historico_cronologico"))
    resumo_cob["tem_partes"]      = bool(dados.get("partes_envolvidas"))
    resumo_cob["alertas"]         = alertas_prevoo

    return not tem_erro_bloqueante, resumo_cob


def _relatorio_pos(dados: dict, caminho_docx: str, resumo_cob: dict) -> None:
    """Exibe precedentes e resumo de cobertura após a geração do documento."""
    try:
        prec.imprimir_relatorio(dados)
    except Exception as e:
        print(f"  {_warn(f'Módulo de precedentes indisponível: {e}')}")

    nome_doc = os.path.basename(caminho_docx) if caminho_docx else "documento"
    cobertos = resumo_cob.get("cobertos", [])
    faltando = resumo_cob.get("faltando", [])
    n_total  = resumo_cob.get("n_total", 8)
    n_cob    = len(cobertos)

    print(f"\n{_BLUE}{'=' * 62}{_RESET}")
    print(f"{_BLUE}  RESUMO DE QUALIDADE — {nome_doc}{_RESET}")

    cobertura_str = f"{n_cob}/{n_total}"
    if n_cob == n_total:
        print(f"  {_ok(f'Temas cobertos: {cobertura_str} — completo!')}")
    elif n_cob >= n_total * 0.7:
        falt_str = ', '.join(faltando) if faltando else ""
        print(f"  {_warn(f'Temas cobertos: {cobertura_str}  (faltam: {falt_str})')}")
    else:
        falt_str = ', '.join(faltando) if faltando else ""
        print(f"  {_err(f'Temas cobertos: {cobertura_str}  (faltam: {falt_str})')}")

    def _flag(val, label):
        if val:
            print(f"  {_ok(label)}")
        else:
            print(f"  {_warn(label + ' — ausente')}")

    _flag(resumo_cob.get("tem_multas"),    "multas_calculadas")
    _flag(resumo_cob.get("tem_excecoes"), "excecoes_aplicadas")
    _flag(resumo_cob.get("tem_sero"),     "sero_metadata")
    _flag(resumo_cob.get("tem_historico"),"historico_cronologico")
    _flag(resumo_cob.get("tem_partes"),   "partes_envolvidas")
    print(f"{_BLUE}{'=' * 62}{_RESET}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = [a for a in sys.argv[1:] if a != "--sem-preview"]

    # Sem argumentos: tentar usar a pasta padrão 1_Colar_JSON_Aqui
    if not args:
        pasta_padrao = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "1_Colar_JSON_Aqui")
        if os.path.exists(pasta_padrao) and glob.glob(os.path.join(pasta_padrao, "*.json")):
            args = [pasta_padrao]
        else:
            print("╔══════════════════════════════════════════════════════════════════╗")
            print("║  Gerador de Documentos – SMOSU Oliveira/MG                     ║")
            print("╠══════════════════════════════════════════════════════════════════╣")
            print("║                                                                ║")
            print("║  Uso: python compilador.py dados.json [saida.docx]             ║")
            print("║                                                                ║")
            print("║  O JSON deve conter o campo 'tipo_relatorio' com um dos tipos  ║")
            print("║  listados abaixo.                                              ║")
            print("║                                                                ║")
            print("╠══════════════════════════════════════════════════════════════════╣")
            print("║  TIPOS DE DOCUMENTO DISPONÍVEIS:                               ║")
            print("╠══════════════════════════════════════════════════════════════════╣")

            categorias = {}
            for tipo, cat in sorted(TIPOS_DOCUMENTO.items()):
                categorias.setdefault(cat, []).append(tipo)

            for cat in ["parecer_tecnico", "parecer_simples", "oficio", "comunicado"]:
                tipos = categorias.get(cat, [])
                if tipos:
                    print(f"║  [{cat.upper():^20}]                                     ║")
                    for t in tipos:
                        print(f"║    • {t:<56} ║")
                    print("║                                                                ║")

            print("╚══════════════════════════════════════════════════════════════════╝")
            sys.exit(0)

    arquivos_para_processar = []
    caminho_saida_fornecido = None

    if os.path.isdir(args[0]):
        print(f"\n[>] MODO EM LOTE: Escaneando pasta '{args[0]}'")
        arquivos_para_processar = glob.glob(os.path.join(args[0], "*.json"))
    else:
        arquivos_para_processar = [a for a in args if a.endswith(".json") and os.path.isfile(a)]
        nao_jsons = [a for a in args if not a.endswith(".json")]
        if len(arquivos_para_processar) == 1 and nao_jsons:
            caminho_saida_fornecido = nao_jsons[0]

    if not arquivos_para_processar:
        print(f"[!] Nenhum arquivo .json encontrado para processar.")
        sys.exit(0)

    if len(arquivos_para_processar) > 1 and caminho_saida_fornecido:
        print("[!] Aviso: Parâmetro de saída único ignorado devido ao processamento em lote.")
        caminho_saida_fornecido = None

    sucessos = 0
    erros    = 0

    from traceback import print_exc

    for arquivo in arquivos_para_processar:
        # Ler JSON de entrada
        try:
            with open(arquivo, encoding="utf-8") as f:
                dados = json.load(f)
            print(f"\n[>] Processando arquivo: {os.path.basename(arquivo)}")
        except json.JSONDecodeError as e:
            print(f"[X] Ignorando {os.path.basename(arquivo)}: JSON inválido ({e})")
            erros += 1
            continue

        # Verificar marcadores de segurança
        json_str = json.dumps(dados, ensure_ascii=False)
        if "⚠️ VERIFICAR" in json_str:
            print(f"  {_warn('JSON contém marcações incompletas (VERIFICAR).')}")
            print(f"  {_info('Dica: peça ao GEM para reler os anexos e preencher os dados.')}")
            print()

        # ── Relatório pré-voo ─────────────────────────────────────────────────
        pode_prosseguir, resumo_cob = _relatorio_prevoo(dados)

        if not pode_prosseguir:
            print(f"\n  {_err('Geração BLOQUEADA por erro de consistência semântica.')}")
            print(f"  {_info('Corrija o JSON antes de compilar.')}")
            erros += 1
            continue

        # ── Preview HTML (se não estiver em modo silencioso) ──────────────────
        modo_sem_preview = "--sem-preview" in sys.argv
        if not modo_sem_preview:
            try:
                from preview_html import gerar_preview
                alertas_html = resumo_cob.get("alertas", [])
                print(f"\n  {_info('Abrindo preview HTML no navegador...')}")
                gerar_preview(dados, alertas=alertas_html)

                print()
                print("  ─────────────────────────────────────────────────────")
                print("  Revise o preview no navegador e responda:")
                print("  [ENTER]  → Confirmar e gerar o DOCX")
                print("  [N]      → Cancelar este documento")
                print("  ─────────────────────────────────────────────────────")
                resp = input("  Sua escolha: ").strip().upper()
                if resp == "N":
                    print(f"  {_warn('Documento cancelado pelo usuário.')}")
                    continue
            except Exception as e:
                print(f"  {_warn(f'Preview indisponível: {e}')}")

        # ── Gerar documento ───────────────────────────────────────────────────
        caminho_gerado = caminho_saida_fornecido
        try:
            pecas_selecionadas = dados.get("documentos_emitir", [])
            if pecas_selecionadas and isinstance(pecas_selecionadas, list):
                print(f"  {_info(f'Gerando MÚLTIPLAS PEÇAS ({len(pecas_selecionadas)})')}")
                for item in pecas_selecionadas:
                    # Suporte para string (novo padrão do painel) ou dict (padrão antigo do Gemini)
                    peca = item if isinstance(item, str) else item.get("tipo", "")
                    # Sanitizar nome da peça caso venha "Alvará de Regularização..." do Gemini
                    if not peca: continue
                    
                    dados_temp = dados.copy()
                    
                    # O motor espera IDs técnicos (ex: parecer_tecnico). 
                    # Se vier descritivo ("Alvará de Regularização"), tentamos deduzir pelo tipo do processo principal.
                    # Mas o ideal é que seja o ID técnico (que o roteador já usa).
                    if " " in peca or "—" in peca:
                        print(f"  {_warn(f'Ignorando tipo descritivo legado: {peca}')}")
                        continue
                        
                    dados_temp["tipo_relatorio"] = peca
                    
                    try:
                        cam = gerar(dados_temp, caminho_saida_fornecido)
                        if cam:
                            caminho_gerado = cam
                        print(f"  {_ok(f'DOCX gerado ({peca}): {os.path.basename(cam or arquivo)}')}")
                        sucessos += 1
                    except Exception as e:
                        print(f"  {_err(f'Falha ao gerar {peca}: {e}')}")
                        erros += 1
            else:
                caminho_gerado = gerar(dados, caminho_saida_fornecido)
                print(f"  {_ok(f'DOCX gerado: {os.path.basename(caminho_gerado or arquivo)}')}")
                sucessos += 1
        except Exception as e:
            print(f"  {_err(f'Falha ao compilar {os.path.basename(arquivo)}: {e}')}")
            erros += 1
            continue

        # ── Precedentes + resumo de qualidade (pós-geração) ──────────────────
        _relatorio_pos(dados, caminho_gerado or "", resumo_cob)

    print()
    print(f"{_BLUE}{'=' * 62}{_RESET}")
    if erros == 0:
        print(f"  {_ok(f'COMPILAÇÃO ENCERRADA — {sucessos} documento(s) gerado(s).')}")
    else:
        print(f"  {_warn(f'COMPILAÇÃO ENCERRADA — Sucessos: {sucessos} | Falhas: {erros}')}")
    print(f"{_BLUE}{'=' * 62}{_RESET}")


if __name__ == "__main__":
    main()
