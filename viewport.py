# viewport.py (수정)
import sys
import ctypes.wintypes
from PySide6.QtWidgets import QWidget, QMenu, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from utils import apply_blur

class Viewport(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.setGeometry(200, 200, 500, 400)
        
        # --- 수정: 기본 블러 효과를 바로 적용 ---
        apply_blur(self.winId())
        
        # --- 상태 변수 (단순화) ---
        self.is_position_locked = False
        self.is_size_locked = False
        self.is_always_on_top = True

    # --- MainWindow에서 호출할 슬롯(Setter 메서드)들 (단순화) ---
    def set_always_on_top(self, checked):
        self.is_always_on_top = checked
        self.setWindowFlag(Qt.WindowStaysOnTopHint, checked)
        self.show()

    def set_position_lock(self, checked):
        self.is_position_locked = checked

    def set_size_lock(self, checked):
        self.is_size_locked = checked

    # --- (이하 contextMenuEvent 및 마우스 이벤트 처리는 이전과 동일) ---
    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        
        always_on_top_action = QAction("Always on Top", self, checkable=True)
        always_on_top_action.setChecked(self.is_always_on_top)
        always_on_top_action.triggered.connect(self.set_always_on_top)
        
        lock_position_action = QAction("Lock Position", self, checkable=True)
        lock_position_action.setChecked(self.is_position_locked)
        lock_position_action.triggered.connect(self.set_position_lock)
        
        close_action = QAction("Close Viewport", self)
        close_action.triggered.connect(self.close)
        
        context_menu.addAction(always_on_top_action)
        context_menu.addAction(lock_position_action)
        context_menu.addSeparator()
        context_menu.addAction(close_action)
        
        context_menu.exec(event.globalPos())
        
    def mousePressEvent(self, event):
        if not self.is_position_locked and event.button() == Qt.LeftButton:
            self._drag_start_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.is_position_locked and hasattr(self, '_drag_start_position'):
            delta = event.globalPosition().toPoint() - self._drag_start_position
            self.move(self.pos() + delta)
            self._drag_start_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if hasattr(self, '_drag_start_position'):
            del self._drag_start_position
            
    def nativeEvent(self, eventType, message):
        if eventType == b"windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message == 0x0084:
                if QApplication.mouseButtons() != Qt.RightButton:
                    return True, -1 
        return super().nativeEvent(eventType, message)