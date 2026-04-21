# Histórico e Memória de Contexto do GEM (SMOSU Oliveira/MG)

> **Instrução para o GEM:** Este arquivo é atualizado automaticamente por `registrar_aprendizado.py`
> após cada parecer processado. Use-o como **few-shot learning**: ao analisar um novo processo,
> identifique casos similares abaixo e replique o padrão de argumentação, ajustando apenas os
> fatos específicos (endereço, área, profissional, datas).

---

## 📊 Estatísticas da Base (atualizado automaticamente)

| Indicador | Valor |
|-----------|-------|
| Total de casos registrados | 2 |
| Tipos mais frequentes | `alvara_regularizacao`, `habitese_multa` |
| Flags mais comuns | `ISENCAO_LOTE_PEQUENO`, `QUESTAO_AMBIENTAL` |

---

## 🏆 Casos de Referência (Aprendizados Fundamentais)

### CASO-1 — Regularização As Built com Isenção de Lote Pequeno
- **Processo:** 6100 | **Tipo:** `alvara_regularizacao`
- **Zona:** ZUR (central) | **Terreno:** 180,00m² | **Construído:** 154,08m²
- **Flags:** `ISENCAO_LOTE_PEQUENO` | `MULTA_ART79` | `DECADENCIA_CTN`
- **Situação:** Terreno de 180m² (< 220m²) com TO de 86,23% e permeabilidade de 5,95% — ambas fora dos parâmetros legais para a zona. Parte da área construída (82,58m²) comprovadamente com mais de 5 anos via aerofotogrametria.
- **Decisão correta:**
  - Multa do Art. 79 (obra sem licença) aplicada sobre a área nova (< 5 anos).
  - Decadência do Art. 150 §4º CTN reconhecida para os 82,58m² antigos.
  - TO e permeabilidade: ISENTAS pela exceção do Art. 15 da LC 267/2019 (lote ≤ 220m²).
- **Lição-chave:** Terreno ≤ 220m² → ignorar infrações de TO e Permeabilidade. Citar explicitamente: *"Art. 15 da Lei Complementar nº 267/2019 — exceção dos parâmetros de ocupação e permeabilidade para lotes iguais ou inferiores a 220m²"*. NÃO cobrar multa do Art. 39.

---

### CASO-2 — APP Urbana como Condicionante Ambiental
- **Processo:** N/D | **Tipo:** `alvara_aprovacao` / `habitese_comum`
- **Flags:** `QUESTAO_AMBIENTAL`
- **Situação:** Imóvel próximo a ribeirão ou zona de proteção ambiental (APP). A planta ou as anotações do fiscal indicavam curso d'água.
- **Decisão correta:**
  - O parecer aprovou o processo tecnicamente, MAS condicionou a emissão ao `oficio_meio_ambiente`.
  - Em `documentos_emitir`, adicionado: *"Ofício à Secretaria de Meio Ambiente — análise e chancela do CODEMA (Condicionante ao Alvará)"*.
- **Lição-chave:** Sempre que houver menção a rio, ribeirão, mata ciliar, APP ou "zona azul" na planta ou anotações do fiscal → emitir `oficio_meio_ambiente` como condicionante paralela obrigatória.

---

## 📋 Casos Registrados em Produção

*(Seção alimentada automaticamente por `registrar_aprendizado.py`)*
