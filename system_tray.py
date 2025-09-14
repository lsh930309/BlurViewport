# system_tray.py
import sys
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication # QApplication 임포트
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Signal

class SystemTrayIcon(QSystemTrayIcon):
    show_window_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- 수정: self.style() -> QApplication.style() ---
        # 애플리케이션의 스타일에서 표준 아이콘을 가져옵니다.
        style = QApplication.style()
        icon = QIcon(style.standardIcon(style.StandardPixmap.SP_ComputerIcon))
        
        self.setIcon(icon)
        self.setToolTip("Blur Viewport Controller")
        
        menu = QMenu()
        show_action = QAction("Show Controller", self)
        show_action.triggered.connect(self.show_window_requested.emit)
        
        # --- 수정: self.parent().quit -> QApplication.instance().quit ---
        # 더 명확하고 안정적인 종료 방법입니다.
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        
        menu.addAction(show_action)
        menu.addAction(quit_action)
        
        self.setContextMenu(menu)
        
        self.activated.connect(self.on_activated)

    def on_activated(self, reason):
        if reason == self.ActivationReason.Trigger:
            self.show_window_requested.emit()