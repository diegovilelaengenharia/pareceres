#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Painel GEM v2 — Interface web completa para SMOSU Oliveira/MG.
http://localhost:8765 — sem API externa.
"""
import http.server, json, os, subprocess, sys, glob, webbrowser, threading
import urllib.parse, tempfile, time
from http.server import BaseHTTPRequestHandler, HTTPServer

SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT  = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PASTA_ENTRADA = os.path.join(PROJECT_ROOT, "1_Colar_JSON_Aqui")
PASTA_SAIDA   = os.path.join(PROJECT_ROOT, "2_Documentos_Prontos")
PASTA_MODELOS = os.path.join(PROJECT_ROOT, "0_Modelos_Prontos")
PASTA_TREINO  = os.path.join(PROJECT_ROOT, "3_Treinar_Inteligencia")
PASTA_RETRO   = os.path.join(os.path.dirname(SCRIPT_DIR), "03_Retroalimentacao_e_Estudos")
PASTA_EXEMPLOS_IN  = os.path.join(PASTA_RETRO, "exemplos_entrada")
PASTA_EXEMPLOS_OUT = os.path.join(PASTA_RETRO, "exemplos_saida")
PASTA_BASE_CONHECIMENTO = os.path.join(PASTA_RETRO, "base_conhecimento")
PASTA_HIST    = os.path.join(PASTA_RETRO, "historico")
HTML_FILE     = os.path.join(SCRIPT_DIR, "painel_gem.html")
PORT          = 8765

if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# ── APIs ──────────────────────────────────────────────────────────────────────

def api_status():
    pdfs  = glob.glob(os.path.join(PASTA_ENTRADA, "*.pdf"))
    jsons = [j for j in glob.glob(os.path.join(PASTA_ENTRADA, "*.json"))
             if not os.path.basename(j).startswith("_")]
    docs  = []
    for pasta in sorted(glob.glob(os.path.join(PASTA_SAIDA, "*")), reverse=True):
        if os.path.isdir(pasta):
            arqs = glob.glob(os.path.join(pasta, "*.docx")) + glob.glob(os.path.join(pasta, "*.pdf"))
            if arqs:
                docs.append({"pasta": os.path.basename(pasta),
                             "arquivos": [os.path.basename(a) for a in arqs]})
    modelos = [os.path.basename(m) for m in sorted(glob.glob(os.path.join(PASTA_MODELOS, "*.json")))]
    return {"pdfs": [{"nome": os.path.basename(p), "kb": round(os.path.getsize(p)/1024,1)} for p in pdfs],
            "jsons": [{"nome": os.path.basename(j)} for j in jsons],
            "docs": docs, "modelos": modelos}

def api_salvar_json(nome, conteudo):
    if not nome.endswith(".json"): nome += ".json"
    nome = os.path.basename(nome)
    caminho = os.path.join(PASTA_ENTRADA, nome)
    try:
        dados = json.loads(conteudo)

        # --- EXTRAÇÃO DE NOVAS VARIÁVEIS ---
        chaves_conhecidas = {
            # ── Identificação do Processo ──
            "tipo_relatorio", "numero_processo", "data_processo", "assunto",
            "requerente", "proprietario", "proprietario_nome", "proprietario_cpf_cnpj",
            # ── Localização e Cadastro ──
            "logradouro", "bairro", "inscricao_municipal", "lote", "quadra",
            # ── Índices Urbanísticos ──
            "area_terreno", "area_total_construida", "taxa_ocupacao",
            "coef_aproveitamento", "taxa_permeabilidade", "zona_uso",
            # ── Responsável Técnico ──
            "profissional_nome", "profissional_registro", "art_rrt", "desenhista",
            # ── Corpo do Parecer ──
            "paragrafo_abertura", "considerandos", "fundamentacao_legal", "conclusao",
            "memoria_de_calculo", "historico_cronologico", "partes_envolvidas",
            # ── Documentos a Emitir ──
            "documentos_emitir", "observacoes_finais",
            # ── Multas e Exceções ──
            "multas_calculadas", "excecoes_aplicadas", "ano_construcao",
            # ── Documentos Oficiais (Alvará/Habite-se/Certidão) ──
            "numero_documento", "data_aprovacao", "nome_obra",
            "area_total_obra", "areas_matriz",
            "autor_projeto_nome", "autor_projeto_crea", "autor_projeto_art",
            "responsavel_tecnico_nome", "responsavel_tecnico_crea", "responsavel_tecnico_art",
            "construtora_nome", "construtora_cpf_cnpj", "observacoes",
            "responsavel_execucao_nome", "responsavel_execucao_cpf_cnpj",
            "texto_despacho_responsavel_tecnico",
            "titulo_documento", "texto_certidao", "assinantes",
            # ── Modo Livre / Extras ──
            "texto_livre", "extras_extraidos", "analise_documental",
            "licao_aprendida", "data_conclusao_obra",
        }
        
        novas_variaveis = {k: v for k, v in dados.items() if k not in chaves_conhecidas}
        
        if novas_variaveis:
            from datetime import datetime
            arq_treino = os.path.join(PASTA_TREINO, "03_NOVAS_VARIAVEIS_PROPOSTAS.md")
            
            # Adiciona cabeçalho se o arquivo não existir
            if not os.path.exists(arq_treino):
                with open(arq_treino, "w", encoding="utf-8") as f:
                    f.write("# Novas Variáveis Propostas pelo Gemini\n\nEste arquivo coleta automaticamente chaves extras geradas pela IA que não fazem parte do schema padrão. Use-as para retroalimentar o sistema (1 vez por semana).\n")
            
            with open(arq_treino, "a", encoding="utf-8") as f:
                f.write(f"\n## Extraído do arquivo `{nome}` em {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write("```json\n")
                json.dump(novas_variaveis, f, ensure_ascii=False, indent=2)
                f.write("\n```\n")
        # -----------------------------------

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return {"ok": True, "nome": nome}
    except json.JSONDecodeError as e:
        return {"ok": False, "erro": f"JSON invalido: {e}"}
    except Exception as e:
        return {"ok": False, "erro": str(e)}

def _compilar_script(script_name, script_args=None):
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        cmd = [sys.executable, os.path.join(SCRIPT_DIR, script_name), "--sem-preview"]
        if script_args:
            cmd.extend(script_args)
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", cwd=PROJECT_ROOT, timeout=120, env=env)
        saida = (result.stdout + result.stderr).strip()
        return {"ok": result.returncode == 0, "saida": saida}
    except subprocess.TimeoutExpired:
        return {"ok": False, "saida": "Timeout (>2min)."}
    except Exception as e:
        return {"ok": False, "saida": str(e)}

def api_compilar(arquivos=None):
    if arquivos:
        # Se veio lista de arquivos, passamos caminhos completos
        caminhos = [os.path.join(PASTA_ENTRADA, f) for f in arquivos]
        return _compilar_script("compilador.py", caminhos)
    return _compilar_script("compilador.py")

def api_compilar_livre():
    return _compilar_script("compilador_livre.py")

def api_preview(nome):
    caminho = os.path.join(PASTA_ENTRADA, nome)
    if not os.path.exists(caminho):
        return {"ok": False, "erro": "JSON nao encontrado."}
    try:
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
        from preview_html import gerar_preview
        fd, tmp = tempfile.mkstemp(suffix=".html", prefix="gem_preview_")
        os.close(fd)
        gerar_preview(dados, destino=tmp, auto_abrir=False)
        with open(tmp, encoding="utf-8") as f:
            html = f.read()
        try: os.unlink(tmp)
        except: pass
        return {"ok": True, "html": html}
    except Exception as e:
        return {"ok": False, "erro": str(e)}

def api_ler_modelo(nome):
    caminho = os.path.join(PASTA_MODELOS, os.path.basename(nome))
    if not os.path.exists(caminho):
        return {"ok": False, "erro": "Modelo nao encontrado."}
    with open(caminho, encoding="utf-8") as f:
        return {"ok": True, "conteudo": f.read()}

def api_instrucoes():
    arq = os.path.join(PASTA_TREINO, "01_GEM_INSTRUCOES.md")
    if not os.path.exists(arq):
        return {"ok": False, "erro": "Arquivo de instrucoes nao encontrado."}
    with open(arq, encoding="utf-8") as f:
        return {"ok": True, "conteudo": f.read()}

def api_remover_json(nome):
    caminho = os.path.join(PASTA_ENTRADA, os.path.basename(nome))
    if not os.path.exists(caminho):
        return {"ok": False, "erro": "Arquivo nao encontrado."}
    try:
        os.remove(caminho)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "erro": str(e)}

def api_ler_json(nome):
    caminho = os.path.join(PASTA_ENTRADA, os.path.basename(nome))
    if not os.path.exists(caminho):
        return {"ok": False, "erro": "Arquivo nao encontrado."}
    with open(caminho, encoding="utf-8") as f:
        return {"ok": True, "conteudo": f.read()}

def api_abrir_pasta(qual):
    pastas = {
        "entrada": PASTA_ENTRADA, 
        "saida": PASTA_SAIDA, 
        "modelos": PASTA_MODELOS, 
        "treino": PASTA_TREINO,
        "exemplos_entrada": PASTA_EXEMPLOS_IN,
        "exemplos_saida": PASTA_EXEMPLOS_OUT,
        "retro": os.path.join(os.path.dirname(SCRIPT_DIR), "03_Retroalimentacao_e_Estudos")
    }
    pasta = pastas.get(qual, PASTA_SAIDA)
    os.makedirs(pasta, exist_ok=True)
    try:
        os.startfile(pasta)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "erro": str(e)}

def api_inspecionar(conteudo):
    """Inspeciona um JSON e retorna relatório de saúde + roteamento."""
    try:
        dados = json.loads(conteudo) if isinstance(conteudo, str) else conteudo
        from inspetor_documental import inspecionar
        from roteador_pecas import rotear
        resultado_inspecao = inspecionar(dados)
        resultado_roteamento = rotear(dados, resultado_inspecao)
        
        # 6B.4: Detecção de Anomalia
        try:
            import metricas_triagem
            mets = metricas_triagem.calcular_metricas()
            media = mets.get("score_medio", 0)
            if media > 0 and resultado_inspecao["score"] < media - 30:
                resultado_inspecao["anomalia"] = f"Atenção: Score ({resultado_inspecao['score']}%) muito abaixo da média histórica ({media}%)."
        except Exception:
            pass
            
        return {
            "ok": True,
            "inspecao": resultado_inspecao,
            "roteamento": resultado_roteamento,
        }
    except Exception as e:
        return {"ok": False, "erro": str(e)}

def api_aprender(data):
    """Registra decisão do engenheiro para retroalimentação."""
    from datetime import datetime
    try:
        tipo = data.get("tipo", "feedback_geral")
        feedback = data.get("feedback", "")
        
        os.makedirs(PASTA_HIST, exist_ok=True)
        
        if tipo == "decisao_triagem":
            # Decisão estruturada de triagem — salvar em JSONL
            arquivo = os.path.join(PASTA_HIST, "decisoes_triagem.jsonl")
            try:
                decisao = json.loads(feedback) if isinstance(feedback, str) else feedback
            except json.JSONDecodeError:
                decisao = {"texto": feedback}
            
            decisao["timestamp"] = datetime.now().isoformat()
            
            with open(arquivo, "a", encoding="utf-8") as f:
                f.write(json.dumps(decisao, ensure_ascii=False) + "\n")
            
            return {"ok": True, "msg": f"Decisão de triagem registrada ({decisao.get('processo', '?')})"}
        else:
            # Feedback textual livre — salvar no RETROALIMENTACAO_IA.md
            arquivo = os.path.join(SCRIPT_DIR, "RETROALIMENTACAO_IA.md")
            with open(arquivo, "a", encoding="utf-8") as f:
                f.write(f"\n## Feedback Manual — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f"{feedback}\n")
            return {"ok": True, "msg": "Feedback registrado no RETROALIMENTACAO_IA.md"}
    except Exception as e:
        return {"ok": False, "erro": str(e)}

def api_registro_sistema():
    """Retorna inventário completo do sistema para visibilidade."""
    from config import TIPOS_DOCUMENTO
    
    # ── Tipos de parecer agrupados por categoria ──
    tipos_por_cat = {}
    for tipo, cat in TIPOS_DOCUMENTO.items():
        tipos_por_cat.setdefault(cat, []).append(tipo)
    
    # ── Leis cadastradas na base_conhecimento ──
    leis = []
    if os.path.isdir(PASTA_BASE_CONHECIMENTO):
        for arq in sorted(os.listdir(PASTA_BASE_CONHECIMENTO)):
            if arq.endswith(('.md', '.json', '.txt')) and arq != 'desktop.ini':
                caminho = os.path.join(PASTA_BASE_CONHECIMENTO, arq)
                tam = round(os.path.getsize(caminho) / 1024, 1)
                leis.append({"arquivo": arq, "tamanho_kb": tam})
    
    # ── Variáveis do schema ──
    chaves_obrig = [
        "tipo_relatorio", "numero_processo", "requerente",
        "paragrafo_abertura", "considerandos", "conclusao"
    ]
    chaves_todas = [
        "tipo_relatorio", "numero_processo", "data_processo", "assunto",
        "requerente", "proprietario", "proprietario_nome", "proprietario_cpf_cnpj",
        "logradouro", "bairro", "inscricao_municipal", "lote", "quadra",
        "area_terreno", "area_total_construida", "taxa_ocupacao",
        "coef_aproveitamento", "taxa_permeabilidade", "zona_uso",
        "profissional_nome", "profissional_registro", "art_rrt", "desenhista",
        "paragrafo_abertura", "considerandos", "fundamentacao_legal", "conclusao",
        "memoria_de_calculo", "historico_cronologico", "partes_envolvidas",
        "documentos_emitir", "observacoes_finais",
        "multas_calculadas", "excecoes_aplicadas", "ano_construcao",
        "numero_documento", "data_aprovacao", "nome_obra",
        "area_total_obra", "areas_matriz",
        "responsavel_execucao_nome", "texto_despacho_responsavel_tecnico",
        "titulo_documento", "texto_certidao", "assinantes",
        "texto_livre", "extras_extraidos", "analise_documental",
    ]
    
    # ── Contar variáveis novas pendentes ──
    novas_pendentes = 0
    arq_novas = os.path.join(PASTA_TREINO, "03_NOVAS_VARIAVEIS_PROPOSTAS.md")
    if os.path.exists(arq_novas):
        with open(arq_novas, encoding="utf-8") as f:
            novas_pendentes = f.read().count("## Extraído")
    
    # ── Zonas urbanísticas ──
    zonas = ["ZUR1", "ZUR2", "ZUR3", "ZUR_Social", "ZC1", "ZC2",
             "ZAE1", "ZAE2", "ZAE3", "ZAE4", "ZIND"]
    
    # ── Checklists por tipo ──
    checklists = [
        "Alvará de Construção", "Regularização de Obra", "Habite-se",
        "Certificado de Averbação", "Alvará de Demolição", "Certidão de Demolição",
        "Alvará de Reforma/Ampliação", "Certidão de Decadência",
        "Certidão Nome de Rua/Localização", "2ª Via (Certidão de Número)",
        "2ª Via (Habite-se)", "Renovação de Alvará", "Substituição de Projeto",
        "Desmembramento/Topografia", "Retificação de Área", "Usucapião"
    ]
    
    # ── Processos exemplo ──
    jsons_exemplo = []
    json_dir = os.path.join(SCRIPT_DIR, "json")
    if os.path.isdir(json_dir):
        jsons_exemplo = [f for f in os.listdir(json_dir)
                         if f.endswith('.json') and f != 'desktop.ini']
    
    # ── Arquivos de treino ──
    treino_arquivos = []
    if os.path.isdir(PASTA_TREINO):
        treino_arquivos = [f for f in os.listdir(PASTA_TREINO)
                           if f.endswith(('.md', '.json')) and f != 'desktop.ini']
    
    # ── Decisões de triagem ──
    total_decisoes = 0
    arq_decisoes = os.path.join(PASTA_HIST, "decisoes_triagem.jsonl")
    if os.path.exists(arq_decisoes):
        with open(arq_decisoes, encoding="utf-8") as f:
            total_decisoes = sum(1 for _ in f)
    
    return {
        "ok": True,
        "registro": {
            "tipos_parecer": tipos_por_cat,
            "total_tipos": len(TIPOS_DOCUMENTO),
            "leis_cadastradas": leis,
            "total_leis": len(leis),
            "variaveis": {
                "total": len(set(chaves_todas)),
                "obrigatorias": chaves_obrig,
                "todas": sorted(set(chaves_todas)),
                "novas_pendentes": novas_pendentes,
            },
            "zonas_urbanisticas": zonas,
            "checklists": checklists,
            "total_checklists": len(checklists),
            "base_conhecimento": {
                "total_arquivos": len(leis),
                "tamanho_total_kb": round(sum(l["tamanho_kb"] for l in leis), 1),
            },
            "treino_arquivos": treino_arquivos,
            "jsons_exemplo": jsons_exemplo,
            "total_decisoes_triagem": total_decisoes,
        }
    }

# ── Handler ───────────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send(self, code, ct, body):
        self.send_response(code)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, d):
        self._send(200, "application/json; charset=utf-8", json.dumps(d, ensure_ascii=False).encode("utf-8"))

    def _html(self, c):
        self._send(200, "text/html; charset=utf-8", c.encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        for h,v in [("Access-Control-Allow-Origin","*"),("Access-Control-Allow-Methods","GET,POST,DELETE,OPTIONS"),("Access-Control-Allow-Headers","Content-Type")]:
            self.send_header(h,v)
        self.end_headers()

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            try:
                with open(HTML_FILE, encoding="utf-8") as f: self._html(f.read())
            except: self._html("<h1>painel_gem.html nao encontrado.</h1>")
        elif path == "/painel_gem.css":
            css_file = os.path.join(SCRIPT_DIR, "painel_gem.css")
            try:
                with open(css_file, encoding="utf-8") as f:
                    self._send(200, "text/css; charset=utf-8", f.read().encode("utf-8"))
            except: self._send(404, "text/plain", b"CSS not found")
        elif path == "/api/status": self._json(api_status())
        elif path == "/api/instrucoes": self._json(api_instrucoes())
        elif path.startswith("/api/preview/"): self._json(api_preview(urllib.parse.unquote(path[13:])))
        elif path.startswith("/api/modelo/"): self._json(api_ler_modelo(urllib.parse.unquote(path[12:])))
        elif path.startswith("/api/ler-json/"): self._json(api_ler_json(urllib.parse.unquote(path[14:])))
        elif path.startswith("/api/abrir/"): self._json(api_abrir_pasta(path[11:]))
        else: self._send(404, "text/plain", b"Not found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        try: data = json.loads(body)
        except: data = {}
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/salvar-json": self._json(api_salvar_json(data.get("nome","processo"), data.get("conteudo","")))
        elif path == "/api/compilar": self._json(api_compilar())
        elif path == "/api/compilar-lote": self._json(api_compilar(data.get("arquivos", [])))
        elif path == "/api/compilar-livre": self._json(api_compilar_livre())
        elif path == "/api/extrair-pdf":
            import time
            time.sleep(1.5)
            mock_json = json.dumps({
                "numero_processo": "IA-Mock/2026",
                "requerente": "Dados Extraídos Via PDF",
                "tipo_relatorio": "Regularização de Obra",
                "assunto": "Regularização com As-Built",
                "ano_construcao": "2015",
                "taxa_permeabilidade": "5"
            }, ensure_ascii=False, indent=2)
            self._json({"ok": True, "json_gerado": mock_json})
        elif path == "/api/aprender":
            self._json(api_aprender(data))
        elif path == "/api/metricas":
            try:
                import metricas_triagem
                self._json({"ok": True, "metricas": metricas_triagem.calcular_metricas()})
            except Exception as e:
                self._json({"ok": False, "erro": str(e)})
        elif path == "/api/exportar-relatorio":
            try:
                import metricas_triagem
                self._json(metricas_triagem.exportar_relatorio())
            except Exception as e:
                self._json({"ok": False, "erro": str(e)})
        elif path == "/api/inspecionar":
            self._json(api_inspecionar(data.get("conteudo", "{}")))
        elif path == "/api/registro-sistema":
            self._json(api_registro_sistema())
        else: self._send(404, "text/plain", b"Not found")

    def do_DELETE(self):
        path = urllib.parse.urlparse(self.path).path
        if path.startswith("/api/remover-json/"):
            self._json(api_remover_json(urllib.parse.unquote(path[18:])))
        else: self._send(404, "text/plain", b"Not found")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Garantir pastas existam
    os.makedirs(PASTA_EXEMPLOS_IN, exist_ok=True)
    os.makedirs(PASTA_EXEMPLOS_OUT, exist_ok=True)
    os.makedirs(PASTA_HIST, exist_ok=True)

    # ── Habilitar cores ANSI no Windows ──
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

    # ── Cores ANSI ──
    R  = "\033[0m"       # Reset
    B  = "\033[1m"       # Bold
    CY = "\033[96m"      # Ciano claro
    GR = "\033[92m"      # Verde claro
    YL = "\033[93m"      # Amarelo
    MG = "\033[95m"      # Magenta
    BL = "\033[94m"      # Azul
    DM = "\033[90m"      # Cinza escuro
    WH = "\033[97m"      # Branco

    # ── Contagens rápidas ──
    from config import TIPOS_DOCUMENTO
    n_tipos = len(TIPOS_DOCUMENTO)
    n_leis = 0
    if os.path.isdir(PASTA_BASE_CONHECIMENTO):
        n_leis = len([f for f in os.listdir(PASTA_BASE_CONHECIMENTO)
                      if f.endswith(('.md', '.json', '.txt')) and f != 'desktop.ini'])
    n_treino = 0
    if os.path.isdir(PASTA_TREINO):
        n_treino = len([f for f in os.listdir(PASTA_TREINO)
                        if f.endswith(('.md', '.json'))])

    print()
    print(f"  {CY}{'═' * 60}{R}")
    print(f"  {CY}║{R}  {B}{WH}██████╗ ███████╗███╗   ███╗{R}                              {CY}║{R}")
    print(f"  {CY}║{R}  {B}{WH}██╔════╝ ██╔════╝████╗ ████║{R}                              {CY}║{R}")
    print(f"  {CY}║{R}  {B}{CY}██║  ███╗█████╗  ██╔████╔██║{R}  {B}{WH}Motor de Inteligência{R}      {CY}║{R}")
    print(f"  {CY}║{R}  {B}{BL}██║   ██║██╔══╝  ██║╚██╔╝██║{R}  {DM}Pareceres Técnicos{R}         {CY}║{R}")
    print(f"  {CY}║{R}  {B}{MG}╚██████╔╝███████╗██║ ╚═╝ ██║{R}  {DM}SMOSU — Oliveira/MG{R}        {CY}║{R}")
    print(f"  {CY}║{R}  {B}{MG} ╚═════╝ ╚══════╝╚═╝     ╚═╝{R}                             {CY}║{R}")
    print(f"  {CY}{'═' * 60}{R}")
    print()
    print(f"  {B}{WH}  Versão 5.0{R}  {DM}│{R}  {GR}Painel Web de Gestão Documental{R}")
    print(f"  {DM}  ─────────────────────────────────────────────────{R}")
    print()
    print(f"  {YL}  ▸ Servidor:{R}     {B}http://localhost:{PORT}{R}")
    print(f"  {YL}  ▸ Documentos:{R}   {n_tipos} tipos registrados")
    print(f"  {YL}  ▸ Base Legal:{R}   {n_leis} leis/normas cadastradas")
    print(f"  {YL}  ▸ Treino IA:{R}    {n_treino} arquivos de instrução")
    print()
    print(f"  {DM}  ┌─────────────────────────────────────────────┐{R}")
    print(f"  {DM}  │{R}  {GR}📂 Entrada:{R}  {DM}1_Colar_JSON_Aqui/{R}             {DM}│{R}")
    print(f"  {DM}  │{R}  {BL}📁 Saída:{R}    {DM}2_Documentos_Prontos/{R}           {DM}│{R}")
    print(f"  {DM}  │{R}  {MG}📚 Treino:{R}   {DM}3_Treinar_Inteligencia/{R}         {DM}│{R}")
    print(f"  {DM}  │{R}  {YL}📋 Base:{R}     {DM}03_Retroalimentacao_e_Estudos/{R}  {DM}│{R}")
    print(f"  {DM}  └─────────────────────────────────────────────┘{R}")
    print()
    print(f"  {DM}  Engenheiro: Diego Tarcísio N. Vilela — CREA 235.474/D{R}")
    print(f"  {DM}  Secretaria Municipal de Obras — Prefeitura de Oliveira{R}")
    print()
    print(f"  {GR}  ✓ Sistema pronto. Abrindo navegador...{R}")
    print(f"  {DM}  Pressione Ctrl+C para encerrar.{R}")
    print()

    server = HTTPServer(("localhost", PORT), Handler)
    def _abrir():
        time.sleep(1)
        webbrowser.open(f"http://localhost:{PORT}")
    threading.Thread(target=_abrir, daemon=True).start()
    try: server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n  {YL}⏹  Painel GEM encerrado com segurança.{R}\n")

if __name__ == "__main__":
    main()
