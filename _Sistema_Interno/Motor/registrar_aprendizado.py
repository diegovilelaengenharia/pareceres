#!/usr/bin/env python3
"""
Registrador de Aprendizado — Sistema GEM SMOSU
===============================================
Uso:
  python registrar_aprendizado.py               # detecta o JSON mais recente em _engine/json/
  python registrar_aprendizado.py meu_processo.json  # usa arquivo específico

O script:
  1. Lê o JSON do último parecer gerado
  2. Detecta padrões e flags automaticamente
  3. Arquiva o JSON em historico_pareceres/ com timestamp
  4. Atualiza historico_memoria_gem.md
  5. Atualiza padroes_recorrentes.md
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
JSON_DIR = BASE_DIR / "json"
HISTORICO_DIR = BASE_DIR / "historico_pareceres"
CONHECIMENTO_DIR = BASE_DIR / "_base_conhecimento"
HISTORICO_MEM = CONHECIMENTO_DIR / "historico_memoria_gem.md"
PADROES_FILE = CONHECIMENTO_DIR / "padroes_recorrentes.md"

HISTORICO_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Detecção de flags e padrões
# ---------------------------------------------------------------------------

FLAG_RULES = {
    "ISENCAO_LOTE_PEQUENO": ["Art. 15", "220m²", "isento", "isenção", "lote pequeno"],
    "MULTA_ART79": ["Art. 79", "sem licença", "sem alvará", "obra irregular"],
    "MULTA_ART80": ["Art. 80", "desacordo com projeto", "desacordo com o projeto"],
    "MULTA_ART82": ["Art. 82", "demolição sem licença"],
    "DECADENCIA_CTN": ["Art. 150", "decadência", "decadencia", "5 anos", "cinco anos"],
    "QUESTAO_AMBIENTAL": ["CODEMA", "APP", "mata ciliar", "curso d", "ribeirão", "oficio_meio_ambiente"],
    "ABERTURA_DIVISA": ["anuência", "anuencia", "lindeiro", "1,50m", "Art. 43", "divisa"],
    "MODO_CONDICIONADO": ["condicionado", "condicionante", "pendente de entrega", "condicoes_pendentes"],
    "CAMPOS_PENDENTES": ["⚠️ VERIFICAR"],
    "HABITE_SE": ["habite-se", "habitese", "habitação", "conclusão de obra"],
    "REGULARIZACAO_AS_BUILT": ["as built", "as-built", "regularização", "regularizacao", "já construída"],
}


def detect_flags(data: dict) -> list[str]:
    """Detecta flags de padrão com base no conteúdo do JSON."""
    all_text = json.dumps(data, ensure_ascii=False).lower()
    found = []
    for flag, keywords in FLAG_RULES.items():
        if any(kw.lower() in all_text for kw in keywords):
            found.append(flag)
    return found


def extract_zone(data: dict) -> str:
    """Tenta identificar a zona urbanística citada no JSON."""
    all_text = json.dumps(data, ensure_ascii=False)
    for zona in ["ZUR1", "ZUR2", "ZUR3", "ZCRE", "OCRE", "ZIND", "ZAE", "ZC"]:
        if zona in all_text:
            return zona
    return "NÃO IDENTIFICADA"


def extract_area_m2(text: str) -> float | None:
    """Extrai o primeiro número decimal de uma string de área."""
    cleaned = text.replace(".", "").replace(",", ".")
    match = re.search(r"\d+\.\d+", cleaned)
    if match:
        return float(match.group())
    match = re.search(r"\d+", cleaned)
    return float(match.group()) if match else None


# ---------------------------------------------------------------------------
# Busca do JSON de entrada
# ---------------------------------------------------------------------------

def find_latest_json() -> Path:
    """Encontra o JSON modificado mais recentemente em _engine/json/."""
    jsons = [f for f in JSON_DIR.glob("*.json") if f.is_file()]
    if not jsons:
        raise FileNotFoundError(f"Nenhum arquivo .json encontrado em {JSON_DIR}")
    return max(jsons, key=lambda f: f.stat().st_mtime)


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Arquivamento
# ---------------------------------------------------------------------------

def archive_json(source: Path, data: dict) -> str:
    """Salva cópia timestampada do JSON em historico_pareceres/."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    processo = data.get("numero_processo", "SEM_NUMERO")
    processo_slug = re.sub(r"[^a-zA-Z0-9]", "_", str(processo))
    tipo = data.get("tipo_relatorio", "desconhecido")
    dest_name = f"{timestamp}_{processo_slug}_{tipo}.json"
    dest_path = HISTORICO_DIR / dest_name
    dest_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return dest_name


# ---------------------------------------------------------------------------
# Geração de entrada no histórico
# ---------------------------------------------------------------------------

def format_case_entry(data: dict, flags: list, zone: str, archived_name: str, lesson: str | None) -> str:
    """Formata o registro do caso para historico_memoria_gem.md."""
    now = datetime.now().strftime("%d/%m/%Y")
    tipo = data.get("tipo_relatorio", "N/A")
    processo = data.get("numero_processo", "N/A")
    requerente = data.get("requerente", "N/A")
    logradouro = data.get("logradouro", "N/A")
    bairro = data.get("bairro", "N/A")
    area_terreno = data.get("area_terreno", "N/A")
    area_construida = data.get("area_total_construida", "N/A")
    flags_str = " | ".join(flags) if flags else "NENHUM"
    gem_lesson = data.get("licao_aprendida", "")

    lines = [
        f"\n---\n",
        f"### [{now}] Processo {processo} — {requerente}",
        f"- **Tipo:** `{tipo}` | **Zona:** `{zone}`",
        f"- **Endereço:** {logradouro}, {bairro}",
        f"- **Terreno:** {area_terreno} | **Construído:** {area_construida}",
        f"- **Flags detectadas:** {flags_str}",
        f"- **Arquivo:** `historico_pareceres/{archived_name}`",
    ]

    # Lições automáticas por flag
    flag_lessons = {
        "ISENCAO_LOTE_PEQUENO": "Lote ≤220m² — isenção do Art. 15 LC 267/2019 aplicada. Não cobrar TO ou permeabilidade.",
        "MULTA_ART79": "Multa Art. 79 incidida. Verificar se memorial de cálculo (valor em R$) consta no considerando.",
        "DECADENCIA_CTN": "Decadência do Art. 150 §4º CTN reconhecida. Exige comprovação de +5 anos via satélite/aerofoto.",
        "QUESTAO_AMBIENTAL": "APP ou curso d'água envolvido. oficio_meio_ambiente deve ser condicionante obrigatório.",
        "ABERTURA_DIVISA": "Abertura < 1,50m da divisa. Termo de Anuência do lindeiro obrigatório (Art. 43 Lei 1.544).",
        "CAMPOS_PENDENTES": "Campos com ⚠️ VERIFICAR presentes. Revisar manualmente antes de emitir documento.",
        "MODO_CONDICIONADO": "Parecer condicionado — emissão sujeita à entrega dos documentos listados em condicoes_pendentes.",
        "REGULARIZACAO_AS_BUILT": "As Built regularizado. Sempre verificar cronologia da obra para aplicar decadência ou multa.",
    }

    for flag, msg in flag_lessons.items():
        if flag in flags:
            lines.append(f"- 💡 **Lição [{flag}]:** {msg}")

    # Lição registrada pelo GEM
    if gem_lesson and gem_lesson != "(OPCIONAL":
        lines.append(f"- 🤖 **Lição do GEM:** {gem_lesson}")

    # Lição manual do engenheiro
    if lesson:
        lines.append(f"- 📝 **Nota do Engenheiro:** {lesson}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Atualização de padrões recorrentes
# ---------------------------------------------------------------------------

def update_padroes(data: dict, flags: list, zone: str) -> None:
    """Registra o caso em padroes_recorrentes.md organizado por tipo."""
    tipo = data.get("tipo_relatorio", "desconhecido")
    bairro = data.get("bairro", "N/A")
    processo = data.get("numero_processo", "N/A")
    now = datetime.now().strftime("%d/%m/%Y")

    content = PADROES_FILE.read_text(encoding="utf-8") if PADROES_FILE.exists() else _padroes_template()

    flags_str = ", ".join(flags) if flags else "nenhum"
    new_entry = f"\n  - [{now}] Proc.{processo} | Zona {zone} | Bairro: {bairro} | Flags: {flags_str}"

    section_marker = f"### `{tipo}`"
    if section_marker in content:
        content = content.replace(section_marker, section_marker + new_entry, 1)
    else:
        content += f"\n\n{section_marker}{new_entry}\n"

    PADROES_FILE.write_text(content, encoding="utf-8")


def _padroes_template() -> str:
    return """# Padrões Recorrentes — Base de Conhecimento Evolutiva

> Arquivo gerado e atualizado automaticamente por `registrar_aprendizado.py`.
> Lido pelo GEM como base de referência para antecipar problemas.

---

## 📌 Como Interpretar
Cada seção agrupa casos por tipo de relatório. Os flags detectados revelam
padrões operacionais (ex: quase todos os As Built da ZUR3 têm MULTA_ART79).

---

## Casos por Tipo de Relatório
"""


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------

def main() -> None:
    SEP = "=" * 62
    print(f"\n{SEP}")
    print("  REGISTRADOR DE APRENDIZADO — GEM SMOSU / OLIVEIRA-MG")
    print(SEP)

    # 1. Localizar JSON de entrada
    if len(sys.argv) > 1:
        source = Path(sys.argv[1])
        if not source.exists():
            print(f"\n❌ Arquivo não encontrado: {source}")
            sys.exit(1)
    else:
        print("\n🔍 Detectando JSON mais recente em _engine/json/ ...")
        try:
            source = find_latest_json()
            print(f"   → Encontrado: {source.name}")
        except FileNotFoundError as e:
            print(f"\n❌ {e}")
            print("   Uso: python registrar_aprendizado.py <caminho.json>")
            sys.exit(1)

    # 2. Carregar e validar
    print(f"\n📋 Lendo: {source.name}")
    try:
        data = load_json(source)
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON inválido: {e}")
        sys.exit(1)

    tipo = data.get("tipo_relatorio", "N/A")
    processo = data.get("numero_processo", "N/A")
    requerente = data.get("requerente", "N/A")
    print(f"   → Processo: {processo}")
    print(f"   → Tipo:     {tipo}")
    print(f"   → Requerente: {requerente}")

    # 3. Análise de padrões
    flags = detect_flags(data)
    zone = extract_zone(data)
    print(f"\n🏷️  Zona detectada: {zone}")
    print(f"🚩 Flags detectadas: {', '.join(flags) if flags else 'nenhuma'}")

    # 4. Lição manual opcional
    lesson = None
    print("\n📝 Deseja registrar uma nota manual sobre este processo?")
    print("   (Pressione Enter para pular)")
    try:
        user_input = input("   Nota: ").strip()
        if user_input:
            lesson = user_input
    except (EOFError, KeyboardInterrupt):
        pass

    # 5. Executar atualizações
    print("\n💾 Arquivando JSON...")
    archived = archive_json(source, data)
    print(f"   → Salvo: historico_pareceres/{archived}")

    print("\n📚 Atualizando historico_memoria_gem.md...")
    entry = format_case_entry(data, flags, zone, archived, lesson)
    existing = HISTORICO_MEM.read_text(encoding="utf-8") if HISTORICO_MEM.exists() else ""
    HISTORICO_MEM.write_text(existing + entry, encoding="utf-8")
    print("   ✅ Histórico atualizado.")

    print("\n📊 Atualizando padroes_recorrentes.md...")
    update_padroes(data, flags, zone)
    print("   ✅ Padrões atualizados.")

    # 6. Resumo final
    print(f"\n{SEP}")
    print(f"  ✅ CONCLUÍDO — Processo {processo} registrado.")
    print(f"  → {len(flags)} padrão(ões) detectado(s):")
    for f in flags:
        print(f"     • {f}")
    print(f"\n  Próximo passo: abra historico_memoria_gem.md para")
    print(f"  confirmar o registro e adicionar notas se necessário.")
    print(SEP + "\n")


if __name__ == "__main__":
    main()
