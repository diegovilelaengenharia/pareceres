# DOCUMENTOS DE EXPEDIÇÃO (SETOR ADMINISTRATIVO / SECRETARIA)

Este arquivo documenta as restrições finais para os documentos da Secretaria. 
A diagramação final do seu JSON (quando do tipo `alvara_oficial`, `carta_habitese_oficial` ou `certidao_oficial`) exige **estrita obediência aos Nomes das Chaves JSON**.

NUNCA INVENTE CHAVES. Use estritamente as chaves listadas nos exemplos abaixo para o bloco principal de compilação. O motor de geração (Python) rejeitará o JSON se faltar alguma chave obrigatória exata.

## 1. ALVARÁS Oficiais (alvara_oficial, alvara_renovacao, etc)
Para emissão dos alvarás finais, você DEVE retornar o seu JSON preenchendo as seguintes chaves obrigatórias e literais.

```json
{
  "tipo_relatorio": "alvara_oficial",
  "numero_documento": "XXX/XXXX",
  "numero_processo": "XXX/XXXX",
  "data_aprovacao": "DD de Mês de AAAA",
  "nome_obra": "Nome / Identificação da Obra",
  "logradouro": "Endereço completo da obra",
  "bairro": "Bairro",
  "proprietario_nome": "Nome do Proprietário",
  "proprietario_cpf_cnpj": "000.000.000-00",
  "autor_projeto_nome": "Nome do Eng/Arq (Opcional, deixe vazio se ausente)",
  "autor_projeto_crea": "XX.000/D",
  "autor_projeto_art": "ART XXXXX",
  "responsavel_tecnico_nome": "Nome do Eng/Arq Responsável pela Execução",
  "responsavel_tecnico_crea": "XX.000/D",
  "responsavel_tecnico_art": "ART XXXXX",
  "construtora_nome": "(Opcional)",
  "construtora_cpf_cnpj": "(Opcional)",
  "area_total_obra": "0,00 m²",
  "areas_matriz": [
    {
      "categoria": "Obra Nova / Área Resultante / Área Liberada",
      "destinacao": "Residencial / Comercial",
      "tipo_obra": "Alvenaria",
      "area_m2": "0,00"
    }
  ],
  "observacoes": "Quaisquer anotações finais ou condições (ex: validade)."
}
```

## 2. CARTA DE HABITE-SE Oficial (carta_habitese_oficial)
Da mesma forma, ao analisar um pedido de habite-se, gere os dados baseados nessas chaves fixas:

```json
{
  "tipo_relatorio": "carta_habitese_oficial",
  "numero_documento": "XXX/XXXX",
  "numero_processo": "XXX/XXXX",
  "logradouro": "Endereço",
  "bairro": "Bairro",
  "proprietario_nome": "Nome do Dono",
  "proprietario_cpf_cnpj": "CPF/CNPJ",
  "responsavel_execucao_nome": "Nome e Titulo",
  "responsavel_execucao_cpf_cnpj": "Dados de conselho",
  "texto_despacho_responsavel_tecnico": "Texto narrando a liberação do imóvel segundo vistoria...",
  "area_total_obra": "0,00",
  "areas_matriz": [ 
    {
      "categoria": "Área Total / Parcial",
      "destinacao": "Habite-se",
      "tipo_obra": "Alvenaria",
      "area_m2": "0,00"
    }
  ]
}
```

## 3. CERTIDÕES (certidao_oficial)
Estrutura para as certidões gerais emitidas do balcão:

```json
{
  "tipo_relatorio": "certidao_oficial",
  "titulo_documento": "CERTIDÃO DE ...",
  "texto_certidao": "Texto corrido com toda a informação da certidão respondendo ao parecer ou deferimento...",
  "assinantes": [
    { "nome": "Nome 1", "titulo": "Cargo" }
  ],
  "observacoes_finais": [
    "Nota final de validade",
    "Pode ser um array de strings das notas de rodapé"
  ]
}
```

## 4. CERTIDÕES DE TOPOGRAFIA E SRI (certidao_topografia_oficial)
Estrutura para Desmembramento, Unificação, Retificação e Usucapião:

```json
{
  "tipo_relatorio": "certidao_topografia_oficial",
  "titulo_documento": "CERTIDÃO DE [DESMEMBRAMENTO/UNIFICAÇÃO/RETIFICAÇÃO/USUCAPIÃO]",
  "numero_processo": "XXX/XXXX",
  "proprietario_nome": "Nome completo",
  "matricula_sri": "Matrícula mãe ou objeto",
  "texto_certidao": "Texto técnico contendo a descrição do perímetro, confrontações e o veredito municipal.",
  "clausulas_especificas": [
    "VALIDADE REGISTRAL: 180 dias (Lei 6.766/79) - Aplicável a Desmembramentos.",
    "ANUÊNCIA DE CONFRONTANTE: Município atesta alinhamento predial - Aplicável a Retificações.",
    "NÃO CONSTITUI TÍTULO DE PROPRIEDADE - Obrigatório para Usucapião."
  ],
  "assinantes": [
    { "nome": "Engenheiro Responsável", "titulo": "Cargo/Registro" },
    { "nome": "Secretário Municipal", "titulo": "Secretário de Obras" }
  ]
}
```

### DICA PARA O GEM:
Sempre inclua o campo `solicitacoes_administrativas` no JSON de resposta (Parecer Técnico) com o resumo formatado conforme o **ANEXO: ORIENTAÇÕES AO SETOR ADMINISTRATIVO** do arquivo `padroes_certidoes.md`. Isso permite que o administrativo identifique instantaneamente o que deve ser feito sem ler o parecer técnico inteiro.

---
### IMPORTANTE AO RESPONDER
Não utilize a marcação `"⚠️ VERIFICAR"` se puder evitar cruzando as informações do processo em PDF. Se estiver em dúvida entre o Requerente inicial e o Proprietário real na matrícula, assuma o Proprietário conforme matrícula/certidão e entregue os dados finais e diretos. As chaves devem ter esses nomes EXATOS para o script de compilação em Python do setor ler o seu JSON corretamente na prefeitura.

