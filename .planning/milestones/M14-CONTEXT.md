# M14-CONTEXT: Fluxo Administrativo de Certidões

## Visão Geral
Transformar o Parecer Técnico em uma "Ordem de Serviço" robusta. Ao detectar a necessidade de múltiplas certidões, o sistema não as gera individualmente, mas sim consolida no Parecer:
1.  **Veredito de Viabilidade**: Se há dados suficientes para emitir cada certidão.
2.  **Bloco de Variáveis**: Lista exata de campos (Matrícula, Lote, Decreto, etc.) que o administrativo deve usar.
3.  **Sugestão de Texto Padronizado**: O texto base que deve constar em cada certidão solicitada.

## Objetivos
- **Redução de Erros Administrativos**: Fornecer dados limpos e validados no Parecer.
- **Rigor Técnico**: Impedir a solicitação de certidões cujos dados base (ex: Matrícula) estejam ausentes.
- **Unificação**: Um único processo gera um único Parecer que desencadeia múltiplas ações administrativas.

## Certidões Mapeadas
- **Certidão de Localização**: Requer Matrícula, Inscrição Municipal, Zona de Uso.
- **Certidão de Confrontação**: Requer Memorial Descritivo, confrontantes identificados.
- **Certidão de Nome de Rua**: Requer Decreto de Denominação, Nome Anterior vs. Atual.
- **Certidão de Numeração**: Requer croqui de localização, histórico de numeração da quadra.

## Critérios de Aceite
- O SIA deve alertar se uma certidão for necessária mas não puder ser emitida por falta de dados.
- O JSON final deve conter um array `solicitacoes_administrativas` com os blocos de dados prontos.
- O modelo de Parecer DOCX deve ter uma seção dedicada a "Orientações ao Setor Administrativo".
