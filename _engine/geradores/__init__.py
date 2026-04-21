"""
Sistema de despacho de geradores de documentos — SMOSU Oliveira/MG.

Identifica o tipo_relatorio no JSON de entrada, carrega o template
correspondente e chama o gerador correto (parecer_tecnico, parecer_simples,
ofício ou comunicado).
"""

import os
import json

from docx import Document
from docx.shared import Pt, Cm

from config import (
    TIPOS_DOCUMENTO, TEMPLATES_DIR, PROJECT_DIR,
    FONT_CORPO, SZ_CORPO,
)
from cabecalho import build_header, add_page_number_footer
from componentes import (
    build_titulo, build_identificacao, build_destinatario,
    build_dados_carimbo, build_corpo, build_fundamentacao,
    build_conclusao_e_docs, build_conclusao_simples, build_assinatura,
)
from alvaras_finais import build_alvara_oficial, build_habitese_oficial, build_certidao_oficial


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
    M = Cm(1.5)
    section.page_height  = Cm(29.7)
    section.page_width   = Cm(21.0)
    section.top_margin   = M
    section.bottom_margin = M
    section.left_margin  = M
    section.right_margin = M
    section.header_distance = Cm(1.0)
    section.footer_distance = Cm(1.0)

    style = doc.styles['Normal']
    style.font.name = FONT_CORPO
    style.font.size = Pt(SZ_CORPO)
    return doc


def _gerar_nome_saida(dados):
    """Gera nome de arquivo baseado nos dados do processo."""
    proc = str(dados.get("numero_processo", "RELATORIO")).replace("/", "-")
    
    # Nomenclatura Inteligente: busca nome na ordem de probabilidade das chaves
    nome_alvo = dados.get("requerente") or dados.get("proprietario_nome") or dados.get("interessado") or "Desconhecido"
    req_str = str(nome_alvo).split()[0]
    
    tipo = dados.get("tipo_relatorio", "PARECER").upper()
    nome = f"{tipo}_{proc} {req_str}.docx"
    for ch in ['<', '>', ':', '"', '|', '?', '*']:
        nome = nome.replace(ch, '')
    return os.path.join(PROJECT_DIR, nome)


# ═══════════════════════════════════════════════════════════
#  GERADORES POR CATEGORIA
# ═══════════════════════════════════════════════════════════

def gerar_parecer_tecnico(doc, dados, template):
    """
    Parecer técnico COMPLETO:
    Header → Título → Identificação → Dados Carimbo → Corpo → Conclusão+Docs
    """
    titulo = template.get("titulo_documento", "PARECER SETOR TÉCNICO - SMOSU")

    build_header(doc)
    add_page_number_footer(doc)
    build_titulo(doc, titulo)
    build_identificacao(doc, dados)
    build_dados_carimbo(doc, dados)
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
    COMUNICADO:
    Header → Título → Identificação → Corpo → Assinatura
    """
    titulo = template.get("titulo_documento", "COMUNICADO")

    build_header(doc)
    add_page_number_footer(doc)
    build_titulo(doc, titulo)
    build_identificacao(doc, dados)
    build_corpo(doc, dados)
    build_assinatura(doc, dados)


def gerar_documento_pronto(doc, dados, template):
    """
    DOCUMENTOS DE SECRETARIA (ALVARÁ FINAL / HABITE-SE)
    Design totalmente único, usando o novo motor em alvaras_finais.py
    Não usa o Header e identificacao padrão.
    """
    tipo = dados.get("tipo_relatorio", "")
    if "habitese" in tipo:
        build_habitese_oficial(doc, dados)
    elif "certidao" in tipo:
        build_certidao_oficial(doc, dados)
    else:
        build_alvara_oficial(doc, dados)


# ═══════════════════════════════════════════════════════════
#  MAPEAMENTO E DESPACHO
# ═══════════════════════════════════════════════════════════

GERADORES = {
    "parecer_tecnico": gerar_parecer_tecnico,
    "parecer_simples": gerar_parecer_simples,
    "oficio":          gerar_oficio,
    "comunicado":      gerar_comunicado,
    "documento_pronto":gerar_documento_pronto,
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
        print("  [ERRO ESTRUTURAL] VALIDAÇÃO DE CHAVES JSON FALHOU")
        print("="*70)
        print("  Parece que o Assistente GEM esqueceu de incluir algumas chaves obrigatórias!")
        print(f"  Tipo do Documento: {tipo}")
        print(f"  Chaves Faltantes : {', '.join(campos_faltantes)}")
        print("-" * 70)
        print("  [Ação de Correção] Copie e cole a mensagem abaixo de volta pro GEM:\n")
        print(f"  Gem, o JSON que você gerou falhou na validação estrutural do sistema.")
        print(f"  O template oficial para '{tipo}' exige o uso EXATO destas CHAVES JSON:")
        print(f"  >>> {', '.join(campos_faltantes)}")
        print(f"  Por favor, revise o PDF do processo, certifique-se de usar estes nomes exatos de chaves")
        print(f"  e gere o bloco de JSON corrigido e completo para eu compilar.")
        print("="*70 + "\n")
        raise ValueError(f"Faltam {len(campos_faltantes)} chaves obrigatórias: {','.join(campos_faltantes)}")


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

def _gerar_pdf(caminho_docx):
    """Tenta gerar PDF a partir do DOCX (docx2pdf ou comtypes)."""
    caminho_pdf = caminho_docx.replace('.docx', '.pdf')
    try:
        from docx2pdf import convert
        convert(caminho_docx, caminho_pdf)
        print(f"[+] Documento PDF  gerado: {caminho_pdf}")
    except ImportError:
        try:
            import comtypes.client
            word = comtypes.client.CreateObject('Word.Application')
            word.Visible = False
            doc_w = word.Documents.Open(os.path.abspath(caminho_docx))
            doc_w.SaveAs(os.path.abspath(caminho_pdf), FileFormat=17)
            doc_w.Close()
            word.Quit()
            print(f"[+] Documento PDF  gerado: {caminho_pdf}")
        except Exception as e:
            print(f"[!] PDF não gerado (instale docx2pdf ou comtypes): {e}")
