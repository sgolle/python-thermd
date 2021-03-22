# -*- coding: utf-8 -*-

"""Dokumentation.

Beschreibung

"""

import logging.config


def get_logger(name: str, file: str = "logfile.txt") -> logging.Logger:
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": "%(levelname)s %(asctime)s %(funcName)s %(lineno)d "
                    "%(message)s",
                    "datefmt": "%d.%b.%Y %H:%M:%S",
                },
                "simple": {"format": "%(levelname)s %(message)s"},
            },
            "handlers": {
                "file": {
                    "level": "INFO",
                    "class": "logging.FileHandler",
                    "filename": file,
                    "formatter": "verbose",
                },
                "console": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {"": {"level": "INFO", "handlers": ["file", "console"]}},
        }
    )

    logging.captureWarnings(True)
    return logging.getLogger(name)


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Helper functions.")
