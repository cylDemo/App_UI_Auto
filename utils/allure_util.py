"""
utils/allure_util.py
Allure 报告附件处理工具模块
提供截图、文本、HTML、JSON 等附件的 Allure 报告集成能力
支持自动截图和失败重连等场景
"""

import time
import uuid
from pathlib import Path
from typing import Optional, Union
import allure


class AllureUtil:
    """
    Allure 报告附件处理工具类
    封装 Allure 报告的附件功能，便于测试过程中自动添加截图、日志等信息
    """

    @staticmethod
    def take_screenshot(driver, name: str) -> str:
        """
        截图并返回文件路径

        :param driver: WebDriver 实例
        :param name: 截图名称前缀
        :return: 截图文件完整路径
        """
        from config.settings import Settings
        screenshot_dir = Settings.SCREENSHOTS_DIR
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{name}_{int(time.time())}_{uuid.uuid4().hex[:6]}.png"
        filepath = screenshot_dir / filename
        driver.save_screenshot(str(filepath))
        return str(filepath)

    @staticmethod
    def attach_screenshot(
        driver,
        name: str,
        description: Optional[str] = None,
        attachment_type: allure.attachment_type = allure.attachment_type.PNG
    ) -> None:
        """
        截图并附加到 Allure 报告

        :param driver: WebDriver 实例
        :param name: 附件名称
        :param description: 附件描述
        :param attachment_type: 附件类型（默认 PNG）
        """
        filepath = AllureUtil.take_screenshot(driver, name)
        allure.attach.file(
            filepath,
            name=name,
            attachment_type=attachment_type
        )

    @staticmethod
    def attach_text(
        text: str,
        name: str,
        attachment_type: allure.attachment_type = allure.attachment_type.TEXT
    ) -> None:
        """
        附加文本到 Allure 报告

        :param text: 文本内容
        :param name: 附件名称
        :param attachment_type: 附件类型（默认 TEXT）
        """
        allure.attach(
            text,
            name=name,
            attachment_type=attachment_type
        )

    @staticmethod
    def attach_html(
        html: str,
        name: str
    ) -> None:
        """
        附加 HTML 到 Allure 报告

        :param html: HTML 内容
        :param name: 附件名称
        """
        allure.attach(
            html,
            name=name,
            attachment_type=allure.attachment_type.HTML
        )

    @staticmethod
    def attach_json(
        data: dict,
        name: str
    ) -> None:
        """
        附加 JSON 到 Allure 报告

        :param data: 要附加的字典数据
        :param name: 附件名称
        """
        import json
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        allure.attach(
            json_str,
            name=name,
            attachment_type=allure.attachment_type.JSON
        )