---
phase: 15-refino-layout-administrativo
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: [
  "Sistema/motor/core/config.py",
  "Sistema/motor/generators/geradores_core.py",
  "Sistema/motor/generators/componentes.py",
  "Sistema/motor/templates/certidoes_separadas_localizacao_confrontacao.json"
]
autonomous: true
requirements: [FR-01, FR-02, ARCH-01]

must_haves:
  truths:
    - "O Parecer Técnico gerado para certidões não contém a tabela de Dados Técnicos (carimbo)."
    - "A categoria 'parecer_administrativo' está corretamente mapeada no config.py."
    - "A tabela de identificação não possui linhas vazias caso campos sejam omitidos."
  artifacts:
    - path: "Sistema/motor/core/config.py"
      provides: "Novo mapeamento de categoria administrativa"
    - path: "Sistema/motor/generators/geradores_core.py"
      provides: "Função gerar_parecer_administrativo"
  key_links:
    - from: "Sistema/motor/generators/geradores_core.py"
      to: "Sistema/motor/core/config.py"
      via: "TIPOS_DOCUMENTO mapping"
---

<objective>
Implementar um novo layout de "Parecer Administrativo" que seja limpo e focado em processos de certidões, removendo tabelas de índices urbanísticos desnecessárias e otimizando a tabela de identificação.

Objetivo: Reduzir a poluição visual em pareceres de certidões.
Saída: Novo gerador de layout e template atualizado.
</objective>

<execution_context>
@$HOME/.gemini/get-shit-done/workflows/execute-plan.md
@$HOME/.gemini/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@Sistema/motor/core/config.py
@Sistema/motor/generators/geradores_core.py
@Sistema/motor/generators/componentes.py
@Sistema/motor/templates/certidoes_separadas_localizacao_confrontacao.json
@Entrada/processo_4467_2026_MARIA_LUCIA.json
</context>

<tasks>

<task type="auto">
  <name>Configuração da Categoria Administrativa</name>
  <files>Sistema/motor/core/config.py</files>
  <action>
    - Adicionar a categoria `"parecer_administrativo": "parecer_administrativo"` ao dicionário `TIPOS_DOCUMENTO` (per D-01).
    - Alterar o mapeamento de `"certidoes_separadas_localizacao_confrontacao"` de `"parecer_tecnico"` para `"parecer_administrativo"`.
  </action>
  <verify>
    <automated>grep "parecer_administrativo" Sistema/motor/core/config.py</automated>
  </verify>
  <done>Configuração atualizada para suportar a nova categoria de layout.</done>
</task>

<task type="auto">
  <name>Implementação do Gerador Administrativo</name>
  <files>Sistema/motor/generators/geradores_core.py</files>
  <action>
    - Criar a função `gerar_parecer_administrativo(doc, dados, template)` baseada na `gerar_parecer_tecnico`.
    - Nesta nova função, remover as chamadas para `build_dados_carimbo(doc, dados)` e `build_memoria_calculo(doc, dados)` (per D-02).
    - Manter os blocos: Header, Título, Identificação, Partes, Histórico, Corpo e Conclusão+Docs.
    - Adicionar `"parecer_administrativo": gerar_parecer_administrativo` ao dicionário `GERADORES`.
  </action>
  <verify>
    <automated>python -c "from Sistema.motor.generators.geradores_core import GERADORES; assert 'parecer_administrativo' in GERADORES"</automated>
  </verify>
  <done>Motor de despacho atualizado com o novo layout administrativo.</done>
</task>

<task type="auto">
  <name>Refinamento Dinâmico da Identificação</name>
  <files>Sistema/motor/generators/componentes.py</files>
  <action>
    - Modificar `build_identificacao(doc, d)` para ser dinâmica (per D-04).
    - Em vez de `rows=3`, calcular a quantidade de linhas baseada em quais campos estão presentes (Processo, Assunto, Requerente).
    - Filtrar a lista `linhas` para remover tuplas onde o valor é vazio ou nulo.
    - Criar a tabela com o número exato de linhas filtradas.
  </action>
  <verify>
    <automated>grep "add_table" Sistema/motor/generators/componentes.py | grep "len("</automated>
  </verify>
  <done>Tabela de identificação otimizada para omitir campos vazios.</done>
</task>

<task type="auto">
  <name>Validação com Caso Maria Lúcia</name>
  <files>Sistema/motor/templates/certidoes_separadas_localizacao_confrontacao.json</files>
  <action>
    - Atualizar o template `certidoes_separadas_localizacao_confrontacao.json` para garantir que o `titulo_documento` seja "PARECER ADMINISTRATIVO" (opcional, conforme preferência de design).
    - Executar o compilador para o processo da Maria Lúcia: `python Sistema/motor/generators/compilador.py` (usando o arquivo em Entrada).
    - Verificar se o arquivo "Parecer Administrativo - 4467-2026 - Maria Lucia De Fatima Silva.docx" foi gerado sem a tabela de índices urbanísticos.
  </action>
  <verify>
    <automated>python Sistema/motor/generators/compilador.py --sem-preview</automated>
  </verify>
  <done>Novo layout validado visualmente e funcionalmente no pipeline de certidões.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Template -> Word | Dados injetados no DOCX podem conter caracteres especiais. |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-15-01 | Tampering | Templates | mitigate | Validação de esquema JSON existente já previne injeções maliciosas básicas. |
| T-15-02 | Information Disclosure | DOCX | accept | Documentos internos de uso administrativo, risco baixo. |
</threat_model>

<verification>
1. Verificar se `config.py` tem o mapeamento correto.
2. Gerar o documento da Maria Lúcia.
3. Abrir o DOCX e confirmar a ausência da tabela "DADOS TÉCNICOS DO PROJETO (Ref. Decreto nº 4.149/2019)".
</verification>

<success_criteria>
- Categoria `parecer_administrativo` funcional.
- Parecer de certidões gerado sem tabelas de índices (limpo).
- Tabela de identificação sem linhas vazias.
</success_criteria>

<output>
After completion, create `.planning/phases/15-refino-layout-administrativo/15-01-SUMMARY.md`
</output>
