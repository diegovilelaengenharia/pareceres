# Sistema GEM — SMOSU Oliveira/MG

Automação de pareceres técnicos e gestão documental.

---

## Como Usar

1. Dê duplo clique em `GERAR_DOCUMENTOS.bat` para abrir o Painel.
2. Copie um modelo de `Sistema/modelos/` para `Entrada/`, renomeie (ex: `processo_1234_2026.json`) e preencha os dados.
3. No Painel (que abre no navegador), valide e compile o documento.
4. O `.docx` e `.pdf` gerados aparecem automaticamente em `Saida/`.

---

## Solução de Problemas

**PDF não gerado (Word COM Error)**
- Certifique-se de que o Microsoft Word está instalado e ativado.
- Abra o Word manualmente uma vez antes de rodar o sistema.
- Se houver instância travada, encerre `WINWORD.EXE` no Gerenciador de Tarefas.

**Painel não abre / "Arquivo não encontrado"**
- Execute sempre pelo `GERAR_DOCUMENTOS.bat` na raiz.
- No Google Drive, confirme que o Drive para Desktop está sincronizado offline.

**Erro de dependências (ModuleNotFoundError)**
- Abra o PowerShell na pasta `Sistema/motor/` e execute:
  ```powershell
  pip install -r requirements.txt
  ```

**JSON inválido / erro de sintaxe**
- Use o [JSONLint](https://jsonlint.com/) para encontrar a linha do erro.
- Cole apenas o conteúdo entre `{ ... }`, sem os blocos ` ```json `.

**OCR lento ou travando**
- PDFs grandes (> 50 MB) podem demorar minutos.
- Se persistir, reduza o PDF ou use o Gemini anexando o arquivo diretamente.

---

**Engenheiro Responsável:** Diego Tarcísio Nunes Vilela — Prefeitura Municipal de Oliveira/MG
