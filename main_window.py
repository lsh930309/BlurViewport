# main_window.py (수정)
from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QGroupBox, 
                               QCheckBox, QFormLayout)
from PySide6.QtCore import QRect
from PySide6.QtGui import QCloseEvent

from viewport import Viewport
from selection_overlay import SelectionOverlay
# --- 추가: 시스템 트레이 모듈 임포트 ---
from system_tray import SystemTrayIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blur Viewport Controller")
        self.setGeometry(100, 100, 350, 250)
        
        self.selection_overlay = None
        self.viewport = None

        # --- 추가: 시스템 트레이 아이콘 생성 ---
        self.tray_icon = SystemTrayIcon(self)
        self.tray_icon.show_window_requested.connect(self.show_from_tray)
        self.tray_icon.show()
        
        # (이하 UI 생성 코드는 이전과 동일)
        main_layout = QVBoxLayout(self)
        self.create_viewport_button = QPushButton("Create New Viewport")
        properties_group = QGroupBox("Viewport Properties")
        properties_layout = QFormLayout()
        self.check_always_on_top = QCheckBox("Always on Top")
        self.check_always_on_top.setChecked(True)
        self.check_lock_position = QCheckBox("Lock Position")
        self.check_lock_size = QCheckBox("Lock Size (Not Implemented)")
        properties_layout.addRow(self.check_always_on_top)
        properties_layout.addRow(self.check_lock_position)
        properties_layout.addRow(self.check_lock_size)
        properties_group.setLayout(properties_layout)
        main_layout.addWidget(self.create_viewport_button)
        main_layout.addWidget(properties_group)
        self.create_viewport_button.clicked.connect(self.start_viewport_selection)

    def start_viewport_selection(self):
        self.selection_overlay = SelectionOverlay()
        self.selection_overlay.region_selected.connect(self.create_viewport)
        self.selection_overlay.show()
        # --- 추가: 뷰포트 생성 시작 시 메인 창 숨김 ---
        # self.hide()
        
    def create_viewport(self, rect: QRect):
        if self.viewport:
            self.viewport.close()
            
        self.viewport = Viewport()
        self.viewport.setGeometry(rect)
        
        # --- 추가: 뷰포트가 닫힐 때의 신호를 메인 창 복귀 함수와 연결 ---
        self.viewport.destroyed.connect(self.show_from_tray)
        
        self.connect_controls_to_viewport()
        self.update_viewport_from_ui()
        
        self.viewport.show()

    def show_from_tray(self):
        """트레이에서 창을 다시 보여줍니다."""
        self.showNormal()
        self.activateWindow()

    def closeEvent(self, event: QCloseEvent):
        """창 닫기 버튼 클릭 시 트레이로 최소화합니다."""
        event.ignore() # 기본 닫기 이벤트를 무시
        self.hide()     # 창을 숨김
        self.tray_icon.showMessage(
            "Running in background",
            "Blur Viewport Controller is still running in the system tray.",
            self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon),
            2000
        )
        
    # (이하 connect 및 update 함수는 이전과 동일)
    def connect_controls_to_viewport(self):
        if not self.viewport: return
        self.check_always_on_top.toggled.connect(self.viewport.set_always_on_top)
        self.check_lock_position.toggled.connect(self.viewport.set_position_lock)
        self.check_lock_size.toggled.connect(self.viewport.set_size_lock)

    def update_viewport_from_ui(self):
        if not self.viewport: return
        self.viewport.set_always_on_top(self.check_always_on_top.isChecked())
        self.viewport.set_position_lock(self.check_lock_position.isChecked())
        self.viewport.set_size_lock(self.check_lock_size.isChecked())