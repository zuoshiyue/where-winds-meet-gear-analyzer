"""
燕云十六声装备分析工具 - 主入口
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database.models import DatabaseHelper
from src.ui.main_window import MainWindow
from src.config_manager import ConfigManager


def main():
    """主函数"""
    # 加载配置
    config_manager = ConfigManager("config.yaml")
    config = config_manager.config

    # 初始化数据库
    db_path = config.get("database", {}).get(
        "path", "data/database/gear_analyzer.db"
    )
    db_helper = DatabaseHelper(f"sqlite:///{db_path}")

    # 初始化默认数据
    db_helper.init_default_data()

    # 创建应用
    app = MainWindow.create QApplication(sys.argv)

    # 设置应用属性
    app.setApplicationName("燕云十六声装备分析工具")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("GearAnalyzer")

    # 创建主窗口
    window = MainWindow(db_helper=db_helper, config=config)
    window.show()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
