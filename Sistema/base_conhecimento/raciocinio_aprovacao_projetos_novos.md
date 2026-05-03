# RACIOCÍNIO: ANÁLISE DE PROJETOS NOVOS — ALVARÁ DE CONSTRUÇÃO
## Modelo Aprendido do Processo 2765/2026 — Welington Rita

> **Finalidade deste arquivo:** Mapear o raciocínio humano por trás da análise de um processo de **aprovação de projeto novo** (obra ainda não iniciada), para que o sistema GEM replique esse raciocínio de forma autônoma em casos futuros.

---

## 1. O QUE É UM PROCESSO DE APROVAÇÃO DE PROJETO NOVO?

Diferente da **regularização (As-Built)**, onde a obra já está executada e se busca legalizar o passado, na **aprovação de projeto novo** o requerente busca licença **antes** de iniciar a construção. Isso muda radicalmente a análise:

| Aspecto | Regularização | Projeto Novo |
|---|---|---|
| Estado da obra | Já construída (total ou parcialmente) | Não iniciada |
| Multa Art. 79 (Lei 1.544/86) | **Obrigatória** (construiu sem licença) | **Não se aplica** |
| Multas LC 267/2019 | Aplicável se parâmetros violados | Aplicável se projeto em desacordo |
| Decadência (CTN) | Verificar sempre | Não se aplica |
| Foco da análise | Adequar o existente à lei | Verificar se o projeto cumpre a lei |

**REGRA DE OURO:** Em projeto novo com obra não iniciada → **NUNCA lançar multa do Art. 79**. A multa só existe após construção irregular.

---

## 2. FLUXO DE TRAMITAÇÃO DO PROCESSO (APRENDIDO DO PROCESSO 2765/2026)

```
PROTOCOLO (Abertura do processo)
    ↓
FISCALIZAÇÃO (OBRAS) — Vistoria In Loco
    → Confirma: obra iniciada ou não?
    → Levanta o número predial
    → Verifica denominação da rua
    → Emite Parecer Fiscal
    ↓
TRIAGEM (OBRAS) — Conferência Documental
    → Verifica se toda a documentação exigida pelo Decreto 4.149/2019 está presente
    → Se INDEFERIDA: envia para "Entrega de Documentos" com lista de pendências
    → Se DEFERIDA: encaminha diretamente para ANÁLISE
    ↓
ENTREGA DE DOCUMENTOS (OBRAS)
    → Requerente/outorgado junta documentos faltantes
    → Encaminhado para ANÁLISE
    ↓
ANÁLISE (OBRAS) — Setor Técnico
    → Engenheiro Civil analisa projeto e emite Parecer Técnico
    → Se houver pendência no projeto → emite COMUNICADO e envia para CONFECÇÃO DE DOCUMENTOS
    ↓
CONFECÇÃO DE DOCUMENTOS (OBRAS)
    → Prepara Alvará, Certidões, etc.
    → Se houver comunicado pendente → envia para ENTREGA DE DOCUMENTOS
    ↓
ENTREGA DE DOCUMENTOS (OBRAS) [2ª vez]
    → Requerente retira comunicado ou entrega documentos corrigidos
    → Encaminhado novamente para CONFECÇÃO após atendimento
    ↓
ARQUIVAMENTO
```

**LIÇÃO DO PROCESSO 2765/2026:** A triagem indeferiu o processo por falta da Matrícula de Inteiro Teor atualizada (exigiu Matrícula SRI 38.551 atualizada em até 30 dias). Após juntada, o processo foi liberado para análise. Durante a análise, foi detectado que o logradouro no projeto estava incorreto ("Rua Onze" ao invés de "Rua Dona Didi Moreira"), resultando em comunicado de pendência antes da emissão do alvará.

---

## 3. CHECKLIST DE DOCUMENTOS — ALVARÁ DE CONSTRUÇÃO (Decreto 4.149/2019, Art. 4º)

O GEM deve verificar se os seguintes documentos estão presentes no processo:

- [x] Documento pessoal do requerente com foto (CNH, RG)
- [x] Procuração (se houver outorgado — verificar se o outorgado assinou)
- [x] Documento do outorgado (se houver procuração)
- [x] Comprovante de endereço do requerente (atualizado)
- [x] Certidão de Inscrição Imobiliária (Espelho Cadastral)
- [x] Certidão de propriedade atualizada (Matrícula de Inteiro Teor — máx. 30 dias) **OU** Contrato de Compra e Venda
- [x] Projeto Arquitetônico em PDF (assinado pelo proprietário e pelo responsável técnico)
- [x] Projeto Arquitetônico em DWG (arquivo digital)
- [x] ART/RRT/TRT — Projeto Arquitetônico
- [x] ART/RRT/TRT — Execução de Obra
- [x] Certidão Negativa de Débitos Municipais (válida)
- [x] Comprovante de pagamento da Taxa de Alvará (DAM pago)

**ATENÇÃO ESPECIAL — Obras acima de 100m²:** Exigir RT específica de Projeto Estrutural e, se acima de 250m², Projeto Elétrico e Hidrossanitário separados.

**CASO 2765/2026:** O requerente entrou com Contrato de Compra e Venda (não é proprietário formal — a matrícula está em nome da loteadora Barros e Almeida). A triagem exigiu a Matrícula SRI de Inteiro Teor atualizada. Isso é padrão: **quando o requerente não é o proprietário constante na matrícula, exigir a matrícula atualizada + contrato de compra e venda para vincular a cadeia de propriedade**.

---

## 4. ANÁLISE DOS PARÂMETROS URBANÍSTICOS — PASSO A PASSO

### Passo 1 — Identificar o imóvel e sua zona
Fonte: Espelho Cadastral + Projeto Arquitetônico

```
Dados extraídos do processo 2765/2026:
- Inscrição Municipal: 01.05.219.0265
- Logradouro: Rua Dona Didi Moreira (antiga Rua 11)
- Bairro: Residencial César Almeida
- Quadra: 02 | Lote: 18
- Zoneamento (Espelho): AMARELO → ZUR-2 (conforme tabela bairros/zoneamento)
- Categoria de uso: Residencial UR1
```

> **NOTA PARA O GEM:** O Espelho Cadastral mostra o código de zoneamento (ex: "AMARELO" = ZUR-2). Consulte a tabela `bairros_zoneamento_ipm.md` para confirmar a zona.

### Passo 2 — Extrair medidas do terreno
```
Área do terreno: 200,01m²
Testada principal: 14,23m
Profundidade: 14,06m
```

### Passo 3 — Verificar exceção de lote ≤ 220m²
```
200,01m² ≤ 220m²  →  SIM → Aplicar Art. 9º §13 da LC 267/2019
Efeito: Afastamentos pelo Código Civil (Arts. 1.299-1.301), não pela LC 267/2019
ATENÇÃO: A exceção NÃO dispensa a Taxa de Permeabilidade mínima de 20%
```

### Passo 4 — Extrair parâmetros do projeto apresentado
```
Dados extraídos do processo 2765/2026:
- Área construída: 126,80m²
- Taxa de Ocupação (TO): 126,80 ÷ 200,01 = 63,40%
- Coeficiente de Aproveitamento (CA): 126,80 ÷ 200,01 = 0,63
- Taxa de Permeabilidade (TP): declarada 24,00% → 200,01 × 24% = 48,00m² livres
```

### Passo 5 — Comparar com os limites da zona ZUR-2
```
Parâmetro       | Projeto  | Limite ZUR-2 | Situação
----------------|----------|--------------|----------
TO              | 63,40%   | máx. 70%     | ✅ APROVADO
CA              | 0,63     | máx. 2,5     | ✅ APROVADO
TP              | 24,00%   | mín. 20%     | ✅ APROVADO
TP em m²        | 48,00m²  | mín. 40,00m² | ✅ APROVADO
Afastamentos    | Cod.Civil | Isenção §13  | ✅ APROVADO
```

**RESULTADO: PROJETO APROVADO — não há infrações urbanísticas.**

### Passo 6 — Verificar denominação do logradouro no projeto
O projeto inicialmente constava com o nome "Rua Onze" (denominação antiga). Conforme **Decreto nº 4.145/2019**, a rua foi renomeada para **"Rua Dona Didi Moreira"**. A análise técnica emitiu **comunicado de pendência** exigindo a troca do projeto para o logradouro correto.

> **LIÇÃO PARA O GEM:** Sempre verificar se o logradouro no projeto corresponde ao nome oficial vigente (Decreto de denominação de ruas). Se o projeto estiver com nome de rua desatualizado, emitir comunicado antes do alvará.

---

## 5. RESPONSABILIDADE TÉCNICA — O QUE VERIFICAR

O processo de aprovação de projeto para obras residenciais unifamiliares exige:

| RT | Tipo | Atividade | Conselho |
|---|---|---|---|
| RRT Projeto | Registro | Projeto Arquitetônico + Estrutural + Elétrico + Hidrossanitário | CAU (Arquiteto) ou CREA (Eng. Civil) |
| RRT Execução | Registro | Execução de Obra + Instalações | CAU ou CREA |

**Do processo 2765/2026:**
- Responsável: Arq. Vera Lúcia Gurgel Costa Oliva de Vasconcelos (CAU A58084)
- RRT Projeto nº SI16583426I00CT001 — Projeto Arq., Estrutural, Elétrico, Hidrossanitário
- RRT Execução nº SI16583592I00CT001 — Execução de Obra, Elétrico, Hidrossanitário
- Outorgado/Intermediário: Sidney Cesar Caminha (CFT — Técnico em Edificações), CPF 041.336.156-28
- **ATENÇÃO:** O técnico (Sidney) atuou como representante junto à prefeitura (procurador), não como responsável técnico. O RT é a Arquiteta Vera Lúcia.

---

## 6. O QUE CONSTA NO PARECER TÉCNICO FINAL

### Estrutura do Parecer Técnico (modelo validado):

1. **Cabeçalho** — Prefeitura, Secretaria, endereço, contato
2. **Identificação** — Processo, assunto, requerente
3. **§ Abertura** — Quem solicita, o quê, onde (área, lote/quadra, logradouro, bairro, zona, inscrição municipal)
4. **§ Propriedade** — Como é demonstrada (matrícula, contrato), vistoria fiscal (inicio/não início da obra, número predial)
5. **§ Responsabilidade Técnica** — Nome do profissional, conselho, nº dos RRTs e atividades cobertas
6. **§ Legislação** — "a análise ateve-se à Lei nº 1.544/86 e à LC nº 267/2019"
7. **Considerandos** — Bullet points com: zona, exceção 220m², TP, parâmetros verificados, validade do alvará, número predial, nome de rua, pendência corrigida
8. **Conclusão** — Parecer FAVORÁVEL ou DESFAVORÁVEL + lista de documentos a emitir
9. **Assinatura** — Engenheiro Civil, CREA, Secretaria Municipal de Obras

### Documentos emitidos neste tipo de processo:
- Alvará de Construção (com observações de validade e permeabilidade)
- Certidão de Número — SAAE
- Certidão de Número — CEMIG
- Certidão de Nome de Rua

---

## 7. COMUNICADO DE PENDÊNCIA — QUANDO USAR

No processo 2765/2026, foi necessário emitir um comunicado antes da emissão do alvará porque o **logradouro no projeto estava incorreto**. O comunicado deve ser emitido quando:

1. O projeto apresenta o logradouro com nome desatualizado (Decreto de renomeação de rua)
2. O projeto está em desacordo com algum parâmetro urbanístico sanável (ex: precisa refazer o projeto com menor TO)
3. Falta algum documento complementar que só pode ser juntado após a análise técnica
4. Há necessidade de Termo de Anuência de confrontante (Art. 43 da Lei 1.544/86 — janela a menos de 1,50m da divisa)

**Formato do comunicado:**
- "A solicitação só poderá ser aprovada após sanadas as pendências descritas abaixo:"
- Lista de itens em tópicos
- Nota: "Os documentos extraídos para correção deverão ser devolvidos."
- Assinado pelo Engenheiro Civil e pelo servidor responsável

---

## 8. PECULIARIDADES DO BAIRRO RESIDENCIAL CÉSAR ALMEIDA

- **Zoneamento:** ZUR-2 (código "AMARELO" no sistema IPM)
- **Loteadora original:** Barros e Almeida Empreendimentos Imobiliários Ltda (CNPJ 01.550.999/0001-05)
- **Padrão de lotes:** ~200m² (lotes menores que 220m² → exceção de afastamentos)
- **Logradouro renomeado:** Rua Onze → Rua Dona Didi Moreira (Decreto 4.145/2019)
- **Numeração predial levantada pela fiscalização:** número 43 para o lote 18 da quadra 02

---

## 9. JSON MODELO PARA O GEM — ALVARÁ DE CONSTRUÇÃO (PROJETO NOVO APROVADO)

```json
{
  "tipo_relatorio": "alvara_aprovacao",
  "numero_processo": "2765/2026",
  "data_processo": "03 de março de 2026",
  "assunto": "Alvará de Construção, Aprovação de Projeto, Certidão de Número e Nome de Rua",
  "requerente": "WELINGTON RITA",
  "logradouro": "Rua Dona Didi Moreira, nº 43",
  "bairro": "Residencial César Almeida",
  "inscricao_municipal": "01.05.219.0265",
  "area_terreno": "200,01m²",
  "area_total_construida": "126,80m²",
  "taxa_ocupacao": "63,40%",
  "coef_aproveitamento": "0,63",
  "taxa_permeabilidade": "24,00%",
  "profissional_nome": "Vera Lúcia Gurgel Costa Oliva de Vasconcelos",
  "zona": "ZUR-2",
  "lote_menor_220m2": true,
  "obra_iniciada": false,
  "paragrafo_abertura": "...",
  "considerandos": [
    "o imóvel está inserido na ZUR-2 (Art. 15 da LC 267/2019), com TO máx. de 70%, CA de 2,5 e TP mín. de 20%;",
    "o terreno possui área de **200,01m²**, igual ou inferior a 220,00m², aplicando-se a isenção prevista no §13 do Art. 9º da LC 267/2019 para afastamentos;",
    "a taxa de permeabilidade de **24,00%** (48,00m²) supera o mínimo exigido de **40,00m²** (20% de 200,01m²), conforme Art. 9º §14 da LC 267/2019;",
    "os parâmetros urbanísticos atendem integralmente a ZUR-2: TO 63,40% (máx. 70%), CA 0,63 (máx. 2,5), TP 24,00% (mín. 20%);",
    "o projeto foi corrigido constando o logradouro correto **Rua Dona Didi Moreira**, conforme Decreto nº 4.145/2019"
  ],
  "conclusao": "Verificado e aprovado o projeto, em conformidade com a Lei nº 1.544/86 e a LC nº 267/2019, emite-se PARECER FAVORÁVEL.",
  "documentos_emitir": [
    {
      "tipo": "Alvará de Construção de Residência Unifamiliar — 126,80m²",
      "obs": "Válido por 01 (um) ano. Manter taxa de permeabilidade mínima de 20% do terreno (40,00m²). Respeitar o projeto aprovado."
    },
    {
      "tipo": "Certidão de Número — SAAE",
      "obs": "Número 43 — Rua Dona Didi Moreira, Bairro Residencial César Almeida."
    },
    {
      "tipo": "Certidão de Número — CEMIG",
      "obs": "Número 43 — Rua Dona Didi Moreira, Bairro Residencial César Almeida."
    },
    {
      "tipo": "Certidão de Nome de Rua",
      "obs": "Conforme Decreto nº 4.145/2019, a antiga Rua 11 passou a ser denominada Rua Dona Didi Moreira."
    }
  ],
  "extras_extraidos": {
    "fiscais": "Marlei Henrique de Oliveira (Mat. 3087661-8) e Silvânia F. Santos Pedrosa (Mat. 3083160-1)",
    "guias_pagas": "Taxa de Alvará paga em 04/03/2026 (comprovante juntado ao processo)",
    "observacoes_manuscritas": "Pendência de triagem: Matrícula SRI atualizada (Mat. 38.551). Comunicado emitido em 16/03/2026: troca do logradouro no projeto."
  }
}
```

---

## 10. DIFERENÇAS CRÍTICAS: PROJETO NOVO vs. REGULARIZAÇÃO

| Critério | Projeto Novo | Regularização (As-Built) |
|---|---|---|
| **Vistoria fiscal** | Confirma que obra não iniciada | Mede área construída, verifica parâmetros do que existe |
| **Multa Art. 79** | Não se aplica | Obrigatória (salvo decadência) |
| **Multa LC 267** | Só se projeto violar parâmetros | Obrigatória se área construída violar parâmetros |
| **Decadência CTN** | Não se aplica | Verificar sempre (obra com + de 5 anos) |
| **Documentação** | Contrato de C&V ou Matrícula | Matrícula atualizada obrigatória |
| **RTs** | RRT/ART de Projeto + Execução | RRT/ART de As-Built (execução) |
| **Nome na matrícula** | Pode ser a loteadora (comprador com contrato) | Deve estar em nome do requerente ou com procuração clara |
| **Resultado possível** | Aprovado ou com pendências | Aprovado com multas, com comunicado, ou indeferido |

---

*Gerado em 26/04/2026 — Baseado no Processo 2765/2026 (Welington Rita — Residencial César Almeida)*
*Arquivo de retroalimentação do sistema GEM — Prefeitura Municipal de Oliveira/MG*
