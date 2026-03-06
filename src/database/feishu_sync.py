"""
飞书同步模块
将装备数据同步到飞书 Bitable
"""

import json
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import Equipment


class FeishuSync:
    """飞书数据同步器"""

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        bitable_app_token: str,
        table_id: str,
    ):
        """
        初始化飞书同步

        Args:
            app_id: 飞书应用 App ID
            app_secret: 飞书应用 App Secret
            bitable_app_token: 飞书云表格 App Token
            table_id: 数据表 ID
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.bitable_app_token = bitable_app_token
        self.table_id = table_id
        self._access_token: Optional[str] = None
        self._token_expire: Optional[datetime] = None

        # 飞书 API 端点
        self.base_url = "https://open.feishu.cn/open-apis"

    def _get_access_token(self) -> str:
        """获取访问令牌"""
        # 检查 token 是否有效
        if (
            self._access_token
            and self._token_expire
            and datetime.now() < self._token_expire
        ):
            return self._access_token

        # 请求新 token
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}

        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        if data.get("code") == 0:
            self._access_token = data["tenant_access_token"]
            # 提前 5 分钟过期
            self._token_expire = datetime.now().timestamp() + data.get(
                "expire", 7200
            ) - 300
            return self._access_token
        else:
            raise Exception(f"获取飞书 token 失败：{data}")

    def _request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Dict:
        """
        发送 HTTP 请求

        Args:
            method: HTTP 方法
            endpoint: API 端点
            data: 请求数据

        Returns:
            响应数据
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json",
        }

        response = requests.request(
            method, url, headers=headers, json=data, timeout=30
        )
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"飞书 API 请求失败：{result}")

        return result

    def sync_equipment(self, equipment: Equipment) -> Dict[str, Any]:
        """
        同步单个装备到飞书

        Args:
            equipment: 装备对象

        Returns:
            飞书记录 ID
        """
        # 构建飞书记录数据
        fields = {
            "装备名称": equipment.name,
            "装备类型": equipment.type,
            "品质": equipment.quality,
            "强化等级": equipment.level,
            "套装名称": equipment.set_name,
            "属性": json.dumps(equipment.stats, ensure_ascii=False),
            "截图路径": equipment.screenshot_path,
            "备注": equipment.notes,
            "创建时间": equipment.created_at.isoformat()
            if equipment.created_at
            else "",
        }

        # 创建记录
        endpoint = f"bitable/v1/apps/{self.bitable_app_token}/tables/{self.table_id}/records"
        result = self._request("POST", endpoint, {"fields": fields})

        return result.get("data", {})

    def batch_sync(
        self, equipment_list: List[Equipment]
    ) -> List[Dict[str, Any]]:
        """
        批量同步装备到飞书

        Args:
            equipment_list: 装备列表

        Returns:
            飞书记录 ID 列表
        """
        results = []
        for equipment in equipment_list:
            try:
                record = self.sync_equipment(equipment)
                results.append(record)
            except Exception as e:
                print(f"同步装备 {equipment.name} 失败：{e}")
                results.append({"error": str(e)})
        return results

    def get_records(
        self, page_size: int = 100, page_token: str = ""
    ) -> Dict[str, Any]:
        """
        获取飞书记录列表

        Args:
            page_size: 每页数量
            page_token: 分页 token

        Returns:
            记录列表和分页信息
        """
        endpoint = f"bitable/v1/apps/{self.bitable_app_token}/tables/{self.table_id}/records"
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token

        result = self._request("GET", endpoint)
        return result.get("data", {})

    def update_record(
        self, record_id: str, fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        更新飞书记录

        Args:
            record_id: 记录 ID
            fields: 字段数据

        Returns:
            更新结果
        """
        endpoint = f"bitable/v1/apps/{self.bitable_app_token}/tables/{self.table_id}/records/{record_id}"
        result = self._request("PUT", endpoint, {"fields": fields})
        return result.get("data", {})

    def delete_record(self, record_id: str) -> bool:
        """
        删除飞书记录

        Args:
            record_id: 记录 ID

        Returns:
            是否删除成功
        """
        endpoint = f"bitable/v1/apps/{self.bitable_app_token}/tables/{self.table_id}/records/{record_id}"
        result = self._request("DELETE", endpoint)
        return result.get("code") == 0

    def get_table_fields(self) -> List[Dict[str, Any]]:
        """
        获取数据表字段定义

        Returns:
            字段列表
        """
        endpoint = f"bitable/v1/apps/{self.bitable_app_token}/tables/{self.table_id}/fields"
        result = self._request("GET", endpoint)
        return result.get("data", {}).get("items", [])

    @classmethod
    def from_config(cls, config: Dict[str, str]) -> "FeishuSync":
        """
        从配置字典创建实例

        Args:
            config: 配置字典

        Returns:
            FeishuSync 实例
        """
        return cls(
            app_id=config.get("app_id", ""),
            app_secret=config.get("app_secret", ""),
            bitable_app_token=config.get("bitable_app_token", ""),
            table_id=config.get("table_id", ""),
        )
