from __future__ import annotations

import logging
import sys

from app.core.config import settings

_HANDLER_MARKER = "_healthy_system_handler"
_DEFAULT_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging() -> None:
    level_name = str(settings.LOG_LEVEL).upper()
    level = getattr(logging, level_name, logging.INFO)
    root_logger = logging.getLogger()

    if root_logger.level == logging.NOTSET or root_logger.level > level:
        root_logger.setLevel(level)

    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(_DEFAULT_FORMAT))
    setattr(handler, _HANDLER_MARKER, True)
    root_logger.addHandler(handler)
