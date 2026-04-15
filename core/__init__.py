"""
core/__init__.py
核心层模块初始化
封装 Appium Driver 管理、基础动作、断言、日志等核心能力
"""

from .driver_manager import DriverManager
from .base_action import BaseAction
from .assertions import Assertions
from .logger import Logger, TestLogger

__all__ = [
    "DriverManager",
    "BaseAction",
    "Assertions",
    "Logger",
    "TestLogger"
]