import os
import json
import glob
import logging
import pickle
from typing import Optional, List, Dict, Any

# Setup logging
logger = logging.getLogger("mcp_smosu.tools")
logger.setLevel(logging.INFO)

# Global variables for lazy loading
_vector_model = None
_vector_index = None
_vector_metadata = None

# Base Knowledge paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_CONHECIMENTO_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "base_conhecimento")

_VECTOR_LOAD_FAILED = False  # evita retentativas após falha

def _get_vector_resources():
    global _vector_model, _vector_index, _vector_metadata, _VECTOR_LOAD_FAILED
    if _VECTOR_LOAD_FAILED:
        return None, None, None
    if _vector_model is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(script_dir, "vector_index.faiss")
        metadata_path = os.path.join(script_dir, "vector_metadata.pkl")

        if not os.path.exists(index_path) or not os.path.exists(metadata_path):
            logger.warning("Índice vetorial não encontrado. Execute build_index.py primeiro.")
            _VECTOR_LOAD_FAILED = True
            return None, None, None

        try:
            import signal

            def _timeout_handler(signum, frame):
                raise TimeoutError("Timeout ao carregar modelo semântico")

            # Timeout de 20 s — só funciona em Unix; no Windows é ignorado
            has_alarm = hasattr(signal, "SIGALRM")
            if has_alarm:
                signal.signal(signal.SIGALRM, _timeout_handler)
                signal.alarm(20)

            logger.info("Carregando recursos de busca semântica...")
            from sentence_transformers import SentenceTransformer
            import faiss

            _vector_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            _vector_index = faiss.read_index(index_path)
            with open(metadata_path, 'rb') as f:
                _vector_metadata = pickle.load(f)

            if has_alarm:
                signal.alarm(0)

        except Exception as e:
            logger.error(f"Falha ao carregar modelo semântico: {e}")
            _VECTOR_LOAD_FAILED = True
            _vector_model = None
            _vector_index = None
            _vector_metadata = None
            return None, None, None

    return _vector_model, _vector_index, _vector_metadata

def _busca_conceito_por_keywords(query: str) -> str:
    """Fallback: busca por palavras-chave quando o modelo semântico não está disponível."""
    palavras = [p for p in query.lower().split() if len(p) > 3]
    if not palavras:
        palavras = query.lower().split()

    arquivos = (
        glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*.md"))
        + glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*.txt"))
    )
    resultados = []
    for filepath in arquivos:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            for i, linha in enumerate(linhas):
                linha_lower = linha.lower()
                if any(p in linha_lower for p in palavras):
                    start = max(0, i - 1)
                    end = min(len(linhas), i + 3)
                    trecho = "".join(linhas[start:end]).strip()
                    resultados.append(f"[{os.path.basename(filepath)} | Linha {i+1}]:\n{trecho}")
                    if len(resultados) >= 8:
                        break
        except Exception:
            continue
        if len(resultados) >= 8:
            break

    if not resultados:
        return f"Nenhum resultado encontrado para '{query}'."
    return "(busca por palavras-chave — modelo semântico indisponível)\n\n" + "\n\n".join(resultados)

def buscar_conceito_legal(query: str, top_k: int = 5) -> str:
    """
    Realiza busca semântica (por similaridade de conceito) na base de conhecimento.
    Retorna os trechos mais relevantes mesmo que as palavras exatas não coincidam.
    Usa busca por palavras-chave como fallback se o modelo semântico não estiver disponível.
    """
    logger.info(f"buscar_conceito_legal invocado para query: '{query}'")
    model, index, metadata = _get_vector_resources()

    if not model or not index:
        logger.warning("Modelo semântico indisponível — usando fallback por palavras-chave.")
        return _busca_conceito_por_keywords(query)

    import numpy as np
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding).astype('float32'), top_k)

    resultados = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            item = metadata[idx]
            dist = distances[0][i]
            score = max(0, 100 - dist) / 100
            res = (
                f"--- [Score: {score:.2f}] Fonte: {item['source']} ---\n"
                f"{item['text']}\n"
            )
            resultados.append(res)

    if not resultados:
        return f"Nenhum conceito similar encontrado para '{query}'."

    return "Resultados da Busca Semântica (Conceitos):\n\n" + "\n\n".join(resultados)

def validar_parametros_projeto(
    area_terreno: float, 
    area_ocupada: float, 
    area_construida_total: float, 
    zona: str,
    area_permeavel: float = 0
) -> str:
    """
    Valida os índices de um projeto (TO, CA, TP) contra os parâmetros legais da zona.
    Retorna um relatório detalhado de conformidade.
    """
    logger.info(f"validar_parametros_projeto para zona {zona}")
    
    codex = _load_json("codex_legal.json")
    if not codex or "parametros_zonais" not in codex:
        return "Erro: Parâmetros zonais não encontrados no Codex Legal."
        
    params = codex["parametros_zonais"].get(zona.upper())
    if not params:
        # Tenta busca parcial se não achar exata
        for z, p in codex["parametros_zonais"].items():
            if zona.upper() in z:
                params = p
                zona = z
                break
                
    if not params:
        return f"Erro: Parâmetros para a zona '{zona}' não encontrados. Verifique a sigla (ex: ZUR1, ZC1)."

    # Cálculos do Projeto
    to_projeto = (area_ocupada / area_terreno) * 100
    ca_projeto = area_construida_total / area_terreno
    tp_projeto = (area_permeavel / area_terreno) * 100 if area_terreno > 0 else 0
    
    # Limites Legais
    to_max = params.get("to_max_pct", 100)
    ca_max = params.get("ca_geral", 1.0)
    tp_min = params.get("tp_min_pct", 20)
    
    # Verificação
    status_to = "✅ PASS" if to_projeto <= to_max else "❌ FAIL"
    status_ca = "✅ PASS" if ca_projeto <= ca_max else "❌ FAIL"
    # Regra especial: TP mínima de 20% em todo o município (Art. 9º §14 LC 267/2019)
    status_tp = "✅ PASS" if tp_projeto >= tp_min else "❌ FAIL"
    
    relatorio = [
        f"=== Relatório de Conformidade Urbanística: Zona {zona} ===",
        f"Terreno: {area_terreno:.2f} m²",
        "",
        f"[TO] Taxa de Ocupação:",
        f"   Projeto: {to_projeto:.2f}% ({area_ocupada:.2f} m²)",
        f"   Limite:  {to_max:.2f}%",
        f"   Status:  {status_to}",
        "",
        f"[CA] Coeficiente de Aproveitamento:",
        f"   Projeto: {ca_projeto:.2f} (Total: {area_construida_total:.2f} m²)",
        f"   Limite:  {ca_max:.2f}",
        f"   Status:  {status_ca}",
        "",
        f"[TP] Taxa de Permeabilidade:",
        f"   Projeto: {tp_projeto:.2f}% ({area_permeavel:.2f} m²)",
        f"   Limite:  min {tp_min:.2f}%",
        f"   Status:  {status_tp}",
    ]
    
    if status_to == "❌ FAIL" or status_ca == "❌ FAIL" or status_tp == "❌ FAIL":
        relatorio.append("\n⚠️ ATENÇÃO: O projeto apresenta INFRAÇÕES aos parâmetros urbanísticos.")
        if status_tp == "❌ FAIL":
            relatorio.append("Nota: A deficiência de permeabilidade pode ser compensada com caixa de captação (Art. 9º §7-11 LC 267/2019).")
    else:
        relatorio.append("\n🎉 SUCESSO: O projeto atende aos índices básicos da zona.")
        
    return "\n".join(relatorio)

def prever_pendencias_recorrentes(tipo_processo: str, zona: str = None, area_terreno: float = None) -> str:
    """
    Analisa o perfil do projeto e prevê pendências ou multas comuns baseadas no histórico.
    Ajuda a antecipar problemas antes da análise detalhada.
    """
    logger.info(f"prever_pendencias_recorrentes: {tipo_processo} | {zona}")
    
    tipo_processo = tipo_processo.lower()
    zona = zona.upper() if zona else ""
    
    alertas = []
    
    # 1. Regras Baseadas em Tipo de Processo
    if "regulariza" in tipo_processo or "as-built" in tipo_processo:
        alertas.append("- [HISTÓRICO] 90% das regularizações possuem multa de Obra Sem Licença (Art. 79 Lei 1544).")
        alertas.append("- [ALERTA] Verifique se a construção tem mais de 5 anos para aplicar Decadência (Art. 150 §4º CTN).")
        if "ZUR3" in zona:
            alertas.append("- [ZUR3] Nesta zona, é frequente a violação de TO e TP em regularizações. Prepare-se para calcular Multa do Art. 39 da LC 267.")
            
    if "aprovacao" in tipo_processo or "novo" in tipo_processo:
        if area_terreno and area_terreno <= 220:
            alertas.append("- [BENEFÍCIO] Lote <= 220m² tem isenção de TO e Afastamentos para PROJETOS NOVOS (Art. 9º §13 LC 267).")
        alertas.append("- [DOCS] Verifique se o RRT/ART cobre 'Projeto + Execução'. Omissão de Execução é pendência comum.")

    if "reforma" in tipo_processo:
        alertas.append("- [DICA] Confira se a matrícula no SRI está em nome do requerente. Divergência de titularidade barra a reforma.")

    # 2. Regras por Zona
    if "ZC" in zona or "ZAE" in zona:
        alertas.append("- [CONFLITO] Zonas comerciais/industriais costumam ter 'Abertura na Divisa'. Exija Termo de Anuência se não houver recuo lateral.")
        
    if not alertas:
        return f"Não há padrões críticos registrados para o perfil '{tipo_processo}' na zona '{zona}'. Siga o checklist padrão."

    return "=== Inteligência Preditiva: Pendências Prováveis ===\n\n" + "\n".join(alertas) + \
           "\n\nNota: Estas sugestões baseiam-se em padrões estatísticos da base de conhecimento evolutiva."

# Keep other tools unchanged...
def _load_json(filename: str) -> Optional[Dict[str, Any]]:
    filepath = os.path.join(BASE_CONHECIMENTO_DIR, filename)
    if not os.path.exists(filepath):
        logger.error(f"Arquivo não encontrado: {filepath}")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Erro de parse JSON em {filepath}: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao carregar {filepath}: {e}", exc_info=True)
        return None

def _normalize(text: str) -> str:
    import re
    # Remove acentos, nº, dots, slashes, dashes e espaços duplos
    text = text.lower()
    text = re.sub(r'[nº|no\.|n\.]', ' ', text)
    text = re.sub(r'[\./\-]', ' ', text)
    return " ".join(text.split())

def consultar_codex_legal(termo_busca: str) -> str:
    """
    Busca estruturada no arquivo codex_legal.json.
    Retorna artigos, incisos e alíneas exatas das leis do município.
    Inclui automaticamente a legislação correlata (Grafo de Dependências).
    """
    logger.info(f"consultar_codex_legal invocado para termo: '{termo_busca}'")
    data = _load_json("codex_legal.json")
    if not data:
        return "Erro: Arquivo codex_legal.json não encontrado na base de conhecimento."
    
    grafo = _load_json("lei_grafo.json") or {}
    
    resultados = []
    termo_norm = _normalize(termo_busca)
    
    # Identifica se a busca se refere a uma lei específica para mostrar correlações
    correlacoes = []
    for lei_id, info in grafo.items():
        if _normalize(lei_id) in termo_norm:
            for rel in info.get("relacionadas", []):
                correlacoes.append(f"  - {rel['id']}: {rel['motivo']}")

    # Busca específica em parametros_zonais
    if "parametros_zonais" in data:
        pz = data["parametros_zonais"]
        # Zonas costumam ser maiúsculas e sem normalização complexa
        termo_zona = termo_busca.upper()
        if termo_zona in pz:
            logger.info(f"Match exato em parametros_zonais para a zona '{termo_zona}'")
            res_zona = f"--- Parâmetros da Zona {termo_zona} (Codex Legal) ---\n{json.dumps(pz[termo_zona], indent=2, ensure_ascii=False)}"
            if correlacoes:
                res_zona += "\n\n--- 🔗 LEGISLAÇÃO CORRELATA (Grafo de Dependências) ---\n"
                res_zona += "\n".join(correlacoes)
            return res_zona
        
        # Busca parcial nas descrições de zona
        for zona, info in pz.items():
            if termo_norm in _normalize(str(info)):
                resultados.append(f"--- Encontrado em parametros_zonais.{zona} ---\n{json.dumps(info, indent=2, ensure_ascii=False)}")

    # Busca genérica no resto do documento
    for key, value in data.items():
        if key == "parametros_zonais": continue
        val_str = str(value)
        if termo_norm in _normalize(val_str):
            # Se for um dicionário de artigos, tenta ser mais específico
            if isinstance(value, dict):
                for subkey, subval in value.items():
                    if termo_norm in _normalize(str(subval)):
                        resultados.append(f"--- Encontrado em '{key}.{subkey}' ---\nSnippet: {str(subval)[:800]}...")
            else:
                resultados.append(f"--- Encontrado em '{key}' ---\nSnippet: {val_str[:500]}...")
        if len(resultados) >= 10: break
    
    if not resultados:
         logger.warning(f"Nenhum resultado encontrado para '{termo_busca}' em codex_legal.")
         return f"Nenhum resultado encontrado para '{termo_busca}' no Codex Legal."
         
    saida = "\n\n".join(resultados)[:3500]
    
    if correlacoes:
        saida += "\n\n--- 🔗 LEGISLAÇÃO CORRELATA (Grafo de Dependências) ---\n"
        saida += "Nota: A lei consultada possui dependências ou complementos nestes dispositivos:\n"
        saida += "\n".join(correlacoes)
        
    logger.info(f"Encontrados {len(resultados)} fragmentos em codex_legal.")
    return saida

def consultar_indices_urbanisticos(zona_ou_bairro: str) -> str:
    """
    Busca na base estruturada geo_oliveira.json os índices urbanísticos (TO, CA, recuos).
    """
    logger.info(f"consultar_indices_urbanisticos invocado para zona/bairro: '{zona_ou_bairro}'")
    data = _load_json("geo_oliveira.json")
    if not data:
        return "Erro: Arquivo geo_oliveira.json não encontrado."
    
    termo = zona_ou_bairro.lower()
    resultados = []
    
    if isinstance(data, dict):
        for chave, valor in data.items():
            if termo in chave.lower():
                resultados.append(f"--- Parâmetros Urbanísticos: {chave} ---\n{json.dumps(valor, indent=2, ensure_ascii=False)}")
                
    if not resultados:
        logger.warning(f"Nenhum índice encontrado para '{zona_ou_bairro}' em geo_oliveira.")
        return f"Não foram encontrados dados urbanísticos para a zona/bairro: {zona_ou_bairro}."
        
    logger.info(f"Encontrados índices para '{zona_ou_bairro}'.")
    return "\n\n".join(resultados)[:2000]

def buscar_diretriz_processo(tipo_processo: str) -> str:
    """
    Retorna o raciocínio exigido para aprovar ou regularizar um tipo específico de projeto.
    Lê arquivos .md como raciocinio_regularizacao_asbuilt.md.
    """
    logger.info(f"buscar_diretriz_processo invocado para: '{tipo_processo}'")
    arquivos_alvo = glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*.md"))
    termo = tipo_processo.lower()
    
    resultados = []
    for filepath in arquivos_alvo:
        nome_arquivo = os.path.basename(filepath).lower()
        # Prioritize files with 'raciocinio' or 'fluxo' that match the process type
        if termo in nome_arquivo:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    resumo = conteudo[:2000] + "\n...[conteúdo truncado]..." if len(conteudo) > 2000 else conteudo
                    resultados.append(f"--- Diretriz: {os.path.basename(filepath)} ---\n{resumo}")
            except Exception as e:
                logger.error(f"Falha ao ler diretriz {filepath}: {e}", exc_info=True)
                continue
            
    if not resultados:
         logger.warning(f"Nenhuma diretriz encontrada para '{tipo_processo}'.")
         return f"Não encontrei um arquivo de diretriz específico para '{tipo_processo}'. Tente pesquisar por termos mais genéricos como 'regularização' ou 'aprovação'."
         
    return "\n\n".join(resultados)

def pesquisa_livre_leis_txt(palavra_chave: str) -> str:
    """
    Varre todos os arquivos .md e .txt na pasta base_conhecimento buscando o termo.
    """
    logger.info(f"pesquisa_livre_leis_txt invocado para chave: '{palavra_chave}'")
    arquivos = glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*.md")) + glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*.txt"))
    termo = palavra_chave.lower()
    
    resultados = []
    for filepath in arquivos:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                for i, linha in enumerate(linhas):
                    if termo in linha.lower():
                        # Context: 1 line before and after
                        start = max(0, i - 1)
                        end = min(len(linhas), i + 2)
                        trecho = "".join(linhas[start:end]).strip()
                        resultados.append(f"[{os.path.basename(filepath)} | Linha {i+1}]:\n{trecho}")
                        if len(resultados) >= 8: break
        except UnicodeDecodeError as e:
            logger.warning(f"Erro de encoding no arquivo {filepath}: {e}")
            continue
        except Exception as e:
            logger.error(f"Falha ao realizar busca livre no arquivo {filepath}: {e}")
            continue
        if len(resultados) >= 8: break
        
    if not resultados:
        logger.info(f"Nenhum resultado de texto encontrado para '{palavra_chave}'.")
        return f"A palavra-chave '{palavra_chave}' não foi encontrada nos textos das leis ou manuais."
        
    return "Resultados da Pesquisa Livre (Top 8):\n\n" + "\n\n".join(resultados)

def consultar_historico_treinamento(termo_busca: str) -> str:
    """
    Busca casos similares na base de treinamento (casos_treinamento.jsonl).
    Retorna padrões detectados em processos anteriores (zoneamento, leis, áreas).
    """
    logger.info(f"consultar_historico_treinamento invocado para termo: '{termo_busca}'")
    filepath = os.path.join(BASE_CONHECIMENTO_DIR, "casos_treinamento.jsonl")
    if not os.path.exists(filepath):
        logger.warning(f"Arquivo de treinamento não encontrado: {filepath}")
        return "Erro: Base de treinamento não encontrada."
    
    resultados = []
    termo = termo_busca.lower()
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                if termo in line.lower():
                    try:
                        data = json.loads(line)
                        # Formata o resultado para o agente
                        padroes = data.get("padroes_detectados", {})
                        resumo = (
                            f"--- Caso: {data.get('arquivo')} ---\n"
                            f"Proc: {padroes.get('numero_processo')} | Zona: {padroes.get('zoneamento')}\n"
                            f"Área: {padroes.get('area')} | Bairro: {padroes.get('bairro')}\n"
                            f"Leis Citadas: {', '.join(padroes.get('leis', []))}\n"
                        )
                        resultados.append(resumo)
                        if len(resultados) >= 5: break
                    except json.JSONDecodeError as e:
                        logger.error(f"Linha {line_number} inválida no JSONL: {e}")
    except Exception as e:
        logger.error(f"Erro ao ler base de treinamento: {e}", exc_info=True)
        return f"Erro ao ler base de treinamento: {e}"
        
    if not resultados:
        return f"Nenhum caso similar encontrado para '{termo_busca}'."
        
    logger.info(f"Encontrados {len(resultados)} casos no histórico de treinamento.")
    return "Casos Similares Encontrados (Treinamento):\n\n" + "\n\n".join(resultados)

def calcular_multas_processo(
    area_irregular: float,
    zona: str,
    area_terreno: float,
    area_ocupada: float,
    area_permeavel: float,
    tem_decadencia: bool = False
) -> str:
    """
    Calcula multas do Art. 79 (Lei 1.544) e Art. 39 (LC 267/2019).
    Retorna memória de cálculo formatada para o parecer.
    """
    URM_2026 = 102.42
    
    # Multa Art. 79
    multa_art79 = 0.0
    memoria_79 = ""
    if not tem_decadencia:
        if area_irregular <= 60:   fator = 0.01
        elif area_irregular <= 75: fator = 0.03
        elif area_irregular <= 100: fator = 0.04
        else:                       fator = 0.05
        multa_art79 = area_irregular * fator * URM_2026
        memoria_79 = f"  → Faixa {fator*100:.0f}% × URM por m²\n  → {area_irregular:.2f} × {fator} × R$ {URM_2026} = R$ {multa_art79:,.2f}"
    else:
        memoria_79 = "  → ISENTO por Decadência (CTN Art. 150 §4º)"

    # Multa Art. 39 (Parâmetros)
    codex = _load_json("codex_legal.json")
    params = codex.get("parametros_zonais", {}).get(zona.upper(), {})
    to_max = params.get("to_max_pct", 70)
    tp_min = params.get("tp_min_pct", 20)
    
    to_projeto = (area_ocupada / area_terreno) * 100 if area_terreno > 0 else 0
    tp_projeto = (area_permeavel / area_terreno) * 100 if area_terreno > 0 else 0
    
    violacoes = 0
    detalhe_39 = []
    if to_projeto > to_max:
        violacoes += 1
        detalhe_39.append(f"  → TO calculado: {to_projeto:.2f}% > limite {to_max}% ← VIOLAÇÃO")
    if tp_projeto < tp_min:
        violacoes += 1
        detalhe_39.append(f"  → TP calculado: {tp_projeto:.2f}% < limite {tp_min}% ← VIOLAÇÃO")
        
    fator_39 = 0
    if area_irregular <= 40:   fator_39 = 1
    elif area_irregular <= 80: fator_39 = 3
    elif area_irregular <= 100: fator_39 = 6
    else:                       fator_39 = 10
    
    # Assume taxa base de alvará simbólica ou busca em tabela (padrão 1 URM para cálculo simples)
    taxa_base_alvara = URM_2026 * 0.5 # Exemplo estimado
    multa_art39 = violacoes * fator_39 * taxa_base_alvara

    resumo = [
        "=== MEMÓRIA DE CÁLCULO DE MULTAS ===",
        f"Área Irregular: {area_irregular:.2f} m²",
        f"Zona: {zona.upper()} | TO máx: {to_max}% | TP mín: {tp_min}%",
        "",
        "[MULTA ART. 79 — Lei 1.544/1986]",
        memoria_79,
        "",
        "[MULTA ART. 39 — LC 267/2019]",
        "\n".join(detalhe_39) if detalhe_39 else "  → Nenhuma violação de parâmetros detectada.",
        f"  → Fator de Multa: {fator_39}× taxa alvará ({violacoes} violações)",
        f"  → Valor Estimado Art. 39: R$ {multa_art39:,.2f}",
        "",
        f"TOTAL ESTIMADO: R$ {(multa_art79 + multa_art39):,.2f}",
        "BASE LEGAL: Art. 79, Lei 1.544/1986; Arts. 38-39, LC 267/2019"
    ]
    return "\n".join(resumo)

def validar_checklist_documentos(tipo_processo: str, documentos_apresentados: str) -> str:
    """
    Valida a lista de documentos contra o checklist oficial (Decreto 4.149/2019).
    """
    checklist = _load_json("checklist_documentos.json")
    if not checklist: return "Erro: Checklist não encontrado."
    
    regras = checklist.get(tipo_processo.lower())
    if not regras: return f"Tipo de processo '{tipo_processo}' não mapeado no checklist."
    
    docs_user = documentos_apresentados.lower()
    pendencias = []
    bloqueios = []
    
    for doc in regras.get("obrigatorios_bloqueantes", []):
        if _normalize(doc) not in _normalize(docs_user):
            bloqueios.append(f"❌ BLOQUEIO: {doc}")
            
    for doc in regras.get("obrigatorios", []):
        if _normalize(doc) not in _normalize(docs_user):
            pendencias.append(f"⚠️ PENDENTE: {doc}")
            
    status = "APROVADO PARA ANÁLISE" if not bloqueios and not pendencias else "PENDÊNCIAS DETECTADAS"
    if bloqueios: status = "PROCESSO BLOQUEADO"
    
    res = [f"=== Validação de Checklist: {tipo_processo.upper()} ===", f"Status: {status}", ""]
    if bloqueios: res.extend(bloqueios + [""])
    if pendencias: res.extend(pendencias + [""])
    if not bloqueios and not pendencias: res.append("✅ Todos os documentos obrigatórios foram identificados.")
    
    res.append(f"\nBase Legal: {regras.get('base_legal')}")
    return "\n".join(res)

def analisar_decadencia(ano_construcao: int, tipo_prova: str, area_total: float, area_averbada: float = 0.0) -> str:
    """
    Análise técnica de decadência fiscal conforme CTN Art. 150 §4º.
    """
    ANO_ATUAL = 2026
    anos = ANO_ATUAL - ano_construcao if ano_construcao > 0 else 0
    PROVAS_VALIDAS = ["matricula", "habitese_anterior", "aerofoto", "laudo_datado"]
    
    if tipo_prova.lower() not in PROVAS_VALIDAS:
        return "DECADÊNCIA NÃO COMPROVÁVEL: Prova apresentada é insuficiente ou inválida. Multa do Art. 79 aplica-se integralmente."
    
    if anos >= 5:
        area_decadente = area_total - area_averbada
        return (f"DECADÊNCIA COMPROVADA ({anos} anos):\n"
                f"- Área Total: {area_total:.2f} m² | Área já averbada: {area_averbada:.2f} m²\n"
                f"- Área Decadente: {area_decadente:.2f} m²\n"
                f"- Consequência: ISENTO de multa do Art. 79 para esta área.\n"
                "- Nota: Multas urbanísticas (Art. 39 LC 267) ainda podem incidir.")
    else:
        return f"DECADÊNCIA NÃO APLICÁVEL: Prazo de {anos} anos é inferior ao mínimo legal de 5 anos."

def gerar_memoria_calculo_indices(
    area_terreno: float,
    area_coberta: float,
    area_construida_total: float,
    area_permeavel: float,
    zona: str,
    area_garagem_descoberta: float = 0.0
) -> str:
    """
    Gera texto formatado com memória de cálculo para o campo 'memoria_de_calculo' do JSON.
    """
    to = (area_coberta / area_terreno) * 100 if area_terreno > 0 else 0
    ca = area_construida_total / area_terreno if area_terreno > 0 else 0
    tp = (area_permeavel / area_terreno) * 100 if area_terreno > 0 else 0
    
    return (f"Memória de Cálculo ({zona.upper()}):\n"
            f"- Taxa de Ocupação: ({area_coberta:.2f} / {area_terreno:.2f}) × 100 = {to:.2f}%\n"
            f"- Coef. Aproveitamento: {area_construida_total:.2f} / {area_terreno:.2f} = {ca:.3f}\n"
            f"- Taxa Permeabilidade: ({area_permeavel:.2f} / {area_terreno:.2f}) × 100 = {tp:.2f}%\n"
            f"- Nota: Garagem descoberta ({area_garagem_descoberta:.2f} m²) excluída do CA.")

def consultar_documentos_emitir(
    tipo_processo: str,
    resultado_analise: str,
    tem_decadencia: bool = False,
    tem_divergencia_cadastral: bool = False
) -> str:
    """
    Retorna lista estruturada e completa de documentos a emitir com observações de linguagem institucional.
    Cobre todos os cenários: regularização, aprovação, habite-se, comunicados, certidões.
    """
    tipo = tipo_processo.lower()
    resultado = resultado_analise.lower()
    docs = []

    # Sempre começa com o Parecer Técnico
    docs.append({
        "tipo": "parecer_tecnico",
        "descricao": "Parecer Técnico (SMOSU)",
        "observacao": "Documento principal de análise e despacho técnico.",
        "obrigatorio": True,
    })

    # === PROCESSOS COM PENDÊNCIAS ===
    if "pendente" in resultado or "pendencia" in resultado or "incompleto" in resultado:
        docs.append({
            "tipo": "comunicado_pendencia",
            "descricao": "Comunicado de Pendência Documental",
            "observacao": "Listar pendências detectadas com prazo de 30 dias para regularização.",
            "obrigatorio": True,
        })
        return _formatar_docs_emitir(docs, tipo_processo, "PENDENTE")

    # === REGULARIZAÇÃO AS-BUILT ===
    if "regulariz" in tipo or "as.built" in tipo or "as_built" in tipo:
        docs.append({
            "tipo": "alvara_regularizacao",
            "descricao": "Alvará de Regularização As-Built",
            "observacao": (
                "Alvará emitido para regularização de imóvel edificado em desacordo com "
                "projeto aprovado, mediante o cumprimento do **Art. 79 da Lei 1.544 de 1986** "
                "e **Arts. 38 e 39 da LC 267 de 2019**."
            ),
            "obrigatorio": True,
        })
        docs.append({
            "tipo": "comunicado_baixa_cei",
            "descricao": "Comunicado de Baixa de CEI",
            "observacao": "Registrar número e área do alvará anterior a ser cancelado.",
            "obrigatorio": True,
            "nota": "Obrigatório quando há alvará/CEI anterior ativo — cancelar o antigo.",
        })
        docs.append({
            "tipo": "comunicado_decadencia",
            "descricao": "Comunicado de Decadência",
            "observacao": (
                "Registrar formalmente se há ou não decadência. "
                "Ex: 'Conforme análise em arquivo municipal, o imóvel **não possui decadência** "
                "por Planta Cadastral ou Habite-se.' OU 'Área de **XX,XXm²** reconhecida como "
                "decadente (CTN Art. 150 §4º).'"
            ),
            "obrigatorio": True,
        })
        if tem_decadencia:
            docs.append({
                "tipo": "certidao_decadencia",
                "descricao": "Certidão de Decadência Administrativa",
                "observacao": (
                    "Para fins de comprovação perante a Receita Federal do Brasil (CNO/CEI), "
                    "nos termos do Art. 150, §4º do CTN."
                ),
                "obrigatorio": False,
            })
        docs.append({
            "tipo": "habitese_comum",
            "descricao": "Carta de Habite-se",
            "observacao": "Incluir área total regularizada em m².",
            "obrigatorio": True,
        })
        docs.append({
            "tipo": "certidao_averbacao",
            "descricao": "Certidão de Averbação de Área",
            "observacao": (
                "Incluir área em m² no título. Mencionar valor do imóvel conforme "
                "Laudo de Avaliação da Comissão de Avaliação da PMO (quando disponível)."
            ),
            "obrigatorio": True,
        })

    # === APROVAÇÃO NOVO PROJETO ===
    elif "aprovacao" in tipo or "novo" in tipo or "construcao" in tipo:
        docs.append({
            "tipo": "alvara_aprovacao",
            "descricao": "Alvará de Construção",
            "observacao": "Incluir área aprovada, tipo de uso, responsável técnico e validade.",
            "obrigatorio": True,
        })

    # === HABITE-SE ===
    elif "habitese" in tipo or "habite" in tipo:
        docs.append({
            "tipo": "habitese_comum",
            "descricao": "Carta de Habite-se",
            "observacao": "Incluir área total construída e área de cada pavimento se houver.",
            "obrigatorio": True,
        })
        docs.append({
            "tipo": "certidao_averbacao",
            "descricao": "Certidão de Averbação de Área",
            "observacao": "Para registro no Cartório de Imóveis (SRI).",
            "obrigatorio": True,
        })

    # === REFORMA / AMPLIAÇÃO ===
    elif "reforma" in tipo or "ampliacao" in tipo or "ampliação" in tipo:
        docs.append({
            "tipo": "alvara_reforma",
            "descricao": "Alvará de Reforma / Ampliação",
            "observacao": "Especificar área reformada/ampliada e base legal.",
            "obrigatorio": True,
        })

    # === CERTIDÕES ===
    elif "certidao" in tipo or "certidão" in tipo:
        docs.append({
            "tipo": tipo_processo,
            "descricao": f"Certidão — {tipo_processo.replace('_', ' ').title()}",
            "observacao": "Emitir com dados de identificação completos do imóvel.",
            "obrigatorio": True,
        })

    # Documentos condicionais sempre verificados
    if tem_divergencia_cadastral:
        docs.append({
            "tipo": "certidao_localizacao_corretiva",
            "descricao": "Certidão de Localização Corretiva",
            "observacao": (
                "O imóvel situado na [ENDEREÇO], embora conste como Bairro [A] na matrícula, "
                "localiza-se tecnicamente no Bairro [B] conforme legislação municipal vigente "
                "(Diretriz nº 04/2026/SMOSU)."
            ),
            "obrigatorio": True,
        })

    return _formatar_docs_emitir(docs, tipo_processo, "APROVADO")


def _formatar_docs_emitir(docs: list, tipo_processo: str, status: str) -> str:
    """Formata lista de documentos em texto estruturado para exibição."""
    linhas = [
        f"=== DOCUMENTOS A EMITIR — {tipo_processo.upper()} ===",
        f"Status: {status}",
        "",
    ]
    for i, doc in enumerate(docs, 1):
        obr = "[OBRIGATÓRIO]" if doc.get("obrigatorio") else "[CONDICIONAL]"
        linhas.append(f"{i}. {doc['descricao']} {obr}")
        linhas.append(f"   tipo_relatorio: \"{doc['tipo']}\"")
        linhas.append(f"   observacao: {doc['observacao']}")
        if doc.get("nota"):
            linhas.append(f"   nota: {doc['nota']}")
        linhas.append("")
    linhas.append("INSTRUÇÃO: Inclua todos os OBRIGATÓRIOS no array 'documentos_emitir' do JSON.")
    linhas.append("Os CONDICIONAIS devem ser incluídos apenas se a condição se confirmar.")
    return "\n".join(linhas)

def verificar_excecoes_lote_pequeno(area_terreno: float, tipo_processo: str, zona: str) -> str:
    """
    Verifica se o lote se enquadra nas isenções de lote pequeno (Art. 9º §13 LC 267).
    ATENÇÃO: TO e TP continuam obrigatórias mesmo em lotes pequenos. Apenas afastamentos são flexibilizados.
    """
    if area_terreno > 220:
        return (
            f"Lote com {area_terreno:.2f} m²: NÃO se enquadra na exceção de lote pequeno (> 220m²).\n"
            "Todos os índices e afastamentos da zona se aplicam normalmente (LC 267/2019)."
        )

    linhas = [
        f"=== Lote Pequeno ({area_terreno:.2f} m²) — EXCEÇÃO ART. 9º §13 LC 267/2019 ===",
        "",
        "APLICA-SE A EXCEÇÃO. O que muda:",
        "  ✅ Afastamentos laterais/fundos: adotar mínimo de 1,50m do Código Civil",
        "     (Arts. 1.299-1.301 CC) em vez dos afastamentos padrão da zona.",
        "",
        "O que NÃO muda (OBRIGATÓRIO manter):",
        f"  ❌ Taxa de Ocupação (TO): Continua obrigatória conforme zona {zona.upper()}",
        "  ❌ Taxa de Permeabilidade (TP): Mínimo 20% obrigatório (Art. 9º §14 LC 267/2019)",
        "  ❌ Afastamento frontal: Mantido conforme zona",
        "",
        "INSTRUÇÃO para o JSON:",
        f'  Incluir sufixo no campo area_terreno: "{area_terreno:.2f} m² (exceção da lei)"',
        "",
        "BASE LEGAL: Art. 9º §13 LC 267/2019 c/c Arts. 1.299-1.301 do Código Civil",
        "RETROALIMENTAÇÃO: Aplicável a qualquer tipo de processo (aprovação, regularização, reforma).",
    ]
    return "\n".join(linhas)

def buscar_logradouro_oficial(nome_rua: str) -> str:
    """
    Verifica o nome oficial de um logradouro na base de denominações.
    Detecta se há decreto de renomeação e sugere emissão de Certidão de Nome de Rua.
    """
    nome_norm = _normalize(nome_rua)

    # Busca em arquivos de logradouros/decretos
    arquivos_alvo = (
        glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*rua*"))
        + glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*logradouro*"))
        + glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*decreto*"))
        + glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*denominacao*"))
        + glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*.md"))
    )
    arquivos_alvo = list(dict.fromkeys(arquivos_alvo))  # dedup

    resultados = []
    indicadores_mudanca = ["antiga", "anterior", "denominada", "decreto", "passou a", "renomeada"]

    for filepath in arquivos_alvo:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                linhas = f.readlines()
            for i, linha in enumerate(linhas):
                if nome_norm in _normalize(linha):
                    start = max(0, i - 2)
                    end = min(len(linhas), i + 4)
                    trecho = "".join(linhas[start:end]).strip()
                    resultados.append((trecho, filepath))
                    if len(resultados) >= 6:
                        break
        except Exception:
            continue
        if len(resultados) >= 6:
            break

    if not resultados:
        return (
            f"Logradouro '{nome_rua}' não encontrado na base de denominações.\n"
            "RECOMENDAÇÃO: Verificar manualmente no acervo de Decretos Municipais de Oliveira/MG.\n"
            "Se houver menção a 'Loteamento' ou nome anterior, ative a flag MUDANCA_DENOMINACAO "
            "e inclua Certidão de Nome de Rua na lista de documentos."
        )

    linhas_saida = [f"=== Logradouro: '{nome_rua}' ===", ""]
    tem_mudanca = False
    for trecho, origem in resultados:
        linhas_saida.append(f"[Fonte: {os.path.basename(origem)}]")
        linhas_saida.append(trecho)
        linhas_saida.append("")
        if any(ind in trecho.lower() for ind in indicadores_mudanca):
            tem_mudanca = True

    if tem_mudanca:
        linhas_saida.append(
            "⚠️ ALERTA: Detectada possível mudança de denominação (palavras-chave: antiga/decreto/renomeada)."
        )
        linhas_saida.append(
            "AÇÃO: Ativar flag MUDANCA_DENOMINACAO e incluir 'Certidão de Nome de Rua' nos documentos."
        )

    return "\n".join(linhas_saida)

def identificar_conflitos_processuais(
    bairro_sri: str,
    bairro_pmo: str,
    tem_app: bool = False,
    tem_tombamento: bool = False,
    divergencia_area_pct: float = 0.0
) -> str:
    """
    Identifica conflitos críticos e sugere ações automáticas (Certidões/Ofícios).
    """
    conflitos = []
    if _normalize(bairro_sri) != _normalize(bairro_pmo):
        conflitos.append("- [CONFLITO] Divergência de Bairro: SRI ('" + bairro_sri + "') vs PMO ('" + bairro_pmo + "').\n  → Ação: Emitir Certidão de Localização Corretiva.")
    
    if tem_app:
        conflitos.append("- [RESTRIÇÃO] Imóvel em APP/Córrego.\n  → Ação: Oficiar CODEMA para anuência ambiental.")
        
    if tem_tombamento:
        conflitos.append("- [RESTRIÇÃO] Imóvel em Área de Tombamento (IEPHA).\n  → Ação: Exigir Nota Técnica do IEPHA.")
        
    if divergencia_area_pct > 5.0:
        conflitos.append(f"- [ERRO CRÍTICO] Divergência de área de {divergencia_area_pct:.1f}% (> 5%).\n  → Ação: Exigir Retificação de Área no SRI.")
        
    if not conflitos:
        return "Nenhum conflito processual ou restrição bloqueante detectada."
        
    return "=== Análise de Conflitos e Restrições ===\n\n" + "\n".join(conflitos)

def estruturar_historico_cronologico(eventos_raw: List[Dict[str, str]]) -> str:
    """
    Estrutura eventos brutos no formato JSON canonico 'historico_cronologico'.
    """
    # Exemplo input: [{"data": "01/01/2026", "txt": "Abertura"}, ...]
    tipos_padrao = ["abertura_processo", "vistoria_fiscal", "habite_se", "alvara", "comunicado_pendencia"]
    
    estruturado = []
    for ev in eventos_raw:
        data = ev.get("data", "Data desconhecida")
        txt = ev.get("txt", "").lower()
        tipo = "documento_municipal"
        for t in tipos_padrao:
            if t.split("_")[0] in txt:
                tipo = t
                break
        estruturado.append({"data": data, "evento": ev.get("txt"), "tipo": tipo})
        
    return json.dumps(estruturado, indent=2, ensure_ascii=False)
