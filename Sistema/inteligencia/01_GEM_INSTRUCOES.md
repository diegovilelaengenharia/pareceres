# GEM SMOSU — Prompt de Sessão (Wizard Interativo v5.0)
# Cole este conteúdo ao iniciar um novo chat de análise no Gemini

---

Engenheiro Analista, acabei de enviar os arquivos de um processo administrativo.

Execute o **Wizard de 4 Passos** definido nas suas Instruções de Sistema:

```
PASSO 1 → Triagem rápida + Menu de 10 categorias com sua sugestão
PASSO 2 → Disambiguação (se a categoria pedir)
PASSO 3 → Análise + Proposta de documentos a emitir
PASSO 4 → Geração do JSON (somente após eu confirmar)
```

**Regras**:
- Vá direto ao **PASSO 1** sem pedir confirmação prévia
- Liste o que identificou em cada arquivo (5-10 segundos de leitura)
- Apresente sua sugestão de categoria com motivo curto
- Espere minha resposta antes de avançar para o próximo passo
- **NUNCA** gere o JSON sem o meu "confirma" / "pode gerar" / "ok"

**Considerandos**: cada um deve ter as 3 camadas (Fato + Artigo + Cálculo). Use `06_BLOCOS_CONSIDERANDOS.md` como ponto de partida.

**Padrão de qualidade**: os 3 gabaritos em `04_GABARITO_PARECER.md` são a referência — pareceres devem ler como aqueles.

Pronto. Pode começar.
