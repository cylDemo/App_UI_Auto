"""
core/driver_manager.py
Appium Driver 工厂与生命周期管理模块
采用工厂模式创建 Driver，支持多平台（Android/iOS）
提供并发 Session 管理和线程安全操作
"""

import threading
from typing import Dict, Optional, Any
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import RemoteConnection

from config.settings import Settings
from core.logger import TestLogger


class DriverManager:
    """
    Appium Driver 工厂类
    负责 Appium WebDriver 的创建、存储和销毁
    支持多设备并发执行，通过线程锁保证线程安全
    """

    _lock = threading.Lock()
    _drivers: Dict[str, WebDriver] = {}
    _session_count = 0

    @classmethod
    def create_driver(
        cls,
        platform: str,
        device_name: str,
        app_path: Optional[str] = None,
        appium_server_url: Optional[str] = None,
        implicit_wait: Optional[int] = None
    ) -> WebDriver:
        """
        创建 Appium Driver 实例

        :param platform: 平台类型（android/ios）
        :param device_name: 设备名称，用于加载设备配置
        :param app_path: 应用文件路径（APK/IPA），可选
        :param appium_server_url: Appium 服务地址，可选
        :param implicit_wait: 隐式等待时间，可选
        :return: WebDriver 实例
        """
        with cls._lock:
            cls._session_count += 1
            session_id = f"{platform}_{device_name}_{cls._session_count}"
            logger = TestLogger(f"DriverManager-{session_id}")
            logger.info(f"Creating driver for {platform} device: {device_name}")

            # 合并基础能力与设备个性化能力
            capabilities = Settings.merge_capabilities(platform, device_name)

            # 如果指定了应用路径，添加到能力中
            if app_path:
                capabilities["app"] = app_path

            # 创建平台对应的 Options
            options = cls._create_options(platform, capabilities)

            # 确定服务地址
            server_url = appium_server_url or Settings.APPIUM_SERVER_URL

            # 创建 Driver 实例
            driver = WebDriver(
                command_executor=RemoteConnection(server_url, resolve_ip=True),
                options=options
            )

            # 设置隐式等待
            driver.implicitly_wait(implicit_wait or Settings.IMPLICIT_WAIT_TIMEOUT)
            driver.session_id = session_id

            # 存储到 Driver 池
            cls._drivers[session_id] = driver
            logger.info(f"Driver created successfully. Session ID: {session_id}")

            return driver

    @classmethod
    def _create_options(cls, platform: str, capabilities: Dict[str, Any]):
        """
        根据平台类型创建对应的 Appium Options

        :param platform: 平台类型
        :param capabilities: 能力配置字典
        :return: UiAutomator2Options 或 XCUITestOptions
        :raises ValueError: 不支持的平台类型
        """
        if platform == Settings.PLATFORM_ANDROID:
            from appium.options.android import UiAutomator2Options
            options = UiAutomator2Options()
        elif platform == Settings.PLATFORM_IOS:
            from appium.options.ios import XCUITestOptions
            options = XCUITestOptions()
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        # 将 capabilities 设置到 options
        for key, value in capabilities.items():
            if hasattr(options, key):
                setattr(options, key, value)
            else:
                options.set_capability(key, value)

        return options

    @classmethod
    def get_driver(cls, session_id: Optional[str] = None) -> Optional[WebDriver]:
        """
        获取 Driver 实例

        :param session_id: 会话 ID，为空时返回第一个 Driver
        :return: WebDriver 实例或 None
        """
        if session_id:
            return cls._drivers.get(session_id)
        if cls._drivers:
            return list(cls._drivers.values())[0]
        return None

    @classmethod
    def quit_driver(cls, session_id: Optional[str] = None) -> None:
        """
        退出指定的 Driver 会话

        :param session_id: 会话 ID，为空时退出所有 Driver
        """
        with cls._lock:
            if session_id and session_id in cls._drivers:
                driver = cls._drivers.pop(session_id)
                logger = TestLogger(f"DriverManager-{session_id}")
                logger.info(f"Quitting driver: {session_id}")
                try:
                    driver.quit()
                except Exception as e:
                    logger.error(f"Error quitting driver: {e}")
            elif not session_id:
                for sid, driver in list(cls._drivers.items()):
                    logger = TestLogger(f"DriverManager-{sid}")
                    logger.info(f"Quitting driver: {sid}")
                    try:
                        driver.quit()
                    except Exception as e:
                        logger.error(f"Error quitting driver: {e}")
                cls._drivers.clear()

    @classmethod
    def quit_all(cls) -> None:
        """退出所有 Driver 会话"""
        cls.quit_driver()

    @classmethod
    def get_current_session_id(cls) -> Optional[str]:
        """获取当前活跃的会话 ID"""
        if cls._drivers:
            return list(cls._drivers.keys())[0]
        return None