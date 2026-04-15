"""
core/base_action.py
基础动作封装模块
对原生 Appium API 进行二次封装，统一加入显式等待、异常处理和日志记录
是页面对象层与 Appium 驱动之间的桥梁
"""

import time
from typing import Optional, Tuple, Union
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config.settings import Settings
from core.logger import TestLogger


class BaseAction:
    """
    基础动作封装类
    封装常用的 UI 操作（点击、输入、滑动等），统一处理：
    - 显式等待：确保元素可操作后再执行
    - 异常处理：操作失败时自动截图
    - 日志记录：记录每一步操作
    """

    def __init__(self, driver: WebDriver):
        """
        初始化基础动作封装

        :param driver: WebDriver 实例，由外部注入
        """
        self.driver = driver
        self.logger = TestLogger(self.__class__.__name__)
        self.timeout = Settings.EXPLICIT_WAIT_TIMEOUT

    # ==================== 元素查找辅助方法 ====================

    def _find_element(self, by: str, value: str, timeout: Optional[int] = None):
        """
        等待并查找元素（出现）

        :param by: 定位方式（AppiumBy 类型）
        :param value: 定位表达式
        :param timeout: 超时时间
        :return: 找到的元素
        :raises TimeoutException: 元素未在超时时间内出现
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {by}={value}")
            self._take_screenshot(f"element_not_found_{by}_{value}")
            raise

    def _find_clickable_element(self, by: str, value: str, timeout: Optional[int] = None):
        """
        等待并查找可点击的元素

        :param by: 定位方式
        :param value: 定位表达式
        :param timeout: 超时时间
        :return: 可点击的元素
        :raises TimeoutException: 元素未在超时时间内可点击
        """
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Clickable element not found: {by}={value}")
            self._take_screenshot(f"element_not_clickable_{by}_{value}")
            raise

    # ==================== 点击操作 ====================

    def click(self, by: str, value: str, timeout: Optional[int] = None) -> None:
        """
        点击元素

        :param by: 定位方式
        :param value: 定位表达式
        :param timeout: 超时时间
        """
        self.logger.debug(f"Clicking element: {by}={value}")
        element = self._find_clickable_element(by, value, timeout)
        element.click()
        self.logger.debug(f"Clicked element: {by}={value}")

    def tap(self, x: int, y: int, duration: Optional[int] = None) -> None:
        """
        点击指定坐标（手势操作）

        :param x: X 坐标
        :param y: Y 坐标
        :param duration: 按压持续时间（毫秒）
        """
        duration = duration or Settings.TAP_DURATION
        self.logger.debug(f"Tapping at ({x}, {y})")
        self.driver.tap([(x, y)], duration)
        self.logger.debug(f"Tapped at ({x}, {y})")

    # ==================== 输入操作 ====================

    def input_text(
        self,
        by: str,
        value: str,
        text: str,
        clear_first: bool = True,
        timeout: Optional[int] = None
    ) -> None:
        """
        向输入框输入文本

        :param by: 定位方式
        :param value: 定位表达式
        :param text: 要输入的文本
        :param clear_first: 是否先清空输入框，默认 True
        :param timeout: 超时时间
        """
        self.logger.debug(f"Inputting text '{text}' to: {by}={value}")
        element = self._find_element(by, value, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        self.logger.debug(f"Text '{text}' input to: {by}={value}")

    def clear_text(self, by: str, value: str, timeout: Optional[int] = None) -> None:
        """清空输入框文本"""
        element = self._find_element(by, value, timeout)
        element.clear()
        self.logger.debug(f"Cleared text at: {by}={value}")

    # ==================== 获取元素信息 ====================

    def get_text(self, by: str, value: str, timeout: Optional[int] = None) -> str:
        """
        获取元素的文本内容

        :param by: 定位方式
        :param value: 定位表达式
        :param timeout: 超时时间
        :return: 元素文本
        """
        element = self._find_element(by, value, timeout)
        text = element.text
        self.logger.debug(f"Got text '{text}' from: {by}={value}")
        return text

    def get_attribute(self, by: str, value: str, attribute: str, timeout: Optional[int] = None) -> str:
        """
        获取元素的属性值

        :param by: 定位方式
        :param value: 定位表达式
        :param attribute: 属性名称
        :param timeout: 超时时间
        :return: 属性值
        """
        element = self._find_element(by, value, timeout)
        attr = element.get_attribute(attribute)
        self.logger.debug(f"Got attribute '{attribute}': '{attr}' from: {by}={value}")
        return attr

    # ==================== 元素状态判断 ====================

    def is_element_visible(self, by: str, value: str, timeout: Optional[int] = None) -> bool:
        """判断元素是否可见"""
        try:
            timeout = timeout or 5
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def is_element_selected(self, by: str, value: str, timeout: Optional[int] = None) -> bool:
        """判断元素是否被选中（如复选框）"""
        try:
            timeout = timeout or 5
            WebDriverWait(self.driver, timeout).until(
                EC.element_located_to_be_selected((by, value))
            )
            return True
        except TimeoutException:
            return False

    def is_element_present(self, by: str, value: str, timeout: Optional[int] = None) -> bool:
        """判断元素是否存在于 DOM"""
        try:
            timeout = timeout or 5
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = None,
        state: str = "visible"
    ) -> bool:
        """
        等待元素达到指定状态

        :param by: 定位方式
        :param value: 定位表达式
        :param timeout: 超时时间
        :param state: 等待状态，可选值：visible、invisible、clickable
        :return: 是否达到指定状态
        """
        timeout = timeout or self.timeout
        try:
            if state == "visible":
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((by, value))
                )
            elif state == "invisible":
                WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located((by, value))
                )
            elif state == "clickable":
                WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
            return True
        except TimeoutException:
            return False

    # ==================== 滑动操作 ====================

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: Optional[int] = None
    ) -> None:
        """
        执行滑动手势

        :param start_x: 起始 X 坐标
        :param start_y: 起始 Y 坐标
        :param end_x: 结束 X 坐标
        :param end_y: 结束 Y 坐标
        :param duration: 持续时间（毫秒）
        """
        duration = duration or Settings.SWIPE_DURATION
        self.logger.debug(f"Swiping from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        self.logger.debug("Swipe completed")

    def swipe_up(self, percentage: float = 0.5, duration: Optional[int] = None) -> None:
        """向上滑动"""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.8)
        end_x = start_x
        end_y = int(size["height"] * (0.5 - percentage / 2))
        self.swipe(start_x, start_y, end_x, end_y, duration)

    def swipe_down(self, percentage: float = 0.5, duration: Optional[int] = None) -> None:
        """向下滑动"""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.2)
        end_x = start_x
        end_y = int(size["height"] * (0.5 + percentage / 2))
        self.swipe(start_x, start_y, end_x, end_y, duration)

    def swipe_left(self, percentage: float = 0.5, duration: Optional[int] = None) -> None:
        """向左滑动"""
        size = self.driver.get_window_size()
        start_x = int(size["width"] * 0.8)
        start_y = size["height"] // 2
        end_x = int(size["width"] * (0.5 - percentage / 2))
        end_y = start_y
        self.swipe(start_x, start_y, end_x, end_y, duration)

    def swipe_right(self, percentage: float = 0.5, duration: Optional[int] = None) -> None:
        """向右滑动"""
        size = self.driver.get_window_size()
        start_x = int(size["width"] * 0.2)
        start_y = size["height"] // 2
        end_x = int(size["width"] * (0.5 + percentage / 2))
        end_y = start_y
        self.swipe(start_x, start_y, end_x, end_y, duration)

    # ==================== 设备操作 ====================

    def press_keycode(self, keycode: int) -> None:
        """按下物理按键（Android）"""
        self.logger.debug(f"Pressing keycode: {keycode}")
        self.driver.press_keycode(keycode)

    def hide_keyboard(self) -> None:
        """隐藏键盘"""
        try:
            self.driver.hide_keyboard()
            self.logger.debug("Keyboard hidden")
        except Exception:
            pass

    def get_page_source(self) -> str:
        """获取页面源码"""
        return self.driver.page_source

    # ==================== 截图操作 ====================

    def _take_screenshot(self, name: str) -> str:
        """失败时自动截图"""
        screenshot_dir = Settings.SCREENSHOTS_DIR
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        filepath = screenshot_dir / f"{name}_{int(time.time())}.png"
        self.driver.save_screenshot(str(filepath))
        self.logger.error(f"Screenshot saved: {filepath}")
        return str(filepath)

    def take_screenshot(self, name: str) -> str:
        """手动截图"""
        return self._take_screenshot(name)

    # ==================== Context 操作 ====================

    def switch_to_context(self, context_name: str) -> None:
        """切换到指定的 WebView Context"""
        self.driver.switch_to.context(context_name)

    def get_current_context(self) -> str:
        """获取当前 Context"""
        return self.driver.current_context

    def switch_to_default_content(self) -> None:
        """切换到原生 APP（default content）"""
        self.driver.switch_to.default_content()