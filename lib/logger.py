#!/usr/bin/env python3
"""簡易 Logging 工具
提供 get_logger 讓其他模組可快速取得可同時輸出到終端與檔案的 logger.
使用方式:
    from lib import get_logger
    log = get_logger('socket_server', logfile='logs/socket_server.log')
    log.info('Server started')
"""
import logging
import os
import threading
from typing import Optional

# 專案根目錄 logs 位置 (若在封裝後使用, 可以根據當前檔案推導)
DEFAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_LOG_DIR = os.path.join(DEFAULT_ROOT, 'logs')
os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)


class LoggerFactory:
    _lock = threading.Lock()
    _created = {}
    DATEFMT = '%Y-%m-%d %H:%M:%S'  # 統一時間格式，可在此修改

    @classmethod
    def get_logger(
        cls,
        name: str = 'app',
        logfile: Optional[str] = None,
        level: int = logging.INFO,
        fmt: str = '%(asctime)s [%(levelname)s] %(message)s',
        propagate: bool = False,
    ) -> logging.Logger:
        """取得或建立 logger
        若指定 logfile 則自動建立目錄並新增 FileHandler.
        多次呼叫同名 logger 時不重複新增同樣的 handler.
        """
        if logfile is None:
            logfile = os.path.join(DEFAULT_LOG_DIR, f'{name}.log')

        with cls._lock:
            if name in cls._created:
                logger = cls._created[name]
                # 若後續再提供新的 logfile, 並且尚未綁定則新增
                if logfile and not any(
                    isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(logfile)
                    for h in logger.handlers
                ):
                    cls._add_file_handler(logger, logfile, level, fmt)
                return logger

            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.propagate = propagate

            # StreamHandler (stdout)
            if not logger.handlers:
                sh = logging.StreamHandler()
                sh.setLevel(level)
                sh.setFormatter(logging.Formatter(fmt, datefmt=cls.DATEFMT))
                logger.addHandler(sh)

            if logfile:
                cls._add_file_handler(logger, logfile, level, fmt)

            cls._created[name] = logger
            return logger

    @staticmethod
    def _add_file_handler(logger: logging.Logger, logfile: str, level: int, fmt: str):
        path = os.path.abspath(logfile)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        fh = logging.FileHandler(path, encoding='utf-8')
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter(fmt, datefmt=LoggerFactory.DATEFMT))
        logger.addHandler(fh)


def get_logger(*args, **kwargs) -> logging.Logger:
    """取得 logger 的簡化函式"""
    return LoggerFactory.get_logger(*args, **kwargs)
