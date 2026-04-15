"""
utils/adb_helper.py
Android Debug Bridge 辅助工具模块
封装常用的 ADB 命令，提供设备管理、应用安装卸载、文件传输、截图等功能
"""

import subprocess
import re
import time
from pathlib import Path
from typing import List, Optional, Dict, Any, Union


class AdbHelper:
    """
    Android Debug Bridge 辅助工具类
    提供与 Android 设备交互的常用方法
    支持指定设备 UDID 操作，多设备环境可复用
    """

    def __init__(self, device_udid: Optional[str] = None):
        """
        初始化 ADB 辅助工具

        :param device_udid: 设备 UDID（可选，不指定时操作默认设备）
        """
        self.device_udid = device_udid

    def _run_command(self, command: List[str]) -> str:
        """
        执行 ADB 命令的内部方法

        :param command: 命令列表
        :return: 命令输出结果
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error executing command: {e}"

    def devices(self) -> List[Dict[str, str]]:
        """
        获取已连接的设备列表

        :return: 设备列表，每个设备包含 udid 和 status
        """
        output = self._run_command(["adb", "devices"])
        devices = []
        lines = output.split("\n")[1:]
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    devices.append({
                        "udid": parts[0],
                        "status": parts[1]
                    })
        return devices

    def get_device_info(self) -> Dict[str, str]:
        """
        获取设备详细信息

        :return: 设备信息字典（序列号、型号、品牌、Android版本、SDK版本）
        """
        info = {}
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        info["serial"] = self._run_command(cmd_prefix + ["get-serialno"])
        info["model"] = self._run_command(cmd_prefix + ["shell", "getprop", "ro.product.model"])
        info["brand"] = self._run_command(cmd_prefix + ["shell", "getprop", "ro.product.brand"])
        info["android_version"] = self._run_command(cmd_prefix + ["shell", "getprop", "ro.build.version.release"])
        info["sdk_version"] = self._run_command(cmd_prefix + ["shell", "getprop", "ro.build.version.sdk"])
        return info

    def install_app(self, apk_path: Union[str, Path], reinstall: bool = False) -> bool:
        """
        安装应用

        :param apk_path: APK 文件路径
        :param reinstall: 是否覆盖安装（-r 参数）
        :return: 安装是否成功
        """
        apk_path = Path(apk_path)
        if not apk_path.exists():
            return False
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        command = cmd_prefix + ["install"]
        if reinstall:
            command.append("-r")
        command.append(str(apk_path))
        result = self._run_command(command)
        return "Success" in result

    def uninstall_app(self, package_name: str) -> bool:
        """
        卸载应用

        :param package_name: 应用包名
        :return: 卸载是否成功
        """
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["uninstall", package_name])
        return "Success" in result

    def clear_app_data(self, package_name: str) -> bool:
        """
        清除应用数据（相当于重置应用）

        :param package_name: 应用包名
        :return: 清除是否成功
        """
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["shell", "pm", "clear", package_name])
        return result == "Success"

    def start_app(self, package_name: str, activity_name: str) -> bool:
        """
        启动应用

        :param package_name: 应用包名
        :param activity_name: Activity 名称
        :return: 启动是否成功
        """
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["shell", "am", "start", "-n", f"{package_name}/{activity_name}"])
        return "Starting" in result or "started" in result.lower()

    def stop_app(self, package_name: str) -> bool:
        """
        停止应用（强制关闭）

        :param package_name: 应用包名
        :return: 停止是否成功
        """
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["shell", "am", "force-stop", package_name])
        return result == ""

    def get_current_activity(self) -> str:
        """
        获取当前正在显示的 Activity

        :return: Activity 名称
        """
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["shell", "dumpsys", "activity", "activities"])
        match = re.search(r"mResumedActivity.*?([\w.]+)$", result, re.MULTILINE)
        return match.group(1) if match else ""

    def pull_file(self, remote_path: str, local_path: Union[str, Path]) -> bool:
        """
        从设备拉取文件到本地

        :param remote_path: 设备上的远程路径
        :param local_path: 本地保存路径
        :return: 拉取是否成功
        """
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["pull", remote_path, str(local_path)])
        return local_path.exists()

    def push_file(self, local_path: Union[str, Path], remote_path: str) -> bool:
        """
        从本地上传文件到设备

        :param local_path: 本地文件路径
        :param remote_path: 设备上的远程路径
        :return: 上传是否成功
        """
        local_path = Path(local_path)
        if not local_path.exists():
            return False
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["push", str(local_path), remote_path])
        return "pushed" in result.lower()

    def get_screen_resolution(self) -> tuple:
        """
        获取设备屏幕分辨率

        :return: (宽度, 高度) 元组
        """
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["shell", "wm", "size"])
        match = re.search(r"(\d+)x(\d+)", result)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return (0, 0)

    def is_device_online(self) -> bool:
        """
        检查设备是否在线

        :return: 设备是否在线
        """
        if not self.device_udid:
            return False
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["get-state"])
        return "device" in result.lower()

    def reboot_device(self) -> bool:
        """
        重启设备

        :return: 重启命令是否成功执行
        """
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["reboot"])
        return result == ""

    def take_screenshot(self, remote_path: str = "/sdcard/screenshot.png") -> Optional[str]:
        """
        设备截图

        :param remote_path: 设备上的临时存储路径
        :return: 本地截图文件路径，失败返回 None
        """
        from config.settings import Settings
        local_path = Settings.SCREENSHOTS_DIR / f"adb_screenshot_{int(time.time())}.png"
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        self._run_command(cmd_prefix + ["shell", "screencap", "-p", remote_path])
        if self.pull_file(remote_path, local_path):
            return str(local_path)
        return None

    def clear_logcat(self) -> bool:
        """
        清除日志缓冲区

        :return: 清除是否成功
        """
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        result = self._run_command(cmd_prefix + ["logcat", "-c"])
        return result == ""

    def get_logcat(self, log_level: str = "V", count: int = 100) -> str:
        """
        获取日志cat日志

        :param log_level: 日志级别（V/D/I/W/E）
        :param count: 获取日志条数
        :return: 日志内容
        """
        cmd_prefix = ["adb", "-s", self.device_udid] if self.device_udid else ["adb"]
        return self._run_command(cmd_prefix + ["logcat", "-d", "-v", "threadtime", "-g", "-n", str(count), "-s", f"*:{log_level}"])