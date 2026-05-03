# Codebase Concerns

**Analysis Date:** 2026-05-01

## Tech Debt

**Módulos sem Docstrings:**
- Issue: Nem todos os módulos Python possuem docstrings de nível de módulo conforme exigido pelos requisitos de qualidade.
- Files: `_Sistema_Interno/01_Motor_Python/*.py`
- Impact: Dificulta a manutenção e o entendimento rápido por novos desenvolvedores ou IAs.
- Fix approach: Executar a Fase 6 do Roadmap para documentar todos os módulos e funções públicas.

**Lógica Legada no Compilador:**
- Issue: Presença de código de despacho para "tipos descritivos legados" que não seguem o novo padrão `config.TIPOS_DOCUMENTO`.
- Files: `_Sistema_Interno/01_Motor_Python/compilador.py`
- Impact: Aumenta a complexidade do orquestrador e dificulta a manutenção dos tipos de documento.
- Fix approach: Executar a Fase 4 do Roadmap para consolidação total em `config.py`.

## Known Bugs

**Conversão PDF via Word COM:**
- Issue: O bloqueio na conversão automática para PDF via Word COM é um problema pré-existente e ainda não resolvido.
- Files: N/A (Impacta o fluxo de saída)
- Symptoms: Falha ao tentar exportar diretamente para PDF em algumas máquinas.
- Workaround: Exportação manual via Word ou uso de bibliotecas alternativas (pendente análise).

## Security Considerations

**Acesso ao Sistema de Arquivos:**
- Risk: O sistema executa operações de escrita e leitura baseadas em caminhos construídos dinamicamente.
- Files: `config.py`, `compilador.py`, `run_tests.py`.
- Current mitigation: Caminhos são validados e centralizados em `config.py`.
- Recommendations: Implementar verificações de "path traversal" se o sistema for exposto a entradas não confiáveis.

## Fragile Areas

**Sincronização de Templates (.docx):**
- Files: `0_Modelos_Prontos/*.docx` vs `_Sistema_Interno/01_Motor_Python/geradores/`.
- Why fragile: Alterações nos placeholders dos arquivos Word podem quebrar os geradores sem aviso prévio (falha silenciosa ou erro de execução).
- Safe modification: Atualmente requer teste manual após cada alteração de template.
- Test coverage: Gaps na verificação automática de placeholders. (Phase 5 do Roadmap visa resolver isso).

## Missing Critical Features

**Detector de Dessincronização de Templates:**
- Problem: Não há uma ferramenta que garanta que todos os campos exigidos por um template Word estão sendo fornecidos pelo gerador JSON.
- Blocks: Garantia de qualidade visual e técnica dos documentos gerados.
- Phase 5 do Roadmap.

## Test Coverage Gaps

**Testes Unitários:**
- What's not tested: Funções individuais de cálculo e validação não possuem testes unitários isolados, apenas testes de integração E2E.
- Files: `calculadora_indices.py`, `alertas_decadencia.py`.
- Risk: Regressões em lógicas de cálculo podem passar despercebidas se o resultado final do documento parecer correto.
- Priority: Medium.

### C-05 — Insatisfação com Modelo de Parecer Narrativo
- **Symptom**: O modelo v5.0 (narrativo e com bullets administrativos) não atingiu as expectativas do usuário em termos de clareza ou utilidade.
- **Context**: Tentativa de consolidar todo o dossiê em um único texto fluído falhou em agradar esteticamente ou funcionalmente.
- **Action**: Marcar para refatoração completa do motor de templates e da lógica de construção de texto. Evitar o uso do prefixo "Considerando que" de forma rígida.

---

*Concerns audit: 2026-05-01*
