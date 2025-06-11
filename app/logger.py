import logging
import os

import coloredlogs
from fastapi import FastAPI


class NoWarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.WARNING


def setup_logger():
    _logger = logging.getLogger(__name__)

    if not _logger.handlers:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        coloredlogs.install(
            level='DEBUG',
            logger=_logger,
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            isatty=True,
            level_styles={
                'debug': {'color': 'blue'},
                'info': {'color': 'green'},
                'warning': {'color': 'yellow'},
                'error': {'color': 'red'},
                'critical': {'color': 'red', 'bold': True}
            },
            field_styles={
                'asctime': {'color': 'cyan'},
                'levelname': {'bold': True},
                'name': {'color': 'magenta'}
            }
        )
        _logger.addFilter(NoWarningFilter())

        _logger.propagate = False

    return _logger
