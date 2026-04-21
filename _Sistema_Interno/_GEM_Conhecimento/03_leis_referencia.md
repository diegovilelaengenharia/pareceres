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
