# main_window.py (수정)
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import QRect

from viewport import Viewport
from selection_overlay import SelectionOverlay

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blur Viewport Controller")
        self.setGeometry(100, 100, 300, 400)
        
        # 나중에 참조할 수 있도록 멤버 변수로 저장
        self.selection_overlay = None
        self.viewport = None # 현재는 뷰포트를 하나만 관리한다고 가정
        
        self.create_viewport_button = QPushButton("Create New Viewport")
        self.create_viewport_button.clicked.connect(self.start_viewport_selection)
        
        layout = QVBoxLayout()
        layout.addWidget(self.create_viewport_button)
        
        self.setLayout(layout)
        
    def start_viewport_selection(self):
        """'Create' 버튼 클릭 시 영역 선택 오버레이를 표시합니다."""
        self.selection_overlay = SelectionOverlay()
        # 오버레이에서 region_selected 신호가 오면 create_viewport 슬롯을 실행
        self.selection_overlay.region_selected.connect(self.create_viewport)
        self.selection_overlay.show()
        
    def create_viewport(self, rect: QRect):
        """선택된 영역(rect)에 뷰포트를 생성합니다."""
        # 기존 뷰포트가 있다면 닫습니다.
        if self.viewport:
            self.viewport.close()
            
        self.viewport = Viewport()
        self.viewport.setGeometry(rect) # 선택된 영역의 geometry를 설정
        self.viewport.show()