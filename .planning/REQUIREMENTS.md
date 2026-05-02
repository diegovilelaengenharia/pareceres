# Requirements — Milestone v2.0

**Milestone:** v2.0 — Qualidade Interna e Manutenibilidade
**Scope:** Refatoração sem novas features. Foco nos 4 concerns abertos do CONCERNS.md.
**Created:** 2026-05-01

---

## Functional Requirements

### FR-01 — Portabilidade de Paths
- O motor deve ser executável sem edição manual de caminhos após clonar o repositório.
- Paths hardcoded (strings literais com `C:\`, `D:\`, etc.) devem ser substituídos por paths relativos usando `pathlib.Path` ou `os.path`.
- Entry points `.bat` devem usar `%~dp0` ou equivalente para resolução de caminho relativo ao script.
- **Acceptance:** `grep -r "C:\\" _Sistema_Interno/` retorna zero resultados em código Python.

### FR-02 — Limpeza de Lógica Legada no Compilador
- Remover ou consolidar a lógica de "tipos descritivos legados" em `compilador.py`.
- A função de despacho de tipo deve ser limpa, linear e mapeada exclusivamente via `config.TIPOS_DOCUMENTO`.
- Qualquer alias ou mapeamento remanescente de tipos antigos deve ser documentado ou removido se não utilizado.
- **Acceptance:** `compilador.py` não contém branches `if tipo in [...]` com listas hardcoded de tipos antigos.

### FR-03 — Mecanismo de Detecção de Dessincronização de Templates
- Criar um utilitário que compare os placeholders existentes nos templates Word (`.docx` em `0_Modelos_Prontos/`) com as chaves injetadas pelos geradores correspondentes em `geradores/`.
- O utilitário deve emitir um relatório de: (a) placeholders no template sem gerador, (b) campos no gerador sem placeholder no template.
- **Acceptance:** Executar `python template_checker.py` produz relatório sem erros críticos nos templates atuais.

### FR-04 — Documentação de Desenvolvedor
- Todos os módulos Python em `_Sistema_Interno/01_Motor_Python/` devem ter docstring de nível de módulo (`"""..."""` no topo do arquivo).
- Funções públicas com mais de 10 linhas devem ter docstring descrevendo parâmetros, retorno e efeitos colaterais.
- Criar `_Sistema_Interno/01_Motor_Python/ARCHITECTURE.md` descrevendo: fluxo de entrada → pré-voo → geração → saída, lista de módulos e responsabilidades.
- **Acceptance:** `python -c "import compilador; help(compilador)"` exibe documentação legível.

---

## Non-Functional Requirements

### NFR-01 — Sem Quebra de Compatibilidade
- Nenhuma alteração pode quebrar a geração de documentos existentes.
- A suite `run_tests.py --motor` deve passar 100% após cada fase.

### NFR-02 — Execução Local Windows
- O sistema deve continuar executando 100% local no Windows sem dependências externas novas.

### NFR-03 — Commits Atômicos por Fase
- Cada fase entregue em commit(s) rastreáveis, com mensagem descritiva.

---

## Out of Scope

- Novos tipos de documento ou fluxos de tramitação (→ v3.0+)
- Integração com sistemas externos (SEI, banco de dados, APIs) (→ v3.0+)
- Conversão automática para PDF em background (problema de ambiente, não de código)
- Interface web nova (→ backlog)
