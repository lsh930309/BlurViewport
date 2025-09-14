# viewport.py

import sys
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from utils import apply_blur

class Viewport(QWidget):
    """화면의 특정 영역을 흐리게 표시하는 순수 시각적 위젯"""
    def __init__(self):
        """생성자: 뷰포트 창의 시각적 속성만 설정합니다."""
        super().__init__()

        # --- 상태 변수 초기화 ---
        self.is_position_locked = False
        self.is_size_locked = False
        self.is_always_on_top = True
        
        # --- 창 기본 속성 설정 ---
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 이 창은 항상 마우스 이벤트를 통과시킴
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        self.setGeometry(200, 200, 500, 400)
        
        apply_blur(self.winId())

    # --- 외부에서 호출될 슬롯(Setter) 메서드들 ---
    def set_always_on_top(self, checked):
        """'항상 위에 표시' 상태를 설정합니다."""
        self.is_always_on_top = checked
        self.setWindowFlag(Qt.WindowStaysOnTopHint, checked)
        self.show()

    def set_position_lock(self, checked):
        """'위치 잠금' 상태를 설정합니다."""
        self.is_position_locked = checked

    def set_size_lock(self, checked):
        """'크기 잠금' 상태를 설정합니다. (현재는 기능 구현 안됨)"""
        self.is_size_locked = checked

    # 모든 마우스/네이티브 이벤트 핸들러는 제거됨
    # 이 위젯은 더 이상 직접적인 마우스 상호작용을 처리하지 않음
