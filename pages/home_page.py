"""
pages/home_page.py
首页页面对象模块
封装首页的元素定位和业务操作
遵循 POM 模式，提供首页导航和商品浏览等操作方法
"""

from typing import Optional, List
from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class HomePage(BasePage):
    """
    首页页面对象类
    继承自 BasePage，提供首页的所有操作方法
    """

    class Locators:
        """
        首页元素定位符集合
        使用 UiSelector 方式定位，支持正则匹配 resourceId、text 和 description
        """
        SEARCH_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Search")')
        CART_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*cart.*")')
        USER_PROFILE_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*profile.*")')
        NOTIFICATION_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Notifications")')
        BANNER_SLIDER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*banner.*")')
        PRODUCT_ITEMS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*product.*")')
        CATEGORY_ICONS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*category.*")')
        HOME_TITLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Home")')
        LOGOUT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Logout")')
        SETTINGS_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Settings")')

    def __init__(self, driver):
        """
        初始化首页页面对象

        :param driver: WebDriver 实例
        """
        super().__init__(driver)
        self.platform = self.get_platform()

    def is_page_loaded(self, timeout: Optional[int] = None) -> bool:
        """
        判断首页是否加载完成

        :param timeout: 超时时间（秒）
        :return: 页面标题是否可见
        """
        return self.action.is_element_visible(*self.Locators.HOME_TITLE, timeout=timeout or 10)

    def click_search_icon(self) -> None:
        """点击搜索图标"""
        self.logger.step("click_search_icon", "Click search icon")
        self.action.click(*self.Locators.SEARCH_ICON)

    def click_cart_icon(self) -> None:
        """点击购物车图标"""
        self.logger.step("click_cart_icon", "Click cart icon")
        self.action.click(*self.Locators.CART_ICON)

    def click_user_profile(self) -> None:
        """点击用户头像图标"""
        self.logger.step("click_user_profile", "Click user profile icon")
        self.action.click(*self.Locators.USER_PROFILE_ICON)

    def click_notification_icon(self) -> None:
        """点击通知图标"""
        self.logger.step("click_notification_icon", "Click notification icon")
        self.action.click(*self.Locators.NOTIFICATION_ICON)

    def get_product_count(self) -> int:
        """
        获取页面中商品数量

        :return: 商品元素数量
        """
        try:
            products = self.driver.find_elements(*self.Locators.PRODUCT_ITEMS)
            return len(products)
        except Exception:
            return 0

    def get_banner_count(self) -> int:
        """
        获取页面中 Banner 数量

        :return: Banner 元素数量
        """
        try:
            banners = self.driver.find_elements(*self.Locators.BANNER_SLIDER)
            return len(banners)
        except Exception:
            return 0

    def swipe_banner_left(self) -> None:
        """向左滑动 Banner"""
        self.logger.step("swipe_banner_left", "Swipe banner to left")
        self.action.swipe_left(percentage=0.8)

    def swipe_banner_right(self) -> None:
        """向右滑动 Banner"""
        self.logger.step("swipe_banner_right", "Swipe banner to right")
        self.action.swipe_right(percentage=0.8)

    def click_first_product(self) -> None:
        """点击第一个商品"""
        self.logger.step("click_first_product", "Click first product")
        products = self.driver.find_elements(*self.Locators.PRODUCT_ITEMS)
        if products:
            products[0].click()

    def click_category_by_index(self, index: int) -> None:
        """
        根据索引点击分类图标

        :param index: 分类索引（从 0 开始）
        """
        self.logger.step("click_category_by_index", f"Click category at index {index}")
        categories = self.driver.find_elements(*self.Locators.CATEGORY_ICONS)
        if categories and index < len(categories):
            categories[index].click()

    def logout(self) -> None:
        """
        执行登出操作
        流程：点击头像 -> 等待登出按钮可点击 -> 点击登出
        """
        self.logger.step("logout", "Perform logout")
        self.click_user_profile()
        self.action.wait_for_element(*self.Locators.LOGOUT_BUTTON, timeout=10, state="clickable")
        self.action.click(*self.Locators.LOGOUT_BUTTON)

    def is_logged_in(self) -> bool:
        """
        判断用户是否已登录

        :return: 用户头像图标是否可见
        """
        return self.action.is_element_visible(*self.Locators.USER_PROFILE_ICON, timeout=5)

    def click_settings(self) -> None:
        """点击设置按钮"""
        self.logger.step("click_settings", "Click settings button")
        self.action.click(*self.Locators.SETTINGS_BUTTON)