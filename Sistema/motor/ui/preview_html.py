"""
Gerador de Preview HTML — visualização fiel do documento antes de gerar o DOCX.
Abre automaticamente no navegador padrão.
"""

import os
import json
import re
import webbrowser
import tempfile
from datetime import datetime

import sys as _sys
import os as _os
_UI_DIR = _os.path.dirname(_os.path.abspath(__file__))
_MOTOR_DIR = _os.path.dirname(_UI_DIR)
if _MOTOR_DIR not in _sys.path:
    _sys.path.insert(0, _MOTOR_DIR)

try:
    from core.config import TIPOS_DOCUMENTO as _TIPOS_DOCUMENTO
except ImportError:
    _TIPOS_DOCUMENTO = {}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _md_inline(texto: str) -> str:
    """Converte **negrito**, __itálico__ e *itálico* para HTML."""
    if not texto:
        return ""
    # Ordem importa: negrito primeiro
    texto = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', texto)
    # Itálico duplo
    texto = re.sub(r'__(.+?)__', r'<em>\1</em>', texto)
    # Itálico simples (asterisco)
    texto = re.sub(r'\*(.+?)\*', r'<em>\1</em>', texto)
    # Itálico simples (underscore) - apenas se cercado por espaços ou início/fim para evitar conflitos em IDs
    texto = re.sub(r'(^|\s)_(.+?)_(\s|$)', r'\1<em>\2</em>\3', texto)
    return texto


def _safe(val, fallback="—"):
    if val and str(val).strip():
        return str(val).strip()
    return fallback


def _data_hoje():
    meses = ["janeiro","fevereiro","março","abril","maio","junho",
             "julho","agosto","setembro","outubro","novembro","dezembro"]
    d = datetime.now()
    return f"{d.day} de {meses[d.month-1]} de {d.year}"


def _badge_conclusao(conclusao: str) -> str:
    texto = conclusao.upper()
    if "FAVORÁVEL" in texto or "FAVORAVEL" in texto:
        return '<span class="badge badge-ok">✅ FAVORÁVEL</span>'
    if "RESSALVA" in texto or "CONDICIONADO" in texto:
        return '<span class="badge badge-warn">⚠️ FAVORÁVEL COM RESSALVAS</span>'
    if "DESFAVORÁVEL" in texto or "DESFAVORAVEL" in texto or "INDEFERIDO" in texto:
        return '<span class="badge badge-err">❌ DESFAVORÁVEL</span>'
    if "PENDÊNCIA" in texto or "PENDENCIA" in texto or "SUSPEN" in texto:
        return '<span class="badge badge-pend">🔴 PENDÊNCIA</span>'
    return '<span class="badge badge-warn">📋 VER CONCLUSÃO</span>'


# ── Seções HTML ───────────────────────────────────────────────────────────────

def _html_alertas(alertas: list[dict]) -> str:
    if not alertas:
        return ""
    itens = ""
    for a in alertas:
        nivel = a.get("nivel", "aviso")
        icon  = "✗" if nivel == "erro" else "⚠"
        cls   = "alerta-erro" if nivel == "erro" else "alerta-aviso"
        itens += f'<div class="alerta-item {cls}">{icon} {_safe(a.get("msg", ""))}</div>'
    return f"""
    <section class="section-alertas">
      <div class="section-header section-header-alert">
        ⚠ ALERTAS PRÉ-VOO ({len(alertas)} item{'ns' if len(alertas)>1 else ''})
      </div>
      <div class="alertas-body">{itens}</div>
    </section>"""


def _html_identificacao(d: dict) -> str:
    processo  = _safe(d.get("numero_processo"))
    data_proc = _safe(d.get("data_processo"), "")
    assunto   = _safe(d.get("assunto"))
    req       = _safe(d.get("requerente"))
    tipo      = _safe(d.get("tipo_relatorio"), "").replace("_", " ").upper()

    data_info = f" &nbsp;—&nbsp; {data_proc}" if data_proc and data_proc != "—" else ""

    return f"""
    <section class="section-id">
      <table class="id-table">
        <tr><td class="id-label">Processo nº</td>
            <td class="id-value"><strong>{processo}</strong>{data_info}</td></tr>
        <tr><td class="id-label">Tipo</td>
            <td class="id-value">{tipo}</td></tr>
        <tr><td class="id-label">Assunto</td>
            <td class="id-value">{assunto}</td></tr>
        <tr><td class="id-label">Requerente</td>
            <td class="id-value"><strong>{req}</strong></td></tr>
      </table>
    </section>"""


def _html_carimbo(d: dict) -> str:
    """Tabela Inteligente HTML: Oculta campos vazios e agrupa os preenchidos em 4 colunas."""
    logradouro = _safe(d.get("logradouro"), "")
    bairro     = _safe(d.get("bairro"), "")
    endereco   = f"{logradouro} — {bairro}" if logradouro != "—" and bairro != "—" else (logradouro if logradouro != "—" else bairro)

    # 1. Lista de candidatos (Label, Valor)
    candidatos = [
        ("Endereço",        endereco),
        ("Inscrição Mun.",   _safe(d.get("inscricao_municipal"))),
        ("Proprietário",    _safe(d.get("proprietario", d.get("requerente")))),
        ("Resp. Técnico",    _safe(d.get("profissional_nome", d.get("responsavel_tecnico")))),
        ("Lote",            _safe(d.get("lote"))),
        ("Quadra",           _safe(d.get("quadra"))),
        ("Área Terreno",    _safe(d.get("area_terreno"))),
        ("Área Total Const.", _safe(d.get("area_total_construida"))),
        ("Taxa Ocupação",   _safe(d.get("taxa_ocupacao"))),
        ("Coef. Aproveita.", _safe(d.get("coef_aproveitamento"))),
        ("Permeabilidade",  _safe(d.get("taxa_permeabilidade"))),
        ("Pavimentos",       _safe(d.get("pavimentos"))),
        ("Vagas Garagem",   _safe(d.get("vagas_garagem"))),
        ("Zona de Uso",      _safe(d.get("zona_uso"))),
        ("ART/RRT",         _safe(d.get("art_rrt_numero"))),
        ("Multa Específica", _safe(d.get("tipo_multa_especifica"))),
    ]

    # 2. Filtragem (Remove o que estiver vazio ou com marcador de preenchimento)
    def eh_valido(v):
        if not v or v == "—": return False
        v_str = str(v).strip().lower()
        return v_str not in ["", "-", "—", "[preencher]", "n/a", "não informado"]

    validos = [(l, v) for l, v in candidatos if eh_valido(v)]
    if not validos:
        return ""

    # 3. Agrupamento em pares (L1, V1, L2, V2)
    rows = ""
    for i in range(0, len(validos), 2):
        l1, v1 = validos[i]
        l2, v2 = validos[i+1] if (i+1) < len(validos) else ("", "")
        
        row_html = f'<tr><td class="car-label">{l1}</td><td class="car-value">{v1}</td>'
        if l2:
            row_html += f'<td class="car-label">{l2}</td><td class="car-value">{v2}</td>'
        else:
            row_html += '<td class="car-label"></td><td class="car-value"></td>'
        row_html += '</tr>'
        rows += row_html

    return f"""
    <section class="section-carimbo">
      <div class="section-header">📋 DADOS TÉCNICOS DO PROJETO (Ref. Decreto nº 4.149/2019)</div>
      <table class="car-table">{rows}</table>
    </section>"""



def _html_partes_envolvidas(d: dict) -> str:
    """Seção de Partes Envolvidas — espelha build_partes_envolvidas() do DOCX."""
    partes = d.get("partes_envolvidas")
    if not partes:
        return ""

    # Normalizar: pode ser string (nome simples) ou lista de dicts
    if isinstance(partes, str):
        partes = [{"papel": "Interessado", "nome": partes}]
    elif isinstance(partes, dict):
        partes = [partes]

    linhas = ""
    for p in partes:
        papel = _safe(p.get("papel", "Parte"), "Parte")
        nome  = _safe(p.get("nome", "—"))
        cpf   = p.get("cpf_cnpj", "")
        cpf_html = f'<span style="color:#666;font-size:9pt"> — {cpf}</span>' if cpf else ""
        linhas += f"""
        <tr>
          <td class="id-label">{papel}</td>
          <td class="id-value">{nome}{cpf_html}</td>
        </tr>"""

    return f"""
    <section class="section-id">
      <div class="section-header">PARTES ENVOLVIDAS</div>
      <table class="id-table">{linhas}
      </table>
    </section>"""


def _html_historico_cronologico(d: dict) -> str:
    """Seção de Histórico Cronológico — espelha build_historico_cronologico() do DOCX."""
    historico = d.get("historico_cronologico")
    if not historico:
        return ""

    # Normalizar: pode ser lista de dicts ou lista de strings
    if isinstance(historico, str):
        historico = [{"evento": historico}]

    linhas = ""
    for item in historico:
        if isinstance(item, str):
            item = {"evento": item}
        data      = _safe(item.get("data", ""), "—")
        evento    = _safe(item.get("evento", ""))
        referencia = item.get("referencia", "")
        ref_html  = f'<br><span style="font-size:8.5pt;color:#888">{referencia}</span>' if referencia else ""
        linhas += f"""
        <tr>
          <td class="id-label" style="width:90px;white-space:nowrap">{data}</td>
          <td class="id-value">{evento}{ref_html}</td>
        </tr>"""

    return f"""
    <section class="section-id">
      <div class="section-header">HISTÓRICO CRONOLÓGICO</div>
      <table class="id-table">{linhas}
      </table>
    </section>"""


def _html_corpo(d: dict) -> str:
    partes = []

    abertura = d.get("paragrafo_abertura", "")
    if abertura:
        partes.append(f'<p class="par-abertura">{_md_inline(abertura)}</p>')

    considerandos = d.get("considerandos", [])
    if considerandos:
        if isinstance(considerandos, str):
            considerandos = [c.strip() for c in considerandos.split("\n") if c.strip()]

        partes.append('<div class="subsec-header subsec-blue">CONSIDERANDOS</div>')
        for c in considerandos:
            cons_limpo = c.strip()
            
            # 1. Remoção robusta de prefixos redundantes (Sincronizado com corpo.py)
            cons_limpo = re.sub(r'^(considerando\s+(que\s+)?)+', '', cons_limpo, flags=re.IGNORECASE).strip()
            cons_limpo = re.sub(r'^que\s+', '', cons_limpo, flags=re.IGNORECASE).strip()
            
            # 2. Primeira letra em maiúscula
            if cons_limpo and not cons_limpo.startswith('**') and not re.match(r'^(\d+\.|[A-Za-z]\.|\d+\s*\-)', cons_limpo):
                cons_limpo = cons_limpo[0].upper() + cons_limpo[1:]

            # 3. Inteligência de Prefixo (Sincronizado com corpo.py)
            ja_tem_prefixo   = re.match(r'^considerando\b', c.strip(), re.I)
            eh_lista         = re.match(r'^(\d+\.|[A-Za-z]\.|\*\*|\d+\s*\-|\*|\-)', cons_limpo)
            comeca_maiuscula = cons_limpo and cons_limpo[0].isupper() and not cons_limpo.startswith('**')
            tem_abertura     = bool(d.get("paragrafo_abertura"))

            prefixo_html = ""
            if not (ja_tem_prefixo or eh_lista or comeca_maiuscula or tem_abertura):
                prefixo_html = '<span class="kw-considerando">Considerando que</span> '

            partes.append(
                f'<p class="par-considerando">'
                f'{prefixo_html}{_md_inline(cons_limpo)}'
                f'</p>'
            )

    multas = d.get("multas_aplicaveis", [])
    if multas:
        if isinstance(multas, str):
            multas = [m.strip() for m in multas.split("\n") if m.strip()]
        partes.append('<div class="subsec-header subsec-red">MULTAS APLICÁVEIS</div>')
        for m in multas:
            limpo = m.lstrip("•▪- \t")
            partes.append(f'<p class="par-fund" style="color:#7f0000;">▪ {_md_inline(limpo)}</p>')

    condicionantes = d.get("condicionantes_aprovacao", [])
    if condicionantes:
        if isinstance(condicionantes, str):
            condicionantes = [c.strip() for c in condicionantes.split("\n") if c.strip()]
        partes.append('<div class="subsec-header subsec-green">CONDICIONANTES DE APROVAÇÃO</div>')
        for c in condicionantes:
            limpo = c.lstrip("•▪- \t")
            partes.append(f'<p class="par-fund" style="color:#1b5e20;">▪ {_md_inline(limpo)}</p>')

    fund = d.get("fundamentacao_legal", [])
    if fund:
        if isinstance(fund, str):
            fund = [f.strip() for f in fund.split("\n") if f.strip()]
        partes.append('<div class="subsec-header subsec-gray">DA ANÁLISE LEGAL E TÉCNICA</div>')
        for f in fund:
            limpo = f.lstrip("•▪- \t")
            partes.append(f'<p class="par-fund">▪ {_md_inline(limpo)}</p>')

    merito = d.get("analise_merito", "")
    if merito:
        partes.append('<div class="subsec-header subsec-blue" style="border-left-color:var(--accent2)">ANÁLISE DE MÉRITO TÉCNICO</div>')
        partes.append(f'<p class="par-merito" style="font-style:italic; border-left: 3px solid var(--accent2); padding-left: 15px; margin-left: 5px;">{_md_inline(merito)}</p>')

    conclusao = d.get("conclusao", "")
    if conclusao:
        partes.append('<div class="subsec-header subsec-green">CONCLUSÃO TÉCNICA</div>')
        partes.append(f'<div class="conclusao-badge">{_badge_conclusao(conclusao)}</div>')
        partes.append(f'<p class="par-conclusao">{_md_inline(conclusao)}</p>')

    return f"""
    <section class="section-corpo">
      <div class="section-header">📝 PARECER TÉCNICO</div>
      <div class="corpo-content">{''.join(partes)}</div>
    </section>"""


def _html_documentos(d: dict) -> str:
    docs = d.get("documentos_emitir", [])
    if not docs:
        return ""

    itens = ""
    for doc in docs:
        tipo = _safe(doc.get("tipo", ""))
        obs  = doc.get("obs", "")
        obs_html = f'<div class="doc-obs">Obs.: {_md_inline(obs)}</div>' if obs else ""
        itens += f"""
        <div class="doc-card">
          <div class="doc-tipo">✓ {tipo}</div>
          {obs_html}
        </div>"""

    return f"""
    <section class="section-docs">
      <div class="section-header">📄 EMISSÃO DE DOCUMENTOS</div>
      <div class="docs-grid">{itens}</div>
    </section>"""


def _html_assinatura(d: dict) -> str:
    assinante = d.get("assinante", {})
    nome     = d.get("assinante_parecer") or assinante.get("nome",     "Diego Tarcísio Nunes Vilela")
    titulo   = assinante.get("titulo",   "Engenheiro Civil")
    registro = assinante.get("registro", "CREA 235.474/D")
    cidade   = d.get("cidade", "Oliveira")

    return f"""
    <section class="section-assinatura">
      <div class="assinatura-local">{cidade}, {_data_hoje()}.</div>
      <div class="assinatura-linha"></div>
      <div class="assinatura-nome">{nome}</div>
      <div class="assinatura-sub">{titulo} — {registro}</div>
      <div class="assinatura-sub">Secretaria Municipal de Obras e Serviços Urbanos</div>
    </section>"""


def _html_memoria(d: dict) -> str:
    """
    Renderiza a memória de cálculo inline (sempre visível), espelhando
    build_memoria_calculo() do DOCX que usa uma caixa destacada.
    """
    memoria = d.get("memoria_de_calculo")
    if not memoria:
        return ""
    # Escapa HTML básico para segurança (a memória pode ter <, >, &)
    memoria_esc = str(memoria).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <section class="section-memoria">
      <div class="section-header">MEMÓRIA DE CÁLCULO E ÍNDICES URBANÍSTICOS</div>
      <div style="padding: 12px 20px 16px;">
        <pre class="memoria-pre">{memoria_esc}</pre>
      </div>
    </section>"""


# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Calibri', 'Segoe UI', sans-serif;
  font-size: 11pt;
  background: #f0f2f5;
  color: #222;
  padding: 20px;
}
.page-wrapper {
  max-width: 900px;
  margin: 0 auto;
}

/* ── CABEÇALHO INSTITUCIONAL ── */
.header-inst {
  background: #1F3864;
  color: white;
  padding: 18px 24px;
  border-radius: 8px 8px 0 0;
  display: flex;
  align-items: center;
  gap: 20px;
}
.header-inst .inst-nome {
  font-family: 'Cambria', Georgia, serif;
  font-size: 15pt;
  font-weight: bold;
  letter-spacing: 0.5px;
}
.header-inst .inst-sub {
  font-size: 9pt;
  opacity: 0.85;
  margin-top: 3px;
}
.header-inst .inst-contato {
  font-size: 8pt;
  opacity: 0.7;
  margin-top: 2px;
}
.header-badge {
  background: #e8ecf4;
  border-left: 4px solid #1F3864;
  padding: 8px 16px;
  font-size: 9pt;
  color: #555;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header-badge .preview-tag {
  background: #f0ad4e;
  color: #7a4f00;
  font-weight: bold;
  font-size: 8pt;
  padding: 2px 8px;
  border-radius: 4px;
  letter-spacing: 0.3px;
}

/* ── BATCH BANNER ── */
.batch-banner {
  background: #E3F2FD;
  color: #0D47A1;
  border: 1px solid #BBDEFB;
  padding: 12px 20px;
  margin: 15px auto;
  border-radius: 6px;
  max-width: 900px;
  font-size: 10.5pt;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* ── CARD DO DOCUMENTO ── */
.doc-card-wrapper {
  background: white;
  border-radius: 0 0 8px 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
  overflow: hidden;
}

/* ── SEÇÕES ── */
section {
  border-bottom: 1px solid #e8e8e8;
}
section:last-child { border-bottom: none; }

.section-header {
  background: #1F3864;
  color: white;
  font-family: 'Cambria', Georgia, serif;
  font-size: 10pt;
  font-weight: bold;
  padding: 7px 20px;
  letter-spacing: 0.4px;
}
.section-header-alert {
  background: #c0392b !important;
}

/* ── IDENTIFICAÇÃO ── */
.section-id { padding: 0; }
.id-table { width: 100%; border-collapse: collapse; }
.id-table tr { border-bottom: 1px solid #f0f0f0; }
.id-table tr:last-child { border-bottom: none; }
.id-label {
  background: #D6DCE4;
  color: #1F3864;
  font-weight: bold;
  font-size: 9pt;
  padding: 8px 14px;
  width: 160px;
  white-space: nowrap;
}
.id-value {
  padding: 8px 14px;
  font-size: 10pt;
}

/* ── CARIMBO TÉCNICO ── */
.section-carimbo { }
.car-table { width: 100%; border-collapse: collapse; }
.car-table tr { border-bottom: 1px solid #f0f0f0; }
.car-table tr:last-child { border-bottom: none; }
.car-label {
  background: #D6DCE4;
  color: #1F3864;
  font-weight: bold;
  font-size: 8.5pt;
  padding: 6px 12px;
  text-align: right;
  width: 130px;
  white-space: nowrap;
}
.car-value {
  font-size: 9pt;
  padding: 6px 12px;
  width: 310px;
}

/* ── CORPO ── */
.section-corpo { }
.corpo-content { padding: 16px 24px; }
.par-abertura { text-align: justify; line-height: 1.6; margin-bottom: 14px; }
.subsec-header {
  font-family: 'Cambria', Georgia, serif;
  font-weight: bold;
  font-size: 10pt;
  margin: 18px 0 8px 0;
  padding: 4px 10px;
  border-radius: 3px;
  letter-spacing: 0.3px;
}
.subsec-blue {
  color: #1F3864;
  background: #EBF0FA;
  border-left: 3px solid #1F3864;
}
.subsec-gray {
  color: #444;
  background: #f4f4f4;
  border-left: 3px solid #888;
}
.subsec-green {
  color: #1a4f1a;
  background: #edfaed;
  border-left: 3px solid #2e7d32;
}
.subsec-red {
  color: #7f0000;
  background: #ffebee;
  border-left: 3px solid #ef9a9a;
}
.kw-considerando { font-weight: bold; color: #1F3864; }
.par-considerando {
  text-align: justify;
  line-height: 1.6;
  margin-bottom: 10px;
  padding-left: 16px;
  border-left: 2px solid #D6DCE4;
}
.par-fund {
  text-align: justify;
  line-height: 1.6;
  margin-bottom: 8px;
  padding-left: 12px;
  color: #333;
}
.par-fund strong { color: #1F3864; }
.conclusao-badge { margin: 10px 0 8px 0; }
.par-conclusao {
  text-align: justify;
  line-height: 1.6;
  padding: 10px 14px;
  background: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
}

/* ── BADGES DE CONCLUSÃO ── */
.badge {
  display: inline-block;
  padding: 5px 14px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 11pt;
  letter-spacing: 0.3px;
}
.badge-ok   { background: #e8f5e9; color: #1b5e20; border: 1px solid #81c784; }
.badge-warn { background: #fff8e1; color: #7a4f00; border: 1px solid #f0ad4e; }
.badge-err  { background: #ffebee; color: #7f0000; border: 1px solid #ef9a9a; }
.badge-pend { background: #fce4ec; color: #7f0000; border: 1px solid #f48fb1; }

/* ── DOCUMENTOS ── */
.section-docs { }
.docs-grid { padding: 12px 20px 16px; display: flex; flex-direction: column; gap: 6px; }
.doc-card {
  background: #EBF0FA;
  border-radius: 5px;
  padding: 9px 14px;
  border-left: 4px solid #1F3864;
}
.doc-tipo { font-weight: bold; font-size: 10.5pt; color: #1a1a1a; }
.doc-obs { font-size: 9pt; color: #555; font-style: italic; margin-top: 3px; padding-left: 2px; }

/* ── ALERTAS ── */
.section-alertas { }
.alertas-body { padding: 10px 20px; display: flex; flex-direction: column; gap: 5px; }
.alerta-item {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 9.5pt;
}
.alerta-aviso { background: #fff8e1; color: #7a4f00; border-left: 3px solid #f0ad4e; }
.alerta-erro  { background: #ffebee; color: #7f0000; border-left: 3px solid #ef9a9a; }

/* ── MEMÓRIA DE CÁLCULO ── */
.section-memoria { background: #fafafa; }
.memoria-pre {
  font-size: 8.5pt;
  background: #f0f0f0;
  padding: 10px 14px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-word;
  color: #333;
}

/* ── ASSINATURA ── */
.section-assinatura {
  padding: 20px 24px;
  text-align: center;
  background: #fafafa;
}
.assinatura-local { font-size: 10pt; margin-bottom: 30px; }
.assinatura-linha {
  width: 300px;
  margin: 0 auto 8px;
  border-top: 1px solid #999;
}
.assinatura-nome { font-weight: bold; font-size: 11pt; }
.assinatura-sub { font-size: 9pt; color: #555; margin-top: 2px; }

/* ── FOOTER DE NAVEGAÇÃO ── */
.nav-footer {
  max-width: 900px;
  margin: 16px auto 0;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  font-size: 9pt;
  color: #777;
}
.nav-footer span { background: white; padding: 6px 12px; border-radius: 4px; box-shadow: 0 1px 4px rgba(0,0,0,.1); }
"""


# ── Gerador principal ─────────────────────────────────────────────────────────

def gerar_preview(dados: dict, alertas: list[dict] | None = None, destino: str | None = None, auto_abrir: bool = True) -> str:
    """
    Gera o arquivo HTML de preview e abre no navegador.
    Retorna o caminho do arquivo gerado.
    """
    alertas = alertas or []

    # Detecta geração em lote (Removido por solicitação do usuário - gera apenas Parecer Único)
    batch_notice = ""

    # Monta o HTML por partes
    html_alertas    = _html_alertas(alertas)
    html_id         = _html_identificacao(dados)
    # Usar TIPOS_DOCUMENTO para determinar categoria (correto) em vez de startswith (bugado)
    _tipo           = dados.get("tipo_relatorio", "")
    _categoria      = _TIPOS_DOCUMENTO.get(_tipo, "")
    html_carimbo    = _html_carimbo(dados) if _categoria == "parecer_tecnico" else ""
    html_partes     = _html_partes_envolvidas(dados)
    html_historico  = _html_historico_cronologico(dados)
    html_corpo      = _html_corpo(dados)
    html_docs       = _html_documentos(dados)
    html_memoria    = _html_memoria(dados)
    html_assinatura = _html_assinatura(dados)

    tipo_doc   = dados.get("tipo_relatorio", "documento").replace("_", " ").upper()
    processo   = dados.get("numero_processo", "—")
    requerente = dados.get("requerente", "—")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Preview GEM — Processo {processo}</title>
  <style>{CSS}</style>
</head>
<body>
<div class="page-wrapper">

  <!-- Cabeçalho institucional -->
  <div class="header-inst">
    <div>
      <div class="inst-nome">🏛 PREFEITURA MUNICIPAL DE OLIVEIRA</div>
      <div class="inst-sub">Secretaria Municipal de Obras e Serviços Urbanos — SMOSU</div>
      <div class="inst-contato">Praça XV de Novembro, 127 • Centro • Oliveira/MG • (37) 3331-9800</div>
    </div>
  </div>
  <div class="header-badge">
    <span>Tipo: <strong>{tipo_doc}</strong> &nbsp;|&nbsp; Processo: <strong>{processo}</strong> &nbsp;|&nbsp; Requerente: <strong>{requerente}</strong></span>
    <span class="preview-tag">⚡ PREVIEW — revise antes de gerar o DOCX</span>
  </div>

  {batch_notice}

  <!-- Corpo do documento -->
  <div class="doc-card-wrapper">
    {html_alertas}
    {html_id}
    {html_carimbo}
    {html_partes}
    {html_historico}
    {html_corpo}
    {html_docs}
    {html_memoria}
    {html_assinatura}
  </div>

  <div class="nav-footer">
    <span>Preview gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} pelo Motor GEM</span>
  </div>

</div>
</body>
</html>"""

    # Salvar arquivo
    if destino is None:
        fd, destino = tempfile.mkstemp(suffix=".html", prefix="preview_GEM_")
        os.close(fd)

    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)

    if auto_abrir:
        webbrowser.open(f"file:///{destino.replace(os.sep, '/')}")
    return destino


if __name__ == "__main__":
    import sys
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    if _script_dir not in sys.path:
        sys.path.insert(0, _script_dir)
    from core.config import PASTA_ENTRADA
    jsons = [f for f in os.listdir(PASTA_ENTRADA) if f.endswith(".json")]
    if not jsons:
        print(f"[!] Nenhum JSON encontrado em {os.path.basename(PASTA_ENTRADA)}/")
        sys.exit(1)
    with open(os.path.join(PASTA_ENTRADA, jsons[0]), encoding="utf-8") as f:
        dados = json.load(f)
    caminho = gerar_preview(dados)
    print(f"[OK] Preview aberto: {caminho}")

