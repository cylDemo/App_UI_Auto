"""
pages/login_page.py
登录页面对象模块
封装登录页面的元素定位和业务操作
遵循 POM 模式，方法仅包含业务操作，不含断言
"""

from typing import Optional
from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage, Locator


class LoginPage(BasePage):
    """
    登录页面对象类
    继承自 BasePage，提供登录页面的所有操作方法
    """

    class Locators:
        """
        登录页面元素定位符集合
        使用 UiSelector 方式定位，基于实际元素的 resource-id
        """
        ACCOUNT_LOGIN_TAB = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.mymoney.sms:id/account_login_tv")')
        USERNAME_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.mymoney.sms:id/account_et")')
        PASSWORD_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.mymoney.sms:id/edittext")')
        LOGIN_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.mymoney.sms:id/login_btn")')
        AGREEMENT_CHECKBOX = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.mymoney.sms:id/cb_ok")')
        FORGOT_PASSWORD_LINK = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Forgot Password")')
        REGISTER_LINK = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Register")')
        ERROR_MESSAGE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*error.*")')
        LOADING_INDICATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*loading.*")')
        LOGIN_TITLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login")')
        REMEMBER_ME_CHECKBOX = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*remember.*")')

    def __init__(self, driver):
        """
        初始化登录页面对象

        :param driver: WebDriver 实例
        """
        super().__init__(driver)
        self.platform = self.get_platform()

    def is_page_loaded(self, timeout: Optional[int] = None) -> bool:
        """
        判断登录页面是否加载完成

        :param timeout: 超时时间（秒）
        :return: 页面标题是否可见
        """
        return self.action.is_element_visible(*self.Locators.LOGIN_TITLE, timeout=timeout or 10)

    def click_account_login_tab(self) -> None:
        """
        点击账号密码登录切换到账号登录页面
        """
        self.logger.step("click_account_login_tab", "Click account login tab")
        self.action.click(*self.Locators.ACCOUNT_LOGIN_TAB)

    def input_username(self, username: str) -> None:
        """
        输入用户名

        :param username: 用户名
        """
        self.logger.step("input_username", f"Input username: {username}")
        self.action.input_text(*self.Locators.USERNAME_INPUT, username, clear_first=True)

    def input_password(self, password: str) -> None:
        """
        输入密码

        :param password: 密码
        """
        self.logger.step("input_password", f"Input password: {password}")
        self.action.input_text(*self.Locators.PASSWORD_INPUT, password, clear_first=True)

    def click_agreement_checkbox(self) -> None:
        """
        勾选同意协议复选框
        """
        self.logger.step("click_agreement_checkbox", "Click agreement checkbox")
        self.action.click(*self.Locators.AGREEMENT_CHECKBOX)

    def is_agreement_checked(self) -> bool:
        """
        检查同意协议复选框是否已勾选

        :return: 是否已勾选
        """
        return self.action.is_element_selected(*self.Locators.AGREEMENT_CHECKBOX)

    def click_login_button(self) -> None:
        """点击登录按钮"""
        self.logger.step("click_login_button", "Click login button")
        self.action.click(*self.Locators.LOGIN_BUTTON)

    def click_forgot_password(self) -> None:
        """点击忘记密码链接"""
        self.logger.step("click_forgot_password", "Click forgot password link")
        self.action.click(*self.Locators.FORGOT_PASSWORD_LINK)

    def click_register_link(self) -> None:
        """点击注册链接"""
        self.logger.step("click_register_link", "Click register link")
        self.action.click(*self.Locators.REGISTER_LINK)

    def click_remember_me(self) -> None:
        """点击记住我复选框"""
        self.logger.step("click_remember_me", "Click remember me checkbox")
        self.action.click(*self.Locators.REMEMBER_ME_CHECKBOX)

    def get_error_message(self) -> str:
        """
        获取错误提示信息

        :return: 错误信息文本，无错误时返回空字符串
        """
        if self.action.is_element_visible(*self.Locators.ERROR_MESSAGE, timeout=5):
            return self.action.get_text(*self.Locators.ERROR_MESSAGE)
        return ""

    def is_login_button_enabled(self) -> bool:
        """
        判断登录按钮是否可点击

        :return: 按钮是否可点击
        """
        return self.action.is_element_clickable(*self.Locators.LOGIN_BUTTON, timeout=5)

    def is_loading_visible(self) -> bool:
        """
        判断 Loading 指示器是否可见

        :return: Loading 是否可见
        """
        return self.action.is_element_visible(*self.Locators.LOADING_INDICATOR, timeout=3)

    def wait_for_loading_disappear(self, timeout: Optional[int] = None) -> bool:
        """
        等待 Loading 指示器消失

        :param timeout: 超时时间（秒）
        :return: Loading 是否在超时时间内消失
        """
        timeout = timeout or 30
        return self.action.wait_for_element(*self.Locators.LOADING_INDICATOR, timeout=timeout, state="invisible")

    def is_login_success(self, timeout: int = 10) -> bool:
        """
        判断登录是否成功（通过检查是否离开登录页面）

        :param timeout: 等待超时时间
        :return: 是否登录成功
        """
        return not self.action.is_element_visible(*self.Locators.LOGIN_BUTTON, timeout=timeout)

    def is_login_failed(self, timeout: int = 5) -> bool:
        """
        判断登录是否失败（通过检查错误信息是否显示）

        :param timeout: 等待超时时间
        :return: 是否登录失败
        """
        error_msg = self.get_error_message()
        return len(error_msg) > 0

    def perform_login(self, username: str, password: str, remember_me: bool = False) -> None:
        """
        执行完整的登录流程

        :param username: 用户名
        :param password: 密码
        :param remember_me: 是否勾选记住我
        """
        self.logger.step("perform_login", f"Login with username: {username}")
        self.input_username(username)
        self.input_password(password)
        if remember_me:
            self.click_remember_me()
        self.click_login_button()

    def clear_username(self) -> None:
        """清空用户名输入框"""
        self.action.clear_text(*self.Locators.USERNAME_INPUT)

    def clear_password(self) -> None:
        """清空密码输入框"""
        self.action.clear_text(*self.Locators.PASSWORD_INPUT)

    def clear_credentials(self) -> None:
        """清空用户名和密码输入框"""
        self.clear_username()
        self.clear_password()