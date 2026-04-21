# Padrões Recorrentes — Base de Conhecimento Evolutiva

> **Instrução para o GEM:** Este arquivo é gerado e atualizado automaticamente
> a cada parecer processado. Consulte-o para antecipar problemas recorrentes
> antes de iniciar a análise, identificando combinações de zona + tipo de processo
> que historicamente apresentam flags específicas.

---

## 📌 Como Interpretar

Cada seção agrupa casos reais por `tipo_relatorio`. Os flags no final de cada
linha revelam padrões operacionais. Exemplos de uso inteligente:
- Se você vê que todo `alvara_regularizacao` em ZUR3 tem `MULTA_ART79`, verifique já!
- Se `habitese_comum` frequentemente tem `CAMPOS_PENDENTES`, aumente a atenção na Fase Zero.

---

## 🏙️ Padrões por Zona Urbanística

### Zona ZUR1 / ZUR2
- **Perfil típico:** Residencial, terrenos médios (200–400m²), aprovação de projeto novo.
- **Flag recorrente:** `ISENCAO_LOTE_PEQUENO` quando terreno ≤ 220m².
- **Atenção:** TO máx. 70%, Permeabilidade mín. 20%.

### Zona ZUR3
- **Perfil típico:** Misto residencial/comercial, mais edificações irregulares.
- **Flag recorrente:** `MULTA_ART79` + `REGULARIZACAO_AS_BUILT`.
- **Atenção:** CA máx. 1,2. Verificar se há CA excedido.

### Zona ZC / ZCRE
- **Perfil típico:** Comercial, taxa de ocupação elevada, galpões, obras sem recuos.
- **Flag recorrente:** `ABERTURA_DIVISA` (sem recuo lateral).
- **Atenção:** ZCRE admite TO até 80% e Permeabilidade mín. 10%.

---

## 🗂️ Casos por Tipo de Relatório

*(Alimentado automaticamente via `registrar_aprendizado.py` — não edite esta seção manualmente)*

### `alvara_regularizacao`

### `alvara_aprovacao`

### `alvara_ampliacao`

### `alvara_reforma_demolicao_ampliacao`

### `alvara_galpao_comercial`

### `habitese_comum`

### `habitese_multa`

### `comunicado_pendencia`

### `certidao_averbacao_decadencia`

---

## 🚩 Mapa de Alertas por Flag

| Flag | O que indica | Ação obrigatória |
|-----|------|-------|
| `ISENCAO_LOTE_PEQUENO` | Terreno ≤ 220m² | Aplicar Art. 15 LC 267/2019 — isentar TO e permeabilidade |
| `MULTA_ART79` | Obra sem licença | Calcular R$ (memorial) + incluir em documentos_emitir.obs |
| `MULTA_ART80` | Obra diverge do projeto | Calcular multa de R$ 90,60 fixo |
| `DECADENCIA_CTN` | Obra com +5 anos | Exigir comprovação documental ou aerofoto de satélite |
| `QUESTAO_AMBIENTAL` | APP, rio ou CODEMA | Emitir `oficio_meio_ambiente` como condicionante |
| `ABERTURA_DIVISA` | Janela/porta < 1,50m | Exigir Termo de Anuência do lindeiro |
| `MODO_CONDICIONADO` | Docs incompletos | Preencher `condicoes_pendentes` no JSON |
| `CAMPOS_PENDENTES` | ⚠️ VERIFICAR presente | Revisão manual ANTES de emitir documento |
| `REGULARIZACAO_AS_BUILT` | Obra já concluída s/ licença | Verificar decadência + multa Art. 79 |
