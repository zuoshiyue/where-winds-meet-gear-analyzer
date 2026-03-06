"""配置文件管理模块"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ConfigManager:
    """配置管理器"""

    DEFAULT_CONFIG_PATH = "config.yaml"

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}
        return self._config

    def save(self):
        """保存配置文件"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                self._config,
                f,
                allow_unicode=True,
                default_flow_style=False,
            )

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键 (支持点号分隔，如 screenshot.format)
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值
        """
        keys = key.split(".")
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_section(self, section: str) -> Dict[str, Any]:
        """获取配置节"""
        return self._config.get(section, {})

    def set_section(self, section: str, data: Dict[str, Any]):
        """设置配置节"""
        self._config[section] = data

    @property
    def config(self) -> Dict[str, Any]:
        """获取完整配置"""
        return self._config

    @config.setter
    def config(self, value: Dict[str, Any]):
        """设置完整配置"""
        self._config = value
