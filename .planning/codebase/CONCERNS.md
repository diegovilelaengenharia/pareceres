# Codebase Concerns

**Analysis Date:** 2026-05-06 (atualizado pós-Milestone v3.0)

## Resolved Issues (Histórico)

| Issue | Resolução | Fase |
|-------|-----------|------|
| Paths hardcoded | Portabilidade via `pathlib`/`config.py` | Fase 3 (v2.0) |
| Lógica legada no compilador | Consolidado em `TIPOS_DOCUMENTO` | Fase 4 (v2.0) |
| Falta de template checker | `template_checker.py` criado | Fase 5 (v2.0) |
| Modelo narrativo insatisfatório | Reescrita tripartite + enricher | Fases 11, 02.1, 16 |

## Tech Debt Atual

**Shim de Compatibilidade `componentes.py`:**
- Issue: O arquivo `generators/componentes.py` é um shim DEPRECATED que re-exporta funções do pacote `generators/componentes/`.
- Files: `Sistema/motor/generators/componentes.py`
- Impact: Confusão — existem dois "componentes" (arquivo e pasta). Imports antigos continuam funcionando, mas novos devem usar o pacote diretamente.
- Fix: Verificar se algum import ainda usa o shim e removê-lo quando seguro.

**Ausência de Testes Unitários:**
- Issue: Apenas testes E2E (JSON→DOCX). Funções individuais de cálculo, aliases e enricher não possuem testes isolados.
- Files: `calculadora_indices.py`, `_aliases.py`, `enricher.py`
- Impact: Regressões em lógicas internas podem passar despercebidas.
- Priority: Medium — mitigado pelo Golden Dataset.

**Duas bases de conhecimento sem separação clara:**
- Issue: `Sistema/base_conhecimento/` (39 docs) e `Sistema/inteligencia/Knowledge/` (8 docs) coexistem sem documentação de propósito.
- Impact: Dificulta manutenção e pode causar redundância.
- Fix: Documentar que `base_conhecimento/` é o corpus jurídico bruto e `Knowledge/` são instruções processadas para o SIA.

## Known Bugs

**Conversão PDF via Word COM:**
- Issue: O bloqueio na conversão automática para PDF via Word COM persiste em algumas máquinas.
- Workaround: A geração de PDF foi desativada por solicitação do usuário. O DOCX é o formato final.
- Status: Aceito como limitação.

## Security Considerations

**Acesso ao Sistema de Arquivos:**
- Risk: Caminhos construídos dinamicamente a partir de dados do JSON.
- Current mitigation: Caminhos centralizados em `config.py`, caracteres perigosos sanitizados em `_gerar_nome_saida()`.
- Recommendations: Se o sistema for exposto a entradas não confiáveis, adicionar validação de path traversal.

## Fragile Areas

**Sincronização Templates JSON ↔ Componentes DOCX:**
- Files: `motor/templates/*.json` vs `generators/componentes/`
- Why fragile: Adicionar um campo no template sem atualizar o componente resulta em omissão silenciosa.
- Mitigation: `template_checker.py` + Golden Dataset com `validador_fidelidade.py`.

**Mapeamento TIPOS_DOCUMENTO em config.py:**
- Files: `core/config.py` (linhas 128-195)
- Why fragile: Cada novo tipo requer entrada manual no dicionário. Tipo não mapeado causa `ValueError`.
- Mitigation: Mensagem de erro clara com lista de tipos disponíveis.

## Test Coverage Gaps

**Cobertura por módulo:**

| Módulo | Cobertura | Tipo |
|--------|-----------|------|
| `geradores_core.py` | ✅ Alta | E2E via Golden Dataset |
| `enricher.py` | ⚠️ Baixa | Apenas via integração |
| `_aliases.py` | ⚠️ Baixa | Apenas via integração |
| `calculadora_indices.py` | ⚠️ Baixa | Apenas via integração |
| `componentes/` | ✅ Média | Via geração de DOCX |
| `mcp-smosu/tools.py` | ✅ Média | Testes próprios em test_tools.py |

---

*Concerns audit: 2026-05-06 (pós-Milestone v3.0)*
