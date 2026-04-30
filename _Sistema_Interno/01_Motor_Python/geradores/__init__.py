"""
Sistema de despacho de geradores de documentos — SMOSU Oliveira/MG.

Identifica o tipo_relatorio no JSON de entrada, carrega o template
correspondente e chama o gerador correto (parecer_tecnico, parecer_simples,
ofício ou comunicado).
"""

import os
import json
import datetime

from docx import Document
from docx.shared import Pt, Cm

import sys as _sys
import os as _os
_MOTOR_DIR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _MOTOR_DIR not in _sys.path:
    _sys.path.insert(0, _MOTOR_DIR)

from config import (
    TIPOS_DOCUMENTO, TEMPLATES_DIR, PROJECT_DIR,
    FONT_CORPO, SZ_CORPO,
)
from cabecalho import build_header, add_page_number_footer
from componentes import (
    build_titulo, build_identificacao, build_destinatario,
    build_dados_carimbo, build_corpo,
    build_conclusao_e_docs, build_conclusao_simples, build_assinatura,
    build_comunicado_pendencia,
    build_partes_envolvidas, build_historico_cronologico,
)

# ═══════════════════════════════════════════════════════════
#  TEMPLATES
# ═══════════════════════════════════════════════════════════

def carregar_template(tipo_relatorio):
    """Carrega o template JSON para o tipo de documento, se existir."""
    caminho = os.path.join(TEMPLATES_DIR, f"{tipo_relatorio}.json")
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    return {}  # template vazio = usar defaults


# ═══════════════════════════════════════════════════════════
#  DOCUMENTO BASE
# ═══════════════════════════════════════════════════════════

def _criar_documento_base():
    """Cria documento com margens A4 e estilo padrão configurados."""
    doc = Document()
    section = doc.sections[0]
    # Margens 1.5cm + cabeçalho rente ao topo + rodapé com altura
    M = Cm(1.5)
    section.page_height      = Cm(29.7)
    section.page_width       = Cm(21.0)
    section.top_margin       = Cm(3.2)   # corpo começa após o cabeçalho (~2.8cm de altura)
    section.bottom_margin    = Cm(2.2)   # espaço generoso para o rodapé
    section.left_margin      = M
    section.right_margin     = M
    section.header_distance  = Cm(0.3)   # logo colado na borda superior — sem borda branca
    section.footer_distance  = Cm(0.5)   # rodapé colado na borda inferior

    style = doc.styles['Normal']
    style.font.name = FONT_CORPO
    style.font.size = Pt(SZ_CORPO)
    return doc


def _gerar_nome_saida(dados):
    """Gera nome de arquivo e pasta baseados nos dados do processo."""
    now = datetime.datetime.now()

    numero_raw = str(dados.get("numero_processo", "S-N"))
    proc_limpo = numero_raw.replace("/", "-").replace("\\", "-")

    # Separa número e ano — barra tem precedência; hífen só se ambas as partes forem dígitos
    proc_num = numero_raw
    proc_ano = now.strftime("%Y")
    if "/" in numero_raw:
        partes_proc = numero_raw.split("/")
        proc_num = partes_proc[0]
        proc_ano = partes_proc[-1]
    elif "-" in numero_raw:
        partes_proc = numero_raw.split("-")
        if len(partes_proc) == 2 and partes_proc[0].isdigit() and partes_proc[1].isdigit():
            proc_num = partes_proc[0]
            proc_ano = partes_proc[-1]

    nome_alvo = dados.get("requerente") or dados.get("proprietario_nome") or dados.get("interessado") or "Desconhecido"
    nome_completo_title = str(nome_alvo).strip().title()

    tipo = str(dados.get("tipo_relatorio", "Parecer")).replace("_", " ").title()

    nome_arquivo = f"{tipo} - {proc_num}-{proc_ano} - {nome_completo_title}.docx"
    nome_pasta = f"Processo {proc_num}-{proc_ano} - {nome_completo_title}"

    for ch in ['<', '>', ':', '"', '|', '?', '*', '\\']:
        nome_arquivo = nome_arquivo.replace(ch, '')
        nome_pasta = nome_pasta.replace(ch, '')

    root_dir = os.path.dirname(PROJECT_DIR)
    final_out_dir = os.path.join(root_dir, "2_Documentos_Prontos", nome_pasta)
    os.makedirs(final_out_dir, exist_ok=True)
    return os.path.join(final_out_dir, nome_arquivo)


# ═══════════════════════════════════════════════════════════
#  GERADORES POR CATEGORIA
# ═══════════════════════════════════════════════════════════

def gerar_parecer_tecnico(doc, dados, template):
    """
    Parecer técnico COMPLETO:
    Header → Título → Identificação → Dados Carimbo → [Partes] → [Histórico] → Corpo → Conclusão+Docs
    """
    titulo = template.get("titulo_documento", "PARECER SETOR TÉCNICO - SMOSU")

    build_header(doc)
    add_page_number_footer(doc)
    build_titulo(doc, titulo)
    build_identificacao(doc, dados)
    build_dados_carimbo(doc, dados)
    if dados.get("partes_envolvidas"):
        build_partes_envolvidas(doc, dados["partes_envolvidas"])
    if dados.get("historico_cronologico"):
        build_historico_cronologico(doc, dados["historico_cronologico"])
    build_corpo(doc, dados)
    build_conclusao_e_docs(doc, dados)


def gerar_parecer_simples(doc, dados, template):
    """
    Parecer SIMPLES (sem dados do carimbo):
    Header → Título → Identificação → Corpo → Conclusão
    """
    titulo = template.get("titulo_documento", "PARECER SETOR TÉCNICO - SMOSU")

    build_header(doc)
    add_page_number_footer(doc)
    build_titulo(doc, titulo)
    build_identificacao(doc, dados)
    build_corpo(doc, dados)

    if dados.get("documentos_emitir"):
        build_conclusao_e_docs(doc, dados)
    else:
        build_conclusao_simples(doc, dados)


def gerar_oficio(doc, dados, template):
    """
    OFÍCIO:
    Header → Título → Destinatário → Corpo → Assinatura
    """
    titulo = template.get("titulo_documento", "OFÍCIO")

    build_header(doc)
    add_page_number_footer(doc)
    build_titulo(doc, titulo)
    build_destinatario(doc, dados)
    build_corpo(doc, dados)
    build_assinatura(doc, dados)


def gerar_comunicado(doc, dados, template):
    """
    COMUNICADO genérico:
    Header → Título → Identificação → Corpo → Assinatura
    """
    titulo = template.get("titulo_documento", "COMUNICADO")

    build_header(doc)
    add_page_number_footer(doc)
    build_titulo(doc, titulo)
    build_identificacao(doc, dados)
    build_corpo(doc, dados)
    build_assinatura(doc, dados)


def gerar_comunicado_pendencia(doc, dados, template):
    """
    COMUNICADO DE PENDÊNCIA — layout visual dedicado:
    Header → Título → Identificação → [Box Alerta + Box Orientação] → Assinatura
    """
    titulo = template.get("titulo_documento", "COMUNICADO DE PENDÊNCIA DOCUMENTAL")

    build_header(doc)
    add_page_number_footer(doc)
    build_titulo(doc, titulo)
    build_identificacao(doc, dados)
    build_comunicado_pendencia(doc, dados)


# ═══════════════════════════════════════════════════════════
#  MAPEAMENTO E DESPACHO
# ═══════════════════════════════════════════════════════════

GERADORES = {
    "parecer_tecnico":      gerar_parecer_tecnico,
    "parecer_simples":      gerar_parecer_simples,
    "oficio":               gerar_oficio,
    "comunicado":           gerar_comunicado,
    "comunicado_pendencia": gerar_comunicado_pendencia,
}


def gerar(dados, caminho_saida=None):
    """
    Função principal: gera documento baseado nos dados e tipo_relatorio.

    Parâmetros:
        dados: dict com os dados do processo (JSON do Gemini)
        caminho_saida: caminho opcional para o arquivo .docx

    Retorna:
        Caminho do arquivo gerado.
    """
    tipo = dados.get("tipo_relatorio", "regularizacao")
    
    # ---------------------------------------------------------
    # RESILIÊNCIA: Se o LLM agrupar os campos em sub-dicionários
    # como 'campos_obrigatorios' ou 'campos_opcionais', nós os achata.
    # ---------------------------------------------------------
    if "campos_obrigatorios" in dados and isinstance(dados["campos_obrigatorios"], dict):
        dados.update(dados.pop("campos_obrigatorios"))
    if "campos_opcionais" in dados and isinstance(dados["campos_opcionais"], dict):
        dados.update(dados.pop("campos_opcionais"))
    
    # Tratamento caso ele faça lista de strings em documentos_emitir no invés de `{tipo:..}`
    if "documentos_emitir" in dados and isinstance(dados["documentos_emitir"], list):
        lista_corrigida = []
        for d in dados["documentos_emitir"]:
            if isinstance(d, str):
                lista_corrigida.append({"tipo": d})
            else:
                lista_corrigida.append(d)
        dados["documentos_emitir"] = lista_corrigida

    # Injetar obs SERO automaticamente em habite-se com sero_metadata
    _HABITE_SE_TIPOS = {"habitese_comum", "habitese_multa", "habitese_inclusao_area"}
    if tipo in _HABITE_SE_TIPOS and dados.get("sero_metadata"):
        try:
            import gerador_sero
            obs_sero = gerador_sero.gerar_obs_sero(
                dados["sero_metadata"],
                dados.get("area_total_construida", "")
            )
            docs = dados.get("documentos_emitir", [])
            for doc_item in docs:
                if isinstance(doc_item, dict):
                    nome_tipo = str(doc_item.get("tipo", "")).lower()
                    if "habite" in nome_tipo or not doc_item.get("obs"):
                        doc_item["obs"] = obs_sero
                        break
        except Exception as _e:
            print(f"[!] Injeção de obs SERO falhou: {_e}")

    categoria = TIPOS_DOCUMENTO.get(tipo)

    if not categoria:
        print(f"[!] Tipo de documento desconhecido: '{tipo}'")
        print(f"    Tipos disponíveis: {', '.join(sorted(TIPOS_DOCUMENTO.keys()))}")
        raise ValueError(f"Tipo de documento desconhecido: {tipo}")

    print(f"[>] Tipo: {tipo} -> Categoria: {categoria}")

    # Carregar template (se existir)
    template = carregar_template(tipo)

    # === VALIDADOR DE INTEGRIDADE PARA AUTO-CORREÇÃO DO GEM ===
    obrigatorios = template.get("campos_obrigatorios", [])
    campos_faltantes = [c for c in obrigatorios if not dados.get(c)]
    
    if campos_faltantes:
        print("\n" + "="*70)
        print("  [AVISO ESTRUTURAL] VALIDAÇÃO DE CHAVES JSON - PREENCHIMENTO AUTOMÁTICO")
        print("="*70)
        print("  O Assistente GEM não incluiu algumas chaves obrigatórias.")
        print(f"  Tipo do Documento: {tipo}")
        print(f"  Chaves Faltantes : {', '.join(campos_faltantes)}")
        print("-" * 70)
        print("  [Ação] O sistema irá preencher esses campos com marcadores [PREENCHER].")
        print("         Você poderá editar o documento Word gerado e preencher manualmente.")
        print("="*70 + "\n")
        
        for c in campos_faltantes:
            if c == "documentos_emitir":
                dados[c] = [{"tipo": "[PREENCHER: documento a emitir]"}]
            elif c in ["considerandos", "fundamentacao_legal", "paragrafos_adicionais"]:
                dados[c] = [f"[PREENCHER: {c}]"]
            else:
                dados[c] = f"[PREENCHER: {c}]"


    # Criar documento base
    doc = _criar_documento_base()

    # Chamar gerador
    gerador_fn = GERADORES[categoria]
    gerador_fn(doc, dados, template)

    # Salvar
    if caminho_saida is None:
        caminho_saida = _gerar_nome_saida(dados)

    doc.save(caminho_saida)
    print(f"[+] Documento DOCX gerado: {caminho_saida}")

    # Gerar PDF automaticamente
    _gerar_pdf(caminho_saida)

    return caminho_saida


# ═══════════════════════════════════════════════════════════
#  GERAÇÃO DE PDF
# ═══════════════════════════════════════════════════════════

def _gerar_pdf(caminho_docx: str) -> str | None:
    """
    Tenta converter o DOCX em PDF usando comtypes/Word COM.
    Ajustado para NUNCA travar exibindo pop-ups (DisplayAlerts = 0).
    """
    import os
    base, _ = os.path.splitext(caminho_docx)
    caminho_pdf = base + ".pdf"
    abs_docx    = os.path.abspath(caminho_docx)
    abs_pdf     = os.path.abspath(caminho_pdf)

    print(f"  [.] Convertendo DOCX para PDF (via Word)...")
    
    try:
        import comtypes.client
        # Cria a instância do Word
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0  # 0 = wdAlertsNone (Evita qualquer pop-up que trava o código)
        
        try:
            # Abre de forma silenciosa, read-only
            doc_w = word.Documents.Open(abs_docx, ConfirmConversions=False, ReadOnly=True, AddToRecentFiles=False)
            doc_w.SaveAs(abs_pdf, FileFormat=17)  # 17 = wdFormatPDF
            doc_w.Close(0)  # 0 = wdDoNotSaveChanges
        finally:
            word.Quit(0)
            
        print(f"  [+] Documento PDF gerado: {caminho_pdf}")
        return caminho_pdf
    except ImportError:
        print("[!] Biblioteca 'comtypes' não instalada. Execute: pip install comtypes")
        return None
    except Exception as e:
        print(f"[!] Erro ao gerar PDF pelo Word COM: {e}")
        
        # Fallback para docx2pdf caso o comtypes falhe por alguma peculiaridade
        try:
            from docx2pdf import convert
            convert(abs_docx, abs_pdf)
            print(f"  [+] Documento PDF gerado via docx2pdf: {caminho_pdf}")
            return caminho_pdf
        except ImportError:
            print("[!] docx2pdf não instalado.")
        except Exception as e2:
            print(f"[!] docx2pdf também falhou: {e2}")

    print("[!] PDF NÃO GERADO. O Word pode estar bloqueando a automação no fundo.")
    return None
