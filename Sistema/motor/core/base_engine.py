"""
Motor Base de Processamento — Motor GEM / SMOSU Oliveira-MG
Contém a classe BaseEngine com utilitários compartilhados para manipulação de dados,
formatação e logging estruturado.
"""

import re
from typing import Any
try:
    from .logger import log_ok, log_warn, log_err, log_info
except ImportError:
    # Caso seja executado standalone fora do pacote
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from core.logger import log_ok, log_warn, log_err, log_info

class BaseEngine:
    """Classe base com métodos estáticos utilitários para os motores de análise."""
    
    @staticmethod
    def parse_number(text: Any) -> float | None:
        """
        Extrai um valor float de uma string contendo unidades ou símbolos.
        
        Args:
            text: Texto a ser convertido (ex: '180,00m²', '86,23%').
            
        Returns:
            O valor numérico como float ou None se a conversão falhar.
        """
        if text is None:
            return None
        # Remove caracteres que não sejam dígitos, vírgula, ponto ou sinal de menos
        limpo = re.sub(r"[^\d,.\-]", "", str(text)).replace(",", ".")
        try:
            # Lidar com múltiplos pontos decimais se houver sujeira na string
            if limpo.count('.') > 1:
                parts = limpo.split('.')
                limpo = "".join(parts[:-1]) + "." + parts[-1]
            return float(limpo) if limpo and limpo != "." and limpo != "-" else None
        except ValueError:
            return None

    @staticmethod
    def format_currency(value: float | None) -> str:
        """
        Formata um valor numérico para o padrão monetário brasileiro (BRL).
        
        Args:
            value: Valor float a ser formatado.
            
        Returns:
            String formatada como 'R$ 1.234,56'.
        """
        if value is None:
            return "R$ 0,00"
        try:
            # Formatação manual robusta para BRL
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return "R$ 0,00"

    @staticmethod
    def log_report(level: str, msg: str, data: dict = None) -> None:
        """
        Wrapper centralizado para log estruturado, facilitando a observabilidade.
        
        Args:
            level: Nível do log (INFO, OK, WARN, ERR).
            msg: Mensagem descritiva.
            data: Dicionário opcional com dados contextuais para o log JSON.
        """
        level = level.upper()
        if level == "INFO":
            log_info(msg, data)
        elif level in ["OK", "SUCCESS"]:
            log_ok(msg, data)
        elif level in ["WARN", "WARNING"]:
            log_warn(msg, data)
        elif level in ["ERR", "ERROR"]:
            log_err(msg, data)
        else:
            log_info(f"[{level}] {msg}", data)
