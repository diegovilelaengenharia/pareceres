# Phase 16: Refatoração do Gerador DOCX — Research

**Researched:** 2026-05-05
**Domain:** Python-docx pipeline — geração de documentos oficiais (SMOSU Oliveira-MG)
**Confidence:** HIGH (baseado em leitura direta do código-fonte do projeto)

---

## Summary

Este relatório documenta uma investigação completa do pipeline de geração DOCX do sistema GEM, lendo diretamente cada arquivo-fonte relevante. O objetivo é responder com precisão por que os textos dos pareceres ficam pobres, como os templates JSON poderiam ser melhor aproveitados, e qual arquitetura permitiria uma refatoração limpa.

**O problema central identificado** é que os templates JSON contêm modelos narrativos ricos (`modelo_abertura`, `modelo_considerandos`, `modelo_conclusao`) que **nunca são lidos nem aplicados** durante a geração DOCX. O pipeline lê apenas `campos_obrigatorios` e `documentos_tipicos` do template. Todo o conteúdo textual deve vir 100% do JSON de entrada produzido pelo Gemini. Quando o Gemini não produz texto suficientemente específico, não existe fallback de qualidade — apenas marcadores `[PREENCHER: campo]`. Isso explica diretamente a pobreza textual.

**Primary recommendation:** Criar um estágio de "enriquecimento de dados" entre a leitura do JSON de entrada e a geração DOCX. Esse estágio lê o template, interpola os `modelo_*` com os dados concretos do processo, e preenche campos faltantes com conteúdo narrativo real (não marcadores). O resultado é um dicionário enriquecido que alimenta os geradores existentes — sem reescrever a renderização DOCX.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Leitura e validação do JSON de entrada | `compilador.py` | `geradores_core.py` | Compilador faz pré-voo; geradores_core faz normalização de aliases e campos ausentes |
| Enriquecimento de conteúdo textual | AUSENTE (gap atual) | Template JSON | Nenhum módulo faz interpolação dos modelos do template nos dados |
| Renderização DOCX por componente | `componentes.py` | `formatacao.py` | Cada `build_*` constrói uma seção visual; formatacao.py são helpers de baixo nível |
| Preview HTML | `preview_html.py` | — | Módulo autônomo, reflete os dados mas não acompanha todas as seções do DOCX |
| Despacho de gerador por tipo | `geradores_core.py` | `config.TIPOS_DOCUMENTO` | GERADORES dict e config mapeiam tipo → função geradora |
| Templates de conteúdo por tipo de documento | `templates/*.json` | — | 40 arquivos, cada um com modelos narrativos e estrutura esperada |
| Normalização de aliases do Gemini | `_aliases.py` | — | Resolve sinônimos antes do pipeline principal |

---

## Diagnóstico Técnico Detalhado

### Problema 1 — Modelos do template são completamente ignorados

**Evidência verificada em `geradores_core.py`:**

```python
template = carregar_template(tipo)          # linha 393 — carrega o JSON do template
obrigatorios = template.get("campos_obrigatorios", [])  # linha 397 — único uso do template
```

A função `carregar_template()` carrega o JSON completo, mas o código imediatamente após só extrai `campos_obrigatorios` para validação. Os campos `modelo_abertura`, `modelo_considerandos`, `modelo_conclusao` e `documentos_tipicos` **nunca são lidos** após essa linha. O template é depois passado para os geradores (`gerar_parecer_tecnico(doc, dados, template)`) onde é usado apenas para `template.get("titulo_documento", ...)`.

**Exemplo concreto — `habitese_comum.json`:**
```json
"modelo_considerandos": [
    "[SE data_complemento] conforme complemento anexado... a construção confere com o projeto aprovado...",
    "[OBRIGATÓRIO] o imóvel possui Alvará de Construção nº [numero_alvara]...",
    "[OBRIGATÓRIO] o requerente apresentou... Matrícula [matricula_sri]..."
]
```
Estes modelos são ricos, específicos e corretos juridicamente. Eles nunca chegam ao documento gerado. [VERIFIED: leitura direta de geradores_core.py e habitese_comum.json]

### Problema 2 — Fallback de conteúdo ausente usa marcadores, não texto real

**Evidência em `geradores_core.py`, linhas 408-451:**

```python
campos_faltantes = [c for c in obrigatorios if not dados.get(c)]
# ...
for c in faltantes_criticos:
    dados[c] = f"[PREENCHER: {c}]"
```

Quando `considerandos` está ausente ou vazio, o sistema injeta `[PREENCHER: considerandos]` no documento oficial. Isso é tecnicamente correto como sinalização, mas resulta em documentos que literalmente contêm `[PREENCHER: considerandos]` como conteúdo de um parecer técnico oficial. [VERIFIED: leitura direta de geradores_core.py]

### Problema 3 — componentes.py é um monolito de 1048 linhas

**Evidência verificada:**
- Arquivo: `componentes.py` com 1048 linhas [VERIFIED: leitura direta]
- Responsabilidades misturadas: utilitários de string (`_parse_numero`, `_ensure_list`), renderização de tabelas (identificação, carimbo, partes, histórico), corpo narrativo, conclusão, assinatura, cards de documentos, comunicado de pendência, memória de cálculo
- Funções públicas exportadas: `build_titulo`, `build_identificacao`, `build_destinatario`, `build_dados_carimbo`, `build_corpo`, `build_conclusao_e_docs`, `build_conclusao_simples`, `build_assinatura`, `build_comunicado_pendencia`, `build_partes_envolvidas`, `build_historico_cronologico`, `build_memoria_calculo` (12 funções)
- Funções internas: `_ensure_list`, `_parse_numero`, `_data_hoje_extenso`, `_apply_cell_fill`, `_set_cell_width`, `_build_conclusao_bloco`, `_box_colorido`

**Agrupamentos naturais identificados para quebra:**
1. `componentes_tabelas.py` — identificação, carimbo, partes, histórico (todas as tabelas de metadados)
2. `componentes_corpo.py` — abertura, considerandos, multas, condicionantes, parágrafos extras
3. `componentes_conclusao.py` — fundamentação legal, conclusão, documentos a emitir
4. `componentes_assinatura.py` — assinatura e data
5. `componentes_comunicado.py` — layout de pendência (cards coloridos)
6. `componentes_calculo.py` — memória de cálculo

### Problema 4 — Preview HTML não reflete fielmente o DOCX

**Divergências identificadas entre `preview_html.py` e a geração DOCX:**

| Seção | No DOCX | No Preview HTML |
|-------|---------|-----------------|
| Carimbo técnico | Sempre exibido para `parecer_tecnico` | Só exibido se `tipo_relatorio.startswith("alvara", "regularizacao")` (linha 547) — falta `parecer_tecnico` e `regularizacao_complexa_multipla` |
| Partes Envolvidas | Renderizado via `build_partes_envolvidas()` | Completamente ausente no preview |
| Histórico Cronológico | Renderizado via `build_historico_cronologico()` | Completamente ausente no preview |
| Memória de Cálculo | Seção destacada `build_memoria_calculo()` | Mostrada em `<details>` oculto (não inline) |
| Fundamentação Legal | Seção própria com bases legais fixas | Misturada no `_html_corpo()` como lista simples |
| Cabeçalho DOCX | Logo brasão + nome prefeitura (imagem real) | Ícone 🏛 em texto — diferença visual significativa |
| Layout certidoes_separadas | Usa `devolutiva_retificacao` com 3 seções numeradas | Preview usa `_html_corpo()` genérico |

[VERIFIED: leitura direta de preview_html.py e geradores_core.py]

### Problema 5 — Achatamento de campos aninhados é frágil

**Evidência em `geradores_core.py`, linhas 348-350:**

```python
if "campos_obrigatorios" in dados and isinstance(dados["campos_obrigatorios"], dict):
    dados.update(dados.pop("campos_obrigatorios"))
```

Este código presume que o Gemini pode entregar os campos dentro de uma chave `campos_obrigatorios`. Se o Gemini aninhar dentro de qualquer outra chave (ex: `dados_tecnicos`, `informacoes`), o achatamento não ocorre e campos ficam inacessíveis. O alias resolver (`_aliases.py`) ameniza parte disso, mas não resolve estruturas arbitrariamente aninhadas. [VERIFIED: leitura direta]

### Problema 6 — Interpolação de placeholders nos modelos não existe

Os templates usam placeholders estilo `[campo]` (ex: `[numero_processo]`, `[area_total_construida]`). Não existe nenhum código no sistema que realize a substituição `[campo]` → `dados["campo"]`. Isso significa que os modelos do template são inutilizáveis sem um mecanismo de interpolação. [VERIFIED: ausência confirmada em todos os arquivos Python lidos]

---

## Standard Stack

### Core (já instalado e em uso)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| python-docx | 1.2.0 | Geração e manipulação de .docx | Única biblioteca Python madura para DOCX; já em uso extensivo no projeto |
| Python stdlib (re, json, os, pathlib) | 3.x | Regex, JSON, paths | Já em uso; sem dependências novas |

[VERIFIED: `pip show python-docx` retornou Version: 1.2.0]

### Sem novas dependências necessárias

A refatoração proposta não requer novas bibliotecas. O mecanismo de interpolação de templates pode ser implementado com `str.format_map()` ou substituição regex simples — disponível na stdlib. [ASSUMED: regex-based interpolation é suficiente para a sintaxe `[campo]`]

---

## Architecture Patterns

### System Architecture Diagram

```
JSON de Entrada (Gemini)
       |
       v
[_aliases.normalizar_dados()] ── resolve sinônimos
       |
       v
[NOVO: enricher.enriquecer_dados()]
   - carregar_template(tipo)
   - interpolar modelo_abertura → dados["paragrafo_abertura"] se vazio
   - interpolar modelo_considerandos → dados["considerandos"] se vazio
   - interpolar modelo_conclusao → dados["conclusao"] se vazio
   - preencher documentos_tipicos → dados["documentos_emitir"] se vazio
   - validar campos críticos (sem [PREENCHER])
       |
       v
[geradores_core.gerar(dados_enriquecidos)]
   - _criar_documento_base()
   - despacho via GERADORES[categoria]
       |
       v
[componentes/*.py] (pós-quebra do monolito)
   build_header → build_titulo → build_identificacao
   → build_dados_carimbo → build_partes → build_historico
   → build_corpo → build_memoria_calculo
   → build_conclusao_e_docs → build_assinatura
       |
       v
[preview_html.py] (atualizado)
   - deve espelhar exatamente as seções renderizadas pelo DOCX
   - mesmo conjunto de seções condicionais

    DOCX final salvo em Saida/
```

### Recommended Project Structure (após refatoração)

```
Sistema/motor/generators/
├── geradores_core.py          # despacho + documento base (sem mudança de interface)
├── enricher.py                # NOVO: estágio de enriquecimento de dados com template
├── compilador.py              # pré-voo + preview + invoca gerar() (sem mudança)
├── compilador_livre.py        # modo texto_livre (sem mudança)
├── cabecalho.py               # cabeçalho e rodapé (sem mudança)
├── formatacao.py              # helpers de baixo nível (sem mudança)
├── _aliases.py                # normalização de aliases (sem mudança)
├── componentes/               # NOVO: pacote (quebra do monolito)
│   ├── __init__.py            # re-exporta tudo para compatibilidade com imports existentes
│   ├── tabelas.py             # build_identificacao, build_dados_carimbo, build_partes, build_historico
│   ├── corpo.py               # build_corpo (abertura, considerandos, multas, condicionantes)
│   ├── conclusao.py           # build_fundamentacao, build_conclusao_e_docs, build_conclusao_simples
│   ├── assinatura.py          # build_assinatura
│   ├── comunicado.py          # build_comunicado_pendencia
│   └── calculo.py             # build_memoria_calculo
├── gerador_sero.py            # sem mudança
├── gerar_templates.py         # sem mudança
├── gerar_esquema_base.py      # sem mudança
└── componentes.py             # DEPRECATED: mantido como shim de compatibilidade
                               # importa tudo de componentes/ e re-exporta
```

**Estratégia de compatibilidade retroativa para a quebra do monolito:**
O arquivo `componentes.py` atual pode ser transformado em um shim que apenas importa e re-exporta tudo do novo pacote `componentes/`. Isso garante que qualquer import externo existente (`from generators.componentes import build_corpo`) continue funcionando sem alteração. [ASSUMED: não há testes automatizados verificando os imports; baseado na ausência de arquivos de teste identificados]

### Pattern 1: Template Enricher — Interpolação de Modelos

**O que é:** Módulo `enricher.py` que lê o template JSON, interpola placeholders `[campo]` com os valores dos dados concretos, e preenche campos ausentes com conteúdo narrativo de qualidade.

**Quando usar:** Sempre, como primeiro estágio após `normalizar_dados()` e antes de `gerar()`.

**Lógica de prioridade:** Dados do Gemini SEMPRE têm prioridade. O enriquecedor só preenche campos **ausentes ou vazios**. Nunca sobrescreve conteúdo que o Gemini produziu.

```python
# enricher.py — padrão proposto
import re
from generators.geradores_core import carregar_template

def _interpolar(texto: str, dados: dict) -> str:
    """Substitui [campo] pelo valor de dados['campo']. Mantém [campo] se ausente."""
    def repl(m):
        chave = m.group(1)
        val = dados.get(chave, "")
        return str(val) if val else m.group(0)  # mantém placeholder se não tem dado
    return re.sub(r'\[([^\]]+)\]', repl, texto)

def _interpolar_lista(lista: list, dados: dict) -> list:
    return [_interpolar(item, dados) for item in lista]

def enriquecer_dados(dados: dict, template: dict) -> dict:
    """
    Aplica modelos do template em campos ausentes do dict de dados.
    Preserva 100% do que o Gemini já produziu.
    Retorna dados enriquecido (in-place e retorno).
    """
    # paragrafo_abertura: usa modelo_abertura se ausente
    if not dados.get("paragrafo_abertura"):
        modelo = template.get("modelo_abertura", "")
        if modelo:
            dados["paragrafo_abertura"] = _interpolar(modelo, dados)

    # considerandos: usa modelo_considerandos se ausente ou lista vazia
    if not dados.get("considerandos"):
        modelos = template.get("modelo_considerandos", [])
        if modelos:
            # Filtra placeholders condicionais simples e interpola
            interp = _interpolar_lista(modelos, dados)
            # Remove itens com placeholders não resolvidos críticos (ex: [SE campo])
            dados["considerandos"] = [
                c for c in interp
                if not c.startswith("[SE ") or _tem_dado_condicional(c, dados)
            ]

    # conclusao: usa modelo_conclusao se ausente
    if not dados.get("conclusao"):
        modelo = template.get("modelo_conclusao", "")
        if modelo:
            dados["conclusao"] = _interpolar(modelo, dados)

    # documentos_emitir: usa documentos_tipicos se ausente
    if not dados.get("documentos_emitir"):
        tipicos = template.get("documentos_tipicos", [])
        if tipicos:
            dados["documentos_emitir"] = [
                {
                    "tipo": _interpolar(d.get("tipo", ""), dados),
                    "obs": _interpolar(d.get("obs", ""), dados) if d.get("obs") else None
                }
                for d in tipicos
            ]
    return dados
```

### Pattern 2: Preview HTML Fiel ao DOCX

**O que é:** Refatoração de `preview_html.py` para espelhar exatamente as mesmas condicionais de exibição que os geradores DOCX usam.

**Princípio:** O preview deve ter uma função `_decide_secoes(dados, template)` que retorna quais seções estão ativas — e tanto o DOCX quanto o HTML usam a mesma lógica.

**Correções específicas necessárias:**

1. `_html_carimbo()` deve ser exibido para todos os tipos com categoria `parecer_tecnico` — não apenas `startswith("alvara")`:
   ```python
   # Atual (errado):
   html_carimbo = _html_carimbo(dados) if dados.get("tipo_relatorio", "").startswith(("alvara", "regularizacao")) else ""
   
   # Correto:
   from core.config import TIPOS_DOCUMENTO
   categoria = TIPOS_DOCUMENTO.get(dados.get("tipo_relatorio", ""), "")
   html_carimbo = _html_carimbo(dados) if categoria == "parecer_tecnico" else ""
   ```

2. Adicionar `_html_partes_envolvidas(d)` espelhando `build_partes_envolvidas()`
3. Adicionar `_html_historico_cronologico(d)` espelhando `build_historico_cronologico()`
4. Mostrar `memoria_de_calculo` inline (não em `<details>` oculto) para parecer_tecnico

### Anti-Patterns a Evitar

- **Reescrever a renderização DOCX:** Os `build_*` existentes funcionam bem visualmente. A refatoração deve focar em dados e organização, não em reimplementar python-docx.
- **Quebrar imports existentes ao modularizar componentes.py:** Usar o shim `__init__.py` que re-exporta tudo.
- **Lógica condicional `[SE campo]` complexa no enricher:** Manter simples — se o campo existe interpola, se não existe mantém como vazio ou remove o item da lista.
- **Sobrescrever dados do Gemini com modelos do template:** O Gemini é a fonte de autoridade. Template é só fallback.
- **Remover `[PREENCHER]` do pipeline sem substituir por conteúdo real:** O objetivo é que o enriquecedor forneça conteúdo real, tornando os marcadores desnecessários — não apenas ocultá-los.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Interpolação de `[campo]` em strings | Motor de template completo (Jinja2, etc.) | `re.sub()` simples com `str.format_map()` | Os placeholders são simples e uniformes; dependência nova desnecessária |
| Preview fiel de DOCX | Conversor DOCX→HTML via LibreOffice | Reescrever `preview_html.py` com as mesmas condicionais | O preview é intencionalmente uma aproximação visual, não uma conversão exata |
| Validação de schema JSON | JSON Schema validator (jsonschema) | Manter o validador existente em `geradores_core.py` | Já funciona; a melhoria é no enriquecimento, não na validação |

**Key insight:** O maior ganho de qualidade textual vem de um módulo de ~100 linhas (`enricher.py`) que interpola os modelos já escritos nos templates JSON — não de uma reescrita arquitetural profunda.

---

## Common Pitfalls

### Pitfall 1: Quebra de imports ao modularizar componentes.py
**What goes wrong:** Ao mover funções para `componentes/tabelas.py`, etc., os 7 arquivos que importam de `componentes` quebram (`geradores_core.py`, `compilador_livre.py`, `gerar_devolutiva_retificacao` inline, etc.).
**Why it happens:** Python não move imports automaticamente.
**How to avoid:** Manter `componentes.py` como shim: `from generators.componentes.tabelas import *` etc. Todos os imports externos continuam funcionando.
**Warning signs:** `ImportError: cannot import name 'build_corpo' from 'generators.componentes'`

### Pitfall 2: Enriquecedor sobrescrevendo conteúdo do Gemini
**What goes wrong:** Se o Gemini produz `considerandos` parcialmente preenchidos (ex: lista com 1 item) e o enriquecedor os substitui pelo modelo completo, perde-se o conteúdo específico.
**Why it happens:** Verificação `if not dados.get("considerandos")` falha para listas não vazias.
**How to avoid:** Checar `if not dados.get("considerandos") or len(dados["considerandos"]) == 0`.
**Warning signs:** Documentos com considerandos genéricos substituindo os específicos que o Gemini produziu.

### Pitfall 3: Placeholders não resolvidos chegando ao documento
**What goes wrong:** `modelo_abertura` contém `[tipo_projeto_ex_residencial_unifamiliar]` que é um placeholder descritivo (não um campo real do JSON). Após interpolação, aparece literalmente no documento.
**Why it happens:** Os modelos nos templates misturaram campos reais (`[numero_processo]`) com descrições de placeholder para o Gemini (`[tipo_projeto_ex_residencial_unifamiliar]`).
**How to avoid:** No enricher, após interpolação, fazer uma segunda passagem para detectar e remover ou neutralizar qualquer `[PLACEHOLDER]` remanescente. Ou definir nos templates explicitamente quais são campos reais vs. descritivos.
**Warning signs:** Documentos contendo texto como `tipo_projeto_ex_residencial_unifamiliar` no meio de uma sentença.

### Pitfall 4: Preview mostrando carimbo para tipos errados
**What goes wrong:** A condição atual `startswith("alvara")` já está errada — tipo `regularizacao_complexa_multipla` tem categoria `parecer_tecnico` mas não começa com "alvara", logo o carimbo não aparece no preview mesmo que apareça no DOCX.
**Why it happens:** O preview usou uma heurística de nome em vez de consultar `TIPOS_DOCUMENTO`.
**How to avoid:** Sempre derivar a categoria via `TIPOS_DOCUMENTO.get(tipo_relatorio)` e usar isso como critério.
**Warning signs:** Discrepância entre preview e DOCX para `regularizacao_complexa_multipla` e futuros tipos.

### Pitfall 5: Lógica `[SE campo]` nos modelos do habitese
**What goes wrong:** `habitese_comum.json` tem `"[SE data_complemento] conforme complemento..."` — um condicional que o sistema atual não implementa. Se o enricher interpolar isso literalmente, o texto `[SE data_complemento]` aparece no documento.
**Why it happens:** Os templates foram escritos com semântica própria não implementada no motor.
**How to avoid:** Implementar tratamento para `[SE campo]`: se `dados.get("campo")` existe, incluir a sentença sem o prefixo `[SE campo]`; caso contrário, omitir o item inteiro da lista.
**Warning signs:** Texto `[SE data_complemento]` visível no documento gerado.

---

## Code Examples

### Exemplo: Lógica de preview que consulta TIPOS_DOCUMENTO

```python
# preview_html.py — correção da condição do carimbo
# Source: análise direta de config.py e geradores_core.py
from core.config import TIPOS_DOCUMENTO

def gerar_preview(dados: dict, alertas=None, destino=None, auto_abrir=True):
    tipo = dados.get("tipo_relatorio", "")
    categoria = TIPOS_DOCUMENTO.get(tipo, "")
    
    html_carimbo   = _html_carimbo(dados) if categoria == "parecer_tecnico" else ""
    html_partes    = _html_partes_envolvidas(dados) if dados.get("partes_envolvidas") else ""
    html_historico = _html_historico_cronologico(dados) if dados.get("historico_cronologico") else ""
    html_memoria   = _html_memoria(dados)  # inline, não oculto
    # ...
```

### Exemplo: Integração do enricher no fluxo principal

```python
# geradores_core.py — onde inserir o enriquecimento (após normalizar_dados, antes de gerar)
# Source: análise direta de geradores_core.py linhas 382-460
from generators.enricher import enriquecer_dados

def gerar(dados, caminho_saida=None):
    tipo = dados.get("tipo_relatorio")
    # ... (validações existentes) ...
    
    dados = normalizar_dados(dados)  # já existe
    template = carregar_template(tipo)  # já existe
    
    # NOVO: enriquecimento com modelos do template
    dados = enriquecer_dados(dados, template)
    
    # ... (resto do fluxo existente) ...
    doc = _criar_documento_base()
    gerador_fn = GERADORES[categoria]
    gerador_fn(doc, dados, template)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Achatamento de `campos_obrigatorios` | Alias resolver (`_aliases.py`) | Phase 9/10 | Melhorou resiliência, mas não resolve aninhamento arbitrário |
| PDF automático | PDF removido a pedido do usuário | Phase 12 | Simplificou o pipeline |
| Compilador monolítico único | `geradores_core.py` + `compilador.py` separados | Phase 4/9 | Boa separação de orchestração vs. despacho |
| `parecer_administrativo` ausente | Adicionado via Phase 15 | 2026-05-05 | Novo tipo de categoria disponível |

**Deprecated/outdated:**
- `compilador_livre.py` tem lógica de `_caminho_saida_completo()` duplicada de `geradores_core._gerar_nome_saida()` — candidato a deduplicação futura.

---

## Mapa de Templates e Categorias

| Quantidade | Categoria | Exemplos de tipos |
|-----------|-----------|-------------------|
| ~14 | `parecer_tecnico` | alvara_aprovacao, alvara_regularizacao, alvara_mcmv, alvara_construcao_comercial... |
| ~18 | `parecer_simples` | habitese_comum, certidao_localizacao, certidao_averbacao, alvara_renovacao... |
| 1 | `parecer_administrativo` | parecer_administrativo |
| 1 | `devolutiva_retificacao` | certidoes_separadas_localizacao_confrontacao |
| ~6 | `oficio` | oficio_meio_ambiente, memorando, parecer_juridico... |
| ~2 | `comunicado` / `comunicado_pendencia` | comunicado_indeferimento, comunicado_pendencia |

**Total templates JSON:** ~40 arquivos (verificado via `ls templates/`) [VERIFIED]

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Regex `re.sub()` é suficiente para interpolar `[campo]` dos modelos | Architecture Patterns | Se templates usarem sintaxe mais complexa (condicionais aninhadas), a implementação precisará de um mini-parser |
| A2 | Não há testes automatizados verificando imports de componentes.py | Architecture Patterns | Se existirem testes, a quebra de imports falharia imediatamente e a estratégia do shim seria confirmada |
| A3 | compilador_livre.py pode ser mantido sem mudanças na Fase 16 | Standard Stack | Se usuário quiser unificar os dois modos nesta fase, o escopo aumenta |

---

## Open Questions

1. **Tratamento de condicionais `[SE campo]` nos modelos do habitese**
   - What we know: `habitese_comum.json` usa a sintaxe `[SE campo] texto...` que o motor não suporta
   - What's unclear: O usuário quer suporte completo a condicionais, ou apenas interpolação simples?
   - Recommendation: Implementar parsing simples de `[SE campo]`: se campo presente → incluir texto sem o prefixo; se ausente → omitir item da lista

2. **Escopo da quebra de componentes.py**
   - What we know: O monolito tem 12 funções públicas e 7 funções internas
   - What's unclear: O usuário quer apenas refatoração interna (mesmo arquivo melhor organizado) ou criação do pacote `componentes/`?
   - Recommendation: Criar o pacote `componentes/` com shim de compatibilidade é o caminho correto — permite evolução incremental e não quebra nada

3. **Tratamento de placeholders descritivos nos modelos do template**
   - What we know: `alvara_aprovacao.json` tem `[tipo_projeto_ex_residencial_unifamiliar]` que é uma instrução para o Gemini, não um campo real
   - What's unclear: Estes devem ser removidos dos templates agora, ou o enricher deve detectá-los?
   - Recommendation: Limpar os templates ao mesmo tempo que implementa o enricher — é a oportunidade certa para alinhar a semântica dos modelos

---

## Environment Availability

Step 2.6: SKIPPED (sem novas dependências externas — refatoração é código Python puro com python-docx 1.2.0 já instalado)

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Nenhum detectado (sem pytest.ini, tox.ini, ou diretório tests/) |
| Config file | — |
| Quick run command | `python -c "from generators.enricher import enriquecer_dados; print('OK')"` |
| Full suite command | Teste manual com JSON de entrada real |

### Phase Requirements → Test Map

| Req ID | Comportamento | Tipo | Comando Automatizado | Arquivo existe? |
|--------|--------------|------|---------------------|-----------------|
| NFR-01 | Enriquecedor preenche paragrafo_abertura ausente via modelo | unit | `python enricher_test.py` | Criar em Wave 0 |
| NFR-01 | Enriquecedor NÃO sobrescreve paragrafo_abertura existente | unit | idem | Criar em Wave 0 |
| NFR-01 | Preview exibe carimbo para tipo `regularizacao_complexa_multipla` | smoke | render manual | — |
| FR-01 | Documento habitese gerado sem `[PREENCHER]` no conteúdo textual | smoke | geração com JSON mínimo | — |

### Wave 0 Gaps
- [ ] Criar `Sistema/motor/generators/enricher.py` — módulo de enriquecimento (novo)
- [ ] Criar `Sistema/motor/generators/componentes/__init__.py` — shim de re-exportação
- [ ] Criar `Sistema/motor/generators/componentes/tabelas.py` — funções de tabela extraídas
- [ ] Criar `Sistema/motor/generators/componentes/corpo.py` — build_corpo extraído
- [ ] Criar `Sistema/motor/generators/componentes/conclusao.py` — build_conclusao* extraídos
- [ ] Criar `Sistema/motor/generators/componentes/assinatura.py` — build_assinatura extraído
- [ ] Criar `Sistema/motor/generators/componentes/comunicado.py` — build_comunicado_pendencia extraído
- [ ] Criar `Sistema/motor/generators/componentes/calculo.py` — build_memoria_calculo extraído

---

## Security Domain

Não aplicável. A fase é puramente interna (refatoração de pipeline Python local, sem endpoints de rede, sem autenticação, sem dados externos). Os documentos são oficiais mas o vetor de risco não é técnico (autenticidade física da assinatura manuscrita, não digital). [ASSUMED: sem requisitos de segurança técnica específicos para esta fase]

---

## Sources

### Primary (HIGH confidence)
- Leitura direta de `geradores_core.py` (550 linhas) — fluxo completo de geração, onde template é e não é usado
- Leitura direta de `componentes.py` (1048 linhas) — funções de renderização, dimensões do monolito
- Leitura direta de `preview_html.py` (630 linhas) — condições de exibição vs. DOCX
- Leitura direta de `templates/alvara_aprovacao.json` e `templates/habitese_comum.json` — estrutura real dos modelos
- Leitura direta de `templates/certidoes_separadas_localizacao_confrontacao.json` — uso real de dados estruturados
- Leitura direta de `compilador.py` — fluxo preview → confirmação → DOCX
- Leitura direta de `config.py` — TIPOS_DOCUMENTO, constantes visuais
- Leitura direta de `_aliases.py` — normalização de campos
- Leitura direta de `compilador_livre.py` — modo texto_livre

### Secondary (MEDIUM confidence)
- `pip show python-docx` → Version: 1.2.0 confirmada [VERIFIED]
- `ls templates/` → ~40 arquivos JSON confirmados [VERIFIED]

---

## Metadata

**Confidence breakdown:**
- Diagnóstico dos problemas: HIGH — baseado em leitura direta do código, não inferência
- Arquitetura proposta (enricher.py): HIGH — o padrão é simples e direto
- Quebra de componentes.py: HIGH — as fronteiras naturais são claras
- Correções de preview_html.py: HIGH — as divergências foram verificadas linha a linha
- Estimativa de esforço: MEDIUM — depende de quantos templates precisam de limpeza de placeholders descritivos

**Research date:** 2026-05-05
**Valid until:** 2026-06-05 (código não muda sem commits explícitos)
