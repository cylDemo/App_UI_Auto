"""
data/test_data_builder.py
测试数据构造器模块
提供随机测试数据的生成能力，支持：
- 基础类型：字符串、邮箱、手机号、整数、浮点数、布尔值等
- 复合类型：用户信息、商品信息、订单信息等
- 账号数据：从 YAML 文件读取，支持多平台（Android/iOS）
"""

import random
import string
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path


class TestDataBuilder:
    """
    测试数据构造器类
    提供静态方法生成各类随机测试数据
    """

    @staticmethod
    def random_string(length: int = 10, chars: Optional[str] = None) -> str:
        """
        生成随机字符串

        :param length: 字符串长度
        :param chars: 字符集，默认为字母和数字
        :return: 随机字符串
        """
        chars = chars or string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    @staticmethod
    def random_email(domain: str = "example.com") -> str:
        """
        生成随机邮箱地址

        :param domain: 邮箱域名
        :return: 随机邮箱
        """
        username = TestDataBuilder.random_string(8).lower()
        return f"{username}@{domain}"

    @staticmethod
    def random_phone(prefix: str = "+86") -> str:
        """
        生成随机手机号码

        :param prefix: 国际区号前缀
        :return: 随机手机号
        """
        number = "".join(random.choice(string.digits) for _ in range(10))
        return f"{prefix}{number}"

    @staticmethod
    def random_int(min_value: int = 0, max_value: int = 100) -> int:
        """
        生成随机整数

        :param min_value: 最小值
        :param max_value: 最大值
        :return: 随机整数
        """
        return random.randint(min_value, max_value)

    @staticmethod
    def random_float(min_value: float = 0.0, max_value: float = 100.0, decimals: int = 2) -> float:
        """
        生成随机浮点数

        :param min_value: 最小值
        :param max_value: 最大值
        :param decimals: 小数位数
        :return: 随机浮点数
        """
        value = random.uniform(min_value, max_value)
        return round(value, decimals)

    @staticmethod
    def random_date(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> str:
        """
        生成随机日期

        :param start_date: 开始日期，默认为一年前
        :param end_date: 结束日期，默认为一年后
        :return: 随机日期字符串（YYYY-MM-DD）
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now() + timedelta(days=365)
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

    @staticmethod
    def random_datetime(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        fmt: str = "%Y-%m-%d %H:%M:%S"
    ) -> str:
        """
        生成随机日期时间

        :param start_date: 开始日期时间，默认为一年前
        :param end_date: 结束日期时间，默认为一年后
        :param fmt: 日期时间格式
        :return: 随机日期时间字符串
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now() + timedelta(days=365)
        delta = end_date - start_date
        random_seconds = random.randint(0, int(delta.total_seconds()))
        return (start_date + timedelta(seconds=random_seconds)).strftime(fmt)

    @staticmethod
    def random_boolean() -> bool:
        """生成随机布尔值"""
        return random.choice([True, False])

    @staticmethod
    def random_choice(options: list) -> Any:
        """
        从列表中随机选择一个元素

        :param options: 选项列表
        :return: 随机选中的元素
        """
        return random.choice(options)

    @staticmethod
    def random_ip() -> str:
        """生成随机 IP 地址"""
        return ".".join(str(random.randint(1, 254)) for _ in range(4))

    @staticmethod
    def random_url() -> str:
        """生成随机 URL"""
        protocols = ["http", "https"]
        domains = ["example.com", "test.com", "demo.com"]
        paths = ["", "/home", "/api", "/user"]
        return f"{random.choice(protocols)}://{random.choice(domains)}{random.choice(paths)}"

    @classmethod
    def build_user_profile(
        cls,
        username: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        构建随机用户资料

        :param username: 指定用户名（可选）
        :param email: 指定邮箱（可选）
        :param phone: 指定手机号（可选）
        :return: 用户资料字典
        """
        return {
            "user_id": cls.random_string(8),
            "username": username or cls.random_string(10),
            "email": email or cls.random_email(),
            "phone": phone or cls.random_phone(),
            "password": cls.random_string(12, string.ascii_letters + string.digits + "!@#$%"),
            "age": cls.random_int(18, 60),
            "gender": random.choice(["male", "female", "other"]),
            "address": {
                "city": random.choice(["Beijing", "Shanghai", "Guangzhou", "Shenzhen"]),
                "district": f"District {cls.random_int(1, 10)}",
                "street": f"Street {cls.random_string(6)}",
                "zip_code": str(cls.random_int(100000, 999999))
            },
            "registered_at": cls.random_datetime(),
            "is_active": cls.random_boolean()
        }

    @classmethod
    def build_product(
        cls,
        name: Optional[str] = None,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        构建随机商品信息

        :param name: 商品名称（可选）
        :param price: 商品价格（可选）
        :return: 商品信息字典
        """
        categories = ["Electronics", "Clothing", "Food", "Books", "Sports"]
        return {
            "product_id": cls.random_string(10),
            "name": name or f"Product_{cls.random_string(6)}",
            "category": random.choice(categories),
            "price": price or cls.random_float(1.0, 1000.0),
            "stock": cls.random_int(0, 100),
            "description": f"Description for {cls.random_string(20)}",
            "rating": round(cls.random_float(1.0, 5.0, 1), 1),
            "created_at": cls.random_datetime()
        }

    @classmethod
    def build_order(cls) -> Dict[str, Any]:
        """
        构建随机订单信息

        :return: 订单信息字典
        """
        statuses = ["pending", "paid", "shipped", "delivered", "cancelled"]
        return {
            "order_id": cls.random_string(12),
            "user_id": cls.random_string(8),
            "total_amount": cls.random_float(10.0, 5000.0),
            "status": random.choice(statuses),
            "items_count": cls.random_int(1, 10),
            "payment_method": random.choice(["alipay", "wechat", "card"]),
            "created_at": cls.random_datetime(),
            "updated_at": cls.random_datetime()
        }


class AccountData:
    """
    账号数据管理类
    从 YAML 文件读取预置的测试账号数据，支持多平台
    """

    def __init__(self, platform: str = "android"):
        """
        初始化账号数据

        :param platform: 平台类型（android/ios）
        """
        from utils.file_reader import YamlReader
        from pathlib import Path
        self.platform = platform
        self.data = YamlReader.read_yaml(Path(__file__).parent / "account.yaml")

    def get_valid_account(self) -> Dict[str, str]:
        """
        获取有效账号

        :return: 有效账号字典 {username, password}
        """
        return self.data.get("accounts", {}).get(self.platform, {}).get("valid", {})

    def get_invalid_account(self, case_type: str = "wrong_password") -> Dict[str, str]:
        """
        获取无效账号

        :param case_type: 无效类型（wrong_password/wrong_username/empty）
        :return: 无效账号字典
        """
        return (
            self.data.get("accounts", {})
            .get(self.platform, {})
            .get("invalid", {})
            .get(case_type, {})
        )