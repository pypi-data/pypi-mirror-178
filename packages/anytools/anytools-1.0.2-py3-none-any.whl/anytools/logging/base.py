import logging


def init_base_logger():
    fmt = "{asctime} [{levelname}] {filename}.{funcName}:{lineno} {message}"

    logging.basicConfig(
        level=logging.DEBUG,
        format=fmt,
        style="{",
    )
