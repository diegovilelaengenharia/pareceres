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
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return {"ok": True, "nome": nome}
    except json.JSONDecodeError as e:
        return {"ok": False, "erro": f"JSON invalido: {e}"}
    except Exception as e:
        return {"ok": False, "erro": str(e)}

def _compilar_script(script_name):
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, script_name), "--sem-preview"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", cwd=PROJECT_ROOT, timeout=120, env=env)
        saida = (result.stdout + result.stderr).strip()
        return {"ok": result.returncode == 0, "saida": saida}
    except subprocess.TimeoutExpired:
        return {"ok": False, "saida": "Timeout (>2min)."}
    except Exception as e:
        return {"ok": False, "saida": str(e)}

def api_compilar():
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
    pastas = {"entrada": PASTA_ENTRADA, "saida": PASTA_SAIDA, "modelos": PASTA_MODELOS, "treino": PASTA_TREINO}
    pasta = pastas.get(qual, PASTA_SAIDA)
    try:
        os.startfile(pasta)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "erro": str(e)}

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
        elif path == "/api/compilar-livre": self._json(api_compilar_livre())
        else: self._send(404, "text/plain", b"Not found")

    def do_DELETE(self):
        path = urllib.parse.urlparse(self.path).path
        if path.startswith("/api/remover-json/"):
            self._json(api_remover_json(urllib.parse.unquote(path[18:])))
        else: self._send(404, "text/plain", b"Not found")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\n  ================================================")
    print(f"   Painel GEM v2 -- Motor SMOSU Oliveira/MG")
    print(f"   http://localhost:{PORT}")
    print(f"   Pressione Ctrl+C para encerrar")
    print(f"  ================================================\n")
    server = HTTPServer(("localhost", PORT), Handler)
    def _abrir():
        time.sleep(1)
        webbrowser.open(f"http://localhost:{PORT}")
    threading.Thread(target=_abrir, daemon=True).start()
    try: server.serve_forever()
    except KeyboardInterrupt: print("\n  Painel encerrado.")

if __name__ == "__main__":
    main()
