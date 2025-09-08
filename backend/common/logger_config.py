import logging
import time

LOGFILE_PATHNAME = "central.log"
LOG_FORMAT = "%(asctime)s:%(name)s:%(funcName)s:%(lineno)d %(levelname)s %(message)s"


class UTCFormatter(logging.Formatter):
    converter = time.gmtime  # type: ignore[assignment]


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "utc": {
            "()": UTCFormatter,
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "utc",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "utc",
            "level": "DEBUG",
            "filename": LOGFILE_PATHNAME,
            "when": "midnight",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file"]},
}
