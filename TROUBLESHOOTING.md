# 🛠️ Solução de Problemas (Troubleshooting) — Projeto GEM

Este guia contém soluções rápidas para os problemas técnicos mais comuns encontrados durante a operação do sistema.

## 1. Erro de Conversão para PDF (Word COM Error)
**Sintoma:** O documento DOCX é gerado, mas o sistema avisa que falhou ao converter para PDF.
**Causa:** O Microsoft Word local não pôde ser acionado via automação.
**Solução:**
- Certifique-se de que o **Microsoft Word está instalado** e ativado.
- Abra o Microsoft Word manualmente uma vez antes de rodar o sistema para garantir que não há janelas de "Ativação" ou "Atualização" bloqueando a interface.
- Verifique se não há instâncias travadas do Word no Gerenciador de Tarefas (encerre o processo `WINWORD.EXE` se necessário).

## 2. "Arquivo não encontrado" ou "Erro de Caminho"
**Sintoma:** O Painel GEM não abre ou não encontra os JSONs.
**Causa:** Execução fora do diretório correto ou permissões de pasta.
**Solução:**
- Execute sempre pelo arquivo `GERAR_DOCUMENTOS.bat` na raiz.
- Se estiver no Google Drive, certifique-se de que o **Drive para Desktop** está sincronizado e as pastas estão disponíveis "offline".

## 3. Erro de Dependências (ModuleNotFoundError)
**Sintoma:** O terminal fecha rápido ou mostra que falta um módulo (ex: `docx`, `docling`).
**Solução:**
- Abra o terminal (PowerShell) na pasta `_Sistema_Interno/01_Motor_Python/` e execute:
  ```powershell
  pip install -r requirements.txt
  ```

## 4. JSON Inválido / Erro de Sintaxe
**Sintoma:** O Painel GEM avisa que o JSON é inválido e não permite salvar.
**Causa:** Falta de vírgulas, aspas não fechadas ou caracteres especiais colados do Gemini.
**Solução:**
- Use um validador como o [JSONLint](https://jsonlint.com/) para identificar a linha do erro.
- Certifique-se de que não há blocos de texto do tipo ` ```json ` dentro do campo de texto do painel (cole apenas o conteúdo entre as chaves `{ ... }`).

## 5. OCR Local Lento ou Falhando
**Sintoma:** O sistema trava ao processar um PDF escaneado.
**Solução:**
- PDFs muito grandes (acima de 50MB) ou com centenas de páginas podem demorar alguns minutos.
- Se o erro persistir, tente reduzir o arquivo PDF ou use a extração manual via site do Gemini anexando o arquivo.

---
*Para outros problemas, consulte o Engenheiro Responsável.*
