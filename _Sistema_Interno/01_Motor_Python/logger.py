import logging
import sys
import os
import json
from datetime import datetime

try:
    from colorama import init as _colorama_init, Fore, Style
    _colorama_init(autoreset=True)
    _OK    = Fore.GREEN  + Style.BRIGHT
    _WARN  = Fore.YELLOW + Style.BRIGHT
    _ERR   = Fore.RED    + Style.BRIGHT
    _INFO  = Fore.CYAN   + Style.BRIGHT
    _RESET = Style.RESET_ALL
    _BLUE  = Fore.BLUE   + Style.BRIGHT
except ImportError:
    _OK = _WARN = _ERR = _INFO = _RESET = _BLUE = ""

class ColorFormatter(logging.Formatter):
    """Formata logs com cores no terminal."""
    FORMATS = {
        logging.DEBUG:    f"{_INFO}[DEBUG]{_RESET} %(message)s",
        logging.INFO:     f"{_OK}[OK]{_RESET} %(message)s",
        logging.WARNING:  f"{_WARN}[WARN]{_RESET} %(message)s",
        logging.ERROR:    f"{_ERR}[ERR]{_RESET} %(message)s",
        logging.CRITICAL: f"{_ERR}[CRÍTICO]{_RESET} %(message)s"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, "%(message)s")
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class JSONFormatter(logging.Formatter):
    """Formata logs em JSON para facilitar o consumo por IA (Observabilidade Agent-First)."""
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "line": record.lineno
        }
        # Se houver dados extras no log, inclui no JSON
        if hasattr(record, "extra_data"):
            log_record["data"] = record.extra_data
            
        return json.dumps(log_record, ensure_ascii=False)

def get_logger():
    logger = logging.getLogger("motor_gem")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Console Handler (com cores)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(ColorFormatter())

        # JSON Handler (Agent-First Observability)
        log_file_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "motor.json.log")
        jh = logging.FileHandler(log_file_json, encoding="utf-8")
        jh.setLevel(logging.DEBUG)
        jh.setFormatter(JSONFormatter())

        logger.addHandler(ch)
        logger.addHandler(jh)
        
    return logger

# Funções auxiliares
_log = get_logger()

def log_ok(msg, data=None):
    _log.info(msg, extra={"extra_data": data} if data else {})

def log_warn(msg, data=None):
    _log.warning(msg, extra={"extra_data": data} if data else {})

def log_err(msg, data=None):
    _log.error(msg, extra={"extra_data": data} if data else {})

def log_info(msg, data=None):
    _log.debug(msg, extra={"extra_data": data} if data else {})
