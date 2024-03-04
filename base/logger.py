import logging
import os
from logging.handlers import RotatingFileHandler


default_formatter = logging.Formatter(
        "%(asctime)s -%(name)s %(levelname)-8s  - %(message)s",
        "%d.%m.%Y %H:%M:%S"
    )


def setup_logger(
        name=None,
        log_dir="logs",
        file_name="errors.log",
        formatter= default_formatter,
        level=logging.WARNING,
        max_bytes=20000,
        backup_count=1,
        propagate=False,
):
    if not isinstance(formatter, logging.Formatter):
        formatter = formatter()

    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_path = os.path.join(log_dir, file_name)
    rh = RotatingFileHandler(file_path, maxBytes=max_bytes, backupCount=backup_count)

    rh.setFormatter(formatter)
    rh.setLevel(level)
    logger.addHandler(rh)

    ch = logging.StreamHandler()

    ch.setFormatter(default_formatter)
    ch.setLevel(level)
    logger.addHandler(ch)

    logger.propagate = propagate

    return logger
