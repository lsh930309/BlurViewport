# viewport.py (수정)
import sys
import ctypes.wintypes
from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from utils import apply_blur

class Viewport(QWidget):
    def __init__(self):
        super().__init__()
        
        # --- 기본 속성 설정 ---
        self.setWindowFlags(
            Qt.FramelessWindowHint |       # 테두리 없음
            Qt.WindowStaysOnTopHint |     # 항상 위
            Qt.Tool                       # 작업 표시줄에 아이콘 표시 안 함
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # --- '클릭 통과' 활성화를 위한 핵심 속성 ---
        # 이 속성은 마우스 이벤트를 창이 아닌, 창 뒤의 요소로 전달합니다.
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.setGeometry(200, 200, 500, 400)
        
        # --- 블러 효과 적용 ---
        hwnd = self.winId()
        apply_blur(hwnd)
        
        # --- 상태 변수 ---
        self.is_position_locked = False
        self.is_always_on_top = True

    def contextMenuEvent(self, event):
        """우클릭 시 실행될 컨텍스트 메뉴를 정의합니다."""
        context_menu = QMenu(self)
        
        # --- 메뉴 액션 생성 ---
        # 1. 항상 위 (Always on Top)
        always_on_top_action = QAction("Always on Top", self, checkable=True)
        always_on_top_action.setChecked(self.is_always_on_top)
        always_on_top_action.triggered.connect(self.toggle_always_on_top)
        
        # 2. 위치 잠금 (Lock Position)
        lock_position_action = QAction("Lock Position", self, checkable=True)
        lock_position_action.setChecked(self.is_position_locked)
        lock_position_action.triggered.connect(self.toggle_position_lock)
        
        # 3. 뷰포트 닫기 (Close)
        close_action = QAction("Close Viewport", self)
        close_action.triggered.connect(self.close)
        
        # --- 메뉴에 액션 추가 ---
        context_menu.addAction(always_on_top_action)
        context_menu.addAction(lock_position_action)
        context_menu.addSeparator() # 구분선
        context_menu.addAction(close_action)
        
        # 현재 마우스 위치에 메뉴를 표시합니다.
        context_menu.exec(event.globalPos())

    def toggle_always_on_top(self, checked):
        """'항상 위' 상태를 토글합니다."""
        self.is_always_on_top = checked
        if checked:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
        self.show() # 플래그 변경 후 show()를 다시 호출해야 적용됩니다.

    def toggle_position_lock(self, checked):
        """'위치 잠금' 상태를 토글합니다."""
        self.is_position_locked = checked

    def mousePressEvent(self, event):
        # 위치가 잠겨있지 않을 때만 드래그 시작점을 저장합니다.
        if not self.is_position_locked and event.button() == Qt.LeftButton:
            self._drag_start_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        # 드래그 중일 때 창을 이동시킵니다.
        if not self.is_position_locked and hasattr(self, '_drag_start_position'):
            delta = event.globalPosition().toPoint() - self._drag_start_position
            self.move(self.pos() + delta)
            self._drag_start_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if hasattr(self, '_drag_start_position'):
            del self._drag_start_position
            
    # '클릭 통과'를 위해 재정의가 필요한 부분
    # 윈도우 운영체제에 직접 메시지를 보내 처리하는 방식입니다.
    def nativeEvent(self, eventType, message):
        # 윈도우 메시지(WM_NCHITTEST)를 확인하여 마우스 위치를 판단합니다.
        # 이 메시지에 'HTTRANSPARENT'를 반환하면 마우스 이벤트를 무시하고 통과시킵니다.
        if eventType == b"windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message == 0x0084: # WM_NCHITTEST
                # 우클릭이 아닌 경우에만 이벤트를 통과시킵니다.
                # QApplication.mouseButtons()는 현재 눌린 마우스 버튼을 알려줍니다.
                if QApplication.mouseButtons() != Qt.RightButton:
                    # True와 함께 -1 (HTTRANSPARENT)을 반환하여 이벤트를 통과시킵니다.
                    return True, -1 
        return super().nativeEvent(eventType, message)