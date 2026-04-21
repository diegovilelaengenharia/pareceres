# 📚 GEM — Pasta de Conhecimento para Upload

Esta pasta contém os arquivos que devem ser carregados na seção
**"Conhecimento"** do seu GEM no Gemini. Estão numerados na ordem
certa de leitura pela IA.

---

## 📁 Arquivos desta pasta

| Arquivo | Conteúdo | Atualiza quando? |
|---------|----------|-----------------|
| `01_GEM_INSTRUCOES.txt` | Instruções mestras de comportamento | Quando as regras do fluxo mudarem |
| `02_codex_legal.json` | Parâmetros zonais, exceções, sanções | Quando a lei municipal mudar |
| `03_leis_referencia.md` | Árvore de precedência legal (Bíblia) | Quando entrar lei nova |
| `04_tabela_valores_multas.md` | Tabela de multas em R$ (2025) | Todo início de ano |
| `05_bairros_zoneamento.md` | Bairros → Zona urbanística | Quando o zoneamento mudar |
| `06_historico_memoria.md` | Casos anteriores (few-shot learning) | **Após cada parecer processado** |
| `07_padroes_recorrentes.md` | Padrões detectados por tipo/zona | **Após cada parecer processado** |

---

## 🔄 Rotina de Atualização (após cada parecer)

1. Salve o JSON do parecer em `_engine/json/`
2. Rode o compilador (`_gerar_templates.py`) → gera o `.docx`
3. Rode o script de aprendizado:
   ```
   python _engine/registrar_aprendizado.py
   ```
4. Sincronize esta pasta:
   ```
   powershell -File "_GEM_Conhecimento\sincronizar.ps1"
   ```
5. No Gemini → Editar GEM → Conhecimento → **substitua os arquivos 06 e 07**

> 💡 Os arquivos 01 a 05 mudam raramente. Só os arquivos **06 e 07**
> precisam ser atualizados no Gemini com frequência.

---

## ⚙️ Configure o GEM assim

**Campo "Instruções do sistema" (cole este texto curto):**
```
Você é o Assistente Sênior de Pareceres Técnicos da SMOSU de Oliveira/MG.
Leia e siga RIGOROSAMENTE o arquivo 01_GEM_INSTRUCOES.txt do seu Conhecimento.
Esse arquivo define seu fluxo de trabalho completo, incluindo os 3 modos de
análise, o cálculo de multas e o checklist de validação do JSON.
```

**Seção "Conhecimento":** suba todos os 7 arquivos desta pasta.

**Prompt inicial de cada sessão:** use o arquivo
`Prompts para GEM/05_Prompt_Chat_de_Inicializacao.txt`
