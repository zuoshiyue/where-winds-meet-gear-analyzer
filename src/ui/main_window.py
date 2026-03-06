"""
主窗口模块
提供装备分析工具的用户界面
"""

import sys
from pathlib import Path
from typing import Optional, List

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QComboBox,
    QSpinBox,
    QStatusBar,
    QToolBar,
    QMenuBar,
    QMenu,
    QMessageBox,
    QFileDialog,
    QTabWidget,
    QGroupBox,
    QFormLayout,
    QTextEdit,
    QSplitter,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QPixmap

from ..database.models import Equipment, DatabaseHelper
from ..database.repository import EquipmentRepository, ClassConfigRepository
from ..screenshot.capture import ScreenshotCapture
from ..ocr.recognizer import OCRRecognizer
from ..ocr.parser import EquipmentParser
from ..ocr.preprocessor import ImagePreprocessor
from ..analyzer.scorer import EquipmentScorer
from ..analyzer.classifier import ClassClassifier
from ..analyzer.recommender import EquipmentRecommender


class MainWindow(QMainWindow):
    """主窗口"""

    # 信号
    screenshot_taken = pyqtSignal(str)  # 截图完成信号
    ocr_completed = pyqtSignal(object)  # OCR 完成信号

    def __init__(
        self,
        db_helper: Optional[DatabaseHelper] = None,
        config: Optional[dict] = None,
    ):
        """
        初始化主窗口

        Args:
            db_helper: 数据库辅助实例
            config: 配置字典
        """
        super().__init__()

        self.db = db_helper or DatabaseHelper()
        self.config = config or {}

        # 初始化组件
        self.repo = EquipmentRepository(self.db)
        self.class_repo = ClassConfigRepository(self.db)
        self.capture = ScreenshotCapture()
        self.ocr = OCRRecognizer()
        self.parser = EquipmentParser()
        self.preprocessor = ImagePreprocessor()
        self.scorer = EquipmentScorer()

        # 初始化 UI
        self._init_ui()

        # 加载数据
        self._load_equipment_list()
        self._load_class_config()

    def _init_ui(self):
        """初始化 UI"""
        self.setWindowTitle("燕云十六声装备分析工具")
        self.setMinimumSize(1280, 800)

        # 创建菜单栏
        self._create_menu_bar()

        # 创建工具栏
        self._create_tool_bar()

        # 创建中央部件
        self._create_central_widget()

        # 创建状态栏
        self._create_status_bar()

    def _create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件 (&F)")
        export_action = QAction("导出 CSV", self)
        export_action.triggered.connect(self._export_csv)
        file_menu.addAction(export_action)
        file_menu.addSeparator()
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 工具菜单
        tools_menu = menubar.addMenu("工具 (&T)")
        screenshot_action = QAction("截图 (&S)", self)
        screenshot_action.triggered.connect(self._take_screenshot)
        screenshot_action.setShortcut("F12")
        tools_menu.addAction(screenshot_action)

        # 设置菜单
        settings_menu = menubar.addMenu("设置 (&S)")
        class_action = QAction("职业配置", self)
        class_action.triggered.connect(self._show_class_settings)
        settings_menu.addAction(class_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助 (&H)")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar("主工具栏")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # 截图按钮
        screenshot_btn = QPushButton("截图 (F12)")
        screenshot_btn.clicked.connect(self._take_screenshot)
        toolbar.addWidget(screenshot_btn)

        toolbar.addSeparator()

        # 分析按钮
        analyze_btn = QPushButton("分析")
        analyze_btn.clicked.connect(self._analyze_equipment)
        toolbar.addWidget(analyze_btn)

        toolbar.addSeparator()

        # 刷新按钮
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(self._load_equipment_list)
        toolbar.addWidget(refresh_btn)

    def _create_central_widget(self):
        """创建中央部件"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 创建选项卡
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # 装备列表页
        list_tab = self._create_equipment_tab()
        tabs.addTab(list_tab, "装备列表")

        # 分析页
        analysis_tab = self._create_analysis_tab()
        tabs.addTab(analysis_tab, "装备分析")

        # 统计页
        stats_tab = self._create_stats_tab()
        tabs.addTab(stats_tab, "数据统计")

    def _create_equipment_tab(self) -> QWidget:
        """创建装备列表页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 筛选面板
        filter_group = QGroupBox("筛选")
        filter_layout = QHBoxLayout(filter_group)

        # 职业筛选
        filter_layout.addWidget(QLabel("职业:"))
        self.class_filter = QComboBox()
        self.class_filter.addItem("全部", "")
        filter_layout.addWidget(self.class_filter)

        # 品质筛选
        filter_layout.addWidget(QLabel("品质:"))
        self.quality_filter = QComboBox()
        self.quality_filter.addItem("全部", -1)
        self.quality_filter.addItem("白色", 1)
        self.quality_filter.addItem("绿色", 2)
        self.quality_filter.addItem("蓝色", 3)
        self.quality_filter.addItem("紫色", 4)
        self.quality_filter.addItem("金色", 5)
        filter_layout.addWidget(self.quality_filter)

        # 类型筛选
        filter_layout.addWidget(QLabel("类型:"))
        self.type_filter = QComboBox()
        self.type_filter.addItem("全部", "")
        self.type_filter.addItem("武器", "武器")
        self.type_filter.addItem("防具", "防具")
        self.type_filter.addItem("饰品", "饰品")
        filter_layout.addWidget(self.type_filter)

        filter_layout.addStretch()

        # 名称搜索
        filter_layout.addWidget(QLabel("名称:"))
        self.name_filter = QTextEdit()
        self.name_filter.setMaximumHeight(30)
        self.name_filter.setPlaceholderText("输入装备名称...")
        filter_layout.addWidget(self.name_filter, 1)

        # 搜索按钮
        search_btn = QPushButton("搜索")
        search_btn.clicked.connect(self._filter_equipment)
        filter_layout.addWidget(search_btn)

        layout.addWidget(filter_group)

        # 装备表格
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(7)
        self.equipment_table.setHorizontalHeaderLabels([
            "ID", "名称", "类型", "品质", "等级", "套装", "评分"
        ])
        self.equipment_table.horizontalHeader().setStretchLastSection(True)
        self.equipment_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.equipment_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.equipment_table.itemDoubleClicked.connect(
            self._show_equipment_detail
        )
        layout.addWidget(self.equipment_table)

        return widget

    def _create_analysis_tab(self) -> QWidget:
        """创建分析页"""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # 左侧：装备选择
        left_panel = QGroupBox("装备选择")
        left_layout = QVBoxLayout(left_panel)

        self.analysis_equipment_list = QTableWidget()
        self.analysis_equipment_list.setColumnCount(5)
        self.analysis_equipment_list.setHorizontalHeaderLabels([
            "ID", "名称", "品质", "等级", "评分"
        ])
        self.analysis_equipment_list.horizontalHeader().setStretchLastSection(True)
        self.analysis_equipment_list.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        left_layout.addWidget(self.analysis_equipment_list)

        # 右侧：分析结果
        right_panel = QGroupBox("分析结果")
        right_layout = QVBoxLayout(right_panel)

        # 装备详情
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        right_layout.addWidget(self.detail_text)

        # 评分结果
        self.score_text = QTextEdit()
        self.score_text.setReadOnly(True)
        self.score_text.setMaximumHeight(150)
        right_layout.addWidget(self.score_text)

        # 培养建议
        self.recommend_text = QTextEdit()
        self.recommend_text.setReadOnly(True)
        self.recommend_text.setMaximumHeight(150)
        right_layout.addWidget(self.recommend_text)

        # 操作按钮
        btn_layout = QHBoxLayout()
        analyze_btn = QPushButton("分析")
        analyze_btn.clicked.connect(self._analyze_selected)
        btn_layout.addWidget(analyze_btn)

        compare_btn = QPushButton("对比")
        compare_btn.clicked.connect(self._compare_equipment)
        btn_layout.addWidget(compare_btn)

        btn_layout.addStretch()
        right_layout.addLayout(btn_layout)

        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 1)

        return widget

    def _create_stats_tab(self) -> QWidget:
        """创建统计页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 统计信息
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(300)
        layout.addWidget(self.stats_text)

        # 刷新按钮
        refresh_btn = QPushButton("刷新统计")
        refresh_btn.clicked.connect(self._update_stats)
        layout.addWidget(refresh_btn)

        layout.addStretch()

        return widget

    def _create_status_bar(self):
        """创建状态栏"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # 装备数量标签
        self.count_label = QLabel("装备数：0")
        self.statusbar.addPermanentWidget(self.count_label)

        # 状态标签
        self.status_label = QLabel("就绪")
        self.statusbar.addWidget(self.status_label)

    def _load_equipment_list(self):
        """加载装备列表"""
        equipment_list = self.repo.get_all()

        self.equipment_table.setRowCount(len(equipment_list))
        for row, eq in enumerate(equipment_list):
            self.equipment_table.setItem(row, 0, QTableWidgetItem(str(eq.id)))
            self.equipment_table.setItem(row, 1, QTableWidgetItem(eq.name))
            self.equipment_table.setItem(row, 2, QTableWidgetItem(eq.type))
            self.equipment_table.setItem(
                row, 3, QTableWidgetItem(f"{'⭐' * eq.quality}")
            )
            self.equipment_table.setItem(
                row, 4, QTableWidgetItem(f"+{eq.level}")
            )
            self.equipment_table.setItem(row, 5, QTableWidgetItem(eq.set_name))

            # 计算评分
            score = self.scorer.score(eq)
            self.equipment_table.setItem(
                row, 6, QTableWidgetItem(f"{score.total_score:.1f}")
            )

        # 更新计数
        total = self.repo.get_count()
        self.count_label.setText(f"装备数：{total}")

        # 同时更新分析页的列表
        self._load_analysis_equipment_list()

    def _load_analysis_equipment_list(self):
        """加载分析页装备列表"""
        equipment_list = self.repo.get_all()

        self.analysis_equipment_list.setRowCount(len(equipment_list))
        for row, eq in enumerate(equipment_list):
            self.analysis_equipment_list.setItem(row, 0, QTableWidgetItem(str(eq.id)))
            self.analysis_equipment_list.setItem(row, 1, QTableWidgetItem(eq.name))
            self.analysis_equipment_list.setItem(
                row, 2, QTableWidgetItem(f"{'⭐' * eq.quality}")
            )
            self.analysis_equipment_list.setItem(
                row, 3, QTableWidgetItem(f"+{eq.level}")
            )
            score = self.scorer.score(eq)
            self.analysis_equipment_list.setItem(
                row, 4, QTableWidgetItem(f"{score.total_score:.1f}")
            )

    def _load_class_config(self):
        """加载职业配置"""
        configs = self.class_repo.get_all()
        self.class_filter.clear()
        self.class_filter.addItem("全部", "")
        for config in configs:
            self.class_filter.addItem(config.class_name, config.class_name)

    def _take_screenshot(self):
        """执行截图"""
        self.status_label.setText("正在截图...")
        try:
            # 延迟截图，让用户有时间切换到游戏窗口
            QTimer.singleShot(1000, self._do_screenshot)
        except Exception as e:
            self.status_label.setText(f"截图失败：{e}")

    def _do_screenshot(self):
        """实际执行截图"""
        try:
            image = self.capture.capture_full_screen(save=True)
            if image is not None:
                self.status_label.setText("截图完成")
                # TODO: 执行 OCR 识别
            else:
                self.status_label.setText("截图失败")
        except Exception as e:
            self.status_label.setText(f"截图错误：{e}")

    def _analyze_equipment(self):
        """分析装备"""
        self._load_equipment_list()
        self.status_label.setText("分析完成")

    def _filter_equipment(self):
        """筛选装备"""
        # TODO: 实现筛选逻辑
        self.status_label.setText("筛选功能开发中")

    def _show_equipment_detail(self, item):
        """显示装备详情"""
        row = item.row()
        eq_id = int(self.equipment_table.item(row, 0).text())
        equipment = self.repo.get_by_id(eq_id)

        if equipment:
            QMessageBox.information(
                self,
                "装备详情",
                f"名称：{equipment.name}\n"
                f"类型：{equipment.type}\n"
                f"品质：{'⭐' * equipment.quality}\n"
                f"等级：+{equipment.level}\n"
                f"套装：{equipment.set_name}\n"
                f"属性：{equipment.stats}",
            )

    def _analyze_selected(self):
        """分析选中的装备"""
        rows = self.analysis_equipment_list.selectedItems()
        if not rows:
            QMessageBox.warning(self, "提示", "请先选择装备")
            return

        row = rows[0].row()
        eq_id = int(self.analysis_equipment_list.item(row, 0).text())
        equipment = self.repo.get_by_id(eq_id)

        if equipment:
            # 评分
            score_result = self.scorer.score(equipment)

            # 显示详情
            self.detail_text.setText(
                f"装备名称：{equipment.name}\n"
                f"类型：{equipment.type}\n"
                f"品质：{'⭐' * equipment.quality}\n"
                f"强化等级：+{equipment.level}\n"
                f"套装：{equipment.set_name or '无'}\n"
                f"属性：{equipment.stats}"
            )

            # 显示评分
            self.score_text.setText(
                f"总评分：{score_result.total_score:.1f}\n"
                f"  - 品质分：{score_result.quality_score:.1f}\n"
                f"  - 属性分：{score_result.stats_score:.1f}\n"
                f"  - 强化分：{score_result.level_score:.1f}\n"
                f"  - 套装加成：{score_result.set_bonus:.1f}"
            )

            # 显示建议
            self.recommend_text.setText(score_result.recommendation)

    def _compare_equipment(self):
        """对比装备"""
        rows = self.analysis_equipment_list.selectedItems()
        if len(rows) < 2:
            QMessageBox.warning(self, "提示", "请选择两件装备进行对比")
            return

        # TODO: 实现对比功能
        self.status_label.setText("对比功能开发中")

    def _update_stats(self):
        """更新统计"""
        stats = self.repo.get_statistics()

        text = (
            f"装备总数：{stats['total']}\n\n"
            f"按品质统计:\n"
        )
        for quality, count in sorted(stats["by_quality"].items()):
            text += f"  {'⭐' * quality}: {count}\n"

        text += f"\n按类型统计:\n"
        for eq_type, count in sorted(stats["by_type"].items()):
            text += f"  {eq_type}: {count}\n"

        text += f"\n平均强化等级：+{stats['avg_level']}"

        self.stats_text.setText(text)

    def _export_csv(self):
        """导出 CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出 CSV", "", "CSV 文件 (*.csv)"
        )
        if file_path:
            # TODO: 实现导出功能
            self.status_label.setText(f"导出到：{file_path}")

    def _show_class_settings(self):
        """显示职业配置"""
        QMessageBox.information(self, "职业配置", "职业配置功能开发中")

    def _show_about(self):
        """显示关于"""
        QMessageBox.about(
            self,
            "关于",
            "燕云十六声装备分析工具\n\n"
            "版本：v0.1.0\n"
            "开发中...",
        )

    def closeEvent(self, event):
        """关闭事件"""
        reply = QMessageBox.question(
            self,
            "确认退出",
            "确定要退出吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
