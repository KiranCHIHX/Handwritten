#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
import time
import sys

import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from omegaconf import OmegaConf

from app.core.config import cfg

log_level = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARN,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def log_setup(
    cfg: OmegaConf, app_name: str, filelogging: bool = cfg.Logger.File, consolelogging: bool = cfg.Logger.Console
):
    # print("Logger Level:", cfg.Logger[app_name].Level)
    # print("Logger Filename:", cfg.Logger[app_name].Filename)
    logger = logging.getLogger()
    formatter = logging.Formatter(cfg.Logger[app_name].Format)
    formatter.converter = time.gmtime  # if you want UTC time
    if filelogging:
        handler = RotatingFileHandler(
            cfg.Logger[app_name].Filename,
            maxBytes=cfg.Logger[app_name].MaxBytes,
            backupCount=cfg.Logger[app_name].BackupCount,
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    if consolelogging:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(log_level[cfg.Logger[app_name].Level])
    print("Logger Initialised ...")
    return logger


def run_log_setup(
    cfg: OmegaConf,
    job_name: str,
    app_name: str = "run",
    filelogging: bool = cfg.Logger.File,
    consolelogging: bool = cfg.Logger.Console,
):
    # print("Logger Level:", cfg.Logger[app_name].Level)
    logger = logging.getLogger()
    formatter = logging.Formatter(cfg.Logger[app_name].Format)
    formatter.converter = time.gmtime  # if you want UTC time
    log_filename = cfg.Logger[app_name].Filename.replace(".log", f"_{job_name}.log")
    if filelogging:
        handler = RotatingFileHandler(
            cfg.Logger[app_name].Filename,
            maxBytes=cfg.Logger[app_name].MaxBytes,
            backupCount=cfg.Logger[app_name].BackupCount,
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    if consolelogging:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(log_level[cfg.Logger[app_name].Level])
    return logger
