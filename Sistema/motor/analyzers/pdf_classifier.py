import os
import json
import google.generativeai as genai
from core.logger import log_info, log_err

class PDFClassifier:
    """
    Classificador multimodal de PDFs (Pilar 1 - A).
    Utiliza Gemini 2.5 Pro para ler um PDF de engenharia e determinar seu tipo estrutural.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            log_err("GEMINI_API_KEY não encontrada. Classificador PDF não funcionará.")

    def classify_pdf(self, pdf_path: str) -> dict:
        """
        Envia o PDF para a API do Gemini e retorna o tipo do processo classificado.
        Retorna um dicionário: {"tipo_processo": "valor"}
        """
        if not self.api_key:
            return {"tipo_processo": "desconhecido"}
            
        if not os.path.exists(pdf_path):
            log_err(f"Arquivo PDF não encontrado: {pdf_path}")
            return {"tipo_processo": "desconhecido"}
            
        try:
            log_info(f"Enviando PDF para classificação (Gemini Vision): {os.path.basename(pdf_path)}")
            # Fazer upload do arquivo para a API do Gemini
            uploaded_file = genai.upload_file(pdf_path)
            
            # Tipos válidos (limitados aos do motor)
            tipos_validos = [
                "alvara_aprovacao", "alvara_regularizacao", "alvara_construcao_comercial",
                "habitese_comum", "certidao_localizacao", "comunicado_pendencia"
            ]
            
            prompt = f"""
            Analise este documento PDF referente a um processo na prefeitura municipal de Oliveira/MG.
            Identifique qual é o tipo de processo de engenharia civil / arquitetura solicitado, ou a qual ele se refere.
            
            Você deve responder EXCLUSIVAMENTE com um JSON válido contendo a chave "tipo_processo".
            O valor deve ser exatamente um destes: {', '.join(tipos_validos)}
            Se não for claramente nenhum destes, retorne "desconhecido".
            """
            
            model = genai.GenerativeModel('gemini-2.5-pro')
            response = model.generate_content(
                [uploaded_file, prompt],
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            
            # Limpar o arquivo da nuvem após uso para evitar cobranças/poluição
            genai.delete_file(uploaded_file.name)
            
            try:
                result = json.loads(response.text)
                return result
            except json.JSONDecodeError:
                log_err("Falha ao decodificar JSON retornado pelo Gemini.")
                return {"tipo_processo": "desconhecido"}
                
        except Exception as e:
            log_err(f"Erro na classificação do PDF via Gemini: {e}")
            return {"tipo_processo": "desconhecido"}
