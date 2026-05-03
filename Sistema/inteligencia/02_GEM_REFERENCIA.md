# TEMPLATES JSON — DOCUMENTOS DO MOTOR GEM

Este arquivo define as chaves obrigatórias para cada tipo de documento.
NUNCA INVENTE CHAVES. O motor Python rejeitará o JSON se uma chave obrigatória estiver ausente ou com nome errado.

---

# PARTE A — PARECERES E COMUNICADOS (gerados pelo GEM após análise do PDF)

## A1. Parecer Técnico Completo
Usado para: `alvara_aprovacao`, `alvara_regularizacao`, `alvara_ampliacao`, `alvara_reforma_demolicao_ampliacao`, `habitese_multa`, `habitese_inclusao_area`, etc.

```json
{
  "tipo_relatorio": "alvara_aprovacao",
  "numero_processo": "XXX/XXXX",
  "data_processo": "DD de Mês de AAAA",
  "assunto": "Descrição resumida do pedido",
  "requerente": "NOME COMPLETO EM MAIÚSCULAS",
  "logradouro": "Rua/Av., nº XXX",
  "bairro": "Bairro",
  "inscricao_municipal": "XX.XX.XXX.XXXX.XXX",
  "area_terreno": "0,00m²",
  "area_total_construida": "0,00m²",
  "taxa_ocupacao": "0,00%",
  "coef_aproveitamento": "0,00",
  "taxa_permeabilidade": "0,00%",
  "pavimentos": "0",
  "vagas_garagem": "0",
  "modo_recebimento_projeto": "Físico ou Digital",
  "tipo_multa_especifica": "Ex: Lei 1544 - Obra s/ Licença",
  "profissional_nome": "NOME DO ENG/ARQ RESPONSÁVEL",
  "assinante_parecer": "Engenheiro Diego T. N. Vilela",
  "paragrafo_abertura": "Texto de abertura narrativo do processo...",
  "considerandos": [
    "primeiro considerando com citação legal __Art. X da Lei Y__;",
    "segundo considerando com dado numérico em **negrito**;"
  ],
  "fundamentacao_legal": [
    "__Art. X da Lei Y__: Explicação da aplicação ao caso concreto.",
    "__Art. Z do Decreto W__: Explicação da aplicação ao caso concreto."
  ],
  "conclusao": "Texto de conclusão com parecer **FAVORÁVEL** ou **DESFAVORÁVEL**...",
  "documentos_emitir": [
    {
      "tipo": "Nome do documento a emitir (ex: Alvará de Aprovação — 150,00m²)",
      "obs": "Condições, validade e observações do documento."
    }
  ],
  "extras_extraidos": {
    "fiscais": "Nome e matrícula dos fiscais",
    "guias_pagas": "Valor e descrição das guias/DAMs pagos",
    "observacoes_manuscritas": "Qualquer anotação manuscrita relevante"
  }
}
```

## A2. Comunicado de Pendência
Usado para: `comunicado_pendencia`
Emitido quando o processo está **incompleto** (Fase Zero) ou quando há **multas a recolher** antes da análise prosseguir.

```json
{
  "tipo_relatorio": "comunicado_pendencia",
  "numero_processo": "XXX/XXXX",
  "data_processo": "DD de Mês de AAAA",
  "assunto": "COMUNICADO DE PENDÊNCIA — [TIPO DO PROCESSO]",
  "requerente": "NOME COMPLETO EM MAIÚSCULAS",
  "paragrafo_abertura": "A Secretaria Municipal de Obras e Serviços Urbanos (SMOSU) informa que o processo nº XXX/XXXX encontra-se com as seguintes pendências que impedem o prosseguimento da análise técnica:",
  "considerandos": [
    "**Item de Pendência 1:** Descrição clara e acessível ao cidadão, sem jargão excessivo.",
    "**Item de Pendência 2:** Use **negrito** (duplo asterisco) para destacar o título de cada item."
  ],
  "conclusao": "O processo permanecerá suspenso até a regularização das pendências listadas. Após o atendimento de todas as exigências, a análise será retomada."
}
```

> **REGRAS DO COMUNICADO:**
> - Use `**negrito**` (duplo asterisco `**`), NUNCA `__sublinhado__` nos itens de pendência — o engine só processa `**`.
> - Agrupe multas de mesma natureza (ex: TO + TP da LC 267) em **um único item** chamado "Multas Urbanísticas Acumulativas".
> - Linguagem acessível: "área livre no terreno" ao invés de "taxa de permeabilidade".

---

# PARTE B — DOCUMENTOS DE EXPEDIÇÃO (SETOR ADMINISTRATIVO / SECRETARIA)

A diagramação final do seu JSON (quando do tipo `alvara_oficial`, `carta_habitese_oficial` ou `certidao_oficial`) exige **estrita obediência aos Nomes das Chaves JSON**.

NUNCA INVENTE CHAVES. Use estritamente as chaves listadas nos exemplos abaixo para o bloco principal de compilação. O motor de geração (Python) rejeitará o JSON se faltar alguma chave obrigatória exata.

## B1. ALVARÁS Oficiais (alvara_oficial, alvara_renovacao, etc)
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

## B2. CARTA DE HABITE-SE Oficial (carta_habitese_oficial)
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

## B3. CERTIDÕES (certidao_oficial)
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

---

## NOMES CANÔNICOS DAS VARIÁVEIS — TABELA DE ALIASES

O motor Python aceita sinônimos para as variáveis abaixo, mas **sempre prefira o nome canônico** para garantir máxima compatibilidade:

| Nome Canônico (USE ESTE) | Sinônimos aceitos (evitar) |
| --- | --- |
| `responsavel_tecnico` | tecnico_responsavel, rt, eng_responsavel, profissional_responsavel |
| `profissional_nome` | nome_profissional, nome_do_profissional, profissional |
| `art_rrt` | art_rrt_numero, numero_art, art, rrt, numero_rrt |
| `requerente` | proprietario, proprietario_nome, interessado, solicitante |
| `logradouro` | endereco, rua, avenida, endereco_obra |
| `bairro` | bairro_obra, distrito |
| `inscricao_municipal` | inscricao, im, cadastro_imobiliario, inscricao_imobiliaria |
| `area_terreno` | area_lote, area_total_terreno, area_do_terreno |
| `taxa_ocupacao` | ocupacao, taxa_de_ocupacao, to |
| `taxa_permeabilidade` | permeabilidade, taxa_de_permeabilidade, tp |
| `coef_aproveitamento` | ca, coeficiente_aproveitamento |
| `agentes_fiscais` | fiscal, fiscais, agente_fiscal, vistoriadores |
| `assinante_parecer` | assinante, responsavel_parecer, autor_parecer |
| `multas_aplicaveis` | multas, multa_aplicavel, autos_infracao, multas_cabiveis |
| `condicionantes_aprovacao` | condicionantes, condicoes_aprovacao, requisitos_aprovacao |
| `numero_processo` | processo, protocolo, numero_protocolo |
| `pavimentos` | numero_pavimentos, andares, numero_andares |
| `vagas_garagem` | vagas, garagem, numero_vagas, qtd_vagas |

> **Regra:** se o campo canônico estiver ausente no JSON mas um sinônimo estiver presente, o sistema promove o valor automaticamente. Mesmo assim, NUNCA invente campos fora desta lista.

---

### IMPORTANTE AO RESPONDER
Não utilize a marcação `"⚠️ VERIFICAR"` se puder evitar cruzando as informações do processo em PDF. Se estiver em dúvida entre o Requerente inicial e o Proprietário real na matrícula, assuma o Proprietário conforme matrícula/certidão e entregue os dados finais e diretos. As chaves devem ter esses nomes EXATOS para o script de compilação em Python do setor ler o seu JSON corretamente na prefeitura.


---

﻿{
  "_meta": {
    "versao": "1.0",
    "municipio": "Oliveira/MG",
    "fonte": "Bot_Tudão.pdf — extração direta das leis municipais",
    "leis_incluidas": [
      "Decreto nº 4.149/2019 — Procedimentos de aprovação de projetos",
      "Lei nº 1.544/86 — Código de Obras do Município",
      "Lei Complementar nº 267/2019 — Uso e Ocupação do Solo",
      "Lei nº 5.172/1966 — CTN (Art. 150 §4º, decadência)",
      "Lei nº 1.788/1989 — Código de Posturas do Município",
      "Lei Complementar nº 216/2014 — Parcelamento do Solo (Redação LC 313/2024)",
      "Lei Federal nº 6.766/1979 — Parcelamento do Solo Urbano"
    ],
    "instrucao_gem": "CONSULTE ESTE ARQUIVO MECANICAMENTE antes de redigir qualquer considerando ou fundamentação. Use os campos 'citacao_considerando' e 'citacao_fundamentacao' como texto base, substituindo os {placeholders} pelos valores reais do processo. NUNCA invente artigos ou valores fora deste codex."
  },
  "excecoes": {
    "lote_igual_ou_menor_220m2": {
      "lei": "Art. 9º, §13 da Lei Complementar nº 267/2019 c/c Arts. 1.299 a 1.301 do Código Civil Brasileiro",
      "condicao": "area_terreno_m2 <= 220",
      "efeito": "Lote pode adotar afastamentos do Código Civil (Arts. 1.299-1.301) em substituição aos definidos pela LC 267/2019 e pela Lei nº 1.544/86. Não se aplica os afastamentos frontais, laterais e de fundo da zona.",
      "bloqueia_multas": [
        "multa_parametros_lc267"
      ],
      "nao_bloqueia": [
        "multa_sem_licenca_art79"
      ],
      "citacao_considerando": "o terreno possui área de **{area_terreno}m²**, igual ou inferior a 220,00m² (duzentos e vinte metros quadrados), aplicando-se a __isenção prevista no §13 do Art. 9º da Lei Complementar nº 267/2019__, de modo que os afastamentos frontais, laterais e de fundo adotados atendem ao disposto pelos Arts. 1.299 a 1.301 do Código Civil Brasileiro, não se aplicando ao caso os afastamentos previstos pela Lei nº 1.544/86;",
      "nota_tp": "A taxa de permeabilidade mínima de 20% (Art. 9º §14 da LC 267/2019) se aplica a TODOS os lotes, inclusive os menores que 220m². A exceção do §13 cobre apenas afastamentos, não permeabilidade."
    },
    "decadencia_administrativa_5anos": {
      "lei": "Art. 150, §4º da Lei nº 5.172/1966 (Código Tributário Nacional — CTN)",
      "condicao": "anos_desde_conclusao_obra >= 5",
      "efeito": "Isenção da multa por construção sem licença sobre a área decadente. Emitir Certidão de Decadência. A homologação tácita ocorre após 5 anos da conclusão da obra.",
      "bloqueia_multas": [
        "multa_sem_licenca_art79"
      ],
      "documento_emitir": "certidao_averbacao_decadencia",
      "citacao_considerando": "a edificação apresenta evidências robustas de conclusão há mais de 5 (cinco) anos ininterruptos, constatadas por {evidencias} (ex: imagens de satélite, declarações, comprovantes), configurando a __decadência administrativa nos termos do Art. 150, §4º do CTN__, razão pela qual fica afastada a cobrança de multa sobre a área decadente de **{area_decadente}m²**, que será objeto de Certidão de Decadência;",
      "citacao_fundamentacao": "__Art. 150, §4º do Código Tributário Nacional (Lei nº 5.172/1966):__ Se a lei não fixar prazo à homologação, será ele de 5 (cinco) anos, a contar da ocorrência do fato gerador. Transcorrido esse prazo sem que a Fazenda Pública se tenha pronunciado, considera-se homologado o lançamento e definitivamente extinto o crédito. Aplica-se ao caso por analogia administrativa, afastando a incidência de penalidades pecuniárias sobre área edificada há mais de 5 anos."
    }
  },
  "parametros_zonais": {
    "_fonte": "LC 267/2019, Art. 15 e seguintes — valores extraídos das tabelas de parâmetros por zona",
    "_nota_global": "Art. 9º §14 LC 267/2019: taxa de permeabilidade mínima de 20% se aplica a TODOS os lotes de qualquer zona. Art. 9º §15: afastamento frontal e de fundo mínimo de 1,50m aplica-se a todas as zonas.",
    "ZUR1": {
      "descricao": "Zona de Uso Predominantemente Residencial 1 — baixa densidade, bacia do manancial e APPs",
      "to_max_pct": 60,
      "ca_geral": 1.5,
      "ca_institucional": 1.8,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20,
      "alerta_to": "TO acima de 60% → infração aos parâmetros da ZUR1",
      "alerta_tp": "TP abaixo de 20% → infração (salvo §7º a §11 do Art. 9º com caixa de captação)"
    },
    "ZUR2": {
      "descricao": "Zona de Uso Preferencialmente Residencial 2 — declividade acentuada e proteção de aeródromo",
      "to_max_pct": 70,
      "ca_geral": 2.5,
      "ca_institucional": 2.8,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20
    },
    "ZUR3": {
      "descricao": "Zona de Uso Preferencialmente Residencial 3 — bairros com possibilidade de adensamento",
      "to_max_pct": 70,
      "ca_geral": 3.5,
      "ca_institucional": 3.5,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20
    },
    "ZUR_Social": {
      "descricao": "Zona Urbana de Interesse Social — habitações de interesse social, baixa densidade",
      "to_max_pct": 70,
      "ca_geral": 1.2,
      "ca_institucional": 1.5,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20
    },
    "ZC1": {
      "descricao": "Zona Central de Comércio e Serviços 1 — média densidade, comércio e serviços",
      "to_max_pct": 70,
      "ca_geral": 2.8,
      "ca_institucional": 2.8,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20
    },
    "ZC2": {
      "descricao": "Zona Central de Comércio e Serviços 2 — centro comercial consolidado",
      "to_max_pct": 70,
      "ca_geral": 3.5,
      "ca_institucional": 3.5,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 3.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20
    },
    "ZAE1": {
      "descricao": "Zona de Atividades Econômicas 1 — margens da BR-494, atividades de grande porte regional",
      "to_max_pct": 70,
      "ca_geral": 3.5,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20
    },
    "ZAE2": {
      "descricao": "Zona de Atividades Econômicas 2 — Alameda N. S. de Fátima e trechos da Av. Maracanã/Benjamin",
      "to_max_pct": 70,
      "ca_geral": 2.1,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20
    },
    "ZAE3": {
      "descricao": "Zona de Atividades Econômicas 3 — Av. Maracanã, Av. Miguel Resende e Alameda Dr. Cícero",
      "to_max_pct": 70,
      "ca_geral": 3.5,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20
    },
    "ZAE4": {
      "descricao": "Zona de Atividades Econômicas 4 — Av. Benjamin Guimarães (1361 ao limite BR-369) e Av. César Barros",
      "to_max_pct": 70,
      "ca_geral": 3.5,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "afastamento_fundo_min_m": 1.5,
      "tp_min_pct": 20
    },
    "ZIND": {
      "descricao": "Zona Industrial — Distritos Industriais: Dermeval Chagas, David Mattar, Eduardo Abdo, Benedito Landim, Adauto Lopes e Distrito de Morro do Ferro",
      "to_max_pct": 70,
      "ca_geral": 3.5,
      "afastamento_lateral_min_m": 1.5,
      "afastamento_frontal_min_m": 1.5,
      "tp_min_pct": 20
    }
  },
  "artigos": {
    "decreto_4149_2019": {
      "_nome": "Decreto nº 4.149/2019 — Procedimentos para concessão de aprovação de projetos",
      "art_2": {
        "descricao": "Prazo para análise e emissão de autorizações",
        "conteudo": "A análise e emissão de autorizações ou alvarás deverá ser executada por 02 (dois) técnicos da SMOSU no prazo máximo de 15 (quinze) dias úteis.",
        "uso_no_gem": "Informativo. Citar quando o prazo de análise for relevante ao processo."
      },
      "art_4": {
        "descricao": "Documentos obrigatórios para requerimento de alvará de construção",
        "documentos": [
          "I — Cópia do documento pessoal do requerente com foto",
          "II — Procuração, acompanhada da documentação do outorgado (se aplicável)",
          "III — Comprovante de endereço atualizado",
          "IV — Certidão atualizada do imóvel ou contrato de compra e venda",
          "V — Projeto arquitetônico em 01 (uma) via, assinado pelo proprietário e pelo responsável técnico",
          "VI — RT (Responsabilidade Técnica) com atribuição técnica para: Execução de Projeto Arquitetônico, Execução de Projeto e Cálculo Estrutural e Execução de Obra Civil",
          "VII — Guia de recolhimento da Taxa de Licença, devidamente quitada"
        ],
        "nota_para_gem": "Para obras acima de 100m²: exigir cópia do Projeto Estrutural e RT específica. Para obras acima de 250m²: exigir também Projeto Elétrico e Hidrossanitário com RTs."
      },
      "art_5": {
        "descricao": "Documentos obrigatórios para habite-se",
        "documentos": [
          "I — Cópia do documento pessoal do requerente com foto",
          "II — Procuração (se aplicável)",
          "III — Comprovante de endereço atualizado",
          "IV — Certidão atualizada do imóvel ou contrato de compra e venda",
          "V — Cópia do alvará de construção da obra",
          "VI — RT quanto ao Projeto Arquitetônico, com anotação até 30 dias do protocolo"
        ]
      },
      "art_6": {
        "descricao": "Documentos obrigatórios para requerimento de demolição",
        "documentos": [
          "I — Cópia do documento pessoal do requerente com foto",
          "II — Procuração (se aplicável)",
          "III — Comprovante de endereço atualizado",
          "IV — Certidão atualizada do imóvel ou contrato de compra e venda",
          "V — Guia de recolhimento da Taxa de Demolição, devidamente quitada",
          "VI — ART (CREA), RRT (CAU) ou TRT (CFT) com atribuição técnica para demolição"
        ]
      },
      "art_7": {
        "descricao": "Documentos obrigatórios para desmembramento e membramento",
        "documentos": [
          "I — Cópia do documento pessoal do requerente com foto",
          "II — Procuração (se aplicável)",
          "III — Comprovante de endereço atualizado",
          "IV — Certidão atualizada do imóvel com prazo máximo de 30 dias",
          "V — Guia de recolhimento da respectiva taxa, quitada",
          "VI — Levantamento topográfico georreferenciado em 02 vias, assinado pelo proprietário e responsável técnico",
          "VII — ART (CREA), RRT (CAU) ou TRT (CFT) com atribuição técnica para o levantamento",
          "VIII — Documentos descritos no Art. 24 da Lei Complementar nº 216/2014"
        ]
      },
      "art_9": {
        "descricao": "Revalidação do Alvará de Construção",
        "conteudo": "Fica autorizada a revalidação do Alvará de Construção, vencido ou não, sempre que o dono da obra o requerer. O processo deverá ser concluído em 15 dias úteis. A revalidação é condicionada à fidelidade da obra ao projeto aprovado.",
        "citacao_considerando": "o requerente solicitou a revalidação do Alvará de Construção nº {numero_alvara}, nos termos do __Art. 9º do Decreto nº 4.149/2019__, sendo a renovação condicionada à confirmação, por parecer fiscal, de que a obra está sendo executada em conformidade com o projeto originalmente aprovado;"
      }
    },
    "lei_1544_86": {
      "_nome": "Lei nº 1.544/86 — Código de Obras do Município de Oliveira/MG",
      "art_9": {
        "descricao": "Validade do alvará de construção — 1 ano",
        "conteudo": "Após aprovação do projeto e comprovado pagamento das taxas, a Prefeitura fornecerá alvará de construção válido por 1 (um) ano, ressalvando ao interessado requerer revalidação.",
        "uso_no_gem": "Citar quando alvará estiver vencido ou ao informar prazo de validade nos documentos emitidos."
      },
      "art_13": {
        "descricao": "Prorrogação de alvará — 180 dias",
        "conteudo": "Quando expirar o prazo do alvará e a obra não estiver concluída, deverá ser solicitada renovação, que poderá ser concedida por mais 180 (cento e oitenta) dias, sempre após vistoria da obra.",
        "citacao_considerando": "o Alvará de Construção nº {numero_alvara} encontra-se com prazo expirado, sendo a obra ainda não concluída, conforme atestado pelo parecer fiscal, razão pela qual poderá ser concedida a renovação pelo prazo de 180 (cento e oitenta) dias, nos termos do __Art. 13 da Lei nº 1.544/86__, condicionada à vistoria técnica;"
      },
      "art_43": {
        "descricao": "Proibição de aberturas a menos de 1,50m da divisa",
        "conteudo": "Não poderá haver aberturas em paredes levantadas sobre a divisa ou a menos de 1,50m (um metro e cinquenta centímetros) da mesma.",
        "gatilho": "abertura_divisa_sem_anuencia == true",
        "multa_id": null,
        "documento_condicional": "termo_anuencia_confrontante",
        "citacao_considerando": "foi constatada a existência de abertura (janela/porta/basculante) a distância inferior a **1,50m** da divisa lindeira, em desacordo com o __Art. 43 da Lei nº 1.544/86__, sendo condição obrigatória para a emissão dos documentos finais a apresentação de Termo de Anuência formal do proprietário confrontante, devidamente registrado, cedendo o direito àquela abertura;",
        "citacao_fundamentacao": "__Art. 43 da Lei Municipal nº 1.544/86 (Código de Obras):__ Não poderá haver aberturas em paredes levantadas sobre a divisa ou a menos de 1,50m (um metro e cinquenta centímetros) da mesma. A regularização dessa situação está condicionada à apresentação de Termo de Anuência do proprietário lindeiro, registrado em cartório."
      },
      "art_68_a_77": {
        "descricao": "Construções irregulares — Embargo e Interdição",
        "conteudo_resumido": [
          "Art. 68: Obra sem licença sujeita a multa, embargo, interdição e demolição.",
          "Art. 72: Não cabe notificação prévia quando obra iniciar sem licença — o infrator é imediatamente autuado.",
          "Art. 73: A obra será embargada quando: (I) executada sem licença; (II) desrespeitando o projeto aprovado; (III) proprietário recusar-se a atender notificação; (IV) não observados alinhamentos; (V) estiver em risco de estabilidade.",
          "Art. 75: O embargo só será levantado após cumprimento das exigências do auto de embargo."
        ],
        "citacao_considerando_embargo": "foi constatada a execução de obra sem alvará e/ou em desacordo com o projeto aprovado, configurando infração passível de embargo imediato nos termos dos __Arts. 68 e 72 da Lei nº 1.544/86__, sem necessidade de notificação prévia;"
      },
      "art_79": {
        "descricao": "Tabela de multas — Capítulo XI (Das Multas)",
        "base_calculo": "URM — Unidade de Referência Municipal (verificar valor vigente na SMOSU)",
        "escalonamento": {
          "I_sem_licenca": {
            "descricao": "Iniciar ou executar obras sem licença da Prefeitura Municipal",
            "faixas": [
              {
                "faixa": "até 60,00m²",
                "aliquota_pct_por_m2": 1,
                "label": "1% da URM por m²"
              },
              {
                "faixa": "61,00m² a 75,00m²",
                "aliquota_pct_por_m2": 3,
                "label": "3% da URM por m²"
              },
              {
                "faixa": "76,00m² a 100,00m²",
                "aliquota_pct_por_m2": 4,
                "label": "4% da URM por m²"
              },
              {
                "faixa": "acima de 100,00m²",
                "aliquota_pct_por_m2": 5,
                "label": "5% da URM por m²"
              }
            ],
            "formula": "area_m2 × (aliquota_pct / 100) × valor_URM_vigente",
            "excecoes_aplicaveis": [
              "decadencia_administrativa_5anos"
            ],
            "citacao_considerando": "foi constatada a execução de obra sem alvará prévio da Prefeitura Municipal, na área de **{area_irregular}m²**, infração tipificada no __Art. 79, Inciso I, alínea {alínea} da Lei nº 1.544/86__, incidindo multa calculada à razão de **{aliquota}% da URM por m²**, totalizando **R$ {valor_multa}** ({area_irregular}m² × {aliquota}% × URM R$ {valor_urm});",
            "citacao_fundamentacao": "__Art. 79, Inciso I da Lei Municipal nº 1.544/86 (Código de Obras):__ As multas são calculadas por alíquotas percentuais sobre a URM, escalonadas conforme a área edificada irregular: (a) até 60m²: 1%/m²; (b) 61 a 75m²: 3%/m²; (c) 76 a 100m²: 4%/m²; (d) acima de 100m²: 5%/m²."
          },
          "II_desacordo_projeto": {
            "descricao": "Executar obras em desacordo com o projeto aprovado",
            "aliquota_pct_da_urm": 100,
            "formula": "100% × valor_URM_vigente (valor fixo, independente da área)",
            "citacao_considerando": "foi verificado que a obra executada diverge do projeto aprovado, constituindo infração ao __Art. 79, Inciso II da Lei nº 1.544/86__, com aplicação de multa equivalente a **100% da URM**, no valor de **R$ {valor_urm}**;"
          },
          "III_desacordo_alinhamento": {
            "descricao": "Construir em desacordo com o termo de alinhamento",
            "aliquota_pct_da_urm": 100,
            "citacao_considerando": "a edificação apresenta desconformidade com o alinhamento predial, infração tipificada no __Art. 79, Inciso III da Lei nº 1.544/86__, incidindo multa de **100% da URM** (R$ {valor_urm});"
          },
          "IV_omitir_cursos_dagua": {
            "descricao": "Omitir no projeto cursos d'água ou topografia acidentada que exijam contenção",
            "aliquota_pct_da_urm": 50,
            "citacao_considerando": "foi verificada a omissão de {elemento_omitido} no projeto apresentado, infração ao __Art. 79, Inciso IV da Lei nº 1.544/86__, com multa de **50% da URM** (R$ {valor_multa});"
          },
          "V_demolicao_sem_licenca": {
            "descricao": "Demolir prédios sem licença da Prefeitura Municipal",
            "aliquota_pct_da_urm": 50,
            "citacao_considerando": "foi constatada a execução de demolição sem o competente alvará de demolição, infração prevista no __Art. 79, Inciso V da Lei nº 1.544/86__, incidindo multa de **50% da URM** (R$ {valor_multa});"
          },
          "VI_sem_projeto_no_local": {
            "descricao": "Não manter no local da obra o projeto ou alvará",
            "aliquota_pct_da_urm": 20
          },
          "VII_material_logradouro": {
            "descricao": "Deixar materiais sobre o logradouro público além do tempo necessário",
            "aliquota_pct_da_urm": 20
          },
          "VIII_sem_tapumes": {
            "descricao": "Não colocar tapumes e andaimes em obras que atinjam o alinhamento",
            "aliquota_pct_da_urm": 20
          }
        },
        "reincidencia": "Art. 79 §3º (acrescido pela LC 267/2019): a penalidade é aplicada em dobro a cada reincidência.",
        "prazo_legalizacao": "Art. 80: O contribuinte tem 8 (oito) dias, a contar da intimação ou autuação, para legalizar a obra. Esgotado o prazo, é considerado reincidente."
      },
      "art_16_17_tapumes": {
        "descricao": "Proteção de Passeio com Tapumes",
        "conteudo": "Nenhuma construção no alinhamento poderá ser executada sem tapumes (Art. 16). Tapumes e andaimes não poderão ocupar mais do que a metade da largura do passeio (Art. 17).",
        "citacao_considerando": "constatou-se a ocupação irregular do passeio público por tapumes/andaimes além da metade da sua largura, desrespeitando o limite de livre trânsito previsto no __Art. 17 da Lei nº 1.544/86__;"
      }
    },
    "lc_267_2019": {
      "_nome": "Lei Complementar nº 267/2019 — Uso e Ocupação do Solo do Município de Oliveira/MG",
      "art_9_par13": {
        "descricao": "Exceção de afastamentos para lotes ≤220m²",
        "ver": "excecoes.lote_igual_ou_menor_220m2"
      },
      "art_9_par14": {
        "descricao": "Taxa de permeabilidade mínima universal — 20%",
        "conteudo": "Fica definido que a taxa de permeabilidade mínima para lotes de qualquer área será de 20% (vinte por cento). (EMENDA 25)",
        "uso_no_gem": "A TP de 20% é obrigatória para TODOS os lotes, independente de zona ou tamanho. Não há exceção por área do terreno para este parâmetro."
      },
      "art_9_par15": {
        "descricao": "Afastamento frontal e de fundo mínimo universal — 1,50m",
        "conteudo": "Aplica-se a todas as respectivas zonas constantes desta Lei, inclusive as zonas do Distrito de Morro do Ferro, o afastamento frontal e de fundo correspondente a 1,50m. (EMENDA 26)",
        "uso_no_gem": "Afastamento frontal mínimo de 1,50m e de fundo de 1,50m em todas as zonas (salvo exceção do §13 para lotes ≤220m²)."
      },
      "art_38": {
        "descricao": "Infrações à LC 267/2019",
        "infrações": [
          "I — Desatendimento às limitações de uso do solo (Anexo II)",
          "II — Desatendimento dos parâmetros de ocupação do solo (TO, TP, CA, afastamentos)",
          "III — Desatendimento às demais condições complementares da edificação",
          "IV — Desatendimento das condições das Áreas de Diretrizes Especiais (ADE)",
          "V — Desatendimento das condicionantes dos processos de licenciamento",
          "VI — Desatendimento de condicionantes do EIV (Estudo de Impacto de Vizinhança)"
        ],
        "citacao_considerando": "os parâmetros urbanísticos da edificação apresentam desconformidade com os __Arts. 38 e 39 da Lei Complementar nº 267/2019__, especificamente: taxa de ocupação de **{taxa_ocupacao}** (máximo da zona: **{to_max_zona}%**) e taxa de permeabilidade de **{taxa_permeabilidade}** (mínimo exigido: **{tp_min_zona}%**), configurando as infrações previstas nos incisos II e III do Art. 38;"
      },
      "art_39": {
        "descricao": "Penalidades por infrações à LC 267/2019 — escala por área",
        "base_calculo": "Valor da taxa cobrada quando da expedição do alvará de construção (consultar SMOSU para valor vigente)",
        "escalonamento": [
          {
            "faixa": "até 40,00m²",
            "multiplicador": 1,
            "label": "equivalente a 1× o valor da taxa de alvará"
          },
          {
            "faixa": "40,10m² a 80,00m²",
            "multiplicador": 3,
            "label": "equivalente a 3× o valor da taxa de alvará"
          },
          {
            "faixa": "80,10m² a 100,00m²",
            "multiplicador": 6,
            "label": "equivalente a 6× o valor da taxa de alvará"
          },
          {
            "faixa": "acima de 100,10m²",
            "multiplicador": 10,
            "label": "equivalente a 10× o valor da taxa de alvará"
          }
        ],
        "nota": "Parágrafo único: As penalidades do Art. 39 são aplicadas CUMULATIVAMENTE às infrações cometidas (cada tipo de infração gera sua própria multa).",
        "excecoes_aplicaveis": [
          "lote_igual_ou_menor_220m2"
        ],
        "citacao_considerando": "incide multa prevista no __Art. 39 da Lei Complementar nº 267/2019__ sobre a área em desacordo de **{area_desacordo}m²**, enquadrando-se na faixa {faixa_descricao}, equivalente a **{multiplicador}× o valor da taxa de expedição do alvará** (R$ {valor_multa});",
        "citacao_fundamentacao": "__Arts. 38 e 39 da Lei Complementar nº 267/2019 (Uso e Ocupação do Solo):__ Constituem infrações o desatendimento dos parâmetros de ocupação do solo. As penalidades são escalonadas conforme a área em desacordo: até 40m² = 1× a taxa de alvará; de 40,1 a 80m² = 3×; de 80,1 a 100m² = 6×; acima de 100,1m² = 10×. As penalidades são aplicadas cumulativamente."
      }
    },
    "lei_1788_89": {
      "_nome": "Lei nº 1.788/1989 — Código de Posturas do Município de Oliveira/MG",
      "art_111": {
        "descricao": "Alvará de Funcionamento e Localização",
        "conteudo": "Para liberação da licença de funcionamento pela Prefeitura Municipal, o prédio deverá ser previamente vistoriado pelos órgãos competentes quanto às condições de higiene e segurança, qualquer que seja o ramo de atividade.",
        "citacao_considerando": "o requerimento atende às disposições para concessão de Alvará de Funcionamento e Localização, submetendo-se à vistoria prévia exigida pelo __Art. 111 da Lei nº 1.788/1989 (Código de Posturas)__ para verificação das condições de higiene e segurança;"
      },
      "art_114": {
        "descricao": "Cassação de Alvará de Localização",
        "conteudo": "A Licença de Localização poderá ser cassada a qualquer tempo quando se tratar de negócio diferente do requerimento, medida preventiva a bem da higiene ou recusa em exibir o Alvará.",
        "citacao_considerando": "verificou-se infração passível de cassação do Alvará de Localização, com fundamento no __Art. 114 da Lei nº 1.788/1989 (Código de Posturas)__, implicando o fechamento do estabelecimento;"
      },
      "art_13_escavacoes": {
        "descricao": "Escavações e Aberturas em Vias e Passeios Públicos",
        "conteudo": "Não é permitido fazer aberturas no calçamento ou escavações nas vias públicas sem expressa autorização. Na abertura de valas nos passeios, é obrigatória a adoção de ponte provisória. Deve haver sinalização de perigo (luzes vermelhas).",
        "citacao_considerando": "foi constatada a abertura não autorizada do calçamento/passeio para execução de escavações, sem a devida adoção de ponte provisória e/ou sinalização de segurança para pedestres, constituindo infração ao __Art. 13 da Lei nº 1.788/1989 (Código de Posturas)__;"
      },
      "art_13_invasao_logradouro": {
        "descricao": "Demolição de Obra que Invade a Calçada ou Rua",
        "conteudo": "A Prefeitura coibirá invasões de logradouros. Verificada invasão por obra de caráter permanente, será promovida a sua imediata demolição.",
        "citacao_considerando": "a vistoria atestou que a edificação/obra invade o logradouro público (passeio/via), conduta tipificada no logradouro de invasão de área pública, sujeitando-se o infrator à sumária demolição da obra permanente, em deferência ao __Art. 13, § 1º da Lei nº 1.788/1989 (Código de Posturas)__;"
      },
      "art_20_limpeza": {
        "descricao": "Limpeza e Conservação de Calçadas (Passeios)",
        "conteudo": "Os moradores (e donos de lotes) são responsáveis pela limpeza do passeio fronteiriço à sua residência/obra. É proibido varrer lixo para o logradouro.",
        "citacao_considerando": "constatou-se o acúmulo irregular de resíduos, detritos ou falta de higiene no passeio (calçada) fronteiriço ao imóvel, obrigação de conservação que recai sobre o responsável legal pelo lote nos termos do __Art. 20 da Lei nº 1.788/1989 (Código de Posturas)__;"
      },
      "art_27_entulhos": {
        "descricao": "Remoção de Entulhos de Obras",
        "conteudo": "Restos e materiais de construção, assim como entulhos, são lixo de remoção especial (inciso III). Devem ser removidos pelo construtor diretamente ou recolhidos pela Prefeitura mediante pagamento antecipado da taxa.",
        "citacao_considerando": "foram depositados entulhos e restos de materiais de construção no logradouro sem a devida remoção especial custeada pelo interessado, ato violador do __Art. 27 da Lei nº 1.788/1989 (Código de Posturas)__;"
      },
      "art_45_materiais_construcao": {
        "descricao": "Depósito de Materiais de Construção em Via Pública",
        "conteudo": "É proibido embaraçar o livre trânsito das vias com depósitos de quaisquer materiais, inclusive construção. Tolerância máxima de descarga na via é de 5 horas, apenas se a descarga não for possível internamente e com devida sinalização.",
        "citacao_considerando": "foram mantidos depositados materiais de construção na via pública/passeio de forma injustificada, por lapso temporal superior à operação permitida de descarga (máximo de 5 horas admitido por força maior), violando a garantia de livre trânsito expressa no __Art. 45 da Lei nº 1.788/1989 (Código de Posturas)__;"
      },
      "art_81_arvores": {
        "descricao": "Derrubada e Poda de Árvores no Logradouro",
        "conteudo": "É proibido podar, cortar ou sacrificar toda e qualquer vegetação das praças e passeios públicos sem pedido formal, recolhimento da taxa (VRM) e imediato plantio substituto.",
        "citacao_considerando": "houve sacrifício/poda/remoção irregular ou constata-se a pretensão de remoção de cobertura arbórea existente no passeio público, desprovida da licença municipal e desacompanhada da contrapartida de novo plantio fronteiriço imediato, violando o __Art. 81 da Lei nº 1.788/1989 (Código de Posturas)__;"
      }
    },
    "lei_6766_79": {
      "_nome": "Lei Federal nº 6.766/1979 — Parcelamento do Solo Urbano",
      "art_2": {
        "descricao": "Loteamento e Desmembramento",
        "conteudo": "§ 1º Considera-se loteamento a subdivisão de gleba com abertura de novas vias. § 2º Considera-se desmembramento a subdivisão com aproveitamento do sistema viário existente.",
        "citacao_considerando": "o projeto apresentado caracteriza-se como {tipo_parcelamento}, nos termos do __Art. 2º da Lei Federal nº 6.766/1979__, {justificativa_abertura_vias};",
        "citacao_fundamentacao": "__Art. 2º da Lei nº 6.766/1979:__ O parcelamento do solo urbano poderá ser feito mediante loteamento (com abertura de vias) ou desmembramento (aproveitamento do sistema viário existente, sem abertura de vias)."
      }
    },
    "lc_216_2014": {
      "_nome": "Lei Complementar nº 216/2014 (Redação dada pela LC 313/2024) — Parcelamento do Solo",
      "art_6_condominios": {
        "descricao": "Condomínios de Lotes",
        "conteudo": "I. áreas destinadas aos sistemas de circulação interna, com largura mínima de 08 (oito) metros; II. lotes com área mínima de 1.000 m² (um mil metros quadrados) e frente mínima de 20 (vinte) metros.",
        "alerta_gem": "Exija sempre 1.000m² de área e 20m de frente para Condomínio de Lotes.",
        "citacao_considerando": "o projeto de Condomínio de Lotes atende aos parâmetros mínimos estabelecidos pela __Lei Complementar nº 216/2014 (alterada pela LC 313/2024)__, apresentando lotes com área igual ou superior a 1.000m² e frente igual ou superior a 20 metros;"
      }
    }
  },
  "responsabilidade_tecnica": {
    "_instrucao": "Ao identificar o tipo de RT no processo, registrar o campo 'resp_tecnica_tipo' no JSON conforme a tabela abaixo.",
    "tipos": {
      "ART": {
        "nome_completo": "Anotação de Responsabilidade Técnica",
        "conselho": "CREA — Conselho Regional de Engenharia e Agronomia",
        "profissionais": [
          "Engenheiro Civil",
          "Engenheiro Arquiteto",
          "Agrônomo",
          "Geólogo",
          "Técnico Industrial"
        ],
        "sigla_registro": "CREA"
      },
      "RRT": {
        "nome_completo": "Registro de Responsabilidade Técnica",
        "conselho": "CAU — Conselho de Arquitetura e Urbanismo",
        "profissionais": [
          "Arquiteto e Urbanista"
        ],
        "sigla_registro": "CAU"
      },
      "TRT": {
        "nome_completo": "Termo de Responsabilidade Técnica",
        "conselho": "CFT/CRT — Conselho Federal/Regional de Técnicos Industriais",
        "profissionais": [
          "Técnico Industrial"
        ],
        "sigla_registro": "CFT/CRT"
      }
    }
  },
  "checklist_analise_gem": {
    "_instrucao": "Execute esta sequência em TODA análise de processo. Registre cada resultado antes de gerar o JSON final.",
    "passos": [
      {
        "passo": 1,
        "label": "Verificar área do terreno",
        "acao": "Extrair area_terreno_m2 do carimbo do projeto. Se <= 220 → aplicar excecoes.lote_igual_ou_menor_220m2",
        "output": "boolean excecao_220m2"
      },
      {
        "passo": 2,
        "label": "Verificar tempo de conclusão da obra (regularizações)",
        "acao": "Se processo for regularização/as built: verificar evidências da data de conclusão. Se >= 5 anos → aplicar excecoes.decadencia_administrativa_5anos",
        "output": "boolean decadencia_aplicavel"
      },
      {
        "passo": 3,
        "label": "Identificar zona e conferir parâmetros",
        "acao": "Identificar a zona do imóvel. Comparar TO, TP, CA e afastamentos do projeto com os limites de parametros_zonais.{zona}. Se excecao_220m2=true → ignorar afastamentos, verificar apenas TP.",
        "output": "lista de parametros_violados"
      },
      {
        "passo": 4,
        "label": "Calcular multas aplicáveis",
        "acao": "Para cada infração: (a) obra sem licença → Art. 79 Lei 1544; (b) desacordo com parâmetros zona → Art. 39 LC 267. Verificar se decadência ou excecao_220m2 bloqueiam alguma multa.",
        "output": "lista de multas com valores"
      },
      {
        "passo": 5,
        "label": "Verificar Art. 43 (abertura na divisa)",
        "acao": "Conferir na planta se há janelas, portas ou basculantes a menos de 1,50m da divisa lateral. Se sim → condicionar emissão ao Termo de Anuência do confrontante.",
        "output": "boolean abertura_divisa_irregular"
      },
      {
        "passo": 6,
        "label": "Verificar proximidade de APP/curso d'água",
        "acao": "Se a planta ou parecer fiscal indicar APP, ribeirão, área de preservação → emitir oficio_meio_ambiente conjuntamente.",
        "output": "boolean oficio_ambiental_necessario"
      },
      {
        "passo": 7,
        "label": "Selecionar tipo_relatorio e redigir JSON",
        "acao": "Com base em todos os passos anteriores, selecionar o tipo_relatorio correto e redigir considerandos usando os campos citacao_considerando deste codex.",
        "output": "JSON final validado"
      }
    ]
  }
}
# Árvore Mestra da Legislação e Base de Conhecimento RAG (Bíblia Legal)

> **Instrução Primária para a Inteligência Artificial (GEM):** 
> Este documento é o ÍNDICE GERAL (Schema) do banco de dados jurídico. Sempre que você receber um documento PDF (projeto, requerimento, foto de satélite) para análise, você **DEVE** percorrer mentalmente a arquitetura estrutural abaixo em ordem de precedência.
> Toda infração ou adequação jurídica que você levantar e exportar para o "JSON do Parecer" precisa ter citação direta do Artigo e Lei listada nestes arquivos, resolvendo conflitos de lei (Ex: Lei específica > Lei geral).

---

## 🏛️ CAMADA 1: CONSTITUIÇÃO E FUNDAMENTOS MACROS
Nesta camada encontram-se as fundações jurídicas. Raramente aplicar-se-á restrições matemáticas pontuais daqui, mas balizarão processos pesados (como Loteamentos, isenções tributárias religiosas, áreas de preservação ou doações institucionais).

1. **Constituição Municipal:** Consulte o arquivo `lei_1990_organica.md`. Define imunidade de IPTU para entes, aprovação pela Câmara, etc.
2. **Plano Diretor:** Consulte o arquivo `lc_160_2011_plano_diretor.md`. Traz diretrizes, função social, IPTU progressivo no tempo e exigência de compensação ambiental básica.

---

## 📏 CAMADA 2: CÓDIGO DE OBRAS E OCUPAÇÃO DO SOLO (PARÂMETROS EXATOS)
Esta é a camada **principal** para 90% das análises de Alvará e Habite-se. Aqui residem as fórmulas matemáticas urbanísticas (Recuos, CA, TO, Permeabilidade).

3. **Lei de Uso e Ocupação do Solo (A mais importante):** Consulte o arquivo `lc_267_2019_uso_ocupacao.md` (e suas alterações legais contidas nela como a LC 313/2024). 
    * *Destaque de Precedência:* Em caso de regras conflitantes sobre tamanho da edificação vs Código antigo, aplica-se ESTA lei. Contém a tabela de zonas (ZC, ZUR, ZIND).
    * *Exceção Suprema (Art. 15):* Lotes menores que **220m²** estão absolutos ISENTOS de Taxa de Ocupação Mínima e Permeabilidade Mínima.
4. **Código de Obras e Edificações:** Consulte o arquivo `lei_1544_1986_codigo_obras.md`. 
    * Base penal: Obras irregulares ou sem licença aplicam multa calculada sobre este código (Art. 79). Regula o rasgo de lindeiros (distância de janelas a <1,50m exige anuência).
5. **Código de Posturas Urbanas:** Consulte o arquivo `lei_1788_1989_codigo_posturas.md`.
    * Regula multas de limpeza de lotes (VRM), obstrução de calçadas, tapumes e poluição/horário de funcionamento de estabelecimentos.

---

## 🏘️ CAMADA 3: PARCELAMENTO, LOTEAMENTOS E MEIO AMBIENTE
Acionada pelo GEM somente em processos que envolvam divisão da gleba, desmembramento ou chacreamento rural/urbano.

6. **Chacreamento e Lotes Fechados:** Consulte `lc_239_2015_chacreamento.md` e `lc_270_2020_condominio_lotes.md`. Zonas de Urbanização Específica (ZUE), áreas mínimas de 1000m², recuos de 3m e permissões de biodigestores.
7. **Parcelamento de Solo Consolidado:** (Altera a LC 216/2014) - Permite o desdobro e a "Certidão de Número Suplementar" via LC 250/2016 para separar contas de água/luz em casas/puxadinhos antigos sem aprovar todo um desmembramento fundiário.
8. **APP Urbana:** Consulte `lei_3971_2023_app_urbana.md`. Define recuos fluviais de 5 a 30 metros (Zonas ZN-1 a ZN-4) caso rio/curso cruze o terreno do contribuinte.

---

## 💰 CAMADA 4: LEIS TRIBUTÁRIAS E CERTIDÕES ADMINISTRATIVAS
Acionada para definir multas pecuniárias retroativas, gerar "Habite-se de Decadência" fiscal ou tramitar processos por decretos executivos.

9. **Código Tributário Municipal:** Consulte `lc_02_1990_codigo_tributario.md`. Descontos "IPTU Verde" e ISSQN (Retenções na nota de empreiteira).
10. **Código Tributário Nacional (A Anistia dos 5 Anos):** Base legal da Certidão de Decadência Administrativa. Em suma, o GEM deve perdoar infrações ambientais/construtivas se provado via aerofotogrametria/satélite que o "tijolo" já completou **5 (cinco) anos ininterruptos** no terreno (Art. 150, §4º, CTN).
11. **Decreto Padrão de Análise de Projetos:** Consulte `decreto_4149_2019.md`. Define os prazos legais da prefeitura (15 dias úteis) e seções exatas das pranchas (carimbo, plantas elétricas, etc).

---

## 🗃️ CAMADA 5: BANCO DE MANUAIS OFICIAIS AUXILIARES
Sempre que a análise exigir endereços, cruzar bairros ou quantificar custos em Reais, o GEM utilizará o banco de dados local:

* `checklists_obras.md`: A peneira final; cruze se o rol de arquivos PDF mandados na solicitação atende à lista mínima do checklist burocrático (Documentos com firma, registro em cartório, guia ART, etc).
* `bairros_zoneamento_ipm.md`: O roteador; recebe o bairro pelo logradouro do projeto e aponta a "Abreviatura da Zona" (ZC, ZUR, ZAE) que servirá de *query* para olhar a LC 267/2019.
* `ruas_oliveira.md`: A verificação ortográfica. Identifica se a RUA do cidadão realmente existe e qual sua cordenada cartográfica.
* `tabela_valores_e_regras_2025.md`: Tabela econômica. Após decidir pelo JSON quais infrações ocorreram, aplique a multa monetária puxando o valor atualizado das URM / VRM nesta tabela. **VRM 2026 = R$ 102,42** (Valor de Referência Municipal — Lei 1.788/1989, Código de Posturas).

