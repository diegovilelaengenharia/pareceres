import logging
import sys
import os

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

class PlainFormatter(logging.Formatter):
    """Formata logs para arquivo sem caracteres de cor ANSI."""
    def format(self, record):
        level_map = {
            logging.DEBUG: "DEBUG",
            logging.INFO: "OK",
            logging.WARNING: "WARN",
            logging.ERROR: "ERR",
            logging.CRITICAL: "CRITICO"
        }
        level = level_map.get(record.levelno, record.levelname)
        return f"[{record.asctime}] [{level}] {record.getMessage()}"

def get_logger():
    logger = logging.getLogger("motor_gem")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Console Handler (com cores)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(ColorFormatter())

        # File Handler (limpo, sem cores)
        # Salva o log na raiz da pasta _Sistema_Interno/01_Motor_Python/
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "motor.log")
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(PlainFormatter())

        logger.addHandler(ch)
        logger.addHandler(fh)
        
    return logger

# Funções auxiliares para migração rápida
_log = get_logger()

def _ok(msg):   return f"{_OK}[OK]{_RESET} {msg}"
def _warn(msg): return f"{_WARN}[WARN]{_RESET} {msg}"
def _err(msg):  return f"{_ERR}[ERR]{_RESET} {msg}"
def _info(msg): return f"{_INFO}[INFO]{_RESET} {msg}"

def log_ok(msg): _log.info(msg)
def log_warn(msg): _log.warning(msg)
def log_err(msg): _log.error(msg)
def log_info(msg): _log.debug(msg) # Mapeamos info para DEBUG para não confundir com o [OK] no arquivo
