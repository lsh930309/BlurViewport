# main_window.py (수정)
from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QGroupBox, 
                               QCheckBox, QFormLayout)
from PySide6.QtCore import QRect

from viewport import Viewport
from selection_overlay import SelectionOverlay

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blur Viewport Controller")
        self.setGeometry(100, 100, 350, 250) # 창 크기 조절
        
        self.selection_overlay = None
        self.viewport = None
        
        main_layout = QVBoxLayout(self)
        
        self.create_viewport_button = QPushButton("Create New Viewport")
        
        properties_group = QGroupBox("Viewport Properties")
        properties_layout = QFormLayout()
        
        self.check_always_on_top = QCheckBox("Always on Top")
        self.check_always_on_top.setChecked(True)
        self.check_lock_position = QCheckBox("Lock Position")
        self.check_lock_size = QCheckBox("Lock Size (Not Implemented)") # 기능 미구현 명시
        
        properties_layout.addRow(self.check_always_on_top)
        properties_layout.addRow(self.check_lock_position)
        properties_layout.addRow(self.check_lock_size)
        
        # --- 제거: 블러타입 라디오 버튼 ---
        # --- 제거: 투명도 슬라이더 ---
        # --- 제거: 블러강도 슬라이더 ---
        
        properties_group.setLayout(properties_layout)
        
        main_layout.addWidget(self.create_viewport_button)
        main_layout.addWidget(properties_group)
        
        self.create_viewport_button.clicked.connect(self.start_viewport_selection)
        
    def start_viewport_selection(self):
        self.selection_overlay = SelectionOverlay()
        self.selection_overlay.region_selected.connect(self.create_viewport)
        self.selection_overlay.show()
        
    def create_viewport(self, rect: QRect):
        if self.viewport:
            self.viewport.close()
            
        self.viewport = Viewport()
        self.viewport.setGeometry(rect)
        
        self.connect_controls_to_viewport()
        self.update_viewport_from_ui()
        
        self.viewport.show()

    def connect_controls_to_viewport(self):
        if not self.viewport:
            return
            
        self.check_always_on_top.toggled.connect(self.viewport.set_always_on_top)
        self.check_lock_position.toggled.connect(self.viewport.set_position_lock)
        self.check_lock_size.toggled.connect(self.viewport.set_size_lock)
        
        # --- 제거: 라디오/슬라이더 연결부 ---

    def update_viewport_from_ui(self):
        if not self.viewport:
            return
            
        self.viewport.set_always_on_top(self.check_always_on_top.isChecked())
        self.viewport.set_position_lock(self.check_lock_position.isChecked())
        self.viewport.set_size_lock(self.check_lock_size.isChecked())