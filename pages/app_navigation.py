'''
Author: yl18318350969 yl18318350969@163.com
Date: 2026-04-14 18:23:47
LastEditors: yl18318350969 yl18318350969@163.com
LastEditTime: 2026-04-15 14:36:47
FilePath: \App_UI_Auto\pages\app_navigation.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1/FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
pages/app_navigation.py
应用导航页面模块
封装从启动到登录页面的导航操作
包含：协议弹窗、首页登录入口
"""

from typing import Optional
from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class AgreementPage(BasePage):
    """
    服务协议弹窗页面对象
    处理首次启动时的协议同意操作
    """

    class Locators:
        AGREEMENT_AGREE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.mymoney.sms:id/sui_dialog_positive_btn")')

    def __init__(self, driver):
        super().__init__(driver)

    def click_agree_button_if_exists(self, timeout: int = 10) -> bool:
        """
        如果协议弹窗存在则点击同意按钮

        :param timeout: 等待弹窗的最大超时时间
        :return: 弹窗是否存在
        """
        if self.action.is_element_visible(*self.Locators.AGREEMENT_AGREE_BUTTON, timeout=timeout):
            self.logger.step("click_agree_button", "Agreement popup found, clicking agree")
            self.action.click(*self.Locators.AGREEMENT_AGREE_BUTTON)
            self.action.wait_for_element(*self.Locators.AGREEMENT_AGREE_BUTTON, timeout=5, state="invisible")
            return True
        else:
            self.logger.step("click_agree_button", "Agreement popup not found, skipping")
            return False


class HomePage(BasePage):
    """
    首页（账单页面）对象
    提供首页快捷登录入口操作
    """

    class Locators:
        LOGIN_REGISTER_BTN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("登录/注册")')

    def __init__(self, driver):
        super().__init__(driver)

    def click_login_register(self, timeout: int = 10) -> None:
        self.logger.step("click_login_register", "Click login/register button on home page")
        self.action.wait_for_element(*self.Locators.LOGIN_REGISTER_BTN, timeout=timeout, state="clickable")
        self.action.click(*self.Locators.LOGIN_REGISTER_BTN)


class AppNavigation:
    """
    应用导航类
    整合从启动到登录页面的完整流程
    """

    def __init__(self, driver):
        self.driver = driver
        self.agreement_page = AgreementPage(driver)
        self.home_page = HomePage(driver)

    def navigate_to_login(self) -> None:
        """
        从应用启动到进入登录页面的完整导航流程

        流程：
        1. 检查是否已在登录页面
        2. 如果已在登录页面，清空账号密码后返回
        3. 否则执行正常导航流程：点击协议弹窗 -> 点击登录/注册
        """
        from pages.login_page import LoginPage
        temp_login_page = LoginPage(self.driver)

        if temp_login_page.action.is_element_visible(*temp_login_page.Locators.USERNAME_INPUT, timeout=3):
            self.logger.step("navigate_to_login", "Already on login page, clearing fields")
            temp_login_page.action.clear_text(*temp_login_page.Locators.USERNAME_INPUT)
            temp_login_page.action.clear_text(*temp_login_page.Locators.PASSWORD_INPUT)
            return

        self.agreement_page.click_agree_button_if_exists(timeout=10)
        self.home_page.click_login_register()