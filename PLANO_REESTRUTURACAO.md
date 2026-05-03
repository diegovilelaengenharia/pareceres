# Plano de Reestruturação — Projeto Pareceres GEM

> **Data:** Maio de 2026  
> **Objetivo:** Simplificar a estrutura do projeto, corrigir referências quebradas e torná-lo mais rápido de usar e manter.

---

## 1. Diagnóstico — O que está confuso hoje

### Problemas críticos (causam erros)

| # | Problema | Localização |
|---|---------|-------------|
| P1 | `GEMINI.md` aponta para `3_Treinar_Inteligencia/` — pasta que **não existe mais** | `/GEMINI.md` |
| P2 | `painel_gem.py` referencia `03_Retroalimentacao_e_Estudos/` — pasta que **não existe** | `Sistema/motor/ui/painel_gem.py` linhas 22–25 |
| P3 | Tab "Base de Conhecimento" no Painel provavelmente mostra pasta vazia por causa do P2 | Painel web |

### Problemas de organização (causam confusão)

| # | Problema | Localização |
|---|---------|-------------|
| O1 | Arquivos de **log dentro do código-fonte** (`motor.log`, `motor.json.log`) | `Sistema/motor/` e `Sistema/motor/core/` |
| O2 | JSONs de **processos reais e de teste** misturados em `motor/json/` (dentro do código!) | `Sistema/motor/json/` |
| O3 | `historico_pareceres/` (dados gerados) dentro do código | `Sistema/motor/historico_pareceres/` |
| O4 | `generators/geradores/` — pasta **dentro de pasta de mesmo nome** (redundância) | `Sistema/motor/generators/geradores/` |
| O5 | `__pycache__` raiz com 9 arquivos **obsoletos do Python 3.13** ainda presentes | `Sistema/motor/__pycache__/` |
| O6 | **Dois conjuntos de modelos JSON**: `Modelos/` (16 arquivos simplificados) e `motor/templates/` (40 completos) — finalidade pouco clara | `Modelos/` e `Sistema/motor/templates/` |
| O7 | Arquivos de inteligência com **numeração duplicada**: `04_GABARITO_PARECER.md` e `04_GEM_TRIAGEM.md` | `Sistema/inteligencia/` |
| O8 | `docs/` dentro de `Sistema/` com subpastas `base_conhecimento/`, `exemplos_entrada/`, `exemplos_saida/`, `historico/` — mas `base_conhecimento/` deveria ser acessível via Painel | `Sistema/docs/` |
| O9 | `motor/prompt_modelo.md` solto dentro da pasta de código | `Sistema/motor/prompt_modelo.md` |

---

## 2. Estrutura Proposta (Depois)

```
02. Pareceres/
│
├── INICIAR.bat                   ← (renomear de GERAR_DOCUMENTOS.bat)
├── LEIAME.md                     ← (renomear de INSTRUCOES.md)
│
├── Entrada/                      ← coloque aqui os JSONs para processar
├── Saida/                        ← documentos gerados saem aqui
│   └── _Historico/               ← (mover motor/historico_pareceres/ para cá)
│
├── Modelos/                      ← modelos de referência (mantém igual)
│
└── Sistema/
    │
    ├── base_conhecimento/        ← (mover de docs/base_conhecimento/)
    │   ├── bairros_zoneamento_ipm.md
    │   ├── codex_legal.json
    │   ├── decreto_4149_2019.md
    │   └── ... (demais arquivos de leis e diretrizes)
    │
    ├── inteligencia/             ← instruções para a IA (Gemini/Claude)
    │   ├── 00_INSTRUCAO_SISTEMA.md
    │   ├── 01_INSTRUCOES.md
    │   ├── 02_REFERENCIA.md
    │   ├── 03_VARIAVEIS.md
    │   ├── 04_TRIAGEM.md
    │   ├── 05_GABARITO_PARECER.md  ← (renumerar, era 04_GABARITO)
    │   ├── 06_MAPA_INTELIGENCIA.md ← (renumerar, era 05)
    │   ├── 07_BLOCOS_CONSIDERANDOS.md ← (renumerar, era 06)
    │   ├── 08_COMO_USAR.md         ← (renumerar, era 07)
    │   └── prompt_modelo.md        ← (mover de motor/)
    │
    ├── logs/                     ← (novo) todos os logs aqui
    │   ├── motor.log
    │   └── motor.json.log
    │
    └── motor/                    ← código Python (mais limpo)
        ├── core/                 ← config, logger, validação
        ├── analyzers/            ← análise de PDF/Gemini
        ├── extractors/           ← extração de texto
        ├── generators/           ← geração de documentos
        │   └── (fundir geradores/ aqui — sem subpasta)
        ├── utils/                ← utilitários
        ├── ui/                   ← interface web
        ├── scripts/              ← scripts de manutenção
        ├── templates/            ← JSON templates (40 tipos)
        ├── logos/                ← imagens
        └── requirements.txt
```

---

## 3. Passos de Execução

Cada fase é independente — você pode executar uma de cada vez.

---

### FASE 1 — Limpeza sem risco (5 min)
> Remover arquivos desnecessários sem alterar nada que funciona.

```
[ ] 1.1  Deletar toda a pasta:  Sistema/motor/__pycache__/   (arquivos stale Python 3.13)
[ ] 1.2  Deletar arquivo:       Sistema/motor/json/test_inexistente.json
[ ] 1.3  Deletar arquivo:       Sistema/motor/json/teste_desconhecido.json
[ ] 1.4  Deletar arquivo:       Sistema/motor/json/teste_gemma.json
[ ] 1.5  Deletar pastas vazias: Sistema/docs/exemplos_entrada/
                                Sistema/docs/exemplos_saida/
                                Sistema/docs/historico/
```

---

### FASE 2 — Mover dados para fora do código (10 min)
> Arquivos de dados (JSONs de processos, logs, histórico) não devem ficar dentro da pasta de código Python.

```
[ ] 2.1  Criar pasta:           Saida/_Historico/
[ ] 2.2  Mover todos os JSONs:  Sistema/motor/historico_pareceres/*.json  →  Saida/_Historico/
[ ] 2.3  Mover JSONs de output: Sistema/motor/json/_output_testes/        →  Saida/_Testes/
[ ] 2.4  Criar pasta:           Sistema/logs/
[ ] 2.5  Mover logs:            Sistema/motor/motor.log           →  Sistema/logs/
                                Sistema/motor/motor.json.log      →  Sistema/logs/
                                Sistema/motor/core/motor.json.log →  Sistema/logs/

[ ] 2.6  Mover JSONs de processos reais (motor/json/processo_*.json, 1270_*.json)
         →  Entrada/_Arquivo/   (processos antigos fora de uso)
```

---

### FASE 3 — Mover base de conhecimento (5 min)
> Corrige a referência quebrada do Painel (Problema P2).

```
[ ] 3.1  Mover pasta inteira:   Sistema/docs/base_conhecimento/  →  Sistema/base_conhecimento/
[ ] 3.2  Mover docs soltos:     Sistema/docs/Guia_Pareceres_Completos.md  →  Sistema/inteligencia/
                                Sistema/docs/RETROALIMENTACAO_IA.md       →  Sistema/inteligencia/
                                Sistema/docs/TROUBLESHOOTING.md           →  (raiz do projeto)
[ ] 3.3  Deletar pasta vazia:   Sistema/docs/
```

---

### FASE 4 — Corrigir referências no código (15 min)
> Corrige os problemas P1, P2, O1, O3 no código Python.

```
[ ] 4.1  Em painel_gem.py (linhas 22–25), corrigir:
         PASTA_RETRO = ... "03_Retroalimentacao_e_Estudos"
         → PASTA_BASE_CONHECIMENTO = os.path.join(PROJECT_ROOT, "Sistema", "base_conhecimento")
         → PASTA_HIST = os.path.join(PROJECT_ROOT, "Saida", "_Historico")

[ ] 4.2  Em core/config.py, adicionar/corrigir:
         PASTA_BASE_CONHECIMENTO = os.path.join(PROJECT_ROOT, "Sistema", "base_conhecimento")
         PASTA_LOGS = os.path.join(PROJECT_ROOT, "Sistema", "logs")

[ ] 4.3  Em core/logger.py, apontar log para:
         Sistema/logs/motor.log

[ ] 4.4  Atualizar GEMINI.md — corrigir as referências:
         @3_Treinar_Inteligencia/  →  @Sistema/inteligencia/
```

---

### FASE 5 — Simplificações opcionais (20 min)
> Melhorias adicionais que reduzem confusão mas exigem mais cuidado.

```
[ ] 5.1  Fundir generators/geradores/ em generators/
         (mover _aliases.py para generators/, deletar subpasta geradores/)
         → Atualizar imports nos arquivos que referenciam geradores._aliases

[ ] 5.2  Renumerar inteligencia/ para corrigir duplicata no 04:
         04_GABARITO_PARECER.md  →  05_GABARITO_PARECER.md  (e reordenar 05, 06, 07)

[ ] 5.3  Renomear arquivos de entrada do usuário:
         GERAR_DOCUMENTOS.bat  →  INICIAR.bat
         INSTRUCOES.md         →  LEIAME.md
         → Atualizar qualquer referência interna

[ ] 5.4  Mover motor/prompt_modelo.md  →  Sistema/inteligencia/prompt_modelo.md
```

---

## 4. Resumo do Impacto para o Usuário

| O que muda para o usuário diário | Impacto |
|----------------------------------|---------|
| Clicar `INICIAR.bat` para abrir o painel | Nome mais claro (opcional) |
| Colocar JSONs em `Entrada/` | **Sem mudança** |
| Ver resultados em `Saida/` | **Sem mudança** |
| Histórico de pareceres anteriores | Agora em `Saida/_Historico/` (mais lógico) |
| Base de conhecimento no painel web | **Corrigida** (estava quebrada) |
| Logs para diagnóstico | Agora em `Sistema/logs/` (fácil achar) |

---

## 5. Ordem Recomendada de Execução

```
FASE 1 (limpeza)  →  FASE 2 (mover dados)  →  FASE 3 (base_conhecimento)
    →  FASE 4 (corrigir código)  →  TESTAR  →  FASE 5 (opcional)
```

> **Antes de executar as Fases 4 e 5**, faça um commit Git ou uma cópia de segurança da pasta `Sistema/motor/`.
> O projeto já tem `.git` configurado — basta rodar `git add -A && git commit -m "antes da reestruturação"` no terminal.

---

*Gerado por Claude — Cowork mode — Projeto Pareceres GEM / SMOSU Oliveira MG*
