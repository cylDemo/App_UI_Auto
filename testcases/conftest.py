"""
testcases/conftest.py
Pytest 配置和 Fixtures 定义
提供 Driver 管理、页面对象注入、命令行参数等基础设施
"""

import pytest
import allure
from typing import Optional
from pathlib import Path

from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import RemoteConnection

from config.settings import Settings
from core.driver_manager import DriverManager
from core.logger import TestLogger
from utils.allure_util import AllureUtil


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest Hook - 测试报告生成钩子
    在测试失败时自动截图并附加到 Allure 报告

    :param item: 测试项
    :param call: 调用信息
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = None
        if hasattr(item, "fixturenames") and "driver" in item.fixturenames:
            driver_fixture = item.funcargs.get("driver")
            if driver_fixture:
                driver = driver_fixture

        if driver:
            screenshot_path = AllureUtil.take_screenshot(driver, f"failure_{item.name}")
            if screenshot_path:
                allure.attach.file(
                    screenshot_path,
                    name=f"Failure Screenshot - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )


def pytest_addoption(parser):
    """
    添加自定义命令行参数
    支持 --platform, --device, --app-path, --appium-url
    """
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        choices=["android", "ios"],
        help="Target platform: android or ios"
    )
    parser.addoption(
        "--device-name",
        action="store",
        default="android_emulator_1",
        help="Device name from devices.yaml"
    )
    parser.addoption(
        "--app-path",
        action="store",
        default=None,
        help="Path to the application APK or IPA file"
    )
    parser.addoption(
        "--appium-url",
        action="store",
        default=None,
        help="Appium server URL"
    )


@pytest.fixture(scope="session")
def appium_server_url(request):
    """
    获取 Appium 服务器 URL

    :param request: pytest request 对象
    :return: Appium 服务器地址
    """
    return request.config.getoption("--appium-url") or Settings.APPIUM_SERVER_URL


@pytest.fixture(scope="session")
def app_package(request):
    """
    获取应用包名

    :param request: pytest request 对象
    :return: 包名（如 com.example.app）
    """
    platform = request.config.getoption("--platform")
    device = request.config.getoption("--device-name")
    device_config = Settings.get_device_config(platform, device)
    return device_config.get("capabilities", {}).get("appPackage")


@pytest.fixture(scope="session")
def appium_options(request):
    """
    创建 Appium Options 配置
    根据平台类型选择 UiAutomator2Options 或 XCUITestOptions

    :param request: pytest request 对象
    :return: Appium Options 实例
    """
    platform = request.config.getoption("--platform")
    device = request.config.getoption("--device-name")
    app_path = request.config.getoption("--app-path")

    capabilities = Settings.merge_capabilities(platform, device)

    if app_path:
        capabilities["app"] = app_path

    if platform == Settings.PLATFORM_ANDROID:
        from appium.options.android import UiAutomator2Options
        options = UiAutomator2Options()
    elif platform == Settings.PLATFORM_IOS:
        from appium.options.ios import XCUITestOptions
        options = XCUITestOptions()
    else:
        raise ValueError(f"Unsupported platform: {platform}")

    for key, value in capabilities.items():
        if hasattr(options, key):
            setattr(options, key, value)
        else:
            options.set_capability(key, value)

    return options


@pytest.fixture(scope="session")
def driver_pool(request, appium_server_url, appium_options):
    """
    Session 级别的 Driver 池
    支持 pytest-xdist 并发执行，所有测试共享同一个 Driver 实例

    :param request: pytest request 对象
    :param appium_server_url: Appium 服务器地址
    :param appium_options: Appium 配置选项
    :return: WebDriver 实例
    """
    platform = request.config.getoption("--platform")
    device = request.config.getoption("--device-name")

    logger = TestLogger("SessionFixture")
    logger.info(f"Creating session driver for {platform} - {device}")

    driver = WebDriver(
        command_executor=RemoteConnection(appium_server_url),
        options=appium_options
    )
    driver.implicitly_wait(Settings.IMPLICIT_WAIT_TIMEOUT)

    yield driver

    logger.info("Quitting session driver")
    try:
        driver.quit()
    except Exception as e:
        logger.error(f"Error quitting driver: {e}")


@pytest.fixture(scope="function")
def driver(driver_pool):
    """
    Function 级别的 Driver Fixture
    每个测试函数获取独立的 Driver 实例
    自动记录测试开始和结束日志

    :param driver_pool: Session 级别的 Driver 池
    :return: WebDriver 实例
    """
    logger = TestLogger("FunctionFixture")
    test_name = None
    try:
        import sys
        frame = sys._getframe(1)
        test_name = frame.f_code.co_name
    except Exception:
        pass

    if test_name:
        logger.start_test(test_name)

    yield driver_pool

    if test_name:
        logger.end_test(test_name, "Completed")


@pytest.fixture(scope="function")
def login_flow(driver):
    """
    提供登录流程对象

    :param driver: WebDriver 实例
    :return: LoginFlow 实例
    """
    from flows.login_flow import LoginFlow
    return LoginFlow(driver)


@pytest.fixture(scope="function")
def login_page(driver):
    """
    提供登录页面对象

    :param driver: WebDriver 实例
    :return: LoginPage 实例
    """
    from pages.login_page import LoginPage
    return LoginPage(driver)


@pytest.fixture(scope="function")
def home_page(driver):
    """
    提供首页页面对象

    :param driver: WebDriver 实例
    :return: HomePage 实例
    """
    from pages.app_navigation import HomePage
    return HomePage(driver)


@pytest.fixture(scope="function")
def my_page(driver):
    """
    提供我的页面对象

    :param driver: WebDriver 实例
    :return: MyPage 实例
    """
    from pages.app_navigation import MyPage
    return MyPage(driver)


@pytest.fixture(scope="function")
def agreement_page(driver):
    """
    提供协议弹窗页面对象

    :param driver: WebDriver 实例
    :return: AgreementPage 实例
    """
    from pages.app_navigation import AgreementPage
    return AgreementPage(driver)


@pytest.fixture(scope="function")
def app_navigation(driver):
    """
    提供应用导航对象

    :param driver: WebDriver 实例
    :return: AppNavigation 实例
    """
    from pages.app_navigation import AppNavigation
    return AppNavigation(driver)


@pytest.fixture(scope="session")
def platform(request):
    """
    获取测试平台

    :param request: pytest request 对象
    :return: 'android' 或 'ios'
    """
    return request.config.getoption("--platform")


@pytest.fixture(scope="session")
def device_name(request):
    """
    获取设备名称

    :param request: pytest request 对象
    :return: 设备名称
    """
    return request.config.getoption("--device-name")


def pytest_configure(config):
    """
    Pytest 配置钩子
    初始化测试报告和日志目录
    """
    Settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    Settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """
    修改测试用例集合钩子
    自动为测试用例添加标记（login, shopping 等）

    :param config: Pytest 配置对象
    :param items: 测试用例列表
    """
    for item in items:
        if "login" in item.nodeid.lower():
            item.add_marker(pytest.mark.login)
        if "shopping" in item.nodeid.lower() or "cart" in item.nodeid.lower():
            item.add_marker(pytest.mark.shopping)