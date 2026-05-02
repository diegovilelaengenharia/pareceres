import json
import os
import glob

def extrair_chaves(dado, prefixo=""):
    chaves = set()
    if isinstance(dado, dict):
        for k, v in dado.items():
            chaves.add(f"{prefixo}{k}")
            
            # Se for um template que lista campos, adiciona esses campos à lista de chaves conhecidas
            if k in ["campos_obrigatorios", "campos_opcionais"] and isinstance(v, list):
                for campo in v:
                    if isinstance(campo, str):
                        chaves.add(f"{prefixo}{campo}")

            if isinstance(v, dict):
                chaves.update(extrair_chaves(v, f"{prefixo}{k}."))
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                # Para listas de objetos (ex: areas_matriz), pegamos as chaves do primeiro item
                chaves.update(extrair_chaves(v[0], f"{prefixo}{k}[]."))
    return chaves

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, "templates")
    output_file = os.path.join(templates_dir, "_esquema_base.json")
    
    # Chaves base que sempre existem/são válidas
    todas_chaves = {
        "tipo_relatorio", "numero_processo", "data_processo", "assunto",
        "requerente", "paragrafo_abertura", "considerandos", "conclusao",
        "fundamentacao_legal", "documentos_emitir", "paragrafos_adicionais",
        "logradouro", "bairro", "inscricao_municipal", "proprietario",
        "profissional_nome", "profissional_registro", "cidade"
    }
    tipos_disponiveis = []
    
    # Lista de arquivos para ignorar
    ignorar = ["_esquema_base.json", "_esquema_base_bkp.json"]
    
    arquivos = glob.glob(os.path.join(templates_dir, "*.json"))
    
    for arquivo in sorted(arquivos):
        nome_arquivo = os.path.basename(arquivo)
        if nome_arquivo in ignorar:
            continue
            
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
            tipo = dados.get("tipo_relatorio")
            if tipo:
                tipos_disponiveis.append(tipo)
                
            todas_chaves.update(extrair_chaves(dados))
        except Exception as e:
            print(f"Erro ao ler {nome_arquivo}: {e}")

    # Organizar chaves por categorias (heurística baseada no uso atual)
    schema = {
        "_status": "Gerado automaticamente",
        "tipos_disponiveis": sorted(list(set(tipos_disponiveis))),
        "todas_chaves": sorted(list(todas_chaves))
    }
    
    # Preservar descrições se possível? 
    # O plano pede para gerar o arquivo. Vamos manter uma estrutura limpa mas informativa.
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=4, ensure_ascii=False)
        
    print(f"Esquema base atualizado em {output_file}")
    print(f"Total de chaves únicas: {len(todas_chaves)}")
    print(f"Total de tipos: {len(tipos_disponiveis)}")

if __name__ == "__main__":
    main()
