"""
flows/__init__.py
业务流模块初始化
提供业务场景的流程编排，将多个页面操作组合成完整的业务流程
用于复用复杂的业务操作序列
"""

from .login_flow import LoginFlow

__all__ = ["LoginFlow"]