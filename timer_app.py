from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                           QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                           QSystemTrayIcon, QMenu)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QIcon, QAction
import sys
import time
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
        print(f"使用 MEIPASS 路径: {base_path}")
    else:
        base_path = os.path.abspath(".")
        print(f"使用当前路径: {base_path}")
    
    full_path = os.path.join(base_path, relative_path)
    print(f"完整路径: {full_path}")
    print(f"文件是否存在: {os.path.exists(full_path)}")
    return full_path

class TimerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计时器")
        self.showMaximized()
        
        # 设置应用图标
        self.setWindowIcon(QIcon(resource_path('icon.png')))
        
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path('icon.png')))
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = tray_menu.addAction("显示")
        quit_action = tray_menu.addAction("退出")
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(app.quit)
        
        # 设置托盘菜单
        self.tray_icon.setContextMenu(tray_menu)
        
        # 确保显示托盘图标
        self.tray_icon.show()
        
        # 可选：添加托盘图标的提示文字
        self.tray_icon.setToolTip("计时器")
        
        # 初始化计时器状态
        self.is_running = False
        self.elapsed_time = 0
        self.start_time = None
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建时间显示标签
        self.time_label = QLabel("00:00:00")
        self.time_label.setFont(QFont("Arial", 120, QFont.Weight.Bold))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                background-color: #2d2d2d;
                border-radius: 20px;
                padding: 40px;
                margin: 20px;
            }
        """)
        layout.addWidget(self.time_label)
        
        # 创建按钮容器
        button_layout = QHBoxLayout()
        
        # 创建按钮
        self.start_button = QPushButton("开始(&S)")
        self.pause_button = QPushButton("暂停(&P)")
        self.stop_button = QPushButton("停止(&T)")
        
        # 设置按钮样式
        button_style = """
            QPushButton {
                font-size: 24px;
                padding: 20px;
                min-width: 200px;
                min-height: 60px;
                border-radius: 10px;
                color: white;
                margin: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
            QPushButton:disabled {
                background-color: #666666;
                opacity: 0.7;
            }
            QPushButton:focus {
                border: 2px solid #ffffff;
            }
        """
        
        self.start_button.setStyleSheet(
            button_style + "background-color: #00b894;"
        )
        self.pause_button.setStyleSheet(
            button_style + "background-color: #fdcb6e;"
        )
        self.stop_button.setStyleSheet(
            button_style + "background-color: #d63031;"
        )
        
        # 初始状态下暂停按钮不可用
        self.pause_button.setEnabled(False)
        
        # 添加按钮到布局
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.stop_button)
        
        # 将按钮布局添加到主布局
        layout.addLayout(button_layout)
        
        # 设置布局的间距
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # 连接按钮信号
        self.start_button.clicked.connect(self.start_timer)
        self.pause_button.clicked.connect(self.pause_timer)
        self.stop_button.clicked.connect(self.stop_timer)
        
        # 创建定时器用于更新显示
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)
        
        # 修改主窗口背景色
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
        """)
        
        # 添加工具提示
        self.start_button.setToolTip("快捷键: Alt+S")
        self.pause_button.setToolTip("快捷键: Alt+P")
        self.stop_button.setToolTip("快捷键: Alt+T")
    
    def start_timer(self):
        self.is_running = True
        self.start_time = time.time()
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
    
    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            self.elapsed_time += time.time() - self.start_time
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
    
    def stop_timer(self):
        self.is_running = False
        self.elapsed_time = 0
        self.start_time = None
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.update_display()
    
    def update_time(self):
        if self.is_running:
            current_time = time.time()
            total_time = self.elapsed_time + (current_time - self.start_time)
        else:
            total_time = self.elapsed_time
        self.update_display(total_time)
    
    def update_display(self, total_time=0):
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_label.setText(time_str)

    # 添加键盘事件处理
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def closeEvent(self, event):
        # 重写关闭事件，点击关闭按钮时最小化到托盘
        event.ignore()  # 忽略关闭事件
        self.hide()     # 隐藏窗口
        self.tray_icon.showMessage(
            "计时器",
            "程序已最小化到系统托盘",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )

    def quit_app(self):
        # 完全退出应用程序
        self.tray_icon.hide()  # 隐藏托盘图标
        QApplication.quit()     # 退出应用

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()
            self.setWindowState(Qt.WindowState.WindowActive)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("系统不支持托盘图标")
        sys.exit(1)
        
    icon_path = resource_path('icon.png')
    app.setWindowIcon(QIcon(icon_path))
    
    window = TimerWindow()
    window.show()
    sys.exit(app.exec()) 