# DOCUMENTOS DE EXPEDIÇÃO (SETOR ADMINISTRATIVO / SECRETARIA)

Este arquivo documenta as estruturas formatadas dos documentos impressos que a secretaria emite para entrega no balcão a partir do seu **Parecer Técnico de Parecer**.  A diagramação do seu JSON e dados deverão espelhar esse conhecimento de "como sairá na folha final" para esses casos.

## ESTRUTURA METÁLICA (ALVARÁ DE CONSTRUÇÃO)
O Alvará de construção deve conter invariavelmente:
1. `numero_alvara`
2. Identificação do `Proprietário` (Nome e CPF)
3. Identificação do `Autor do Projeto` (Nome e CREA e ART PROJETO)
4. Identificação do `Responsável Técnico` (Nome e CREA e ART OBRA)
5. Identificação da `Construtora` (Opcional, com Nome e CNPJ)
6. Escopo (Ex: "Tendo em vista o processo nº X, fica concedida a licença para execução em DD/MM/AAAA da obra denominada Y no endereço Z.")
7. Matrizes/Dados da Obra:
   - Categoria | Destinação | Tipo Base | Área(m²)
   - Área Total da Obra / Especificação (Vagas de Garagem Tabela)
   - Observações e Fim de Validade.

## ESTRUTURA METÁLICA (CARTA DE HABITE-SE)
O Documento de Habite-se diverge na estrutura:
1. `numero_habitese`
2. `endereco_completo` da Obra destacado.
3. `Proprietário`
4. `Responsável pela Execução`
5. `Responsável Técnico` (Texto narrativo: "Conforme despacho... processo X com área Y licenciada pelo Alvará Z concluída em...")
6. `Tipo_de_Habitese` (Total, Parcial etc).
7. Tabela de Matrizes Áreas (semelhante ao alvara).
8. `Observacao` final (Ex: "Em atenção ao processo digital").

Ao gerar o seu JSON nestas especificações Administrativas de balcão, construa rigidamente todos estes sub-nós sob a chave "dados_da_licenca" por exemplo, garantindo a fidelidade para impressão oficial da guia em nosso sistema.
