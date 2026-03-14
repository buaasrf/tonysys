"""
日志工具（复用 MiroFish 的日志模式）
"""

import logging
import sys

_loggers = {}


def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s]: %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    _loggers[name] = logger
    return logger


def get_logger(name: str) -> logging.Logger:
    if name in _loggers:
        return _loggers[name]
    return setup_logger(name)
