import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import functools
import time

from kitchen_ledger.infrastructure.config import LOG_DIR, LOG_LEVEL
from kitchen_ledger.infrastructure.paths import ensure_runtime_directories

class LogLevels():
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10

def setup_logging() -> logging.Logger:
    ensure_runtime_directories()

    logger = logging.getLogger("kitchen_ledger")
    level = getattr(logging, LOG_LEVEL, logging.INFO)

    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | %(levelname)-7s | "
            "%(name)-60s | %(funcName)-25s | %(message)s"
        ),
        datefmt="%y-%m-%d %H:%M:%S"
    )

    log_path = LOG_DIR / "kitchen_core.log"

    file_handler = next(
        (
            handler
            for handler in logger.handlers
            if isinstance(handler, RotatingFileHandler)
            and Path(handler.baseFilename) == log_path.resolve()
        ),
        None
    )

    if file_handler is None:
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10_000_000,
            backupCount=5,
            encoding="utf-8"
        )
        logger.addHandler(file_handler)

    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    return logger

def log_operation(func=None, *, level: int = logging.DEBUG):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(f.__module__)
            start = time.perf_counter()
            logger.log(level, f"Starting {f.__qualname__}", stacklevel=2)
            try:
                return f(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                logger.log(level, f"Finished {f.__qualname__} in {elapsed:.4f}s", stacklevel=2)
        return wrapper
    if func is None:
        return decorator
    return decorator(func)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)