import re
from typing import Any
try:
    from .logger import log_ok, log_warn, log_err, log_info
except ImportError:
    # Caso seja executado standalone fora do pacote
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from logger import log_ok, log_warn, log_err, log_info

class BaseEngine:
    @staticmethod
    def parse_number(text: Any) -> float | None:
        """Extrai float de strings como '86,23%', '180,00m²', '1,5'."""
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
        """Formata valor para o padrão BRL (R$ 1.234,56)."""
        if value is None:
            return "R$ 0,00"
        try:
            # Formatação manual robusta para BRL
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return "R$ 0,00"

    @staticmethod
    def log_report(level: str, msg: str, data: dict = None) -> None:
        """Wrapper centralizado para log estruturado."""
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
