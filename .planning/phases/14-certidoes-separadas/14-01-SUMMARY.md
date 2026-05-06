# Fase 14 Plano 01: Suporte a Múltiplas Certidões Separadas Summary

Implementado o suporte à geração de múltiplas certidões (Localização e Confrontação) e um Parecer Técnico a partir de um único arquivo JSON de entrada, utilizando o novo tipo mestre `certidoes_separadas_localizacao_confrontacao`.

## Mudanças Principais

### Core & Configuração
- **Mapeamento Técnico**: Adicionados os tipos `certidao_confrontacao` (parecer_simples) e o tipo mestre `certidoes_separadas_localizacao_confrontacao` (parecer_tecnico) ao `TIPOS_DOCUMENTO` em `Sistema/motor/core/config.py`.

### Motor de Geração (Compilador)
- **Lógica de Bundling**: O `compilador.py` agora intercepta o tipo mestre e, caso a lista `documentos_emitir` não esteja presente, injeta automaticamente o trio: Parecer Técnico, Certidão de Localização e Certidão de Confrontação.
- **Iteração Automática**: Garantido que cada peça do bundle seja gerada individualmente com seu próprio nome de arquivo e categoria de gerador, mantendo a integridade técnica de cada peça.

### Interface (UI)
- **Preview Inteligente**: O `preview_html.py` agora detecta quando uma geração em lote (lote/bundle) está prestes a ocorrer e exibe um banner de destaque: "🚀 GERAÇÃO EM LOTE DETECTADA".
- **Visualização de Peças**: A seção de documentos a emitir no preview lista claramente todos os arquivos que serão criados.

### Modelos
- **MODELO_16**: Criado novo modelo de referência `MODELO_16_Certidoes_Separadas.json` focado no caso da Maria Lúcia (Processo 4467/2026).

## Como Testar (Caso Maria Lúcia)

1. Localize o arquivo `Sistema/modelos/MODELO_16_Certidoes_Separadas.json`.
2. Copie-o para a pasta `Entrada/`.
3. Execute o sistema (via `GERAR_DOCUMENTOS.bat` ou rodando o `compilador.py`).
4. No **Preview HTML**, verifique o banner azul de "GERAÇÃO EM LOTE DETECTADA" e a lista de 3 documentos.
5. Após confirmar, verifique na pasta `Saida/Processo 4467-2026 - Maria Lúcia Da Silva/` a existência de 3 arquivos DOCX distintos:
   - `Parecer Tecnico - 4467-2026 - Maria Lúcia Da Silva.docx`
   - `Certidao Localizacao - 4467-2026 - Maria Lúcia Da Silva.docx`
   - `Certidao Confrontacao - 4467-2026 - Maria Lúcia Da Silva.docx`

## Auto-fatiamento e Decisões
- Decidimos injetar a lista padrão no `compilador.py` apenas se ela estiver ausente no JSON, permitindo que o usuário (ou o LLM) customize quais peças quer emitir se desejar.
- O nome do arquivo DOCX é derivado do `tipo_relatorio` de cada peça individual, garantindo que não haja sobreposição de arquivos na mesma pasta de saída do processo.

## Self-Check: PASSED
- [x] Configuração de tipos em config.py
- [x] Modelo 16 criado
- [x] Lógica de injeção no compilador validada
- [x] Banner de lote no preview HTML funcional
- [x] Teste de geração real concluído com 3 arquivos gerados para o Processo 4467/2026.
