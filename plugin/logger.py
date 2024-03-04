import os
import logging

from .base import setup_logger as base_setup_logger

from .config import Config


def get_formatter():
    return logging.Formatter(
        "%(asctime)s -%(name)s %(levelname)-8s - %(message)s",
        "%d.%m.%Y %H:%M:%S"
    )


def setup_debug_loger(log_dir, cfg):
    return base_setup_logger(
        name="debugger",
        log_dir=os.path.join(cfg.log_folder, log_dir),
        file_name="debug.log",
        level=logging.DEBUG,
        max_bytes=1048576,  # 1Mb
        backup_count=2,
        propagate=True,
    )


def setup_warnings_loger(log_dir, cfg):
    return base_setup_logger(
        name="warnings",
        log_dir=os.path.join(cfg.log_folder, log_dir),
        file_name="warnings.log",
        level=logging.WARNING,
    )


def setup_errors_logger(log_dir, cfg):
    return base_setup_logger(
        log_dir=os.path.join(cfg.log_folder, log_dir),
        file_name="errors.log",
        level=logging.WARNING,
        max_bytes=500000,
        backup_count=5,
    )


def setup_logger(log_dir):
    cfg = Config()
    if not os.path.exists(cfg.log_folder):
        os.makedirs(cfg.log_folder)

    logs_dir = os.path.join(cfg.log_folder, log_dir)

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    setup_debug_loger(log_dir, cfg)
    setup_warnings_loger(log_dir, cfg)
    setup_errors_logger(log_dir, cfg)
