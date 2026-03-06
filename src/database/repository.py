"""
装备数据仓库模块
提供装备数据的 CRUD 操作
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import and_, or_, desc, func
from sqlalchemy.orm import Session, joinedload

from .models import Equipment, ClassConfig, ScoreRecord, DatabaseHelper


class EquipmentRepository:
    """装备数据仓库"""

    def __init__(self, db_helper: DatabaseHelper):
        """
        初始化仓库

        Args:
            db_helper: 数据库辅助实例
        """
        self.db = db_helper

    def add(self, equipment: Equipment) -> Equipment:
        """
        添加装备

        Args:
            equipment: 装备对象

        Returns:
            添加后的装备对象 (含 ID)
        """
        session = self.db.get_session()
        try:
            session.add(equipment)
            session.commit()
            session.refresh(equipment)
            return equipment
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_id(self, equipment_id: int) -> Optional[Equipment]:
        """
        根据 ID 获取装备

        Args:
            equipment_id: 装备 ID

        Returns:
            装备对象，不存在返回 None
        """
        session = self.db.get_session()
        try:
            return (
                session.query(Equipment)
                .options(joinedload(Equipment.score_records))
                .filter(Equipment.id == equipment_id)
                .first()
            )
        finally:
            session.close()

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        desc_order: bool = True,
    ) -> List[Equipment]:
        """
        获取所有装备 (分页)

        Args:
            page: 页码
            page_size: 每页数量
            sort_by: 排序字段
            desc_order: 是否降序

        Returns:
            装备列表
        """
        session = self.db.get_session()
        try:
            query = session.query(Equipment)
            sort_column = getattr(Equipment, sort_by, Equipment.created_at)
            if desc_order:
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(sort_column)

            offset = (page - 1) * page_size
            return query.offset(offset).limit(page_size).all()
        finally:
            session.close()

    def get_count(self) -> int:
        """获取装备总数"""
        session = self.db.get_session()
        try:
            return session.query(Equipment).count()
        finally:
            session.close()

    def filter(
        self,
        name: Optional[str] = None,
        quality: Optional[int] = None,
        eq_type: Optional[str] = None,
        set_name: Optional[str] = None,
        min_level: Optional[int] = None,
        max_level: Optional[int] = None,
    ) -> List[Equipment]:
        """
        筛选装备

        Args:
            name: 装备名称 (模糊匹配)
            quality: 品质
            eq_type: 类型
            set_name: 套装名称
            min_level: 最低等级
            max_level: 最高等级

        Returns:
            装备列表
        """
        session = self.db.get_session()
        try:
            query = session.query(Equipment)
            conditions = []

            if name:
                conditions.append(Equipment.name.like(f"%{name}%"))
            if quality:
                conditions.append(Equipment.quality == quality)
            if eq_type:
                conditions.append(Equipment.type == eq_type)
            if set_name:
                conditions.append(Equipment.set_name.like(f"%{set_name}%"))
            if min_level is not None:
                conditions.append(Equipment.level >= min_level)
            if max_level is not None:
                conditions.append(Equipment.level <= max_level)

            if conditions:
                query = query.filter(and_(*conditions))

            return query.all()
        finally:
            session.close()

    def update(self, equipment_id: int, data: Dict[str, Any]) -> Optional[Equipment]:
        """
        更新装备

        Args:
            equipment_id: 装备 ID
            data: 更新数据

        Returns:
            更新后的装备对象
        """
        session = self.db.get_session()
        try:
            equipment = session.query(Equipment).filter(Equipment.id == equipment_id).first()
            if equipment:
                for key, value in data.items():
                    if hasattr(equipment, key):
                        setattr(equipment, key, value)
                equipment.updated_at = datetime.now()
                session.commit()
                session.refresh(equipment)
            return equipment
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, equipment_id: int) -> bool:
        """
        删除装备

        Args:
            equipment_id: 装备 ID

        Returns:
            是否删除成功
        """
        session = self.db.get_session()
        try:
            equipment = session.query(Equipment).filter(Equipment.id == equipment_id).first()
            if equipment:
                session.delete(equipment)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def batch_delete(self, equipment_ids: List[int]) -> int:
        """
        批量删除装备

        Args:
            equipment_ids: 装备 ID 列表

        Returns:
            删除的数量
        """
        session = self.db.get_session()
        try:
            count = (
                session.query(Equipment)
                .filter(Equipment.id.in_(equipment_ids))
                .delete(synchronize_session=False)
            )
            session.commit()
            return count
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计数据

        Returns:
            统计信息字典
        """
        session = self.db.get_session()
        try:
            total = session.query(func.count(Equipment.id)).scalar()

            # 按品质统计
            quality_stats = (
                session.query(Equipment.quality, func.count(Equipment.id))
                .group_by(Equipment.quality)
                .all()
            )

            # 按类型统计
            type_stats = (
                session.query(Equipment.type, func.count(Equipment.id))
                .group_by(Equipment.type)
                .all()
            )

            # 平均强化等级
            avg_level = session.query(func.avg(Equipment.level)).scalar() or 0

            return {
                "total": total,
                "by_quality": {q: c for q, c in quality_stats},
                "by_type": {t: c for t, c in type_stats},
                "avg_level": round(avg_level, 2),
            }
        finally:
            session.close()


class ClassConfigRepository:
    """职业配置仓库"""

    def __init__(self, db_helper: DatabaseHelper):
        self.db = db_helper

    def get_all(self) -> List[ClassConfig]:
        """获取所有职业配置"""
        session = self.db.get_session()
        try:
            return session.query(ClassConfig).all()
        finally:
            session.close()

    def get_by_name(self, class_name: str) -> Optional[ClassConfig]:
        """根据名称获取职业配置"""
        session = self.db.get_session()
        try:
            return session.query(ClassConfig).filter(ClassConfig.class_name == class_name).first()
        finally:
            session.close()

    def save(self, config: ClassConfig) -> ClassConfig:
        """保存职业配置"""
        session = self.db.get_session()
        try:
            session.merge(config)
            session.commit()
            return config
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, class_name: str) -> bool:
        """删除职业配置"""
        session = self.db.get_session()
        try:
            config = session.query(ClassConfig).filter(ClassConfig.class_name == class_name).first()
            if config:
                session.delete(config)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class ScoreRecordRepository:
    """评分记录仓库"""

    def __init__(self, db_helper: DatabaseHelper):
        self.db = db_helper

    def add(self, record: ScoreRecord) -> ScoreRecord:
        """添加评分记录"""
        session = self.db.get_session()
        try:
            session.add(record)
            session.commit()
            session.refresh(record)
            return record
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_equipment(
        self, equipment_id: int, class_name: Optional[str] = None
    ) -> List[ScoreRecord]:
        """根据装备 ID 获取评分记录"""
        session = self.db.get_session()
        try:
            query = session.query(ScoreRecord).filter(ScoreRecord.equipment_id == equipment_id)
            if class_name:
                query = query.filter(ScoreRecord.class_name == class_name)
            return query.all()
        finally:
            session.close()

    def get_latest(self, equipment_id: int) -> Optional[ScoreRecord]:
        """获取最新评分记录"""
        session = self.db.get_session()
        try:
            return (
                session.query(ScoreRecord)
                .filter(ScoreRecord.equipment_id == equipment_id)
                .order_by(desc(ScoreRecord.created_at))
                .first()
            )
        finally:
            session.close()
