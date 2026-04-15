"""
utils/file_reader.py
文件读取工具模块
提供 YAML 和 JSON 格式配置文件的读取能力
"""

import json
import yaml
from pathlib import Path
from typing import Any, Dict, List, Union


class YamlReader:
    """
    YAML 文件读取工具类
    封装 PyYAML 库，提供安全的 YAML 文件读取方法
    """

    @staticmethod
    def read_yaml(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        读取 YAML 文件

        :param file_path: 文件路径
        :return: 解析后的字典数据
        :raises FileNotFoundError: 文件不存在时抛出
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    @staticmethod
    def read_yaml_list(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        读取 YAML 文件（列表格式）

        :param file_path: 文件路径
        :return: 解析后的列表数据
        """
        data = YamlReader.read_yaml(file_path)
        if isinstance(data, list):
            return data
        return []


class JsonReader:
    """
    JSON 文件读取工具类
    提供 JSON 文件的读取和写入方法
    """

    @staticmethod
    def read_json(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        读取 JSON 文件

        :param file_path: 文件路径
        :return: 解析后的字典数据
        :raises FileNotFoundError: 文件不存在时抛出
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def write_json(file_path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> None:
        """
        写入 JSON 文件

        :param file_path: 文件路径
        :param data: 要写入的数据
        :param indent: 缩进空格数
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)