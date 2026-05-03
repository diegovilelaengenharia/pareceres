# 🏛️ Guia de Pareceres Técnicos — Motor GEM (v5.0)

Este guia orienta o Engenheiro e a IA (Gemini) sobre como produzir pareceres com excelência técnica utilizando o **Sistema GEM da SMOSU Oliveira/MG**.

## 1. O Fluxo de Trabalho Moderno
Com a interface **Painel GEM**, o fluxo de geração mudou de scripts isolados para um ambiente integrado:

1.  **Extração (Gemini/OCR)**: Utilize o Gemini para analisar os processos e extrair o JSON. Se o PDF for escaneado, o motor GEM usará automaticamente o **OCR Docling** para leitura estruturada.
2.  **Auditoria (Dashboard de Saúde)**: Ao colar o JSON no painel, o sistema realiza o "Pré-voo" automático.
    - **Score de Saúde**: Uma nota de 0 a 100 baseada na completude dos dados.
    - **Alertas de Consistência**: O motor avisa se você tentar aprovar um processo com conclusão negativa, ou se faltarem dados de decadência em processos de regularização.
3.  **Compilação Multicamadas**: O sistema agora permite gerar **múltiplas peças** de uma só vez (ex: Parecer + Ofício Ambiental + Sero).

## 2. Padrões de Qualidade (Injetar no Gemini)

Para que o Gemini gere dados compatíveis com a versão 5.0, utilize estas diretrizes:

### A. Raciocínio Explícito (Chain of Thought)
Sempre ordene que a IA justifique cada índice urbanístico antes de gerar o JSON.
> *"Justifique cada infração ou taxa fora da norma com base nas Leis (ex: LC 267/2019 ou Lei 1.544/86). Declare explicitamente 'O índice X atende à norma Y'."*

### B. Linha do Tempo Cronológica
O campo `historico_cronologico` é essencial para a narrativa do parecer.
> *"Monte a linha do tempo completa do processo — do evento mais antigo ao mais recente. Cada fato relevante deve citar sua data e documento de origem no array `historico_cronologico`."*

### C. Campos Técnicos Estruturados
Certifique-se de que a IA preencha os novos campos de especialidade:
- `areas_matriz`: Detalhamento de cada área (existente, a construir, a regularizar).
- `multas_calculadas`: Lista de infrações com enquadramento legal.
- `condicoes_pendentes`: Itens que o requerente deve sanar.

## 3. Modos de Geração
- **Modo Motor (Estruturado)**: Utiliza templates fixos de alta precisão (Alvarás, Habite-se). Exige o campo `tipo_relatorio`.
- **Modo Livre**: Ideal para memorandos ou despachos rápidos. O sistema gera o documento mantendo o timbre institucional, mas sem as tabelas rígidas de cálculo.

## 4. Retroalimentação e Aprendizado
Sempre que notar que a IA inventou uma variável nova (ex: `distancia_do_corrego`), o sistema salvará essa sugestão em `3_Treinar_Inteligencia/03_NOVAS_VARIAVEIS_PROPOSTAS.md`. Revise este arquivo semanalmente para atualizar as instruções do Gemini.

---
**Dúvidas Técnicas?** Consulte o arquivo `_Sistema_Interno/docs/TROUBLESHOOTING.md` para erros de sistema.
