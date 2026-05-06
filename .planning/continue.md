# Continue — Fase 14 (Emissão de Certidões em Lote)

## Última Ação
Concluí a **Fase 3.1 (Integração MCP)**. O SIA v1.1 está publicado e validado, com 13 ferramentas operacionais e o Protocolo de Rigor Técnico implementado. A IA agora é capaz de realizar análises matemáticas e legais infalíveis via MCP.

## Próxima Ação
Iniciar a **Fase 14: Emissão de Certidões em Lote**.

**Passos imediatos:**
1. Analisar os requisitos da Fase 14 (emissão de múltiplas certidões — ex: Localização + Confrontação — a partir de um único processo/JSON).
2. Criar a SPEC da Fase 14.
3. Ajustar o `motor/generators/geradores_core.py` (ou script de orquestração) para iterar sobre a lista `documentos_emitir` do JSON e gerar múltiplos arquivos DOCX de uma só vez.

## Por Que
Atualmente, o motor gera um arquivo por execução. A Fase 14 permitirá que processos complexos que exigem várias certidões sejam resolvidos em um único clique, aumentando drasticamente a produtividade.

## Open Threads
- Definir como o motor deve nomear os arquivos múltiplos na pasta `Saida/`.
- Verificar se os modelos de certidão isolada (Localização, Confrontação, etc.) já possuem os campos mapeados corretamente no JSON unificado.
