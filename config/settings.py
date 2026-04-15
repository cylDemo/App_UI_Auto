"""
config/settings.py
全局配置管理模块
定义超时时间、报告路径、平台能力等全局配置项
采用类属性方式组织，支持跨模块直接引用
"""

import os
from pathlib import Path
from typing import Dict, Any


class Settings:
    """
    全局配置管理类
    统一管理测试框架的所有配置项，包括：
    - 目录路径配置
    - 超时时间配置
    - 平台能力配置
    - 日志配置
    """

    # ==================== 目录路径配置 ====================
    # 项目根目录（框架所在位置）
    PROJECT_ROOT = Path(__file__).parent.parent

    # 报告相关目录
    REPORTS_DIR = PROJECT_ROOT / "reports"           # 测试报告根目录
    LOGS_DIR = PROJECT_ROOT / "logs"                  # 日志文件目录
    SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"     # 失败截图目录
    ALLURE_RESULTS_DIR = REPORTS_DIR / "allure-results"  # Allure XML结果目录
    ALLURE_HTML_DIR = REPORTS_DIR / "allure-html"      # Allure HTML报告目录

    # 自动创建目录
    for _dir in [REPORTS_DIR, LOGS_DIR, SCREENSHOTS_DIR, ALLURE_RESULTS_DIR]:
        _dir.mkdir(parents=True, exist_ok=True)

    # ==================== Appium 服务配置 ====================
    APPIUM_SERVER_URL = "http://localhost:4723"  # 默认 Appium 服务地址

    # ==================== 等待超时配置（秒） ====================
    IMPLICIT_WAIT_TIMEOUT = 10   # 隐式等待：元素查找重试间隔
    EXPLICIT_WAIT_TIMEOUT = 20   # 显式等待：条件判断超时
    PAGELOAD_TIMEOUT = 30        # 页面加载超时

    # ==================== 重试机制配置 ====================
    MAX_RETRIES = 3    # 操作失败最大重试次数
    RETRY_DELAY = 1    # 重试间隔（秒）

    # ==================== 手势操作配置 ====================
    SWIPE_DURATION = 500   # 滑动持续时间（毫秒）
    TAP_DURATION = 100     # 点击持续时间（毫秒）

    # ==================== 日志配置 ====================
    LOG_LEVEL = "INFO"                                          # 日志级别
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # 日志格式
    LOG_FILE = LOGS_DIR / "test_execution.log"                   # 日志文件路径

    # ==================== 平台常量 ====================
    PLATFORM_ANDROID = "android"
    PLATFORM_IOS = "ios"

    # ==================== 基础能力配置 ====================
    # Android 平台基础能力
    CAPABILITIES_ANDROID = {
        "platformName": PLATFORM_ANDROID,
        "automationName": "UiAutomator2",     # 使用 UiAutomator2 驱动
        "noReset": False,                     # 测试后不重置应用
        "autoGrantPermissions": True,         # 自动授权运行时权限
        "disableWindowAnimation": True,        # 禁用窗口动画（加速测试）
    }

    # iOS 平台基础能力
    CAPABILITIES_IOS = {
        "platformName": PLATFORM_IOS,
        "automationName": "XCUITest",         # 使用 XCUITest 驱动
        "noReset": False,
        "autoAcceptAlerts": True,              # 自动接受系统弹窗
    }

    @classmethod
    def get_device_config(cls, platform: str, device_name: str) -> Dict[str, Any]:
        """
        获取指定设备的完整配置

        :param platform: 平台类型（android/ios）
        :param device_name: 设备名称（对应 devices.yaml 中的 name 字段）
        :return: 设备配置字典，包含 UDID、版本、个性化 capabilities 等
        """
        from utils.file_reader import YamlReader
        devices = YamlReader.read_yaml(cls.PROJECT_ROOT / "config" / "devices.yaml")
        for device in devices.get("devices", []):
            if device.get("platform") == platform and device.get("name") == device_name:
                return device
        return {}

    @classmethod
    def merge_capabilities(cls, platform: str, device_name: str) -> Dict[str, Any]:
        """
        合并基础能力与设备个性化能力

        :param platform: 平台类型
        :param device_name: 设备名称
        :return: 合并后的完整 capabilities 字典
        """
        # 根据平台选择基础能力
        base_caps = cls.CAPABILITIES_ANDROID if platform == cls.PLATFORM_ANDROID else cls.CAPABILITIES_IOS

        # 合并设备个性化配置
        device_config = cls.get_device_config(platform, device_name)
        if device_config:
            device_caps = device_config.get("capabilities", {})
            base_caps = {**base_caps, **device_caps}
        return base_caps