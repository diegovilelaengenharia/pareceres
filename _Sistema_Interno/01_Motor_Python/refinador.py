"""
Refinador de JSON via Claude API.
Recebe o JSON atual + texto de ajustes em linguagem natural → retorna JSON refinado.
"""

import os
import sys
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from config import PASTA_ENTRADA

AJUSTES_FILE = os.path.join(PASTA_ENTRADA, "AJUSTES.txt")


def _extrair_json(texto: str) -> dict | None:
    match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', texto)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    match = re.search(r'\{[\s\S]*\}', texto)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return None


def _garantir_ajustes_txt():
    """Cria AJUSTES.txt vazio com instruções se não existir."""
    if not os.path.exists(AJUSTES_FILE):
        with open(AJUSTES_FILE, "w", encoding="utf-8") as f:
            f.write(
                "# AJUSTES DESEJADOS — escreva aqui as mudanças que quer aplicar ao documento\n"
                "# Uma linha por ajuste. Linhas começando com # são ignoradas.\n"
                "# Exemplos:\n"
                "#   Corrigir área construída para 142,50m²\n"
                "#   Mudar conclusão para FAVORÁVEL COM RESSALVAS\n"
                "#   Adicionar observação sobre prazo de 2 anos no alvará\n"
                "#   Remover o considerando sobre decadência\n"
                "\n"
            )


def _ler_ajustes(texto_direto: str | None = None) -> str:
    """
    Lê os ajustes do AJUSTES.txt (ignorando linhas com #) ou usa texto_direto.
    """
    if texto_direto and texto_direto.strip():
        return texto_direto.strip()

    if not os.path.exists(AJUSTES_FILE):
        return ""

    linhas = []
    with open(AJUSTES_FILE, encoding="utf-8") as f:
        for linha in f:
            linha = linha.rstrip()
            if linha and not linha.startswith("#"):
                linhas.append(linha)
    return "\n".join(linhas)


def refinar_json(dados_atuais: dict, ajustes: str) -> dict:
    """
    Chama a Claude API para aplicar os ajustes ao JSON atual.
    Retorna o JSON refinado.
    """
    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "Biblioteca 'anthropic' não instalada.\n"
            "  Execute: pip install anthropic"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "Variável ANTHROPIC_API_KEY não definida.\n"
            "  Execute: set ANTHROPIC_API_KEY=sk-ant-..."
        )

    json_str = json.dumps(dados_atuais, ensure_ascii=False, indent=2)

    prompt_system = (
        "Você é um assistente especializado em ajustar JSONs de pareceres técnicos municipais. "
        "Receberá o JSON atual do documento e uma lista de ajustes em linguagem natural. "
        "Aplique EXATAMENTE os ajustes solicitados, mantendo a estrutura e todas as outras chaves intactas. "
        "Retorne APENAS o JSON refinado em bloco ```json, sem texto adicional depois."
    )

    prompt_user = (
        f"JSON ATUAL:\n```json\n{json_str}\n```\n\n"
        f"AJUSTES SOLICITADOS:\n{ajustes}\n\n"
        "Aplique os ajustes e retorne o JSON completo refinado."
    )

    print("  [API] Enviando ajustes para Claude API...")
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        system=prompt_system,
        messages=[{"role": "user", "content": prompt_user}],
    )

    resposta = msg.content[0].text
    dados_refinados = _extrair_json(resposta)

    if dados_refinados is None:
        print("  [AVISO] Não foi possível extrair JSON da resposta. Mantendo JSON original.")
        return dados_atuais

    return dados_refinados


def loop_de_ajustes(json_path: str) -> str:
    """
    Loop interativo: mostra preview → pede ajustes → refina → repete até aprovação.
    Retorna o caminho do JSON final (pode ser diferente se renomeado).
    """
    from preview_html import gerar_preview

    _garantir_ajustes_txt()

    rodada = 1
    while True:
        with open(json_path, encoding="utf-8") as f:
            dados = json.load(f)

        print(f"\n  [Preview] Abrindo visualização no navegador (rodada {rodada})...")
        preview_path = os.path.join(
            PASTA_ENTRADA, f"preview_rodada_{rodada}.html"
        )
        gerar_preview(dados, destino=preview_path)

        print()
        print("  ─────────────────────────────────────────────────────────")
        print(f"  Preview aberto no navegador. Rodada {rodada}.")
        print()
        print("  O que deseja fazer?")
        print("  [ENTER]    → Aprovar e gerar o DOCX")
        print("  [A]        → Digitar ajustes agora")
        print("  [F]        → Editar AJUSTES.txt e pressionar ENTER")
        print("  ─────────────────────────────────────────────────────────")
        escolha = input("  Sua escolha: ").strip().upper()

        if escolha == "":
            print("\n  [OK] Aprovado! Seguindo para geração do DOCX...")
            # Limpar AJUSTES.txt após aprovação
            _garantir_ajustes_txt()
            break

        ajustes = ""

        if escolha == "A":
            print("\n  Descreva os ajustes (uma linha cada, ENTER em branco para terminar):")
            linhas = []
            while True:
                linha = input("  › ").strip()
                if not linha:
                    break
                linhas.append(linha)
            ajustes = "\n".join(linhas)

        elif escolha == "F":
            print(f"\n  Edite o arquivo: {AJUSTES_FILE}")
            print("  Descreva os ajustes e salve. Pressione ENTER quando pronto.")
            input("  [ENTER para continuar]")
            ajustes = _ler_ajustes()

        if not ajustes.strip():
            print("  [!] Nenhum ajuste informado. Voltando ao menu...")
            continue

        print(f"\n  Ajustes recebidos:\n  ──────────────────")
        for linha in ajustes.split("\n"):
            print(f"  › {linha}")
        print()

        try:
            dados_refinados = refinar_json(dados, ajustes)

            # Salvar JSON refinado (sobrescreve o atual)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(dados_refinados, f, ensure_ascii=False, indent=2)

            print(f"  [OK] JSON refinado e salvo.")
            rodada += 1

        except RuntimeError as e:
            print(f"  [ERRO] {e}")
            break

    return json_path


if __name__ == "__main__":
    # Teste: refina o primeiro JSON da pasta
    jsons = [
        os.path.join(PASTA_ENTRADA, f)
        for f in os.listdir(PASTA_ENTRADA)
        if f.endswith(".json") and not f.startswith("_")
    ]
    if not jsons:
        print(f"[!] Nenhum JSON encontrado em {os.path.basename(PASTA_ENTRADA)}/")
        sys.exit(1)
    loop_de_ajustes(jsons[0])
