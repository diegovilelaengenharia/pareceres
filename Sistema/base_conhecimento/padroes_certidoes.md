# PADRÕES DE CERTIDÕES — SMOSU Oliveira/MG

Este arquivo define os templates de texto e as variáveis obrigatórias para a confecção de certidões pelo setor administrativo, conforme solicitado no Parecer Técnico.

---

## 1. Certidão de Localização
**Objetivo**: Confirmar o zoneamento e a localização oficial do imóvel.

### Variáveis Obrigatórias:
- `logradouro`: Nome oficial da rua.
- `bairro`: Bairro conforme cadastro municipal.
- `inscricao_municipal`: Código do imóvel.
- `matricula`: Número do registro no SRI.
- `zona_uso`: Sigla da zona (ex: ZCS, ZUR).

### Template de Texto:
*"Certificamos, para os devidos fins, que o imóvel situado à **{{logradouro}}**, Bairro **{{bairro}}**, inscrito sob o nº **{{inscricao_municipal}}** e Matrícula nº **{{matricula}}**, encontra-se inserido na Zona de Uso **{{zona_uso}}**, conforme a Lei Complementar nº 267/2019."*

---

## 2. Certidão de Nome de Rua (Denominação)
**Objetivo**: Corrigir ou confirmar a alteração de nome de um logradouro.

### Variáveis Obrigatórias:
- `nome_anterior`: Nome que consta na matrícula ou projeto.
- `nome_atual`: Nome oficial atualizado.
- `decreto_lei`: Número do dispositivo que deu o nome.

### Template de Texto:
*"Certificamos que o logradouro anteriormente denominado **{{nome_anterior}}** passou a denominar-se oficialmente **{{nome_atual}}**, em conformidade com o **{{decreto_lei}}**, devendo tal alteração ser averbada junto ao registro do imóvel."*

---

## 3. Certidão de Confrontação
**Objetivo**: Certificar formalmente os limites e confrontantes do imóvel conforme arquivos municipais e matrícula do SRI.

### Variáveis Obrigatórias:
- `numero_processo`: Processo administrativo.
- `matricula_sri`: Número da matrícula no Registro de Imóveis.
- `inscricao_cadastral`: Código de cadastro do imóvel na prefeitura.
- `frente`: Nome da rua/logradouro frontal.
- `lado_direito`: Nome do confrontante e, se possível, sua inscrição cadastral.
- `lado_esquerdo`: Nome do confrontante ou logradouro lateral.
- `fundos`: Nome do confrontante e sua inscrição cadastral.
- `data_emissao`.

### Template de Texto:
*"Certifico pelo Processo nº **{{numero_processo}}**, que revendo os arquivos existentes nesta Prefeitura, que o imóvel da matrícula nº **{{matricula_sri}}** do SRI, neste município de Oliveira/MG, Inscrição Cadastral nº **{{inscricao_cadastral}}**, possui as seguintes Confrontações: 

Frente: **{{frente}}**.
Lado direito: **{{lado_direito}}**.
Lado esquerdo: **{{lado_esquerdo}}**.
Fundos: **{{fundos}}**."*

---

## 4. Certidão de Numeração
**Objetivo**: Atribuir ou confirmar o número predial oficial, geralmente para fins de averbação ou ligação de serviços (CEMIG/COPASA).

### Variáveis Obrigatórias:
- `numero_processo`: Processo administrativo.
- `proprietario_nome`: Nome completo.
- `endereco_detalhado`: Logradouro e indicação de Lote/Quadra (ex: "Quadra 10 Parte do Lote 02").
- `bairro`.
- `numero_atribuido`: O número oficial (ex: 338).
- `finalidade`: Ex: "conforme exigências da CEMIG - Companhia Energética de Minas Gerais".
- `validade_meses`: Prazo de validade (ex: "06 meses").
- `data_emissao`.

### Template de Texto:
*"Certifico pelo Processo nº **{{numero_processo}}** que o imóvel de propriedade do(a) Sr.(a) **{{proprietario_nome}}**, situado na **{{endereco_detalhado}}**, Bairro **{{bairro}}**, possui o número **{{numero_atribuido}}**, município de Oliveira/MG, **{{finalidade}}**. Esta certidão é válida por **{{validade_meses}}**."*

---

## 5. Alvará de Construção Residencial
**Objetivo**: Licenciar a execução de obras novas, reformas ou ampliações residenciais.

### Variáveis Obrigatórias:
- `numero_alvara`: Número sequencial (ex: 064/2026).
- `proprietario_nome`: Nome completo do proprietário.
- `proprietario_cpf_cnpj`: CPF ou CNPJ do proprietário.
- `autor_projeto_nome`: Nome do profissional autor.
- `autor_projeto_registro`: CREA ou CAU do autor.
- `art_rrt_projeto`: Número da ART/RRT de projeto.
- `rt_obra_nome`: Nome do responsável técnico pela execução.
- `rt_obra_registro`: CREA ou CAU do RT.
- `art_rrt_obra`: Número da ART/RRT de execução.
- `construtora_nome`: Nome da empresa ou responsável pela execução.
- `construtora_cpf_cnpj`: CPF ou CNPJ da construtora.
- `numero_processo`: Número do processo administrativo.
- `data_aprovacao_projeto`: Data em que o projeto foi aprovado.
- `denominacao_obra`: Ex: "CASA RESIDENCIAL", "EDIFÍCIO MULTIFAMILIAR".
- `endereco_obra`: Logradouro, número e bairro.
- `area_nova`: Área da construção nova (m²).
- `area_total_obra`: Área total licenciada (m²).
- `vaga_garagem_desc`: Área de garagem descoberta (se houver).
- `taxa_permeabilidade_min`: Percentual e área (m²) mínima exigida.
- `data_validade`: Data de vencimento do alvará (geralmente 1 ano após emissão).

### Template de Texto (Observações):
*"Área útil total **{{area_total_obra + vaga_garagem_desc}}**m², sendo **{{vaga_garagem_desc}}**m² referente a uma vaga de garagem descoberta sem estrutura. A edificação licenciada deverá atender a taxa mínima de permeabilidade de **{{taxa_permeabilidade_min_perc}}**% do terreno que corresponde a **{{taxa_permeabilidade_min_m2}}**m², e respeitar o projeto aprovado. Alvará válido até **{{data_validade}}**."*

---

## 6. Alvará de Construção Comercial / Residencial (Misto/Multifamiliar)
**Objetivo**: Licenciar edificações complexas com mais de uma destinação ou múltiplas unidades autônomas.

### Variáveis Obrigatórias:
- `numero_alvara`: Número sequencial.
- `proprietario_nome` / `proprietario_cpf_cnpj`.
- `autor_projeto_nome` / `autor_projeto_registro` / `art_rrt_projeto`.
- `rt_obra_nome` / `rt_obra_registro` / `art_rrt_obra`.
- `construtora_nome` / `construtora_cpf_cnpj`.
- `numero_processo`.
- `data_aprovacao_projeto`.
- `denominacao_obra`: Ex: "COMERCIAL / RESIDENCIAL", "RESIDENCIAL MULTIFAMILIAR".
- `unidades_autonomas`: Listagem de apartamentos/salas (ex: "APT.01, APT.02, APT.03").
- `endereco_obra`: Incluindo todas as frentes e unidades.
- `quadro_areas`: Array com Categoria, Destinação e Área (m²) para cada tipo.
- `area_resultante`: Soma das áreas computáveis.
- `vagas_garagem_estacionamento_desc`: Área de vagas descobertas (m²).
- `quantidade_vagas`: Número de vagas (ex: "04 vagas de garagem e 01 vaga de estacionamento").
- `area_util_total`: `area_resultante` + `vagas_garagem_estacionamento_desc`.
- `taxa_permeabilidade_min_perc` e `taxa_permeabilidade_min_m2`.
- `data_validade`.

### Template de Texto (Observações):
*"Edificação de prédio (**{{denominacao_obra}}**) com **{{area_resultante}}**m², com área útil total de **{{area_util_total}}**m², sendo **{{vagas_garagem_estacionamento_desc}}**m² referente a **{{quantidade_vagas}}** descoberto sem estrutura. A edificação licenciada deverá atender a taxa mínima de permeabilidade de **{{taxa_permeabilidade_min_perc}}**% do terreno que corresponde a **{{taxa_permeabilidade_min_m2}}**m², e respeitar o projeto aprovado. Alvará válido até **{{data_validade}}**."*

---

## 7. Carta de Habite-se
**Objetivo**: Certificar a conclusão da obra de acordo com o projeto aprovado e autorizar a ocupação.

### Variáveis Obrigatórias:
- `numero_habitese`: Número sequencial (ex: 068/2026).
- `endereco_obra` / `bairro`.
- `proprietario_nome` / `proprietario_cpf_cnpj`.
- `executor_nome` / `executor_cpf_cnpj`.
- `rt_nome`: Nome do Responsável Técnico.
- `processo_aprovacao`: Processo que originou a licença (ex: 7682/2024).
- `alvara_referencia_numero`: Número do Alvará de Construção vinculado.
- `alvara_referencia_data`: Data de expedição do alvará vinculado.
- `area_total_obra`: Área total concluída (m²).
- `data_conclusao_obra`: Data em que a obra foi concluída.
- `tipo_habitese`: "Total" ou "Parcial".
- `quadro_areas`: Listagem de categorias e destinações concluídas.
- `processo_emissao`: Processo atual de solicitação do habite-se (ex: 3825/2026).
- `data_emissao`: Data de emissão do documento.

### Template de Texto (Contextual):
*"Conforme despacho exarado no processo nº **{{processo_aprovacao}}**, com área total da obra **{{area_total_obra}}** m². Licenciada pelo Alvará de Construção nº **{{alvara_referencia_numero}}**, expedido em **{{alvara_referencia_data}}**, foi concluída em **{{data_conclusao_obra}}** de acordo com o projeto aprovado. **TIPO DE HABITE-SE: {{tipo_habitese}}**."*

---

## 8. Certidão de Averbação
**Objetivo**: Consolidar os dados da edificação concluída para fins de registro e averbação junto ao Cartório de Registro de Imóveis (SRI).

### Variáveis Obrigatórias:
- `numero_processo`: Processo administrativo atual.
- `proprietario_nome`: Nome completo conforme matrícula.
- `matricula_sri`: Número da matrícula no SRI.
- `endereco_completo`: Rua, número e bairro.
- `inscricao_imobiliaria`: Código de cadastro na prefeitura.
- `descricao_imovel`: Ex: "Imóvel residencial", "Prédio comercial".
- `area_total`: Área total a ser averbada (m²).
- `data_alvara`: Data de expedição do Alvará de Construção.
- `data_habitese`: Data de expedição da Carta de Habite-se.
- `infraestrutura`: Confirmação de redes (ex: "Possui redes elétricas e hidráulicas completas").
- `data_emissao`: Data atual.

### Template de Texto:
*"Certifico pelo Processo nº **{{numero_processo}}**, que o(a) Sr.(a) **{{proprietario_nome}}** é proprietário(a) do imóvel de Matrícula nº **{{matricula_sri}}**, situado na **{{endereco_completo}}**, cadastrado nesta Prefeitura Inscrição Imobiliária nº **{{inscricao_cadastral}}**, onde consta: **{{descricao_imovel}}**: **{{area_total}}**m². Data do Alvará de Construção: **{{data_alvara}}**. Data do Habite-se: **{{data_habitese}}**. **{{infraestrutura}}**."*

---

## 9. Certidão de Averbação Complexa (Mista / Múltiplas Unidades)
**Objetivo**: Certificar edificações multifamiliares ou mistas, discriminando cada unidade autônoma, sua respectiva inscrição imobiliária e área individual para averbação.

### Variáveis Obrigatórias:
- `numero_processo` / `data_processo`.
- `proprietario_nome`.
- `matricula_sri`: Matrícula mãe do imóvel.
- `endereco_principal`: Rua e Bairro principal.
- `lista_unidades`: Array de objetos contendo:
    - `identificacao`: Ex: "Apto 101", "Loja 569".
    - `logradouro_especifico`: Se houver mais de uma frente (ex: Rua X e Av. Y).
    - `inscricao_imobiliaria`: Código individual de cada unidade.
    - `area_unidade`: Área privativa da unidade (m²).
- `resumo_pavimentos`: Array de objetos contendo:
    - `pavimento`: Ex: "Superior", "Inferior".
    - `uso`: "Residencial", "Comercial".
    - `area_total_pavimento`: Soma das áreas das unidades daquele pavimento.
- `data_alvara` / `data_habitese`.
- `data_emissao`.

### Template de Texto (Cabeçalho):
*"Certifico pelo processo nº **{{numero_processo}}** de **{{data_processo}}**, que o Sr.(a) **{{proprietario_nome}}** é proprietário de um imóvel de matrícula **{{matricula_sri}}**, situado na **{{endereco_principal}}**, cadastrado nesta Prefeitura sob as seguintes inscrições imobiliárias: **{{lista_unidades | join_inscricoes}}**."*

### Template de Texto (Corpo - Discriminação):
*"Pavimento **{{pavimento}}**: Imóveis **{{uso}}**, área total **{{area_total_pavimento}}**m²: 
{% for uni in lista_unidades if uni.pavimento == pav.pavimento %}
   Nº **{{uni.identificacao}}** área **{{uni.area_unidade}}**m².
{% endfor %}"*

---

## 10. Certidão de Cancelamento
**Objetivo**: Anular formalmente um ato administrativo anterior (ex: desmembramento, certidão, numeração) devido a erro, falta de registro ou alteração física no imóvel (incorporação).

### Variáveis Obrigatórias:
- `numero_processo`: Processo onde o cancelamento foi solicitado.
- `requerente_nome`: Nome do solicitante (pode incluir "e Outra").
- `ato_cancelado`: Identificação precisa do documento/ato (ex: "Certidão de Número 64 referente à área de 22,00m² Unidade 002").
- `justificativa`: Motivo técnico (ex: "o imóvel foi incorporado à construção" ou "não efetuou o registro").
- `data_emissao`: Data atual.

### Template de Texto:
*"Em atendimento ao processo nº **{{numero_processo}}**, onde a requerente **{{requerente_nome}}** solicita o cancelamento da **{{ato_cancelado}}**. Certifico o cancelamento da certidão supracitada, devido que, **{{justificativa}}**."*

---

## 11. Certidão de Número para Abertura de Firma (Econômico)
**Objetivo**: Certificar a existência e o número oficial de um ponto comercial para fins de registro de empresas e alvará de funcionamento.

### Variáveis Obrigatórias:
- `numero_processo`: Processo administrativo.
- `proprietario_nome`: Nome completo (pode incluir "e Outra").
- `tipo_imovel`: Sempre "imóvel comercial".
- `endereco_completo`: Rua, número e bairro.
- `area_comercial`: Área vinculada à unidade (ex: 19,66m²).
- `validade_meses`: Geralmente "06 meses".
- `data_emissao`.

### Template de Texto:
*"Certifico pelo processo nº **{{numero_processo}}**, que revendo o Cadastro Técnico Econômico Imobiliário desta Prefeitura, consta em nome do(a) Sr(a). **{{proprietario_nome}}** um **{{tipo_imovel}}** na **{{endereco_completo}}**, município de Oliveira/MG, referente à área de **{{area_comercial}}**m². Este documento tem validade de **{{validade_meses}}**."*

---

## 12. Comunicado de Pendência, Divergência ou Indeferimento
**Objetivo**: Notificar o requerente sobre inconsistências, necessidade de novos processos (ex: regularização antes de desmembramento) ou indeferimentos por conformidade.

### Variáveis Obrigatórias:
- `numero_processo` / `requerente_nome`.
- `assunto`: Ex: "Certidão de desmembramento", "Certidão de nome de rua".
- `texto_informativo`: Ex: "a solicitação só poderá ser aprovada, após sanadas as pendências descritas abaixo" ou "fica indeferida, pois não houve alteração em nome".
- `lista_pendencias`: Lista numerada ou em tópicos das exigências técnicas.
- `observacoes_adicionais`: Ex: "anexar ART, taxa de habite-se no outro processo que será aberto".

### Template de Texto:
*"Em atenção ao Processo nº **{{numero_processo}}**, Assunto: **{{assunto}}**. Informamos que **{{texto_informativo}}**:
{% for item in lista_pendencias %}
• {{item}}
{% endfor %}
**Obs**: {{observacoes_adicionais}}"*

---

## 13. Comunicado de Baixa de CNO / CEI (Receita Federal)
**Objetivo**: Instruir o requerente a proceder com a baixa do cadastro de obra na Receita Federal após o cancelamento ou substituição de um alvará no sistema SISOBRAS.

### Variáveis Obrigatórias:
- `numero_processo_atual`.
- `alvara_cancelado_numero` / `alvara_cancelado_data`.
- `processo_origem_alvara`.
- `orientacao_fiscal`: Ex: "deverá o requerente solicitar sob sua inteira responsabilidade, a baixa da CEI junto a Receita Federal do Brasil".

### Template de Texto:
*"Em atenção ao Processo nº **{{numero_processo_atual}}**, no qual foi solicitado o cancelamento do Alvará **{{alvara_cancelado_numero}}** emitido em **{{alvara_cancelado_data}}** através do Processo nº **{{processo_origem_alvara}}**. Informamos que, devido ao cancelamento do alvará no novo sistema SISOBRAS, **{{orientacao_fiscal}}**, relativo ao alvará supracitado."*

---

## 14. Certidão de Decadência Fiscal (Receita Federal)
**Objetivo**: Certificar que a edificação foi concluída há mais de 05 (cinco) anos para fins de comprovação de decadência de débitos previdenciários (CNO/CEI) junto à Receita Federal do Brasil.

### Variáveis Obrigatórias:
- `proprietario_nome`.
- `tipo_imovel` / `area_total`.
- `documento_prova`: Ex: "Habite-se nº 2613/2013 datado em 31/07/2013".
- `matricula_sri`.
- `endereco_completo`.
- `tempo_construcao`: Geralmente "mais de 05 (cinco) anos".
- `data_emissao`.

### Template de Texto:
*"Certifico para fins de comprovação de decadência de débitos junto a Receita Federal do Brasil, incidentes sobre mão-de-obra em construção civil, que revendo o cadastro técnico econômico imobiliário desta Prefeitura, dele consta lançado pelo cadastro imobiliário, um **{{tipo_imovel}}** com área construída de **{{area_total}}**m², comprovado por **{{documento_prova}}**, Matrícula nº **{{matricula_sri}}**, localizado na **{{endereco_completo}}**, município de Oliveira/MG, de propriedade de **{{proprietario_nome}}**, tendo sido, portanto, construído há **{{tempo_construcao}}**."*

---

## 15. Certidão de Demolição
**Objetivo**: Certificar a remoção física de uma edificação para fins de baixa cadastral e atualização no SRI.

### Variáveis Obrigatórias:
- `numero_processo`.
- `area_demolida` / `uso_anterior` (ex: residencial).
- `endereco_completo` / `proprietario_nome`.
- `alvara_demolicao_numero` / `alvara_demolicao_ano`.
- `matricula_sri` / `inscricao_imobiliaria`.
- `validade_meses`: "06 meses".

### Template de Texto:
*"Certifico pelo processo nº **{{numero_processo}}**, que foi verificado pelos fiscais desta Prefeitura, a demolição com área **{{uso_anterior}}** de **{{area_demolida}}**m², situada à **{{endereco_completo}}**, de propriedade de **{{proprietario_nome}}**, que a mesma foi demolida conforme Alvará de Demolição nº **{{alvara_demolicao_numero}}**, Matrícula SRI nº **{{matricula_sri}}**, Inscrição imobiliária **{{inscricao_imobiliaria}}**. Este documento tem validade de **{{validade_meses}}**."*

---

## 16. Certidão de Parcelamento do Solo (Desmembramento / Unificação / Divisão)
**Objetivo**: Certificar alterações na configuração de lotes ou glebas, incluindo a descrição técnica para registro imobiliário.

### Variáveis Obrigatórias:
- `numero_processo`.
- `fundamentacao_legal`: Ex: "Art 4º Lei 216/2014 e Art 990 Provimento 93/2020".
- `proprietario_nome` / `cpf_cnpj`.
- `matricula_mae`: Número da matrícula original.
- `localizacao_gleba`: Nome da gleba ou bairro.
- `area_total`.
- `finalidade`: "desmembramento", "unificação" ou "divisão de área urbana".
- `descricao_perimetro`: Bloco técnico com vértices, azimutes, distâncias e coordenadas UTM.
- `quadro_areas_resultantes`: Descrição das novas áreas criadas (ex: Área 01, Área 02).

### Template de Texto:
"Certifico pelo processo nº **{{numero_processo}}**, mediante o cumprimento do **{{fundamentacao_legal}}**, que revendo o cadastro técnico imobiliário desta Prefeitura, dele consta um imóvel de Matrícula **{{matricula_mae}}** do SRI, situado na **{{localizacao_gleba}}**, de propriedade de **{{proprietario_nome}}**, com área total de **{{area_total}}**, para fins de **{{finalidade}}** com as seguintes medidas e confrontações:

**DESCRIÇÃO DA PROPRIEDADE**
{{descricao_perimetro}}

**OBS**: Imóvel com a Inscrição Cadastral na Prefeitura sob o nº **{{inscricao_cadastral}}**."

---

## 17. Carta de Habite-se Simplificado (REURB)
**Objetivo**: Autorizar a ocupação de imóveis regularizados via processo de REURB, com isenções específicas.

### Variáveis Obrigatórias:
- `numero_habitese_reurb`.
- `proprietario_nome` / `cpf_cnpj`.
- `endereco_obra` / `bairro`.
- `area_total`.
- `processo_reurb`: Número do processo administrativo.
- `observacao_reurb`: Ex: "isento de alvará de construção sem comunicação com a RFB".

### Template de Texto:
"Conforme processo nº **{{processo_reurb}}**, imóvel com área total da obra **{{area_total}}**m². **OBSERVAÇÃO**: Habite-se isento de alvará de construção sem comunicação com a RFB, autorizado pela REURB. **{{identificacao_lote_quadra}}**."

---

## 18. Certidão para SRI (Topografia / Inclusão de Medidas)
**Objetivo**: Atestar ao Cartório de Registro de Imóveis que a retificação de medidas ou confrontações não invade área pública nem fere os interesses do município.

### Variáveis Obrigatórias:
- `numero_processo`.
- `objetivo_topografia`: Ex: "inclusão de medidas e confrontações do terreno urbano".
- `endereco_detalhado` / `bairro`.
- `proprietario_nome` / `cpf_cnpj`.
- `matricula_sri` / `inscricao_imobiliaria`.
- `veredito_municipio`: Sempre "NÃO FERE aos interesses do Município".
- `alinhamento_avaliado`: Ex: "avaliado apenas a situação do alinhamento do imóvel que confronta com frente da via de domínio público".

### Template de Texto:
"Certifico pelo Processo nº **{{numero_processo}}**, que a **{{objetivo_topografia}}** na **{{endereco_detalhado}}**, Bairro **{{bairro}}**, requerido(a) por **{{proprietario_nome}}**, CPF nº **{{cpf_cnpj}}**, Matrícula nº **{{matricula_sri}}**, inscrição imobiliária **{{inscricao_imobiliaria}}**, **{{veredito_municipio}}**. Salientamos que foi avaliado por esta secretaria, apenas a situação do **{{alinhamento_avaliado}}**, não sendo avaliado o contexto geral do projeto."

---

## 19. Certidão de Nome de Rua (Decreto de Denominação)
**Objetivo**: Formalizar a alteração de nome de um logradouro com base em legislação municipal.

### Variáveis Obrigatórias:
- `numero_processo`.
- `nome_anterior` / `nome_atual`.
- `bairro`.
- `decreto_numero` / `decreto_data`.

### Template de Texto:
"Certifico que revendo os arquivos existentes nesta Prefeitura e atendendo ao Processo nº **{{numero_processo}}**, que a **{{nome_anterior}}** passou a denominar-se oficialmente **{{nome_atual}}**, no Bairro **{{bairro}}**, nesta cidade de Oliveira/MG, conforme Decreto nº **{{decreto_numero}}** de **{{decreto_data}}**."

---

## 20. Certidão de Usucapião (Extrajudicial/Judicial)
**Objetivo**: Atestar a localização, o zoneamento e a inexistência de interesse público municipal sobre a área objeto de usucapião, sem atestar domínio.

### Variáveis Obrigatórias:
- `numero_processo`.
- `proprietario_posseiro` / `cpf_cnpj`.
- `endereco_imovel` / `bairro`.
- `area_usucapienda`.
- `confrontacoes_descritivas`.
- `clausula_nao_dominio`: Texto padrão isentando a prefeitura de atestar a propriedade.
- `interesse_publico`: Declaração de inexistência de ruas, praças ou áreas verdes sobre o polígono.

### Template de Texto:
"Certifico pelo processo nº **{{numero_processo}}**, que o imóvel situado à **{{endereco_imovel}}**, Bairro **{{bairro}}**, com área de **{{area_usucapienda}}**, ocupado por **{{proprietario_posseiro}}**, inscrito no CPF sob nº **{{cpf_cnpj}}**, conforme levantamento topográfico anexo:
1. Localiza-se em zona urbana consolidada (**{{zona_uso}}**);
2. **NÃO HÁ INTERESSE PÚBLICO** municipal sobre a referida área, não havendo sobreposição com logradouros, praças ou áreas institucionais;
3. A presente certidão **NÃO CONSTITUI TÍTULO DE PROPRIEDADE**, limitando-se a atestar a situação fática e urbanística para fins de instrução de processo de Usucapião.

**CONFRONTAÇÕES**: {{confrontacoes_descritivas}}."

---

## ANEXO: ORIENTAÇÕES AO SETOR ADMINISTRATIVO (Resumo para Emissão)
**Objetivo**: Facilitar a triagem e preenchimento dos documentos finais pelo setor administrativo, resumindo o veredito técnico e os dados chave.

### Regras de Resumo:
1. **Veredito**: Indicar claramente se é DEFERIDO ou INDEFERIDO.
2. **Documento**: Nome exato do modelo a ser utilizado no Word.
3. **Variáveis Críticas**: Listar os dados que NÃO podem ser digitados errado (Área, Inscrição, Matrícula).
4. **Condicionantes**: Caso haja algo a ser conferido no balcão (ex: pagar taxa).

### Exemplo de Saída (Campo `solicitacoes_administrativas`):
> **RESUMO PARA EMISSÃO (ADMIN):**
> - **Tipo**: Certidão de Desmembramento.
> - **Status**: DEFERIDO.
> - **Dados Chave**: Área Total (1.000m²) -> Área 01 (400m²) e Área 02 (600m²).
> - **Inscrição**: 01.02.003.0456.
> - **Matrícula Mãe**: 12.345.
> - **OBS**: Exigir comprovante de pagamento da taxa de expediente antes da entrega.

---
*Uso Exclusivo: IA do SIA deve extrair estes textos para o campo `solicitacoes_administrativas` do JSON.*















