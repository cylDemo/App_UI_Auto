"""
core/assertions.py
自定义断言方法库
提供丰富的断言方法，用于测试用例中的验证
断言失败时自动记录日志并抛出 AssertionError
"""

from typing import Optional, Any, List
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config.settings import Settings
from core.logger import TestLogger


class Assertions:
    """
    自定义断言方法库
    封装常用的断言操作，统一处理：
    - 显式等待：等待元素达到预期状态后再验证
    - 日志记录：记录断言执行过程
    - 失败截图：断言失败时自动截图
    """

    def __init__(self, driver):
        """
        初始化断言库

        :param driver: WebDriver 实例
        """
        self.driver = driver
        self.logger = TestLogger(self.__class__.__name__)

    def assert_element_visible(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = None,
        message: Optional[str] = None
    ) -> None:
        """
        断言元素可见

        :param by: 定位方式
        :param value: 定位表达式
        :param timeout: 超时时间
        :param message: 自定义失败消息
        """
        timeout = timeout or Settings.EXPLICIT_WAIT_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            self.logger.debug(f"Assert passed: Element visible {by}={value}")
        except TimeoutException:
            self.logger.error(f"Assert failed: Element not visible {by}={value}")
            raise AssertionError(message or f"Element not visible: {by}={value}")

    def assert_element_invisible(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = None,
        message: Optional[str] = None
    ) -> None:
        """
        断言元素不可见（已消失/隐藏）

        :param by: 定位方式
        :param value: 定位表达式
        :param timeout: 超时时间
        :param message: 自定义失败消息
        """
        timeout = timeout or Settings.EXPLICIT_WAIT_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, value))
            )
            self.logger.debug(f"Assert passed: Element invisible {by}={value}")
        except TimeoutException:
            self.logger.error(f"Assert failed: Element still visible {by}={value}")
            raise AssertionError(message or f"Element still visible: {by}={value}")

    def assert_element_clickable(
        self,
        by: str,
        value: str,
        timeout: Optional[int] = None,
        message: Optional[str] = None
    ) -> None:
        """
        断言元素可点击

        :param by: 定位方式
        :param value: 定位表达式
        :param timeout: 超时时间
        :param message: 自定义失败消息
        """
        timeout = timeout or Settings.EXPLICIT_WAIT_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            self.logger.debug(f"Assert passed: Element clickable {by}={value}")
        except TimeoutException:
            self.logger.error(f"Assert failed: Element not clickable {by}={value}")
            raise AssertionError(message or f"Element not clickable: {by}={value}")

    def assert_text_equals(
        self,
        by: str,
        value: str,
        expected_text: str,
        timeout: Optional[int] = None,
        message: Optional[str] = None
    ) -> None:
        """
        断言元素文本等于预期值

        :param by: 定位方式
        :param value: 定位表达式
        :param expected_text: 预期的文本内容
        :param timeout: 超时时间
        :param message: 自定义失败消息
        """
        element = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT_TIMEOUT).until(
            EC.presence_of_element_located((by, value))
        )
        actual_text = element.text
        if actual_text != expected_text:
            self.logger.error(f"Assert failed: Text mismatch. Expected: '{expected_text}', Actual: '{actual_text}'")
            raise AssertionError(
                message or f"Text mismatch. Expected: '{expected_text}', Actual: '{actual_text}'"
            )
        self.logger.debug(f"Assert passed: Text equals '{expected_text}'")

    def assert_text_contains(
        self,
        by: str,
        value: str,
        expected_text: str,
        timeout: Optional[int] = None,
        message: Optional[str] = None
    ) -> None:
        """
        断言元素文本包含预期字符串

        :param by: 定位方式
        :param value: 定位表达式
        :param expected_text: 预期的子字符串
        :param timeout: 超时时间
        :param message: 自定义失败消息
        """
        element = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT_TIMEOUT).until(
            EC.presence_of_element_located((by, value))
        )
        actual_text = element.text
        if expected_text not in actual_text:
            self.logger.error(f"Assert failed: Text does not contain. Expected to contain: '{expected_text}', Actual: '{actual_text}'")
            raise AssertionError(
                message or f"Text does not contain: '{expected_text}', Actual: '{actual_text}'"
            )
        self.logger.debug(f"Assert passed: Text contains '{expected_text}'")

    def assert_attribute(
        self,
        by: str,
        value: str,
        attribute: str,
        expected_value: str,
        timeout: Optional[int] = None,
        message: Optional[str] = None
    ) -> None:
        """
        断言元素属性值等于预期值

        :param by: 定位方式
        :param value: 定位表达式
        :param attribute: 属性名称
        :param expected_value: 预期的属性值
        :param timeout: 超时时间
        :param message: 自定义失败消息
        """
        element = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT_TIMEOUT).until(
            EC.presence_of_element_located((by, value))
        )
        actual_value = element.get_attribute(attribute)
        if actual_value != expected_value:
            self.logger.error(f"Assert failed: Attribute '{attribute}' mismatch. Expected: '{expected_value}', Actual: '{actual_value}'")
            raise AssertionError(
                message or f"Attribute '{attribute}' mismatch. Expected: '{expected_value}', Actual: '{actual_value}'"
            )
        self.logger.debug(f"Assert passed: Attribute '{attribute}' equals '{expected_value}'")

    def assert_attribute_contains(
        self,
        by: str,
        value: str,
        attribute: str,
        expected_value: str,
        timeout: Optional[int] = None,
        message: Optional[str] = None
    ) -> None:
        """
        断言元素属性值包含预期字符串

        :param by: 定位方式
        :param value: 定位表达式
        :param attribute: 属性名称
        :param expected_value: 预期的子字符串
        :param timeout: 超时时间
        :param message: 自定义失败消息
        """
        element = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT_TIMEOUT).until(
            EC.presence_of_element_located((by, value))
        )
        actual_value = element.get_attribute(attribute) or ""
        if expected_value not in actual_value:
            self.logger.error(f"Assert failed: Attribute '{attribute}' does not contain. Expected to contain: '{expected_value}', Actual: '{actual_value}'")
            raise AssertionError(
                message or f"Attribute '{attribute}' does not contain: '{expected_value}', Actual: '{actual_value}'"
            )
        self.logger.debug(f"Assert passed: Attribute '{attribute}' contains '{expected_value}'")

    def assert_toast_message(
        self,
        message: str,
        timeout: Optional[int] = None,
        custom_message: Optional[str] = None
    ) -> None:
        """
        断言 Toast 提示信息出现

        :param message: Toast 中的关键词
        :param timeout: 超时时间
        :param custom_message: 自定义失败消息
        """
        timeout = timeout or Settings.EXPLICIT_WAIT_TIMEOUT
        try:
            toast_locator = f"//*[contains(@text, '{message}')]"
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(("xpath", toast_locator))
            )
            self.logger.debug(f"Assert passed: Toast message visible '{message}'")
        except TimeoutException:
            self.logger.error(f"Assert failed: Toast message not visible '{message}'")
            raise AssertionError(custom_message or f"Toast message not visible: {message}")

    def assert_list_not_empty(
        self,
        elements: List[Any],
        message: Optional[str] = None
    ) -> None:
        """
        断言列表不为空

        :param elements: 元素列表
        :param message: 自定义失败消息
        """
        if not elements or len(elements) == 0:
            self.logger.error(f"Assert failed: List is empty")
            raise AssertionError(message or "List is empty")
        self.logger.debug(f"Assert passed: List has {len(elements)} elements")

    def assert_equal(
        self,
        actual: Any,
        expected: Any,
        message: Optional[str] = None
    ) -> None:
        """
        断言两个值相等

        :param actual: 实际值
        :param expected: 预期值
        :param message: 自定义失败消息
        """
        if actual != expected:
            self.logger.error(f"Assert failed: Values not equal. Expected: '{expected}', Actual: '{actual}'")
            raise AssertionError(message or f"Values not equal. Expected: '{expected}', Actual: '{actual}'")
        self.logger.debug(f"Assert passed: '{actual}' equals '{expected}'")

    def assert_true(
        self,
        condition: bool,
        message: Optional[str] = None
    ) -> None:
        """
        断言条件为 True

        :param condition: 条件表达式
        :param message: 自定义失败消息
        """
        if not condition:
            self.logger.error(f"Assert failed: Condition is not True")
            raise AssertionError(message or "Condition is not True")
        self.logger.debug("Assert passed: Condition is True")

    def assert_false(
        self,
        condition: bool,
        message: Optional[str] = None
    ) -> None:
        """
        断言条件为 False

        :param condition: 条件表达式
        :param message: 自定义失败消息
        """
        if condition:
            self.logger.error(f"Assert failed: Condition is not False")
            raise AssertionError(message or "Condition is not False")
        self.logger.debug("Assert passed: Condition is False")

    def assert_is_not_none(
        self,
        value: Any,
        message: Optional[str] = None
    ) -> None:
        """
        断言值不为 None

        :param value: 要验证的值
        :param message: 自定义失败消息
        """
        if value is None:
            self.logger.error(f"Assert failed: Value is None")
            raise AssertionError(message or "Value is None")
        self.logger.debug("Assert passed: Value is not None")