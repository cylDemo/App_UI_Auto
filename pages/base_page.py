"""
pages/base_page.py
页面对象基类模块
定义所有页面对象的公共行为和属性
采用 POM 模式将页面元素定位与业务操作分离
"""

from typing import Optional
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy

from core.base_action import BaseAction
from core.assertions import Assertions
from core.logger import TestLogger


class BasePage:
    """
    页面对象基类
    所有具体页面对象都应继承此类
    提供：
    - Driver 注入
    - 基础动作封装 (BaseAction)
    - 断言能力 (Assertions)
    - 日志记录 (TestLogger)
    """

    def __init__(self, driver: WebDriver):
        """
        初始化页面对象

        :param driver: WebDriver 实例，由外部注入（依赖注入模式）
        """
        self.driver = driver
        self.action = BaseAction(driver)
        self.assertion = Assertions(driver)
        self.logger = TestLogger(self.__class__.__name__)

    def is_page_loaded(self, timeout: Optional[int] = None) -> bool:
        """
        判断页面是否加载完成（抽象方法）

        :param timeout: 超时时间
        :return: 页面是否加载完成
        :raises NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError("Subclasses must implement is_page_loaded()")

    def wait_for_page_load(self, timeout: Optional[int] = None) -> bool:
        """
        等待页面加载完成

        :param timeout: 超时时间
        :return: 页面是否在超时时间内加载完成
        """
        timeout = timeout or 10
        if self.is_page_loaded(timeout):
            self.logger.info(f"Page loaded: {self.__class__.__name__}")
            return True
        self.logger.error(f"Page not loaded: {self.__class__.__name__}")
        return False

    def take_screenshot(self, name: str) -> str:
        """
        页面截图

        :param name: 截图名称前缀
        :return: 截图文件路径
        """
        return self.action.take_screenshot(name)

    def get_platform(self) -> str:
        """
        获取当前平台类型

        :return: 'android' 或 'ios'
        """
        return self.driver.capabilities.get("platformName", "").lower()


class Locator:
    """
    元素定位符常量类
    按平台分类管理定位方式，便于多平台适配
    """

    class ANDROID:
        """Android 平台定位方式"""
        ID = AppiumBy.ANDROID_UIAUTOMATOR
        XPath = AppiumBy.XPATH
        ACCESSIBILITY_ID = AppiumBy.ACCESSIBILITY_ID
        CLASS_NAME = AppiumBy.CLASS_NAME
        CSS = AppiumBy.CSS_SELECTOR

    class IOS:
        """iOS 平台定位方式"""
        ID = AppiumBy.IOS_PREDICATE
        XPath = AppiumBy.XPATH
        ACCESSIBILITY_ID = AppiumBy.ACCESSIBILITY_ID
        CLASS_NAME = AppiumBy.IOS_CLASS_CHAIN

    @classmethod
    def by_platform(cls, platform: str):
        """
        根据平台获取对应的定位方式类

        :param platform: 平台类型
        :return: ANDROID 或 IOS 定位方式类
        """
        if platform == "android":
            return cls.ANDROID
        return cls.IOS