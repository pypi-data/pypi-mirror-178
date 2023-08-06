import copy
import logging
import logging.config
import os

import termcolor


class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fmt = fmt
        self.base_formatter = logging.Formatter(fmt, *args, **kwargs)

    def format(self, record):
        if hasattr(record, "color"):
            if record.color:  # type: ignore
                record = copy.copy(record)
                record.msg = termcolor.colored(record.msg, record.color)  # type: ignore
        return self.base_formatter.format(record)


class ColoredLogger(logging.Logger):
    def _log(
        self,
        level,
        msg,
        args,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=1,
        color=None,
    ):
        if color:
            if not extra:
                extra = {}
            extra["color"] = color
        super()._log(
            level,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )


def init_colored_logger(logs_folder_path, logging_level):
    fmt = "{asctime} [{levelname}] {filename}.{funcName}:{lineno} | {message}"
    logger_config = {
        "version": 1,
        "formatters": {
            "std_formatter": {
                "format": fmt,
                "style": "{",
            },
            "colored_formatter": {
                "()": ColoredFormatter,
                "fmt": fmt,
                "style": "{",
            },
        },
        "handlers": {
            "console_handler": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "colored_formatter",
            },
            "file_handler": {
                "level": "DEBUG",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": f"{logs_folder_path}/logs.log",
                "when": "midnight",
                # "interval": 1,
                "backupCount": 10,
                # "mode": "a",
                "formatter": "std_formatter",
                "encoding": "UTF-8",
            },
            # add telegram handler for critial errors
        },
        "loggers": {
            "root": {
                "level": logging_level,  # type: ignore
                "handlers": ["console_handler", "file_handler"],
            },
            "asyncio": {
                "level": "CRITICAL",
                "handlers": ["console_handler", "file_handler"],
            },
            "aio_pika": {
                "level": "ERROR",
            },
            "aiormq": {
                "level": "ERROR",
            },
        },
        "filters": {},
    }
    os.makedirs(f"{logs_folder_path}", exist_ok=True)
    logging.config.dictConfig(logger_config)
    log = logging.getLogger()
    log.__class__ = ColoredLogger
