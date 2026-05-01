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


# ── Helpers ──────────────────────────────────────────────────────────────────

def _md_inline(texto: str) -> str:
    """Converte **negrito** e __itálico__ para HTML."""
    if not texto:
        return ""
    texto = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', texto)
    texto = re.sub(r'__(.+?)__', r'<em>\1</em>', texto)
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
    logradouro = _safe(d.get("logradouro"), "")
    bairro     = _safe(d.get("bairro"), "")
    endereco   = f"{logradouro} — {bairro}" if logradouro != "—" and bairro != "—" else (logradouro if logradouro != "—" else bairro)

    linhas = [
        ("Endereço",        endereco,                           "Inscrição Mun.",   _safe(d.get("inscricao_municipal"))),
        ("Proprietário",    _safe(d.get("proprietario", d.get("requerente"))),
                                                                "Resp. Técnico",    _safe(d.get("profissional_nome", d.get("responsavel_tecnico")))),
        ("Lote",            _safe(d.get("lote")),               "Quadra",           _safe(d.get("quadra"))),
        ("Área Terreno",    _safe(d.get("area_terreno")),       "Área Total Const.", _safe(d.get("area_total_construida"))),
        ("Taxa Ocupação",   _safe(d.get("taxa_ocupacao")),      "Coef. Aproveita.", _safe(d.get("coef_aproveitamento"))),
        ("Permeabilidade",  _safe(d.get("taxa_permeabilidade")),"Pavimentos",       _safe(d.get("pavimentos"))),
        ("Vagas Garagem",   _safe(d.get("vagas_garagem")),      "Zona de Uso",      _safe(d.get("zona_uso"))),
        ("ART/RRT",         _safe(d.get("art_rrt_numero")),     "Multa Específica", _safe(d.get("tipo_multa_especifica"))),
    ]

    rows = ""
    for l1, v1, l2, v2 in linhas:
        rows += f"""<tr>
          <td class="car-label">{l1}</td><td class="car-value">{v1}</td>
          <td class="car-label">{l2}</td><td class="car-value">{v2}</td>
        </tr>"""

    return f"""
    <section class="section-carimbo">
      <div class="section-header">📋 DADOS TÉCNICOS DO PROJETO (Ref. Decreto nº 4.149/2019)</div>
      <table class="car-table">{rows}</table>
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
            limpo = c
            if limpo.lower().startswith("considerando que "):
                limpo = limpo[17:].strip()
            elif limpo.lower().startswith("considerando "):
                limpo = limpo[13:].strip()
            partes.append(
                f'<p class="par-considerando">'
                f'<span class="kw-considerando">Considerando que</span> {_md_inline(limpo)}'
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
    mem = d.get("memoria_de_calculo", "")
    if not mem or mem.strip() == "PREENCHER":
        return ""
    return f"""
    <section class="section-memoria">
      <details>
        <summary>🧮 Memória de Cálculo (clique para expandir)</summary>
        <pre class="memoria-pre">{mem}</pre>
      </details>
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
.section-memoria details { padding: 10px 20px; }
.section-memoria summary {
  cursor: pointer; color: #1F3864; font-weight: bold; font-size: 9pt;
  padding: 6px 0;
}
.memoria-pre {
  font-size: 8.5pt;
  background: #f0f0f0;
  padding: 10px 14px;
  border-radius: 4px;
  margin-top: 8px;
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

    # Monta o HTML por partes
    html_alertas   = _html_alertas(alertas)
    html_id        = _html_identificacao(dados)
    html_carimbo   = _html_carimbo(dados) if dados.get("tipo_relatorio", "").startswith(("alvara", "regularizacao")) else ""
    html_corpo     = _html_corpo(dados)
    html_docs      = _html_documentos(dados)
    html_memoria   = _html_memoria(dados)
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

  <!-- Corpo do documento -->
  <div class="doc-card-wrapper">
    {html_alertas}
    {html_id}
    {html_carimbo}
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
    # Teste rápido com JSON de exemplo
    import sys, os
    SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
    pasta = os.path.join(PROJECT_ROOT, "1_Colar_JSON_Aqui")
    jsons = [f for f in os.listdir(pasta) if f.endswith(".json")]
    if not jsons:
        print("[!] Nenhum JSON encontrado em 1_Colar_JSON_Aqui/")
        sys.exit(1)
    with open(os.path.join(pasta, jsons[0]), encoding="utf-8") as f:
        dados = json.load(f)
    caminho = gerar_preview(dados)
    print(f"[OK] Preview aberto: {caminho}")
