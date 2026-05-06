class DecisionTree:
    """
    Árvore de Decisão Automática (Pilar 3 - A).
    Avalia regras de negócio para processos da engenharia/PMO e retorna a recomendação.
    """
    def __init__(self):
        # A árvore será expandida com SQLite (Sprint 2) e Calculadora Completa (Sprint 4)
        pass

    def evaluate(self, dados: dict, tipo_processo: str) -> dict:
        """
        Avalia as regras lógicas estritas para os 5 tipos de processos mais comuns.
        Retorna {"recomendacao": "APROVADO"|"PENDENCIA"|"INDEFERIDO", "motivo": str}
        """
        # Trata o caso do dict ser None
        if not dados:
            dados = {}
            
        recomendacao = "INDEFINIDO"
        motivo = "Tipo de processo não mapeado pela árvore de decisão."
        
        # Mapeamento para os 5 tipos prioritários
        if "alvara" in tipo_processo and "regularizacao" not in tipo_processo:
            return self._evaluate_alvara(dados, regularizacao=False)
            
        elif tipo_processo == "alvara_regularizacao" or "regularizacao" in tipo_processo:
            return self._evaluate_alvara(dados, regularizacao=True)
            
        elif "habitese" in tipo_processo:
            return self._evaluate_habitese(dados)
            
        elif "certidao_localizacao" in tipo_processo:
            return {
                "recomendacao": "APROVADO", 
                "motivo": "Certidão baseada em mapa aprovado. Emissão autorizada."
            }
            
        elif "pendencia" in tipo_processo:
            return {
                "recomendacao": "PENDENCIA", 
                "motivo": "Processo tipificado nativamente como comunicado de pendência."
            }
            
        return {"recomendacao": recomendacao, "motivo": motivo}

    def _evaluate_alvara(self, dados: dict, regularizacao=False) -> dict:
        """Avaliação de índices urbanísticos básicos para Alvará."""
        to_str = dados.get("taxa_ocupacao", "0")
        tp_str = dados.get("taxa_permeabilidade", "0")
        
        try:
            to_val = float(str(to_str).replace('%', '').replace(',', '.'))
            tp_val = float(str(tp_str).replace('%', '').replace(',', '.'))
        except ValueError:
            return {
                "recomendacao": "PENDENCIA", 
                "motivo": "Índices urbanísticos (TO/TP) ausentes ou inválidos para avaliação automática."
            }
            
        motivos = []
        aprovado = True
        
        # Regras de negócio (exemplo genérico, será substituído pelos limites do Zoneamento no Sprint 4)
        if to_val > 70.0:
            if regularizacao:
                motivos.append(f"Taxa de Ocupação ({to_val}%) acima de 70% sujeita a multa de regularização.")
            else:
                aprovado = False
                motivos.append(f"Taxa de Ocupação ({to_val}%) excede limite padrão de 70% para obra nova.")
                
        if tp_val < 20.0:
            aprovado = False
            motivos.append(f"Taxa de Permeabilidade ({tp_val}%) abaixo do mínimo de 20%.")
            
        # Simulação de verificação de documentos obrigatórios (Sprint 2)
        pendencias = dados.get("pendencias_checklist", [])
        if pendencias:
            aprovado = False
            motivos.append(f"Documentos faltantes: {', '.join(pendencias)}.")
            
        if aprovado:
            return {
                "recomendacao": "APROVADO", 
                "motivo": "Índices urbanísticos e documentação dentro das conformidades."
            }
        else:
            rec = "PENDENCIA" if (not regularizacao and pendencias) else "INDEFERIDO"
            if regularizacao and to_val > 70.0 and not pendencias:
                rec = "APROVADO COM MULTA"
            return {"recomendacao": rec, "motivo": " ".join(motivos)}

    def _evaluate_habitese(self, dados: dict) -> dict:
        """Avaliação básica para Habite-se."""
        pendencias = dados.get("pendencias_checklist", [])
        if pendencias:
            return {
                "recomendacao": "PENDENCIA", 
                "motivo": f"Documentos faltantes: {', '.join(pendencias)}."
            }
            
        return {
            "recomendacao": "APROVADO", 
            "motivo": "Documentação completa. Processo segue para vistoria e emissão."
        }
