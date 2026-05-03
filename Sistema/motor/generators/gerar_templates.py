"""
Script auxiliar para gerar todos os templates JSON.
Execute uma vez: python _gerar_templates.py
"""
import json, os

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

def salvar(nome, dados):
    caminho = os.path.join(TEMPLATES_DIR, f"{nome}.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"  [+] {nome}.json")

# ═══════════════════════════════════════════════════════════
#  ESQUEMA BASE
# ═══════════════════════════════════════════════════════════
salvar("_esquema_base", {
    "_descricao": "Esquema mestre — todos os campos possíveis e seus tipos",
    "campos_comuns": {
        "tipo_relatorio":       "string — ID do tipo (ver lista abaixo)",
        "numero_processo":       "string — ex: '6100'",
        "data_processo":         "string — ex: '15 de julho de 2025'",
        "assunto":               "string — descrição do assunto",
        "requerente":            "string — nome completo",
    },
    "campos_carimbo_tecnico": {
        "logradouro":            "string — endereço completo",
        "bairro":                "string",
        "inscricao_municipal":   "string — ex: '01.01.048.0038.001'",
        "proprietario":          "string — (usa requerente se omitido)",
        "desenhista":            "string",
        "lote":                  "string",
        "quadra":                "string",
        "area_terreno":          "string — ex: '180,00m²'",
        "area_total_construida": "string — ex: '154,08m²'",
        "taxa_ocupacao":         "string — ex: '86,23%'",
        "coef_aproveitamento":   "string — ex: '0,85'",
        "taxa_permeabilidade":   "string — ex: '5,95%'",
        "profissional_nome":     "string — nome do responsável técnico",
    },
    "campos_corpo": {
        "paragrafo_abertura":    "string — texto de abertura (suporta **negrito** e __itálico__)",
        "considerandos":         "array de strings — cada item é um considerando",
        "paragrafos_adicionais": "array de strings — parágrafos extras",
        "fundamentacao_legal":   "array de strings — itens de fundamentação",
        "conclusao":             "string — texto de conclusão",
    },
    "campos_documentos": {
        "documentos_emitir": [
            {"tipo": "string — título do documento", "obs": "string — observação (opcional)"}
        ]
    },
    "campos_oficio": {
        "destinatario_titulo":   "string — título do ofício (ex: 'OFÍCIO À SECRETARIA DE MEIO AMBIENTE')",
        "destinatario_para":     "string — destinatário",
        "destinatario_de":       "string — remetente",
    },
    "campos_assinatura": {
        "assinante": {
            "nome":     "string — default: 'Diego Tarcísio Nunes Vilela'",
            "titulo":   "string — default: 'Engenheiro Civil'",
            "registro": "string — default: 'CREA 235.474/D'",
        },
        "cidade": "string — default: 'Oliveira'",
    },
    "tipos_disponiveis": [
        "alvara_aprovacao", "alvara_regularizacao", "alvara_ampliacao",
        "alvara_galpao_comercial", "alvara_reforma_demolicao_ampliacao",
        "alvara_substituicao_projeto", "alvara_renovacao", "alvara_cancelamento",
        "alvara_substituicao_titular", "alvara_demolicao",
        "certidao_numero_2via", "certidao_nome_rua", "certidao_localizacao",
        "certidao_conjunta", "certidao_numero_comercial",
        "certidao_averbacao_decadencia", "certidao_desmembramento",
        "certidao_demolicao", "certidao_retificacao_area",
        "habitese_comum", "habitese_multa", "habitese_2via", "habitese_inclusao_area",
        "oficio_meio_ambiente", "parecer_juridico", "oficio_juridico_embargo",
        "oficio_interno_materiais", "oficio_decreto_utilidade",
        "comunicado_indeferimento",
    ]
})

# ═══════════════════════════════════════════════════════════
#  PARECERES TÉCNICOS (COM DADOS DO CARIMBO)
# ═══════════════════════════════════════════════════════════

salvar("alvara_aprovacao", {
    "tipo_relatorio": "alvara_aprovacao",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_tecnico",
    "descricao": "Aprovação de projeto residencial ou popular — emissão de alvará de construção e certidão de número",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "assunto", "requerente",
        "logradouro", "bairro", "area_terreno", "area_total_construida",
        "taxa_ocupacao", "taxa_permeabilidade", "coef_aproveitamento",
        "profissional_nome", "considerandos", "documentos_emitir"
    ],
    "campos_opcionais": [
        "inscricao_municipal", "proprietario", "desenhista", "lote", "quadra",
        "zoneamento", "paragrafos_adicionais", "fundamentacao_legal"
    ],
    "modelo_abertura": "A Secretaria Municipal de Obras e Serviços Urbanos, através do Departamento Técnico, em face deste Processo Administrativo, onde o requerente solicita a aprovação de projeto residencial unifamiliar [inserir 'popular' se aplicável] de [Área] m², em terreno localizado no Lote [X], Quadra [Y], no Zoneamento [ZURX], em Categoria de uso [UR1], com área total de [Área Lote] m², taxa de ocupação de [X]%, taxa de permeabilidade de [Y]% e coeficiente de aproveitamento de [Z], localizado na [Endereço Completo].",
    "modelo_considerandos": [
        "De acordo com o Parecer Fiscal emitido, a construção ainda não foi iniciada, sendo retirado o nº [Número da Porta]. O proprietário apresentou título de propriedade (Matrícula nº [Número] e Inscrição Cadastral [Número]). Para o projeto, foi emitida a ART/RRT nº [Número] pelo [Título e Nome do Profissional], CREA/CAU nº [Número]."
    ],
    "modelo_conclusao": "Diante disto, verificado e aprovado o projeto, poderá ser emitido:",
    "documentos_tipicos": [
        {"tipo": "Alvará de Construção de [Tipo de Edificação] de [Área] m², válido por 01 ano.", "obs": "colocar no campo de observação: [notas do projeto]"},
        {"tipo": "Certidão de Número."}
    ],
    "legislacao_aplicavel": [
        "Decreto nº 4.149/2019",
        "Lei nº 1.544/86 (Código de Obras)",
        "Lei nº 267/2019 (Uso e Ocupação do Solo)"
    ]
})

salvar("alvara_regularizacao", {
    "tipo_relatorio": "alvara_regularizacao",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_tecnico",
    "descricao": "Regularização de imóvel (As Built) — alvará de regularização, habite-se, certidão de averbação e decadência",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "assunto", "requerente",
        "logradouro", "bairro", "area_terreno", "area_total_construida",
        "taxa_ocupacao", "taxa_permeabilidade", "coef_aproveitamento",
        "profissional_nome", "considerandos", "fundamentacao_legal",
        "documentos_emitir"
    ],
    "campos_opcionais": [
        "inscricao_municipal", "proprietario", "desenhista", "lote", "quadra",
        "zoneamento", "paragrafos_adicionais"
    ],
    "modelo_abertura": "A Secretaria Municipal de Obras e Serviços Urbanos, no uso de suas atribuições legais, **emite o presente parecer técnico** conforme segue:",
    "modelo_considerandos": [
        "a requerente é proprietária do imóvel registrado sob **Matrícula nº [Número]** do SRI, com área de terreno de **[Área]m²**, situado na [Endereço], Oliveira/MG;",
        "o parecer fiscal emitido pelos Agentes [Nomes e Matrículas] atesta que a área construída total de **[Área]m²** confere com o Projeto As Built apresentado;",
        "para o projeto foi emitida a ART/RRT/TRT **nº [Número]** pelo [Profissão] **[Nome]**, CREA/CAU/CFT [Número];"
    ],
    "modelo_conclusao": "Diante do exposto, aprovado e verificado o projeto as built, constar:",
    "documentos_tipicos": [
        {"tipo": "Alvará de Regularização de Imóvel de [Área] m²", "obs": "Alvará emitido para regularização de imóvel edificado sem projeto aprovado na prefeitura mediante o cumprimento do Art. 79 da Lei 1544/1986 e Arts. 38/39 da Lei 267/2019"},
        {"tipo": "Carta de Habite-se referente à área total de [Área] m²"},
        {"tipo": "Certidão de Averbação referente à área total de [Área] m²"},
        {"tipo": "Certidão de Decadência — [Área] m²", "obs": "Se aplicável, conforme Art. 150, §4º do CTN"}
    ],
    "legislacao_aplicavel": [
        "Art. 150, §4º do CTN (Decadência)",
        "Art. 79 da Lei nº 1.544/86 (Construir sem licença)",
        "Arts. 38 e 39 da Lei nº 267/2019 (Parâmetros urbanísticos)",
        "Art. 43 da Lei nº 1.544/86 (Abertura na divisa)",
        "Art. 15 da Lei nº 267/2019 (Exceção terreno < 220m²)"
    ]
})

salvar("regularizacao", {
    "tipo_relatorio": "regularizacao",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_tecnico",
    "descricao": "Alias para alvara_regularizacao — mantido para compatibilidade com JSONs anteriores",
    "alias_de": "alvara_regularizacao"
})

salvar("alvara_ampliacao", {
    "tipo_relatorio": "alvara_ampliacao",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_tecnico",
    "descricao": "Ampliação de edificação existente (sem demolição)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "assunto", "requerente",
        "logradouro", "bairro", "area_terreno", "area_total_construida",
        "taxa_ocupacao", "taxa_permeabilidade", "coef_aproveitamento",
        "profissional_nome", "considerandos", "documentos_emitir"
    ],
    "modelo_abertura": "A Secretaria Municipal de Obras e Serviços Urbanos, através do Departamento Técnico, em face deste Processo Administrativo, onde o requerente solicita a ampliação de edificação residencial unifamiliar com área total de [Área Total] m² (sendo [Área Existente] m² já existente e [Área da Ampliação] m² que será construída), em terreno localizado no Zoneamento [ZUR...], em Categoria de uso [UR...], com área total de [Área Terreno] m², taxa de ocupação de [X]%, taxa de permeabilidade de [Y]% e coeficiente de aproveitamento de [Z], localizado na [Endereço Completo].",
    "modelo_conclusao": "Diante disto, verificado e aprovado o projecto, poderá ser emitido:",
    "documentos_tipicos": [
        {"tipo": "Alvará de Ampliação de edificação residencial unifamiliar de [Área da Ampliação] m², válido por 01 ano."}
    ]
})

salvar("alvara_galpao_comercial", {
    "tipo_relatorio": "alvara_galpao_comercial",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_tecnico",
    "descricao": "Aprovação de projeto de galpão comercial (uso misto/serviços)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "assunto", "requerente",
        "logradouro", "bairro", "area_terreno", "area_total_construida",
        "taxa_ocupacao", "taxa_permeabilidade", "coef_aproveitamento",
        "profissional_nome", "considerandos", "documentos_emitir"
    ],
    "modelo_abertura": "A Secretaria Municipal de Obras e Serviços Urbanos, através do Departamento Técnico, em face deste Processo Administrativo, no qual o requerente solicita a aprovação de projeto de galpão comercial com área construída de [Área] m², em terreno localizado no zoneamento [ZAE...], quadra [X], lote [Y], categoria de uso [UMCS], com área total de [Área] m², taxa de ocupação de [X]%, taxa de permeabilidade de [Y]% e coeficiente de aproveitamento de [Z], localizado na [Endereço Completo].",
    "modelo_conclusao": "Diante disto, concluída a análise técnica e atestada a conformidade do projeto com as normas vigentes, este poderá ser aprovado. Emitir:",
    "documentos_tipicos": [
        {"tipo": "Alvará de Construção de galpão comercial de [Área] m², válido por 01 ano.", "obs": "Colocar no campo de observação: Aprovação de construção de galpão de uso misto comercial e de serviços."}
    ]
})

salvar("alvara_reforma_demolicao_ampliacao", {
    "tipo_relatorio": "alvara_reforma_demolicao_ampliacao",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_tecnico",
    "descricao": "Reforma, demolição e ampliação no mesmo processo",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "assunto", "requerente",
        "logradouro", "bairro", "area_terreno", "area_total_construida",
        "taxa_ocupacao", "taxa_permeabilidade", "coef_aproveitamento",
        "profissional_nome", "considerandos", "documentos_emitir"
    ],
    "modelo_abertura": "(...) onde o requerente solicita a reforma, demolição e ampliação de edificação residencial unifamiliar de [Área Total Final] m² (sendo [Área Averbada] m² de área já existente averbada, da qual ocorrerá a demolição de [Área a Demolir] m², acrescida de [Área Nova] m² de área de ampliação nova), em terreno localizado no Zoneamento [...]",
    "modelo_conclusao": "Diante disto, verificado e aprovado o projecto, poderá ser emitido:",
    "documentos_tipicos": [
        {"tipo": "Alvará de Reforma, Demolição e Ampliação de edificação residencial unifamiliar para área total final de [Área Final] m²", "obs": "Constar observação das metragens demolidas e acrescidas"}
    ]
})

salvar("alvara_substituicao_projeto", {
    "tipo_relatorio": "alvara_substituicao_projeto",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_tecnico",
    "descricao": "Substituição de projeto (alteração de layout ou área)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "assunto", "requerente",
        "logradouro", "bairro", "area_terreno", "area_total_construida",
        "taxa_ocupacao", "taxa_permeabilidade", "coef_aproveitamento",
        "profissional_nome", "considerandos", "documentos_emitir"
    ],
    "modelo_abertura": "(...) onde o requerente solicita a substituição de projecto residencial unifamiliar de [Nova Área] m², em terreno localizado no Zoneamento [...]. De acordo com o Parecer Fiscal, a construção foi iniciada e confere com o novo projecto apresentado.",
    "modelo_conclusao": "Diante disso, após analisado e aprovado o projecto apresentado, poderá ser emitido:",
    "documentos_tipicos": [
        {"tipo": "Alvará de Construção (Substituição) de [Área] m² válido por 01 ano.", "obs": "Colocar no campo de observações: Alvará emitido por substituição de projecto com modificação da área construída/layout do alvará de construção nº [Número Antigo] emitido em [Data]."}
    ]
})

# ═══════════════════════════════════════════════════════════
#  PARECERES SIMPLES (SEM DADOS DO CARIMBO)
# ═══════════════════════════════════════════════════════════

salvar("certidao_numero_2via", {
    "tipo_relatorio": "certidao_numero_2via",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_simples",
    "descricao": "2ª via de Certidão de Número (para SAAE/CEMIG)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "campos_opcionais": ["documentos_emitir"],
    "assunto_padrao": "2ª via Certidão de Número",
    "modelo_considerandos": [
        "a solicitação do requerente.",
        "o parecer fiscal no qual se entende que a construção na [Endereço Completo], Bairro [Bairro] está [iniciada/em andamento].",
        "a requerente apresentou matrícula do SRI em seu próprio nome sob matrícula nº [Número] e inscrição cadastral [Número].",
        "o alvará de construção de nº [Número], com vencimento na data de [Data]."
    ],
    "modelo_conclusao": "Diante disto, poderá ser concedida a 2ª via de certidão de número para SAAE e CEMIG em nome do requerente."
})

salvar("certidao_nome_rua", {
    "tipo_relatorio": "certidao_nome_rua",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Certidão de Nome de Rua (denominação oficial)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Certidão de Nome de Rua",
    "modelo_considerandos": [
        "a solicitação do requerente.",
        "o parecer fiscal que constata, após levantamento nos arquivos da prefeitura, que a antiga Rua [Número/Nome Antigo], localizada no Bairro [Bairro], passou a denominar-se oficialmente Rua [Novo Nome], conforme Decreto nº [Número], de [Data].",
        "o requerente apresentou título de propriedade do terreno (Matrícula nº [Número] e Inscrição Cadastral [Número])."
    ],
    "modelo_conclusao": "Diante disto, poderá ser emitida Certidão de Nome de Rua constando observação: \"Conforme Decreto nº [Número] de [Data], a antiga Rua [Nome Antigo] denomina-se hoje Rua [Novo Nome]\"."
})

salvar("certidao_localizacao", {
    "tipo_relatorio": "certidao_localizacao",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Certidão de Localização (imóvel com duas frentes ou outra situação)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Certidão de Localização",
    "modelo_considerandos": [
        "a solicitação da requerente.",
        "o parecer fiscal, que certifica que o imóvel com Inscrição Imobiliária [Número], localizado na [Rua Principal], nº [Número], Centro, também possui fundos/frente para a [Rua Secundária], nº [Número], Bairro [Bairro].",
        "a requerente apresentou título de propriedade do imóvel em seu nome (Matrícula n° [Número])."
    ],
    "modelo_conclusao": "Diante disto, poderá ser emitida a Certidão de Localização, constando observação que o imóvel possui frentes para ambas as vias mencionadas, para fins de regularização registral."
})

salvar("certidao_conjunta", {
    "tipo_relatorio": "certidao_conjunta",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Certidão Conjunta (Localização + Nome de Rua)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Certidão de Localização e Certidão de Nome de Rua",
    "modelo_considerandos": [
        "a solicitação do requerente.",
        "o Parecer Fiscal emitido em [Data], que atesta que o imóvel cadastrado sob a Inscrição Imobiliária [Número] está fisicamente localizado na antiga \"Rua [Nome Antigo]\".",
        "a referida \"Rua [Nome Antigo]\" denomina-se hoje Rua [Novo Nome], conforme Decreto Municipal nº [Número] de [Data]."
    ],
    "modelo_conclusao": "Diante disto, poderá ser emitida a Certidão de Localização e Nome de Rua com a devida ressalva de atualização de denominação."
})

salvar("certidao_numero_comercial", {
    "tipo_relatorio": "certidao_numero_comercial",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Certidão de Número para fins comerciais (desmembramento de numeração)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Certidão de número para fins comerciais",
    "modelo_considerandos": [
        "o parecer fiscal onde foi retirado o nº [Novo Número] para fins comerciais, para uma área de [Área Comercial] m², sendo esta parte de uma edificação residencial já existente de número [Número Antigo] com [Área Total] m².",
        "o imóvel possui habite-se nº [Número] referente à área total.",
        "o título de propriedade (Escritura Pública/Matrícula nº [Número])."
    ],
    "modelo_conclusao": "Diante disto, poderá ser concedida a Certidão de Número [Novo Número] para fins comerciais, referente à área de [Área] m²."
})

salvar("habitese_comum", {
    "tipo_relatorio": "habitese_comum",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Habite-se e Averbação (processo comum — obra licenciada concluída)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Carta de Habite-se e Certidão de Averbação",
    "modelo_considerandos": [
        "a solicitação do requerente.",
        "o parecer fiscal, que certifica que a obra licenciada pelo Alvará de Construção nº [Número do Alvará]/[Ano], com área liberada de [Área] m², válido até [Data], referente ao projeto aprovado no processo [Número]/[Ano], localizada na [Endereço Completo], Bairro [Bairro], em Oliveira/MG, foi concluída e está Habitável.",
        "o requerente apresentou título de propriedade do terreno, sendo uma Certidão de Matrícula SRI de Inteiro Teor de imóvel em seu nome, registrado sob n° [Número da Matrícula], inscrição cadastral [Número]."
    ],
    "modelo_conclusao": "Diante disso, poderá ser emitida Carta de Habite-se referente à área total do alvará, contendo [Área] m², e a respectiva Certidão de Averbação.",
    "documentos_tipicos": [
        {"tipo": "Carta de Habite-se referente à área total de [Área] m²"},
        {"tipo": "Certidão de Averbação"}
    ]
})

salvar("habitese_multa", {
    "tipo_relatorio": "habitese_multa",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Habite-se com aplicação de multa (quebra de parâmetro/permeabilidade)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Carta de Habite-se e Certidão de Averbação",
    "modelo_considerandos": [
        "a solicitação do requerente.",
        "o parecer fiscal, que certifica que a obra licenciada pelo Alvará de Construção nº [Número]/[Ano], localizada na [Endereço], foi concluída e está Habitável. Contudo, foi identificado que não foi respeitada a área permeável total aprovada em projeto.",
        "o requerente efetuou o pagamento da multa referente à área permeável não respeitada e detetada pelo fiscal.",
        "o título de propriedade do terreno (Matrícula n° [Número] e inscrição cadastral [Número])."
    ],
    "modelo_conclusao": "Diante disso, poderá ser emitida a Carta de Habite-se referente à área total do alvará contendo [Área] m² e a Certidão de Averbação.",
    "notas": "Adicionar observação na averbação, se aplicável, sobre a infração regularizada via multa."
})

salvar("certidao_averbacao_decadencia", {
    "tipo_relatorio": "certidao_averbacao_decadencia",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Certidão de Averbação e Decadência (sem alteração na área total)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Certidão de Averbação e Decadência",
    "modelo_considerandos": [
        "a solicitação do requerente.",
        "o parecer fiscal, entende-se que não houve alteração na área total da construção com [Área] m², que confere com a área do Habite-se nº [Número]/[Ano] anterior.",
        "o requerente apresentou título de propriedade (Matrícula nº [Número] e inscrição cadastral [Número]).",
        "a edificação possui carta de Habite-se desde [Data de Emissão original], comprovando assim a decadência total da área."
    ],
    "modelo_conclusao": "Diante disso, poderá ser emitida a Certidão de Averbação e Decadência referente à área total da construção."
})

salvar("habitese_2via", {
    "tipo_relatorio": "habitese_2via",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Segunda Via de Carta de Habite-se e Averbação",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Segunda Via de Habite-se e Certidão de Averbação",
    "modelo_considerandos": [
        "a solicitação do requerente.",
        "o parecer fiscal, que certifica que a obra liberada pelo Habite-se original nº [Número]/[Ano], com área liberada de [Área] m², localizada na [Endereço], segue sem alteração desde a emissão do seu Habite-se original.",
        "o requerente apresentou título de propriedade do terreno (Matrícula SRI de Inteiro Teor nº [Número] e Inscrição Cadastral [Número])."
    ],
    "modelo_conclusao": "Diante disso, poderá ser emitida a Segunda Via da Carta de Habite-se nº [Número Antigo] e a respectiva Certidão de Averbação."
})

salvar("habitese_inclusao_area", {
    "tipo_relatorio": "habitese_inclusao_area",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Habite-se com inclusão de área irregular (baixa de alvará antigo)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Carta de Habite-se (Inclusão de Área)",
    "modelo_considerandos": [
        "a solicitação do requerente e o parecer fiscal que certifica que a obra licenciada pelo Alvará nº [Número Antigo] foi concluída e está habitável. Porém, foi identificada uma inclusão de área de [Área Extra] m² edificada sem licença, resultando numa área total de [Área Total] m².",
        "o requerente apresentou comprovante de pagamento de multa por execução de obra sem autorização da Prefeitura."
    ],
    "modelo_conclusao": "Diante disso, deverá ser dada a baixa no alvará [Número Antigo] e emitido um Novo Alvará de Regularização referente à área de [Área Total] m² com a observação: (Alvará anterior baixado devido à inclusão de área edificada sem licença, regularizada mediante o cumprimento da legislação vigente). Posteriormente, poderá ser emitida a respectiva Carta de Habite-se."
})

salvar("alvara_renovacao", {
    "tipo_relatorio": "alvara_renovacao",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Renovação (prorrogação) de alvará de construção por 180 dias",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Renovação de Alvará de Construção",
    "modelo_considerandos": [
        "a solicitação do requerente.",
        "o parecer fiscal, que certifica que a obra licenciada pelo Alvará de Construção nº [Número]/[Ano], com área liberada de [Área] m², não foi concluída, encontrando-se em fase de execução no imóvel localizado na [Endereço]."
    ],
    "modelo_conclusao": "Diante disto, poderá ser expedida a renovação do Alvará de Construção por 180 dias, conforme lei 1544 de 04/03/86. Constar no campo de observação: \"Alvará prorrogado por 180 dias, com data de validade a contar do deferimento\"."
})

salvar("alvara_cancelamento", {
    "tipo_relatorio": "alvara_cancelamento",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Cancelamento de alvará de construção (obra não iniciada)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Cancelamento de Alvará de Construção",
    "modelo_considerandos": [
        "a solicitação de cancelamento referente ao Alvará de Construção nº [Número]/[Ano], com área de [Área] m².",
        "o requerente não iniciou as obras, conforme atestado no parecer fiscal."
    ],
    "modelo_conclusao": "Diante disto, poderá ser efetuado o cancelamento do Alvará de Construção no sistema SISOBRAS, bem como emitir separadamente uma Certidão de Cancelamento do Alvará e um comunicado de cancelamento de CEI junto à RFB, justificado pela não execução da obra."
})

salvar("alvara_substituicao_titular", {
    "tipo_relatorio": "alvara_substituicao_titular",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Substituição de titularidade de alvará de construção",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Substituição de Titularidade de Alvará",
    "modelo_considerandos": [
        "o parecer fiscal que certifica a existência de obra licenciada pelo alvará de construção nº [Número anterior] em nome do antigo proprietário [Nome do Antigo], não concluída (em andamento).",
        "o atual requerente apresentou [Tipo de Documento: ex. Cessão de Direitos / Compra e Venda] averbado/comprovado."
    ],
    "modelo_conclusao": "Diante disto, poderá ser expedido novo Alvará de Construção onde deverá constar a observação: \"Alvará emitido por troca de titularidade em substituição ao alvará nº [Número] em nome de [Nome Antigo]\". Emitir comunicado de cancelamento da CEI do antigo proprietário para ciência do mesmo."
})

salvar("alvara_demolicao", {
    "tipo_relatorio": "alvara_demolicao",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Alvará de demolição",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Alvará de Demolição",
    "modelo_considerandos": [
        "a solicitação de alvará de demolição.",
        "não há óbice à autorização da demolição pretendida e que a mesma ainda não foi iniciada, de acordo com o parecer fiscal.",
        "o título de propriedade (Matrícula nº [Número]) e a apresentação da ART/RRT nº [Número] referente à atividade de execução de demolição para a área de [Área] m², sob a responsabilidade de [Nome do Profissional]."
    ],
    "modelo_conclusao": "Diante disto, poderá ser concedido o Alvará de Obra de Demolição referente à área de [Área] m², condicionado à apresentação do comprovante de pagamento da respectiva taxa."
})

salvar("certidao_demolicao", {
    "tipo_relatorio": "certidao_demolicao",
    "titulo_documento": "PARECER SETOR TÉCNICO - SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Certidão de conclusão de demolição",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Certidão de Demolição",
    "modelo_considerandos": [
        "a solicitação do requerente.",
        "o parecer fiscal, onde certifica que a demolição foi concluída no imóvel (Matrícula nº [Número]).",
        "a edificação demolida possui o Alvará de Demolição nº [Número]/[Ano] referente a [Área] m²."
    ],
    "modelo_conclusao": "Diante disto, poderá ser concedida a Certidão de Demolição referente à área total do alvará supracitado."
})

salvar("certidao_desmembramento", {
    "tipo_relatorio": "certidao_desmembramento",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Certidão de Desmembramento / Divisão de terreno",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Certidão de Desmembramento",
    "modelo_abertura": "Poderá ser aprovado o [desmembramento / divisão] de [X] áreas (Área 01 com [Área] m², Área 02 com [Área] m²...), ficando uma área remanescente com [Área] m² (se aplicável), conforme os projetos e memoriais descritivos apresentados. O terreno encontra-se registado sob a Matrícula nº [Número] do SRI, composto por um lote inicial de [Área Total] m², com inscrição imobiliária [Número], localizado na [Endereço Completo].",
    "modelo_considerandos": [
        "O processo decorre sob a responsabilidade do(a) [Engenheiro(a) / Técnico(a)], CREA/CAU/CFT nº [Número], que emitiu a ART/RRT/TRT nº [Número]."
    ]
})

salvar("certidao_retificacao_area", {
    "tipo_relatorio": "certidao_retificacao_area",
    "titulo_documento": "PARECER SETOR TÉCNICO – SMOSU",
    "categoria": "parecer_simples",
    "descricao": "Parecer para retificação de área (geralmente para o Registro Predial)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Certidão de Retificação de Área",
    "modelo_abertura": "Verificando o processo de retificação de área formulado pelo requerente para o terreno urbano localizado na [Endereço Completo], lote [X], quadra [Y], no município de Oliveira/MG, no qual o Serviço Registral de Imóveis solicitou desta Prefeitura que se manifestasse quanto às confrontações e alinhamento do imóvel.",
    "modelo_considerandos": [
        "foi constatado que a retificação NÃO FERE os interesses do Município."
    ],
    "modelo_conclusao": "Salientamos que foi avaliada por esta secretaria apenas a situação do alinhamento do imóvel que confronta com a frente da via de domínio público, não sendo avaliado o contexto geral do projeto ou litígios entre confrontantes particulares.",
    "notas": "Este parecer é direcionado ao SRI (Serviço Registral de Imóveis)."
})

# ═══════════════════════════════════════════════════════════
#  OFÍCIOS
# ═══════════════════════════════════════════════════════════

salvar("oficio_meio_ambiente", {
    "tipo_relatorio": "oficio_meio_ambiente",
    "titulo_documento": "OFÍCIO À SECRETARIA DE MEIO AMBIENTE",
    "categoria": "oficio",
    "descricao": "Ofício de encaminhamento ao Meio Ambiente (CODEMA) para avaliação ambiental",
    "campos_obrigatorios": [
        "numero_processo", "requerente", "destinatario_para",
        "destinatario_de", "assunto", "considerandos"
    ],
    "modelo_destinatario": {
        "destinatario_titulo": "OFÍCIO À SECRETARIA DE MEIO AMBIENTE",
        "destinatario_para": "Secretário(a) de Meio Ambiente / CODEMA",
        "destinatario_de": "Setor Técnico - SMOSU"
    },
    "modelo_abertura": "Solicitamos a avaliação da Vossa secretaria para dar andamento ao pedido de alvará de construção de [Nome do Requerente] (Processo nº [Número]/[Ano]). O projeto prevê uma obra próxima a um [córrego / área de preservação]. Precisamos garantir que a nova construção não invada ou prejudique esta área.",
    "modelo_considerandos": [
        "Para facilitar a análise, enviamos em anexo a cópia do projeto, a planta de situação e a matrícula do imóvel. Agradecemos a atenção e aguardamos o retorno para darmos sequência ao processo."
    ]
})

salvar("parecer_juridico", {
    "tipo_relatorio": "parecer_juridico",
    "titulo_documento": "PARECER TÉCNICO – SMOSU",
    "categoria": "oficio",
    "descricao": "Parecer para o Setor Jurídico (usucapião, retificação, etc.)",
    "campos_obrigatorios": [
        "numero_processo", "requerente", "destinatario_para",
        "assunto", "considerandos"
    ],
    "modelo_destinatario": {
        "destinatario_titulo": "AO SETOR JURÍDICO",
        "destinatario_para": "Setor Jurídico",
        "destinatario_de": "Setor Técnico - SMOSU"
    },
    "modelo_abertura": "Em resposta ao memorando nº [Número]/[Ano], a Secretaria Municipal de Obras e Serviços Urbanos (SMOSU), por meio de seu Departamento Técnico, vem prestar esclarecimentos acerca do processo supracitado.",
    "modelo_considerandos": [
        "Após a análise do levantamento planimétrico, do memorial descritivo e da ART/RRT nº [Número], elaborados por [Nome do Profissional], constatou-se que a área em questão, localizada em [Endereço], com [Área] m², NÃO FERE os interesses do Município, não apresentando qualquer inconveniência ou interferência nas áreas e patrimônios públicos municipais."
    ]
})

salvar("oficio_juridico_embargo", {
    "tipo_relatorio": "oficio_juridico_embargo",
    "titulo_documento": "OFÍCIO PARA SETOR JURÍDICO",
    "categoria": "oficio",
    "descricao": "Ofício ao Jurídico para denúncia de obra irregular / embargo",
    "campos_obrigatorios": [
        "numero_processo", "requerente", "destinatario_para",
        "assunto", "considerandos"
    ],
    "modelo_destinatario": {
        "destinatario_titulo": "OFÍCIO PARA SETOR JURÍDICO",
        "destinatario_para": "Procuradoria Jurídica do Município",
        "destinatario_de": "Setor Técnico - SMOSU"
    },
    "modelo_abertura": "Ao cumprimentá-lo(a) cordialmente, sirvo-me do presente para encaminhar a Vossa Senhoria os autos do Processo Administrativo em epígrafe, para análise e adoção das medidas judiciais cabíveis, em face do proprietário do imóvel localizado na [Endereço da Obra Irregular].",
    "modelo_considerandos": [
        "DOS FATOS CONSTATADOS: O referido processo foi instaurado a partir de denúncia relatando a execução de obra irregular [descrição]. Em diligência in loco, a equipe de Fiscalização de Obras atestou as infrações ao Código de Obras do Município.",
        "DOS REQUERIMENTOS: Considerando o esgotamento das vias administrativas e a resistência do autuado à regularização, solicitamos a exigência judicial para regularização completa da edificação."
    ]
})

salvar("oficio_interno_materiais", {
    "tipo_relatorio": "oficio_interno_materiais",
    "titulo_documento": "OFÍCIO AO GABINETE",
    "categoria": "oficio",
    "descricao": "Ofício interno para requisição de materiais de expediente",
    "campos_obrigatorios": [
        "destinatario_para", "assunto", "considerandos"
    ],
    "modelo_destinatario": {
        "destinatario_titulo": "OFÍCIO AO GABINETE",
        "destinatario_para": "[Nome do Chefe de Gabinete/Secretário]",
        "destinatario_de": "Setor Técnico - SMOSU"
    },
    "modelo_abertura": "Cumprimentando-o cordialmente, venho por meio deste solicitar a aquisição dos materiais de expediente relacionados abaixo. A aquisição destes itens faz-se necessária para a reposição de estoque e manutenção das atividades administrativas diárias desta Secretaria.",
    "notas": "Incluir no JSON a lista de itens nos considerandos."
})

salvar("oficio_decreto_utilidade", {
    "tipo_relatorio": "oficio_decreto_utilidade",
    "titulo_documento": "OFÍCIO À PROCURADORIA DO MUNICÍPIO",
    "categoria": "oficio",
    "descricao": "Solicitação de Decreto de Utilidade Pública (Sistema Viário)",
    "campos_obrigatorios": [
        "destinatario_para", "assunto", "considerandos"
    ],
    "modelo_destinatario": {
        "destinatario_titulo": "À PROCURADORIA DO MUNICÍPIO",
        "destinatario_para": "Procuradoria do Município",
        "destinatario_de": "Setor Técnico - SMOSU"
    },
    "modelo_abertura": "Cumprimentando-os cordialmente, venho solicitar a análise técnica e a adoção das providências necessárias para a elaboração de um decreto que reconheça como de domínio e utilidade pública a área localizada em [Bairro/Endereço].",
    "modelo_considerandos": [
        "A solicitação fundamenta-se na necessidade de implementação de melhorias urbanas na referida localidade e na adequada articulação do sistema viário municipal existente, conforme a Lei Municipal nº 216/2014."
    ]
})

# ═══════════════════════════════════════════════════════════
#  COMUNICADOS
# ═══════════════════════════════════════════════════════════

salvar("comunicado_indeferimento", {
    "tipo_relatorio": "comunicado_indeferimento",
    "titulo_documento": "COMUNICADO",
    "categoria": "comunicado",
    "descricao": "Comunicado de indeferimento (Ação Civil Pública — alvará caduco)",
    "campos_obrigatorios": [
        "numero_processo", "data_processo", "requerente", "considerandos"
    ],
    "assunto_padrao": "Indeferimento de Renovação de Alvará",
    "modelo_considerandos": [
        "em atenção ao Processo supracitado, no qual foi solicitada a renovação do Alvará de Construção nº [Número]/[Ano] com área liberada de [Área] m², informamos que, conforme parecer fiscal datado de [Data], a obra não foi iniciada, estando o alvará vencido desde [Data de Vencimento].",
        "devido à decisão judicial proferida na Ação Civil Pública (Processo nº 5002141-25.2021.8.13.0456), que proíbe a renovação de alvarás caducos cuja obra não tenha sido iniciada (determinando como critério de aferição de início de obra a conclusão das fundações), fica indeferida a renovação.",
        "no caso de alvarás caducos de obras não iniciadas, deverá ser realizado um novo procedimento administrativo, com todas as etapas necessárias para a concessão de um novo alvará, observando a legislação vigente."
    ],
    "modelo_conclusao": "Portanto, o Alvará de Construção nº [Número] encontra-se cancelado."
})

# ═══════════════════════════════════════════════════════════
#  CHECKLIST DE DOCUMENTOS
# ═══════════════════════════════════════════════════════════

salvar("checklist_documentos", {
    "tipo": "referencia",
    "descricao": "Checklist de documentos obrigatórios para abertura de processos na SMOSU",
    "alvara_construcao_reforma_ampliacao": [
        "Documento Pessoal (CPF, RG) / Procuração (se aplicável)",
        "Comprovante de endereço atualizado",
        "Certidão Imobiliária (Matrícula atualizada, ou Contrato de Compra e Venda + Matrícula)",
        "Projeto Arquitetônico (Digital: DWG e PDF)",
        "ART / RRT / TRT (Projeto e Execução)",
        "Guia de Recolhimento de Taxa de Licença quitada",
        "Certidão Negativa de Débitos Municipais",
        "Espelho Cadastral"
    ],
    "regularizacao_as_built": [
        "Mesmos documentos do alvará",
        "Projeto As Built",
        "Laudo Técnico de Vistoria (com ART/RRT de laudo)"
    ],
    "desmembramento_divisao_retificacao": [
        "Documentos pessoais e propriedade do terreno",
        "Levantamento Topográfico Georreferenciado (DWG e PDF)",
        "Memorial Descritivo (PDF)",
        "ART / RRT / TRT pertinente ao levantamento",
        "Certidão Negativa de Débitos"
    ],
    "certidoes_simples": [
        "Documentos Pessoais",
        "Matrícula ou Contrato de Compra e Venda",
        "Espelho Cadastral do imóvel"
    ]
})

print(f"\n[✓] Todos os templates gerados em: {TEMPLATES_DIR}")
print(f"    Total de arquivos: {len(os.listdir(TEMPLATES_DIR))}")

