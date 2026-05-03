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
- **Flag recorrente:** `ISENCAO_LOTE_PEQUENO` quando terreno ≤ 220m² (isenção de TO/TP para **novos projetos**).
- **Atenção:** TO máx. 70%, Permeabilidade mín. 20%.

### Zona ZUR3
- **Perfil típico:** Misto residencial/comercial, mais edificações irregulares.
- **Flag recorrente:** `MULTA_ART79` + `REGULARIZACAO_AS_BUILT`.
- **Atenção:** CA máx. 1,2. Verificar se há CA excedido.

### Zona ZC / ZCRE
- **Perfil típico:** Comercial, taxa de ocupação elevada, galpões, obras sem recuos.
- **Flag recorrente:** `ABERTURA_DIVISA` (sem recuo lateral).
- **Atenção:** ZCRE admite TO até 80% e Permeabilidade mín. 10%.

### Zona ZUR 3 (Residencial 3 — Adensamento)
- **Bairros típicos:** Acácio Ribeiro, Alvorada, Aparecida, Dom Bosco, Novo Horizonte, São Geraldo, São Bernardo, Pedra Negra, Maria Amélia, Martins, entre outros (ver tabela completa em `bairros_zoneamento_ipm.md`).
- **Parâmetros LC 267/2019:** TO máx. 70% | CA máx. 3,5 | TP mín. 20% | Afastamentos 1,5m.
- **Perfil típico:** Alta densidade construtiva, terrenos pequenos (150–250m²), regularizações frequentes, obras antigas sem licença.
- **Flag recorrente:** `MULTA_ART79` + `MULTA_ART39` + `DECADENCIA_CTN` + `ABERTURA_DIVISA`.
- **Caso de referência:** Processo 6100/2025 — Acácio Ribeiro, terreno 180m², TO 86,23%, TP 5,95%, área total 154,08m².
- **Regra CRÍTICA:** Mesmo sendo lote ≤ 220m², em REGULARIZAÇÃO As-Built as multas do Art. 38/39 DEVEM ser calculadas e cobradas sobre a área que excedeu TO e/ou permeabilidade. Não confundir com aprovação de novo projeto (que sim, seria isenta pelo Art. 15).

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
| `ISENCAO_LOTE_PEQUENO` | Terreno ≤ 220m² + **novo projeto** | Art. 15 LC 267/2019 — isentar TO e permeabilidade apenas em aprovação de projeto novo. **NÃO isenta multa Art. 39 em regularização As-Built.** |
| `MULTA_ART79` | Obra sem licença (área < 5 anos) | Calcular R$ por faixa de metragem irregular (tabela Anexo VI) + incluir em documentos_emitir.obs |
| `MULTA_ART39` | Área violou TO e/ou TP (regularização) | Calcular R$ sobre área somada (TO excedente + TP insuficiente) pela tabela Anexo X de forma acumulativa |
| `MULTA_ART80` | Obra diverge do projeto aprovado | Calcular multa de R$ 102,42 fixo (100% VRM 2026) |
| `DECADENCIA_CTN` | Área com +5 anos comprovados | Exigir Habite-se anterior, escritura ou aerofoto com data — emitir Certidão de Decadência |
| `QUESTAO_AMBIENTAL` | APP, rio ou CODEMA | Emitir `oficio_meio_ambiente` como condicionante paralela obrigatória |
| `ABERTURA_DIVISA` | Janela/porta/basculante < 1,50m da divisa | Exigir Termo de Anuência assinado pelo proprietário lindeiro (CPF + assinatura); citar Art. 43 Lei 1.544/86 c/c Art. 1.301 CC |
| `MODO_CONDICIONADO` | Docs incompletos | Preencher `condicoes_pendentes` no JSON |
| `CAMPOS_PENDENTES` | ⚠️ VERIFICAR presente | Revisão manual ANTES de emitir documento |
| `REGULARIZACAO_AS_BUILT` | Obra concluída sem licença prévia | Verificar decadência (> 5 anos?) + calcular multa Art. 79 + calcular multa Art. 39 se TO ou TP violadas |
| `ESPOLIO` | Proprietário registrado é falecido | Exigir Certidão de Óbito + Termo de Inventariante ou Procuração antes de qualquer análise de mérito; campos: `tipo_requerente: "Espólio"`, `nome_espolio`, `nome_representante_legal` |
| `INFRACAO_RECUO` | Construção no afastamento lateral ou frontal | Calcular multa específica LC 267/2019 (limitações de uso) sobre a área em recuo — discriminar separadamente das demais multas |
| `BAIXA_ALVARA_ANTIGO` | Existe alvará anterior sem Habite-se vinculado ao lote | Incluir instrução no Parecer Final: "Dar Baixa no Alvará nº XX/AAAA — CEI" para evitar duplicidade no sistema |
| `DECOMPOSICAO_MULTAS` | Processo tem mais de um tipo de infração simultânea | Não agregar em valor único — discriminar cada infração com sua lei, metragem e valor no Comunicado de Pendência |
| `PERMEABILIDADE_ZERO` | TP = 0% — lote totalmente impermeabilizado | Multa LC 267/2019 domina (~60% do custo total). Citar no parecer que a impermeabilização transfere ônus de drenagem ao sistema público, justificando a severidade |
| `DIVERGENCIA_CADASTRAL_BAIRRO` | Bairro na matrícula (SRI/cartório) difere do bairro no cadastro municipal | Emitir **Certidão de Localização** para garantir segurança jurídica da averbação. Não tentar corrigir matrícula — isso é competência do cartório |
| `CNO_CEI_TRANSFERENCIA` | Alvará antigo substituído por novo — CNO/CEI em nome do proprietário na Receita Federal | Emitir comunicado transferindo ao proprietário a responsabilidade pela baixa do CNO/CEI junto à RFB (Receita Federal do Brasil). Não fazer a baixa internamente |
