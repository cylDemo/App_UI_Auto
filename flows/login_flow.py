"""
flows/login_flow.py
登录业务流程封装模块
组合多个页面对象的操作，形成完整的登录业务流程
支持有效/无效凭证登录、登出等场景
"""

from appium.webdriver.webdriver import WebDriver
from typing import Optional

from pages.login_page import LoginPage
from pages.home_page import HomePage
from core.logger import TestLogger


class LoginFlow:
    """
    登录业务流程封装类
    组合 LoginPage 和 HomePage 的操作，提供完整的登录业务能力
    """

    def __init__(self, driver: WebDriver):
        """
        初始化登录流程

        :param driver: WebDriver 实例
        """
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)
        self.logger = TestLogger(self.__class__.__name__)

    def login_with_valid_credentials(
        self,
        username: str,
        password: str,
        remember_me: bool = False,
        wait_for_home: bool = True
    ) -> bool:
        """
        使用有效凭证登录

        :param username: 用户名
        :param password: 密码
        :param remember_me: 是否记住我
        :param wait_for_home: 是否等待首页加载
        :return: 登录是否成功
        """
        self.logger.step("login_with_valid_credentials", f"Login with username: {username}")
        self.login_page.perform_login(username, password, remember_me)

        if wait_for_home:
            return self.home_page.wait_for_page_load(timeout=30)
        return True

    def login_with_valid_account(
        self,
        platform: str = "android",
        remember_me: bool = False
    ) -> bool:
        """
        使用预置的有效账号登录

        :param platform: 平台类型（android/ios）
        :param remember_me: 是否记住我
        :return: 登录是否成功
        """
        from data.test_data_builder import AccountData
        account_data = AccountData(platform)
        valid_account = account_data.get_valid_account()
        return self.login_with_valid_credentials(
            username=valid_account.get("username"),
            password=valid_account.get("password"),
            remember_me=remember_me
        )

    def login_with_invalid_password(
        self,
        username: str,
        password: str
    ) -> str:
        """
        使用无效密码登录（验证错误提示）

        :param username: 用户名
        :param password: 错误密码
        :return: 错误提示信息
        """
        self.logger.step("login_with_invalid_password", f"Login with invalid password for: {username}")
        self.login_page.perform_login(username, password)
        self.login_page.wait_for_loading_disappear()
        return self.login_page.get_error_message()

    def login_with_empty_credentials(self) -> tuple:
        """
        使用空凭证登录（验证必填提示）

        :return: 用户名错误提示
        """
        self.logger.step("login_with_empty_credentials", "Login with empty credentials")
        self.login_page.click_login_button()
        username_error = self.login_page.get_error_message()
        return username_error

    def logout(self) -> None:
        """执行登出流程"""
        self.logger.step("logout", "Perform logout flow")
        self.home_page.logout()

    def is_login_successful(self) -> bool:
        """
        判断登录是否成功

        :return: 首页是否加载完成
        """
        return self.home_page.is_page_loaded(timeout=10)

    def is_on_login_page(self) -> bool:
        """
        判断当前是否在登录页

        :return: 登录页是否加载完成
        """
        return self.login_page.is_page_loaded(timeout=5)

    def wait_for_login_page(self, timeout: Optional[int] = None) -> bool:
        """
        等待登录页加载

        :param timeout: 超时时间（秒）
        :return: 登录页是否在超时时间内加载完成
        """
        timeout = timeout or 10
        return self.login_page.wait_for_page_load(timeout=timeout)