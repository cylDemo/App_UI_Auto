"""
testcases/test_login.py
登录模块测试用例集
包含登录相关测试场景，覆盖正常流程和异常流程
使用 Allure 报告标记，支持 Pytest 参数化执行
"""

import pytest
import allure
from typing import Dict

from pages.login_page import LoginPage
from core.logger import TestLogger


@allure.feature("登录模块")
@allure.story("用户登录功能")
class TestLogin:
    """
    登录功能测试类
    测试用例涵盖：正常登录、异常登录等场景
    """

    @allure.title("TC_001 - 使用错误密码登录失败")
    @allure.description("验证账号13033130008 + 密码123456 + 同意协议登录失败")
    @pytest.mark.login
    def test_login_with_wrong_password(
        self,
        driver,
        login_page: LoginPage,
        app_navigation
    ):
        """
        TC_001 - 使用错误密码登录失败

        测试步骤：
        0. 从启动页导航到登录页面
        1. 点击账号密码登录切换到账号登录页面
        2. 输入账号：13033130008
        3. 输入密码：123456
        4. 勾选同意协议
        5. 点击登录按钮
        6. 断言登录失败
        """
        logger = TestLogger("TestLogin")
        logger.start_test("TC_001 - Login with Wrong Password")

        with allure.step("0. 从启动页导航到登录页面"):
            app_navigation.navigate_to_login()

        with allure.step("1. 切换到账号密码登录页面"):
            login_page.click_account_login_tab()

        with allure.step("2. 输入账号和错误密码"):
            login_page.input_username("13033130008")
            login_page.input_password("123456")

        with allure.step("3. 勾选同意协议"):
            login_page.click_agreement_checkbox()

        with allure.step("4. 点击登录按钮"):
            login_page.click_login_button()

        with allure.step("5. 断言登录失败"):
            assert login_page.is_login_failed(timeout=10), "错误密码应该导致登录失败"
            error_msg = login_page.get_error_message()
            assert len(error_msg) > 0, "应该显示错误提示信息"
            self.logger.info(f"登录失败，错误信息：{error_msg}")

        logger.end_test("TC_001 - Login with Wrong Password", "PASSED")

    @allure.title("TC_002 - 使用正确密码登录成功")
    @allure.description("验证账号13033130008 + 密码test123 + 同意协议可成功登录")
    @pytest.mark.login
    @pytest.mark.smoke
    def test_login_with_correct_password(
        self,
        driver,
        login_page: LoginPage
    ):
        """
        TC_002 - 使用正确密码登录成功

        测试步骤：
        0. 清空账号和密码（TC_001失败后仍在登录页面）
        1. 输入账号：13033130008
        2. 输入密码：test123
        3. 勾选同意协议
        4. 点击登录按钮
        5. 断言登录成功
        """
        logger = TestLogger("TestLogin")
        logger.start_test("TC_002 - Login with Correct Password")

        with allure.step("0. 清空密码"):
            login_page.clear_password()

        with allure.step("2. 输入密码"):
            login_page.input_password("test123")

        with allure.step("3. 点击登录按钮"):
            login_page.click_login_button()

        with allure.step("4. 断言登录成功"):
            assert login_page.is_login_success(timeout=15), "登录成功"
            self.logger.info("登录成功")

        logger.end_test("TC_002 - Login with Correct Password", "PASSED")