"""
core/logger.py
日志记录器模块
提供统一格式的日志输出能力，支持控制台和文件双输出
包含通用 Logger 类和测试执行日志管理器 TestLogger
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class Logger:
    """
    统一日志记录器工厂类
    采用单例模式缓存 Logger 实例，避免重复创建
    支持控制台和文件双渠道输出
    """

    _loggers = {}

    @classmethod
    def get_logger(
        cls,
        name: str,
        log_file: Optional[Path] = None,
        level: str = "INFO",
        log_format: Optional[str] = None
    ) -> logging.Logger:
        """获取或创建指定名称的 Logger 实例"""
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        logger.handlers.clear()

        # 格式化器
        formatter = logging.Formatter(
            log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 文件处理器（可选）
        if log_file:
            log_file = Path(log_file)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        cls._loggers[name] = logger
        return logger


class TestLogger:
    """
    测试执行日志管理器
    封装常用日志操作，提供结构化的测试步骤记录
    """

    def __init__(self, name: str = "TestExecution"):
        """
        初始化测试日志管理器

        :param name: 日志记录器名称，默认 "TestExecution"
        """
        from config.settings import Settings
        self.logger = Logger.get_logger(
            name=name,
            log_file=Settings.LOG_FILE,
            level=Settings.LOG_LEVEL,
            log_format=Settings.LOG_FORMAT
        )

    def info(self, message: str) -> None:
        """记录 INFO 级别日志"""
        self.logger.info(message)

    def debug(self, message: str) -> None:
        """记录 DEBUG 级别日志"""
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        """记录 WARNING 级别日志"""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """记录 ERROR 级别日志"""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """记录 CRITICAL 级别日志"""
        self.logger.critical(message)

    def step(self, step_name: str, description: str) -> None:
        """
        记录测试步骤

        :param step_name: 步骤名称
        :param description: 步骤描述
        """
        self.logger.info(f"[STEP] {step_name}: {description}")

    def start_test(self, test_name: str) -> None:
        """
        记录测试开始

        :param test_name: 测试名称
        """
        self.logger.info(f"{'='*60}")
        self.logger.info(f"TEST START: {test_name}")
        self.logger.info(f"{'='*60}")

    def end_test(self, test_name: str, status: str) -> None:
        """
        记录测试结束

        :param test_name: 测试名称
        :param status: 测试状态（PASSED/FAILED/SKIPPED）
        """
        self.logger.info(f"{'='*60}")
        self.logger.info(f"TEST END: {test_name} - Status: {status}")
        self.logger.info(f"{'='*60}")