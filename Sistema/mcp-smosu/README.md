# SMOSU Conhecimento - Servidor MCP

Servidor de Protocolo de Contexto de Modelo (MCP) para a Secretaria Municipal de Obras e Serviços Urbanos de Oliveira/MG.

Este servidor permite que modelos de linguagem (IA) consultem em tempo real a base de conhecimento local, incluindo leis estruturadas, parâmetros urbanísticos e diretrizes de processo.

## Ferramentas Disponíveis

- `consultar_codex_legal(termo_busca)`: Busca artigos e leis no `codex_legal.json`.
- `consultar_indices_urbanisticos(zona_ou_bairro)`: Consulta TO, CA e recuos no `geo_oliveira.json`.
- `buscar_diretriz_processo(tipo_processo)`: Lê manuais de raciocínio e fluxos em `.md`.
- `pesquisa_livre_leis_txt(palavra_chave)`: Busca textual em todos os arquivos da base de conhecimento.

## Instalação

Certifique-se de ter o Python 3.10+ instalado.

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

O servidor opera via transporte `stdio`, o que permite a integração direta com interfaces que suportam MCP (como o Gemini CLI ou Claude Desktop).

Para rodar manualmente (teste de sintaxe):
```bash
python server.py
```

## Estrutura
- `server.py`: Ponto de entrada (FastMCP).
- `tools.py`: Lógica de busca e carregamento de dados.
- `evals.xml`: Conjunto de testes para validação de performance do modelo.
