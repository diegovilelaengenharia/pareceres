# ==========================================
# PARTE 1: CODEX LEGAL E REFERÊNCIAS
# ==========================================

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
* `tabela_valores_e_regras_2025.md`: Tabela econômica. Após decidir pelo JSON quais infrações ocorreram, aplique a multa monetária puxando o valor atualizado das URM / VRM nesta tabela de 2025.


`json
{
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
`

# ==========================================
# PARTE 2: ZONEAMENTO E MULTAS
# ==========================================

# MAPEAMENTO GEOGRÁFICO DE BAIRROS, CÓDIGOS IPM E ZONEAMENTO — OLIVEIRA/MG

Este documento consolida os dados do sistema municipal (Atende.Net IPM) cruzados com a classificação de Zoneamento Urbano da Lei Complementar nº 267/2019. O GEM deve consultar esta tabela sempre que precisar validar a Zona de um Bairro indicado nos projetos, para aplicar os parâmetros corretos de Coeficiente de Aproveitamento (CA), Taxa de Ocupação (TO) e Taxa de Permeabilidade (TP).

| Cód IPM | Nome do Bairro (Sistema IPM) | Ocorrência Comum / Equivalente | Zoneamento (LC 267/2019) |
| :--- | :--- | :--- | :--- |
| 922 | ACACIO RIBEIRO | Acácio Ribeiro | ZUR 3 |
| 59 | ACACIO RIBEIRO II | Acácio Ribeiro 2 | ZUR 3 |
| 65 | ACACIO RIBEIRO III | Acácio Ribeiro 3 | ZUR 3 |
| 2 | ALDEIA SAO VICENTE | | |
| 56 | ALVORADA | Alvorada | ZUR 3 |
| 66 | ALVORADA II | | |
| 7203 | ANEL RODOVIÁRIO | | |
| 3 | APARECIDA | Aparecida | ZUR 3 |
| 4 | ARTUR HENRIQUE DE MELO | Artur Henrique de Mello / Alameda Euclides Ribeiro | ZUR 3 |
| 5 | BARRO PRETO | Barro Preto | ZUR 2 |
| 6 | BELA VISTA | | |
| 10 | CABRAIS | | |
| 4981 | CAETANO MASCARENHAS | Caetano Mascarenhas | ZUR 3 |
| 1 | Centro | Centro | ZC e ZCHC |
| 13 | CHACARA DOS AREOES | Chacara do Areão | ZUR 3 |
| 20272 | CHACREAMENTO HARMONIA | | |
| 20048 | CHACREAMENTO MORRO DIAMANTE | | |
| 20624 | CHACREAMENTO VALE DO PARAISO | | |
| 14 | CINTIA | Cintia | ZUR 3 |
| 917 | COMERCIAL CESAR ALMEIDA | Comercial Cesar Almeida | ZAE 4 |
| 7135 | CONDOMINIO DIAMANTE | | |
| 73 | CONDOMINIO IMPERIAL | Condomínio Imperial | ZUR 3 |
| 7174 | CONDOMÍNIO MATA TROPICAL | | |
| 7208 | CONDOMÍNIO NOVO REINO | Condomínio Novo Reino | ZUE (Zona Urbanização Específica) |
| 15 | CONDOMINIO ROCHA COSTA | Condomínio Rocha Costa | ZUR 3 |
| 904 | CONDOMINIO VALE VERDE | | |
| 907 | CONDOMINIO VILLA RICA | Condomínio Vila Rica / Vila Rica | ZUR 1 |
| 20706 | CONJ. HABITACIONAL JOAO P | | |
| 50 | CONJUNTO HABITACIONAL ANTONIO LARANJO | Antonio Laranjo | ZUR SOCIAL |
| 898 | CONJUNTO HABITACIONAL JOAO PAULO II | João Paulo II | ZUR SOCIAL |
| 16 | CRISTO REDENTOR | Cristo Redentor | ZUR 2 |
| 17 | DAS GRACAS | Das Graças | ZUR 2 |
| 19 | DE LOURDES | | |
| 892 | DISTRITO INDUSTRIAL 4 | | ZIND |
| 67 | DISTRITO INDUSTRIAL BENEDITO LANDIM | | ZIND |
| 5078 | DISTRITO INDUSTRIAL DAVID MATT | | ZIND |
| 64 | DISTRITO INDUSTRIAL DAVID MATTAR II | | ZIND |
| 21 | DISTRITO INDUSTRIAL DEMERVAL CHAGAS ALMEIDA | Distrito Industrial Dermeval | ZIND |
| 72 | DISTRITO INDUSTRIAL EDUARDO ABDO | Distrito Industrial Eduardo | ZIND |
| * | DISTRITO INDUSTRIAL ADAUTO LOPES | Distrito Industrial Adauto | ZIND |
| 22 | DO ROSARIO | Do Rosário | ZUR 3 ou ZAE 3 |
| 23 | DOM BOSCO | Dom Bosco | ZUR 3 |
| 55 | DOMINGOS RIBEIRO | Domingos Ribeiro | ZUR 2 |
| 20207 | DONA FIGUINHA | Dona Fiquinha | ZUR 2 |
| 24 | DONA NENEM CAMPOS | Dona Neném Campos / Nenem Campos | ZUR 3 |
| 25 | DONA SINHANINHA | Sinhaninha | ZUR 3 |
| 26 | DONA ZICA | | |
| 27 | DOUTOR FROM | | |
| 28 | ELDORADO | Eldorado | ZUR 2 |
| 5780 | ELIAS RAIMUNDO | Elias Raimundo | ZUR SOCIAL |
| 920 | EUCLIDES RIBEIRO DE OLIVEIRA E SILVA | | |
| 7550 | FRADIQUES | | |
| 20619 | IPANEMA | | |
| 29 | IVAN JUNQUEIRA | | |
| 30 | JARDIM DOS BANDEIRANTES | Jardim dos Bandeirantes | ZUR 1 |
| 53 | JARDIM PANORAMICO | | |
| 57 | JARDIM PANORAMICO II | Jardim Panorâico 2 | ZUR 3 |
| 77 | JARDINS | Jardins | ZUR 3 |
| 20626 | JARDINS RESIDENCE | | |
| 31 | MARIA AMELIA | Maria Amélia | ZUR 3 |
| 32 | MARTINS | Martins | ZUR 3 |
| 54 | MORADA DO SOL | | |
| 33 | MORRO DO FERRO | Morro do Ferro | ZURU (Zona Urbana Rural) |
| 34 | NAZLE SIMAO RAIMUNDO | Nazle Simão Raimundo | ZUR SOCIAL |
| 35 | NOVO ELDORADO | Novo Eldorado | ZUR 2 |
| 910 | NOVO ELDORADO II | Novo Eldorado 2 | ZUR 2 |
| 36 | NOVO HORIZONTE | Novo Horizonte | ZUR 3 |
| 37 | OSCAR DE FARIA LOBATO | Oscar de Faria Lobato | ZUR 2 |
| 20489 | Parque Florestal | | |
| 38 | PEDRA NEGRA | Pedra Negra | ZUR 3 |
| 20723 | PERIMETRO DE EXPANSÃO URBANA | | |
| 20703 | PLANALTO | | |
| 52 | PROGRESSO | | |
| 902 | RESIDENCIAL BELVEDERE | Belvedere | ZUR 2 |
| 916 | RESIDENCIAL CESAR ALMEIDA | Residencial Cesar Almeida | ZUR 2 |
| 20722 | RESIDENCIAL CESAR ALMEIDA 3 | | |
| 900 | RESIDENCIAL DONA FIGUINHA | | |
| 912 | RESIDENCIAL OLIVEIRA | Residencial Oliveira Monte Cristo | ZUR 2 |
| 897 | RESIDENCIAL PORTAL DAS OLIVEIRAS | Portal das Oliveiras / Residencial Portal das Oliveiras | ZUR 2 / ZUR 3 |
| 901 | RESIDENCIAL RECANTO DA SERRA | Recanto da Serra / Residencial Recanto da Serra | ZUR 3 |
| 909 | RESIDENCIAL RENASCER | | |
| 20672 | RESIDENCIAL SALETE | | |
| 895 | RESIDENCIAL SARAIVA | Saraiva / Residencial Saraiva | ZUR 2 |
| 6106 | RESIDENCIAL SINHANINHA II | | |
| 70 | RESIDENCIAL VALE DO SOL - MORRO DO FERRO | Vale do Sol Morro do Ferro | ZUE, ZIND, ZURU |
| 915 | RESIDENCIAL VALE DOS CRISTAIS | | |
| 7451 | RESIDENCIAL VALE DO SOL | Vale do Sol / Residencial Vale do Sol | ZUR 3 |
| 39 | RETIRO DAS PEDRAS | | |
| 7187 | ROSARIO. | | |
| 40 | ROSARIO DE CIMA | Rosário de cima | ZUR 2 |
| 20253 | SANTA LUZIA | | |
| 43 | SANTA MARIA | Santa Maria | ZUR 2 |
| 20712 | SANTO AMARO | | |
| 44 | SANTO ANTONIO | Santo Antônio | ZUR 2 |
| 45 | SAO BERNARDO | SÃo Bernardo | ZUR 3 |
| 46 | SÃO GERALDO | São Geraldo | ZUR 3 |
| 20702 | Sao Sabastiao | São Sebastião | ZUR 3 |
| 3527 | SÃO SEBASTIÃO | São Sebastião | ZUR 3 |
| 48 | SEGREDO | Segredo | ZUR 2 |
| 60 | SITIO DO LOI | | |
| 42 | SITIO RECREIO CATIGUÁ | | |
| 41 | TRIANGULO | Triangulo | ZUR 2 |
| 78 | VALE DO SOL | Vale do Sol | ZUR 3 |
| 61 | VILA BELLA | Vila Bella | ZUR 1 |
| 18 | VILA PROGRESSO | Vila Progresso | ZUR 3 |

*(Loteamentos sem correspondência imediata na lista de Zoneamento permanecem em branco na coluna até atualização legal).*


# MANUAL DEFINITIVO DE APROVAÇÃO (LEIS DE OURO E TABELAS 2025)
*Autor: Analista BoMbAdÃo - SMOSU*

Este é o nosso documento definitivo consolidado. A Bíblia Legal da Aprovação de Projetos, formatada para não deixar brechas. Sempre utilize os valores e regras deste documento para a redação dos pareceres no ano de 2025.

---

### 🥇 AS LEIS DE OURO DA APROVAÇÃO E REGULARIZAÇÃO DE PROJETOS

#### 1. A Exceção do Lote Pequeno (A Regra dos 220 m²)
O município pune a quebra de parâmetros, mas resguarda o lote de pequenas dimensões.
* **A Grande Exceção Urbanística:** Lotes com área total inferior ou igual a **220m² (duzentos e vinte metros quadrados)** ficam completamente isentos das exigências de Taxa de Ocupação Mínima e de Taxa de Permeabilidade Mínima. Ao gerar parecer para terrenos desse porte, isentamos o processo dessas restrições.
* **Referência:** **Art. 15 da Lei Complementar nº 267/2019**.

#### 2. Código de Lindeiros e Aberturas na Divisa
Ninguém invade a privacidade alheia sem autorização legal.
* **A Regra (Abertura inferior à distância obrigatória):** Nenhuma abertura de janela, basculante, chaminé ou porta poderá ser instalada perpendicularmente ou colada à divisa estreita do muro limitrofe a uma distância inferior a **1,50 metros** do terreno vizinho.
* **Exceção de Anuência:** Caso a obra já possua essa abertura, o deferimento fica condicionado, obrigatoriamente, à apresentação de um "Termo de Anuência Formal e Registrado do Proprietário Lindeiro". 
* **Referência:** **Art. 43 da Lei nº 1.544/1986**.

#### 3. As Infrações do Código de Obras (Lei nº 1.544/1986)
O desrespeito ao trâmite processual atrai sanções pecuniárias severas previstas em lei.
* **Construir Sem Licença:** Executar obras com ausência de alvará preliminar é infração e gera multa sob o caput do artigo aplicável, taxa que deve constar em todo Parecer de Regularização As Built. **(Art. 79)**.
* **Desacordo com o Projeto:** Modificar o objeto edificado após obter a aprovação sem requerer nova revalidação gera multa. **(Art. 80)**.
* **Desrespeito a Embargo:** Desobedecer ativamente o embargo afixado pelo conselho municipal na parede do imóvel acarreta inativação de Habite-se futuro e multa dobrada. **(Art. 81)**.
* **Demolição Irregular:** Executar demolição pesada sem licença prévia exige penalização. **(Art. 82)**.

#### 4. Quebra de Parâmetros Urbanísticos (Lei Complementar nº 267/2019)
O zoneamento de Oliveira exige áreas permeáveis e recuos adequados para o controle urbano. 
* A infração aos afastamentos mínimos e à permeabilidade gera embargo pré-calculado e deve constar expressamente no parecer como "Quebra de Parâmetros Urbanísticos". As proibições para recuo com varandas se chocam frontalmente contra a segurança sem a devida permissão da vizinhança.
* **Referências:** **Artigos 38 e 39 da LC 267/2019**. *Atenção especial:* Para o cálculo de multas sobre quebra de parâmetros na Lei 267, as áreas são tratadas de forma **acumulativa**.

#### 5. A Decadência Administrativa e Fiscal Tributária
O tempo prescreve o direito de punir do município.
* **A Regra de Ouro do CTN:** Se há evidências robustas e imagens de satélite provando que a ampliação ou a edificação possui concretamente mais de **5 (cinco) anos ininterruptos** de finalização, o município é obrigado a conceder a "Decadência Administrativa". Isso perdoa financeiramente as infrações dessa metragem por decurso de prazo. O processo é finalizado com uma "Certidão de Decadência".
* **Referência:** **Art. 150, § 4º do Código Tributário Nacional (CTN)**.

---

### 💰 QUADRO OFICIAL DE TAXAS E MULTAS (ATUALIZADO 2025 - Ajuste 4,76%)

Para não haver erro no recolhimento, aqui está o quadro completo e absoluto de valores a serem aplicados em pareceres fiscais de 2025.

#### Taxas de Licença e Alvarás
| Tipo de Serviço | Valor Atualizado 2025 (R$) |
| :--- | :--- |
| **Aprovação de projetos (por m²)** | **R$ 4,28** |
| **Alteração de projeto aprovado (por m²)** | **R$ 4,28** |
| **Construção (Edificação/Galpões) (por m²)** | **R$ 4,28** |
| **Reconstruções, reformas, reparos (por m²)** | **R$ 2,14** |
| **Demolições (por m²)** | **R$ 2,14** |
| **Emissão de Habite-se** | **R$ 81,20** |

#### Multas do Código de Obras (Art. 79 - Lei 1544/86)
*Aplicado sobre a metragem irregular.*

| Enquadramento / Situação | Proporção / Multa | Valor Atualizado 2025 (R$/m²) |
| :--- | :--- | :--- |
| **Construir sem licença (até 60,00m²)** | 1% por m² | **R$ 0,90** |
| **Construir sem licença (61,00m² a 75,00m²)** | 3% por m² | **R$ 2,71** |
| **Construir sem licença (76,00m² a 100,00m²)** | 4% por m² | **R$ 3,62** |
| **Construir sem licença (Acima de 100,00m²)** | 5% por m² | **R$ 4,52** |
| **Executar obra em desacordo com projeto aprovado** | 100% | **R$ 90,60** |

#### Multas de Zoneamento (Art. 39 - LC 267/2019)
*Aplicado em casos de quebra de taxa de ocupação, recuos e permeabilidade. **Aviso:** As faixas de área nesta lei são de caráter **acumulativa** para a composição do cálculo da multa.*

| Faixa de Metragem Irregular | Proporção da Multa | Valor Atualizado 2025 (R$/m²) |
| :--- | :--- | :--- |
| **Até 40m²** | 1x o valor da aprovação | **R$ 4,28** |
| **De 40,01m² até 80,00m²** | 3x o valor da aprovação | **R$ 12,85** |
| **De 80,01m² até 100,00m²** | 6x o valor da aprovação | **R$ 26,75** |
| **Acima de 100,01m²** | 10x o valor da aprovação | **R$ 42,85** |

---
**Diretriz Prática:** Ao analisar qualquer processo, aplicar essas regras e a tabela de 2025 estritamente. Analisar a área, verificar o zoneamento, conferir a isenção subsidiária (<= 220m²), checar prescrição de prazo (> 5 anos para decadência). Para aquilo que não cair nessas amortizações: **aplica-se o cálculo rigoroso das tabelas acima de 2025**.




# ==========================================
# PARTE 1: GUIA DA RECEITA FEDERAL (SERO)
# ==========================================

# 📘 GUIA PROFUNDO: INTEGRAÇÃO PREFEITURA x RECEITA FEDERAL (CNO/SERO)
*Análise Técnica Avançada do Manual Oficial do Sero (Versão 2.0 - 04/2022)*

A elaboração dos documentos da Prefeitura (Alvarás, Habite-se e Certidões) tem impacto direto no bolso do cidadão quando ele for aferir a obra na Receita Federal para registro em Cartório. Se o parecer for genérico, o munícipe pode perder dezenas de milhares de reais em descontos legais.

Este guia revela a "engenharia tributária" do Sero para parametrizar a IA (GEM) na blindagem do cidadão.

---

### 1. Fator Social (O Peso do Tamanho da Obra) - *Item 22.4*
A Receita aplica um "redutor drástico" no imposto (RMT - Remuneração da Mão de Obra Total) para pessoas físicas, de acordo com o tamanho **total** do projeto:
*   Até 100 m²: Paga-se **apenas 20%** da mão de obra.
*   De 101 m² a 200 m²: Paga-se **apenas 40%**.
*   De 201 m² a 300 m²: Paga-se **apenas 55%**.
*   De 301 m² a 400 m²: Paga-se **apenas 70%**.
*   Acima de 400 m²: Paga-se **90%**.

**🚀 Diretriz para o GEM:** Nos projetos de desmembramento ou chacreamento com várias casas, o parecer não deve aprovar "Conjunto de 3 Casas de 80m²" em um único Habite-se global de 240m² (o que jogaria o Fator Social para 55%). Deve instruir o cidadão a aprovar 3 projetos distintos, mantendo cada um abaixo de 100m² para garantir a alíquota mínima de 20%.

---

### 2. A Brutal Redução de Reforma e Demolição - *Item 22.2*
As obras não são cobradas de forma igual no CNO:
*   **Obra Nova e Acréscimo:** Pagam 100% da base de cálculo.
*   **Reforma:** Tem redução de 65%. Paga **apenas 35%**.
*   **Demolição:** Paga **apenas 10%**.

**🚀 Diretriz para o GEM:** Quando o cidadão faz um "Alvará de Reforma e Ampliação", o projeto e o Alvará DEVEM discriminar em linhas separadas a metragem exata da "Área de Reforma" e da "Área de Ampliação". Se a IA jogar tudo num bolo só como "Área Modificada: 150m²", a Receita cobrará 100% sobre tudo. Separar a Reforma salva 65% do imposto do munícipe.

---

### 3. Redução Absurda nas "Áreas Complementares" - *Item 20.2*
As áreas que não compõem a Edificação Principal pagam muito menos INSS.
*   **Área Complementar Coberta** (Ex: Garagem externa, Quadra Coberta): **Redução de 50%**.
*   **Área Complementar Descoberta** (Ex: Piscina, Quadra Descoberta, Estacionamento Térreo Externo): **Redução de 75%**. *(Se o cidadão tem 40m² de piscina, a Receita só tributa 10m²)*.

**🚀 Diretriz para o GEM:** O quadro de áreas do Alvará/Habite-se deve **OBRIGATORIAMENTE** separar de forma expressa as áreas principais das "Áreas Complementares Descobertas" (ex: Piscinas) e "Áreas Complementares Cobertas" (ex: Garagem fora da projeção do telhado). 

---

### 4. Estruturas Pré-Moldadas e Metálicas (Tipo "Mista") - *Item 22.5*
Se a obra utilizar parede externa ou estrutura de **Pré-Moldado ou Pré-Fabricado** (ex: pilares pré-moldados, galpões metálicos), o valor da base de cálculo do INSS sofre uma **REDUÇÃO DE 70%** (o cidadão paga apenas 30%).
*   Para garantir o direito, a obra precisa estar classificada oficialmente.
*   **🚀 Diretriz para o GEM:** Se a descrição do projeto evidenciar Galpão Metálico ou Estrutura Pré-moldada de Concreto, o GEM deve inserir a observação legal: *"Atesta-se para os devidos fins de regularização junto à Receita Federal que a obra é caracterizada por Estrutura Pré-Moldada/Metálica e alvenaria não portante."*

---

### 5. Loteamentos e Chacreamentos (Obras Não Prediais) - *Capítulo V*
Loteamentos, pavimentações e infraestrutura não pagam INSS com base no metro quadrado (CUB/m²) como as casas. A aferição é indireta e se baseia exclusivamente no valor global dos contratos e nas notas fiscais (aplicando alíquota de 40% da mão de obra sobre os serviços).
*   **🚀 Diretriz para o GEM:** Ao aprovar Alvarás de Loteamento ou Termos de Verificação de Infraestrutura, listar rigorosamente todos os serviços prestados (terraplenagem, rede de água, asfalto, meio-fio) no memorial, para dar lastro legal às Notas Fiscais que a loteadora apresentará na Receita.

---

### 6. Casa Popular (Imunidade Total) - *Item 35*
Uma residência unifamiliar com **até 70 m²** construída por pessoa física sem mão de obra remunerada (mutirão/própria) e classificada como "econômica/popular" pelas posturas do Município **fica totalmente dispensada de CNO, SERO e da emissão da Certidão da Receita Federal** para averbar no Cartório.
*   **🚀 Diretriz para o GEM:** Toda obra residencial unifamiliar regularizada até 70m² deve OBRIGATORIAMENTE vir com a nomenclatura *"Residência Unifamiliar - Padrão Econômico / Casa Popular"*. Além disso, adicionar a observação: *"Averbação Cartorária: Nos termos do Manual do Sero/RFB (Item 35.1), por se tratar de obra residencial padrão popular até 70m², a presente edificação está isenta de CNO e SERO para fins de registro imobiliário."*

---

### 7. Decadência Proporcional e As-Built - *Item 23 e 36*
Obras concluídas há mais de 5 anos não pagam nada (Decadência de 100%).
Contudo, obras **parcialmente executadas há mais de 5 anos** pagam apenas a fração recente!
*   **🚀 Diretriz para o GEM:** Na emissão de **Alvarás As-Built (Regularização)** ou Habite-se Parciais, a IA deve cravar a data exata da imagem do satélite histórico: *"De acordo com as imagens de satélite do sistema municipal, atesta-se que a Área X foi edificada e concluída até a data limite de DD/MM/AAAA, possuindo consolidação retroativa superior a 5 (cinco) anos, caracterizando fato gerador decadente para fins tributários e previdenciários."* 

---

### 8. Salvação de Obras Inacabadas (Troca de Titular) - *Item 28.4*
Quando um munícipe compra o "esqueleto" de uma obra paralisada (obra inacabada) e vai terminá-la sob seu próprio CPF/CNPJ, ele não precisa pagar o INSS sobre a parte que o dono antigo construiu. Para isso, o SERO exige um Laudo de Avaliação Técnica (com ART).
*   **🚀 Diretriz para o GEM:** Ao aprovar um pedido de "Transferência de Responsabilidade de Obra Paralisada/Inacabada", a IA deve redigir um Alvará retificador que liste OBRIGATORIAMENTE o percentual ou a metragem atestada pelo engenheiro no laudo.

---

### 9. Aferição do Adquirente (Construtoras Falidas) - *Item 33*
Se a construtora não pagou o INSS do prédio ou faliu, os moradores ficam bloqueados no Cartório de Imóveis. O Manual do SERO permite que **um único morador (condômino)** consiga a CND exclusivamente para o seu apartamento, vinculando seu CNO ao CNO da construtora. 
Para isso, ele precisa comprovar a sua "fração ideal das áreas de uso comum".
*   **🚀 Diretriz para o GEM:** Nos pareceres de Habite-se de Unidade Autônoma (desmembramento de prédios), o sistema deve discriminar rigorosamente as áreas para viabilizar a CND individual: *"Área Privativa da Unidade: X m² | Área correspondente à Fração Ideal de Uso Comum: Y m² | Área Total a ser Aferida (Unidade): Z m²."* Sem essa soma detalhada, o morador não consegue liberar o seu próprio apartamento na Receita Federal.

---

### 10. Igrejas, Entidades Beneficentes e Mutirões (Isenção Absoluta) - *Item 32.2.1.1*
Se uma Igreja ou Entidade Filantrópica constrói um prédio para *uso próprio* utilizando *mão de obra voluntária* (mutirão), eles NÃO PAGAM nenhum INSS na Receita Federal, desde que mantenham uma lista de colaboradores voluntários.
*   **🚀 Diretriz para o GEM:** Nos Alvarás e Habite-se para instituições sem fins lucrativos, a IA deve registrar a imunidade no projeto: *"Obra executada por Entidade Religiosa/Beneficente para uso próprio. Conforme declaração, a execução deu-se por intermédio de trabalho voluntário não remunerado, amparada pela isenção previdenciária do Item 32.2.1.1 do Manual do SERO."*

---

### 11. Certidão de Retificação Pós-Cartório - *Item 14.2*
Às vezes o munícipe tira a CND com a metragem errada, averba no Cartório, cai na malha fina da Receita e a multa vem astronômica. O SERO permite cancelar e consertar isso retroativamente, mas exige um Alvará Retificador do Município para embasar o "Processo Digital" da Receita.
*   **🚀 Diretriz para o GEM:** Ao emitir uma "Certidão de Retificação de Área", o sistema deve blindar o munícipe redigindo: *"A presente Certidão possui finalidade expressa de instruir Processo Digital junto à Receita Federal para Cancelamento/Retificação de Aferição no SERO (Item 14 do Manual do Contribuinte), atestando o equívoco material da metragem lançada anteriormente."*


# ==========================================
# PARTE 2: GUIA DO CARTÓRIO DE IMÓVEIS
# ==========================================

# 🏛️ GUIA ABSOLUTO: BLINDAGEM CARTORÁRIA DA PREFEITURA
*Base Legal: Lei 6.015/73 (Lei de Registros Públicos), Lei 6.766/79 (Parcelamento do Solo), Provimento 65 do CNJ (Usucapião) e Lei 14.382/2022 (SERP).*

Este documento serve como o núcleo de inteligência para que os documentos municipais (Pareceres, Certidões e Alvarás) não sejam devolvidos pelo Cartório de Registro de Imóveis (CRI) com "nota de exigência", blindando a responsabilidade do analista municipal.

---

### 1. Desmembramentos, Unificações e a "Caducidade de 180 Dias"
* **Base Legal:** Art. 18 da Lei 6.766/1979 e Art. 234 da Lei 6.015/1973.
* **A Regra Cartorária:** Todo projeto de parcelamento do solo (loteamento ou desmembramento) aprovado pela Prefeitura **caduca se não for registrado no Cartório em 180 dias**.
* **Como a IA (GEM) atuará:** Nas Certidões de Desmembramento, Desdobro e Unificação, o parecerista deve OBRIGATORIAMENTE incluir a restrição:
  > *"VALIDADE REGISTRAL: Conforme o Art. 18 da Lei Federal 6.766/79, a presente Certidão de Desmembramento/Aprovação possui validade improrrogável de 180 (cento e oitenta) dias para fins de protocolo junto ao Cartório de Registro de Imóveis. Decorrido o prazo sem a averbação, a presente aprovação municipal caducará automaticamente."*

---

### 2. Retificação de Área (A "Garantia de Não Invasão de Rua")
* **Base Legal:** Art. 212 e Art. 213 da Lei 6.015/1973.
* **A Regra Cartorária:** Se o lote físico for maior que o lote na matrícula do Cartório, o cidadão pede Retificação de Área. O Oficial do Cartório sempre exige anuência dos vizinhos. Sabe quem é o vizinho da frente de todos os lotes? **A Prefeitura (Dona da Rua).** O Cartório exige um documento da Prefeitura jurando que o cidadão não avançou o muro para a calçada (espaço público).
* **Como a IA (GEM) atuará:** Nas Certidões de Retificação de Área ou Anuência de Confrontante, a IA redigirá:
  > *"ANUÊNCIA DE CONFRONTANTE (MUNICÍPIO): Atesta-se, em atenção ao Art. 213, §1º da Lei 6.015/73, que o polígono retificado apresentado respeita rigorosamente o alinhamento predial/viário municipal. O Município atesta não haver sobreposição, esbulho ou invasão do requerente sobre calçadas, logradouros, praças ou áreas de domínio público municipal."*

---

### 3. Usucapião Extrajudicial (Certidões Estratégicas da Prefeitura)
* **Base Legal:** Art. 216-A da Lei 6.015/1973 e Provimento nº 65/2017 do CNJ.
* **A Regra Cartorária:** No Usucapião no Cartório, a prefeitura não atesta que o cidadão é o "dono" do lote, pois o município não é o juiz. A prefeitura atesta apenas a localização, a ausência de interesse e o caráter urbano da via. Se a prefeitura atestar domínio, pode ser processada pelo dono verdadeiro.
* **Como a IA (GEM) atuará:** Na emissão de documentos para Usucapião, a IA deve se blindar com o texto:
  > *"CERTIDÃO DE NATUREZA E ENDEREÇO: Atesta-se que o lote descrito possui natureza urbana e está inserido no sistema viário consolidado do município. Ressalta-se, contudo, que o presente documento possui caráter meramente urbanístico e fiscal (cadastro de IPTU), não valendo, por si só, como atestado de propriedade, domínio ou posse legal, restando resguardado eventual interesse público que recaia sobre a gleba maior originária."*

---

### 4. Demolições e o Fantasma na Matrícula
* **Base Legal:** Princípio da Especialidade Objetiva do Registro de Imóveis.
* **A Regra Cartorária:** A Certidão de Demolição municipal serve para o cidadão parar de pagar IPTU Predial. Mas se ele não a levar ao Cartório, a casa continua "existindo" na matrícula e ele não consegue vender o lote como terreno baldio. Pior: pode bloquear financiamentos na Caixa Econômica.
* **Como a IA (GEM) atuará:** Em Certidões de Demolição, o GEM forçará o aviso na observação do documento:
  > *"AVERBAÇÃO OBRIGATÓRIA: A emissão da presente Certidão encerra a tributação predial na esfera municipal, todavia, não extingue automaticamente a existência da edificação na Matrícula Imobiliária. É dever do requerente protocolar este documento no Registro de Imóveis competente para a devida averbação da demolição."*

---

### 5. Edifícios de Apartamentos / Condomínios (Frações Ideais)
* **Base Legal:** Lei 4.591/64 (Incorporação) e NBR 12.721.
* **A Regra Cartorária:** O Oficial não averba um Habite-se de um prédio se o documento da prefeitura estiver genérico ("Prédio de 4 andares"). O cartório precisa casar o Habite-se com a *Planilha de Fração Ideal* averbada na matrícula originária.
* **Como a IA (GEM) atuará:** Em Habite-se de edifícios multifamiliares ou unidades autônomas, a redação deverá conter a discriminação completa para viabilizar a "Instituição de Condomínio":
  > *"DA CLASSIFICAÇÃO DAS UNIDADES AUTÔNOMAS: O presente Alvará de Habite-se certifica a regularidade da edificação multifamiliar. Para fins de averbação cartorária e posterior instituição de condomínio (Lei 4.591/64), a área global construída divide-se em X unidades habitacionais autônomas, somadas às áreas de uso comum vinculadas e respectivas frações ideais de terreno."*

---

### 6. Desmembramentos Lindeiros a APPs e Cursos d'Água (Atenção Máxima)
* **Base Legal:** Lei Federal 12.651/12 (Código Florestal) c/c Lei de Registros Públicos.
* **A Regra Cartorária:** Cartórios de vanguarda e Corregedorias de Justiça barram desmembramentos e retificações que "apaguem" cursos d'água das plantas topográficas.
* **Como a IA (GEM) atuará:** Se houver rio ou córrego no levantamento topográfico para desmembramento/retificação:
  > *"CONDICIONANTE REGISTRAL - APP: A planta anexa faz parte indissociável da aprovação. Constatada a presença de curso d'água/nascente, o Oficial do Registro de Imóveis e o requerente deverão respeitar a Faixa Non Aedificandi (Área de Preservação Permanente) gravada, sendo vedado o cômputo da APP para fins de regularização edilícia principal."*


# ==========================================
# PARTE 3: GUIA AMBIENTAL E URBANISMO
# ==========================================

# 🌳 GUIA DE BLINDAGEM: URBANISMO E MEIO AMBIENTE
*Base Legal: Lei Municipal 3.971/2023 (APP Urbana), LC 270/2020 (Condomínio de Lotes) e LC 267/2019.*

Este documento compila as estratégias de emissão de pareceres e alvarás focadas na defesa do Município contra responsabilidades indevidas e na proteção do cidadão consolidado contra sanções ambientais retroativas.

---

### 1. O Escudo Ambiental do Habite-se (A Salvação na APP)
* **Base Legal:** Art. 9º, §2º da Lei Municipal 3.971/2023.
* **O Problema:** Casas antigas construídas na beira do rio (APP). Pela regra geral, para regularizar, o cidadão precisa pagar uma "Compensação Ambiental Pecuniária" pesadíssima (multa do CODEMA). Porém, a Lei 3971 abriu uma exceção de ouro: quem tem Alvará ou Habite-se está **isento** dessa multa.
* **A Estratégia para a IA (GEM):** Quando a Prefeitura for emitir um Alvará de Regularização (As-Built) ou Habite-se de uma edificação antiga que tangencia o rio (Área Urbana Consolidada - AUC), o documento da Prefeitura será a salvação do morador contra o Ministério Público e a fiscalização ambiental.
* **Texto Obrigatório da IA:**
  > *"ISENÇÃO DE COMPENSAÇÃO AMBIENTAL: Atesta-se que a presente edificação encontra-se consolidada e passa a ser munida do presente Alvará de Regularização/Habite-se, fazendo jus, portanto, à isenção da medida de compensação ambiental pecuniária, em estrito cumprimento ao disposto no Art. 9º, §2º da Lei Municipal nº 3.971/2023 (Lei de APP Urbana)."*

---

### 2. A "Armadilha" do Condomínio de Lotes vs Loteamento
* **Base Legal:** Art. 3º, §1º da Lei Complementar 270/2020.
* **O Problema:** Loteadores espertos aprovam "Condomínios Fechados de Lotes/Chácaras" (onde vendem a ideia de segurança particular). Anos depois, o asfalto cede e os moradores cobram da Prefeitura a manutenção das ruas e da iluminação. Mas num Condomínio de Lotes, as ruas são **particulares** (propriedade dos condôminos), e a Prefeitura é proibida por lei de gastar dinheiro público ali.
* **A Estratégia para a IA (GEM):** A aprovação municipal deve "carimbar" na testa do loteador e na matrícula do cartório que a rua não é da Prefeitura, matando a chance de qualquer ação judicial futura dos moradores contra o Município.
* **Texto Obrigatório da IA nas Aprovações de Condomínio de Lotes:**
  > *"ADVERTÊNCIA DE INFRAESTRUTURA: Em obediência ao Art. 3º, §1º da LC Municipal 270/2020, fica expressamente declarado que as vias de circulação, infraestrutura e áreas de uso comum constituem propriedade exclusiva dos condôminos adquirentes. É terminantemente vedado o repasse de tais áreas ao Poder Público, sendo de responsabilidade integral do Condomínio a manutenção do asfalto, drenagem, coleta de lixo interna e congêneres."*

---

### 3. A Regra do Muro nas Zonas Ambientais
* **Base Legal:** LC 270/2020 (Art. 6º, XI).
* **A Regra:** Condomínios de chácaras não podem construir muros dividindo os lotes internamente (apenas cercas). O muro só é permitido na confrontação externa (muro do condomínio). Se a Prefeitura aprovar um projeto com muros de arrimo gigantes dividindo chácaras internamente, estará violando o princípio ambiental do fluxo da fauna e da permeabilidade do condomínio rural/urbano.
* **Ação do GEM:** Barrar e emitir pendência sempre que identificar projetos de chácaras ou condomínios de lotes com "muros de alvenaria de divisa interna", exigindo a troca por "cerca viva ou de arame".

---

### 4. Reformas em APP (A Liberação Legal)
* **Base Legal:** Art. 11 da Lei 3.971/2023.
* **A Regra:** Moradores que têm casas dentro da APP (à beira do rio) acham que nunca mais poderão arrumar a casa. A lei permite reforma, divisão de quartos, troca de telhado e até criação de mezaninos, **desde que não amplie o tamanho da casa para fora (limites externos)**.
* **A Estratégia para a IA:** Ao emitir um "Alvará de Reforma em AUC/APP", justificar a legalidade do ato para evitar denúncias ambientais infundadas.
* **Texto Obrigatório da IA:**
  > *"DA LEGALIDADE AMBIENTAL DA REFORMA: A presente licença autoriza as modificações construtivas internas e de fachada, atestando que não há ampliação da projeção dos limites externos da edificação, estando o ato administrativo amparado pelo Art. 11 da Lei Municipal 3.971/2023, sendo permitida a manutenção da edificação consolidada em APP Urbana."*


