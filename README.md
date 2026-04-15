# App\_UI\_Auto 移动端 UI 自动化测试框架

## 项目概述

基于 Python + Pytest + Appium 2.x + Allure 的企业级移动端 UI 自动化测试框架，采用 Page Object Model (POM) 设计模式，支持 Android/iOS 双平台。

### 核心特性

- **POM 模式**：页面元素定位与业务操作分离，代码复用性高
- **分层架构**：清晰的模块划分（Config/Core/Pages/Flows/TestCases）
- **多平台支持**：一套代码支持 Android 和 iOS
- **丰富断言**：内置多种断言方法，失败自动截图
- **Allure 报告**：美观的测试报告，支持截图、日志等附件
- **并发执行**：支持 pytest-xdist 多进程并行

## 技术栈

| 类别         | 技术           | 版本要求   |
| ---------- | ------------ | ------ |
| 语言         | Python       | 3.8+   |
| 测试框架       | Pytest       | 7.0+   |
| 移动端        | Appium       | 2.x    |
| Android 驱动 | UiAutomator2 | Latest |
| iOS 驱动     | XCUITest     | Latest |
| 报告         | Allure       | 2.x    |
| 并发         | pytest-xdist | Latest |

## 项目结构

```
App_UI_Auto/
├── config/                 # 配置模块
│   ├── __init__.py
│   ├── settings.py        # 全局配置管理
│   └── devices.yaml        # 设备配置
├── core/                  # 核心层
│   ├── __init__.py
│   ├── base_action.py     # 基础动作封装
│   ├── assertions.py       # 自定义断言库
│   ├── driver_manager.py   # Driver 工厂
│   └── logger.py           # 日志工具
├── pages/                 # 表现层 - 页面对象
│   ├── __init__.py
│   ├── base_page.py        # 页面基类
│   ├── login_page.py       # 登录页
│   └── home_page.py        # 首页
├── flows/                 # 业务流层
│   ├── __init__.py
│   └── login_flow.py       # 登录流程
├── data/                  # 数据层
│   ├── __init__.py
│   ├── account.yaml        # 测试账号数据
│   └── test_data_builder.py # 数据构造器
├── testcases/             # 测试用例
│   ├── __init__.py
│   ├── conftest.py         # Pytest 配置
│   ├── test_login.py       # 登录测试
│   └── test_shopping_cart.py # 购物车测试
├── utils/                  # 工具模块
│   ├── __init__.py
│   ├── file_reader.py      # 文件读取
│   ├── adb_helper.py       # ADB 工具
│   └── allure_util.py       # Allure 辅助
├── scripts/                # 脚本目录
│   └── start_appium.bat    # Appium 启动脚本
├── pytest.ini              # Pytest 配置
├── requirements.txt        # 依赖清单
└── README.md               # 本文档
```

## 快速开始

### 1. 环境准备

```bash
# Python 环境
python --version  # 确保 Python 3.8+

# 安装依赖
pip install -r requirements.txt

# 安装 Appium Server
npm install -g appium

# 启动 Appium Server
appium --host 127.0.0.1 --port 4723
```

### 2. 配置设备

编辑 `config/devices.yaml` 配置待测设备：

```yaml
android_emulator_1:
  platform: android
  capabilities:
    appPackage: com.example.app
    appActivity: .MainActivity
    platformVersion: "11.0"
    deviceName: emulator-5554
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行指定测试类
pytest testcases/test_login.py

# 运行带标记的测试
pytest -m smoke

# 指定平台和设备
pytest --platform=android --device=android_emulator_1
```

## 使用指南

### 编写测试用例

```python
import pytest
import allure
from flows.login_flow import LoginFlow
from data.test_data_builder import AccountData

@allure.feature("登录模块")
@allure.story("用户登录功能")
class TestLogin:

    @allure.title("TC_001 - 使用有效账号登录成功")
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, driver, login_flow, platform):
        """测试有效账号登录"""
        account_data = AccountData(platform)
        valid_account = account_data.get_valid_account()

        with allure.step("1. 执行登录"):
            result = login_flow.login_with_valid_credentials(
                username=valid_account["username"],
                password=valid_account["password"]
            )

        with allure.step("2. 验证结果"):
            assert result is True
```

### 编写页面对象

```python
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class LoginPage(BasePage):

    class Locators:
        USERNAME_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*username.*")')
        LOGIN_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login")')

    def input_username(self, username: str) -> None:
        """输入用户名"""
        self.action.input_text(*self.Locators.USERNAME_INPUT, username)

    def click_login(self) -> None:
        """点击登录"""
        self.action.click(*self.Locators.LOGIN_BUTTON)
```

### 使用自定义断言

```python
# 断言元素可见
self.assertion.assert_element_visible(*locators)

# 断言文本内容
self.assertion.assert_text_equals(*locators, expected_text="Hello")

# 断言 Toast 消息
self.assertion.assert_toast_message("操作成功")

# 断言属性值
self.assertion.assert_attribute(*locators, attribute="checked", expected_value="true")
```

## 配置说明

### 命令行参数

| 参数             | 说明        | 默认值                     |
| -------------- | --------- | ----------------------- |
| `--platform`   | 目标平台      | android                 |
| `--device`     | 设备名称      | android\_emulator\_1    |
| `--app-path`   | 应用路径      | None                    |
| `--appium-url` | Appium 地址 | <http://127.0.0.1:4723> |

### Pytest 标记

| 标记                      | 说明    |
| ----------------------- | ----- |
| `@pytest.mark.smoke`    | 冒烟测试  |
| `@pytest.mark.login`    | 登录模块  |
| `@pytest.mark.shopping` | 购物车模块 |

## 测试报告

### 生成报告

```bash
# 生成 Allure 报告
pytest --alluredir=allure-results

# 查看报告
allure serve allure-results
```

### 报告内容

- 测试用例执行状态
- 失败截图自动附加
- 每步操作耗时统计
- 日志输出追溯

## 常见问题

### Q: 元素定位失败怎么办？

A: 检查以下几点：

1. 元素定位表达式是否正确
2. 元素是否在可见区域内（滚动）
3. 页面是否完全加载（增加等待时间）
4. 平台类型是否匹配（Android/iOS 定位方式不同）

### Q: 如何处理弹窗/广告？

A: 在 `conftest.py` 中配置弹窗处理：

```python
@pytest.fixture(scope="function")
def driver(driver_pool):
    # 忽略 SSL 证书弹窗
    driver_pool.switch_to.alert.accept()
    yield driver_pool
```

### Q: 如何实现失败重试？

A: 在 `pytest.ini` 中配置：

```ini
addopts = --tb=short --reruns=3 --reruns-delay=2
```

### Q: 多设备并发执行？

```bash
pytest -n 3  # 3个进程并行
```

## 开发规范

### 代码风格

- 遵循 PEP 8 规范
- 使用 Type Hints 类型注解
- 所有公开方法添加 Docstring

### Git 提交规范

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试相关
chore: 构建/工具
```

## 联系方式

- 项目地址：\[GitHub Repository]

## License

MIT License
