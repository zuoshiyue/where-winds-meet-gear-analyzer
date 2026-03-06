"""
数据库模型模块
定义装备、职业配置、评分记录等数据模型
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
import json

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.sql import func

# 创建基类
Base = declarative_base()


class Equipment(Base):
    """装备表"""

    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="装备名称")
    type = Column(String(50), default="", comment="装备类型 (武器/防具/饰品)")
    quality = Column(Integer, default=1, comment="品质 (1-5)")
    level = Column(Integer, default=0, comment="强化等级")
    set_name = Column(String(100), default="", comment="套装名称")
    stats = Column(JSON, default=list, comment="属性列表")
    screenshot_path = Column(String(500), default="", comment="截图路径")
    notes = Column(Text, default="", comment="备注")
    created_at = Column(
        DateTime, default=datetime.now, comment="创建时间"
    )
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )

    # 关联评分记录
    score_records = relationship(
        "ScoreRecord", back_populates="equipment", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Equipment(id={self.id}, name='{self.name}', quality={self.quality})>"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "quality": self.quality,
            "level": self.level,
            "set_name": self.set_name,
            "stats": self.stats if self.stats else [],
            "screenshot_path": self.screenshot_path,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Equipment":
        """从字典创建"""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            type=data.get("type", ""),
            quality=data.get("quality", 1),
            level=data.get("level", 0),
            set_name=data.get("set_name", ""),
            stats=data.get("stats", []),
            screenshot_path=data.get("screenshot_path", ""),
            notes=data.get("notes", ""),
        )


class ClassConfig(Base):
    """职业配置表"""

    __tablename__ = "class_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(50), unique=True, nullable=False, comment="职业名称")
    preferred_sets = Column(JSON, default=list, comment="推荐套装列表")
    stat_weights = Column(JSON, default=dict, comment="属性权重")
    notes = Column(Text, default="", comment="备注")
    created_at = Column(
        DateTime, default=datetime.now, comment="创建时间"
    )
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )

    def __repr__(self):
        return f"<ClassConfig(id={self.id}, class_name='{self.class_name}')>"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "class_name": self.class_name,
            "preferred_sets": self.preferred_sets if self.preferred_sets else [],
            "stat_weights": self.stat_weights if self.stat_weights else {},
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClassConfig":
        """从字典创建"""
        return cls(
            id=data.get("id"),
            class_name=data.get("class_name", ""),
            preferred_sets=data.get("preferred_sets", []),
            stat_weights=data.get("stat_weights", {}),
            notes=data.get("notes", ""),
        )

    @classmethod
    def default_configs(cls) -> List["ClassConfig"]:
        """返回默认职业配置"""
        return [
            cls(
                class_name="通用",
                preferred_sets=[],
                stat_weights={
                    "attack": 1.0,
                    "defense": 0.8,
                    "health": 0.7,
                    "crit": 1.5,
                    "crit_damage": 1.5,
                    "element_damage": 1.3,
                },
            ),
            cls(
                class_name="输出",
                preferred_sets=["输出套装", "暴击套装"],
                stat_weights={
                    "attack": 1.2,
                    "defense": 0.5,
                    "health": 0.5,
                    "crit": 1.8,
                    "crit_damage": 1.8,
                    "element_damage": 1.5,
                },
            ),
            cls(
                class_name="坦克",
                preferred_sets=["防御套装", "生命套装"],
                stat_weights={
                    "attack": 0.5,
                    "defense": 1.8,
                    "health": 1.8,
                    "crit": 1.0,
                    "crit_damage": 1.0,
                    "element_damage": 0.8,
                },
            ),
        ]


class ScoreRecord(Base):
    """评分记录表"""

    __tablename__ = "score_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(
        Integer, ForeignKey("equipment.id", ondelete="CASCADE"), nullable=False
    )
    class_name = Column(String(50), nullable=False, comment="职业名称")
    total_score = Column(Float, nullable=False, comment="总分")
    sub_scores = Column(JSON, default=dict, comment="分项评分")
    recommendation = Column(Text, default="", comment="培养建议")
    created_at = Column(
        DateTime, default=datetime.now, comment="创建时间"
    )

    # 关联装备
    equipment = relationship("Equipment", back_populates="score_records")

    def __repr__(self):
        return f"<ScoreRecord(id={self.id}, equipment_id={self.equipment_id}, score={self.total_score})>"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "equipment_id": self.equipment_id,
            "class_name": self.class_name,
            "total_score": self.total_score,
            "sub_scores": self.sub_scores if self.sub_scores else {},
            "recommendation": self.recommendation,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# 数据库辅助类
class DatabaseHelper:
    """数据库辅助类"""

    def __init__(self, db_url: str = "sqlite:///data/database/gear_analyzer.db"):
        """
        初始化数据库

        Args:
            db_url: 数据库连接 URL
        """
        self.engine = create_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False},  # SQLite 需要
        )

        # 创建所有表
        Base.metadata.create_all(self.engine)

        # 创建 Session
        SessionLocal = sessionmaker(bind=self.engine)
        self.SessionLocal = SessionLocal

    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()

    def init_default_data(self):
        """初始化默认数据"""
        session = self.get_session()
        try:
            # 检查是否已有职业配置
            count = session.query(ClassConfig).count()
            if count == 0:
                # 插入默认配置
                for config in ClassConfig.default_configs():
                    session.add(config)
                session.commit()
                print("已初始化默认职业配置")
        except Exception as e:
            session.rollback()
            print(f"初始化默认数据失败：{e}")
        finally:
            session.close()
