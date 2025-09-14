# selection_overlay.py
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QPainter, QBrush, QColor, QPen

class SelectionOverlay(QWidget):
    # 선택이 완료되었을 때 QRect 객체를 전달하는 신호를 정의합니다.
    region_selected = Signal(QRect)

    def __init__(self):
        super().__init__()
        # 모든 화면을 포함하도록 데스크탑의 가상 크기를 가져옵니다.
        screen_geometry = QApplication.instance().primaryScreen().virtualGeometry()
        self.setGeometry(screen_geometry)
        
        # 창 속성 설정: 테두리 없음, 항상 위, 배경 투명
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 마우스 추적 및 커서 설정
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)
        
        self.start_point = None
        self.end_point = None

    def paintEvent(self, event):
        """위젯의 배경과 선택 영역을 그립니다."""
        painter = QPainter(self)
        
        # 1. 전체 화면을 반투명한 검은색으로 덮습니다.
        overlay_color = QColor(0, 0, 0, 120) # 검은색, 120/255 투명도
        painter.fillRect(self.rect(), QBrush(overlay_color))
        
        # 2. 사용자가 영역을 선택 중이라면 해당 영역을 그립니다.
        if self.start_point and self.end_point:
            selection_rect = QRect(self.start_point, self.end_point).normalized()
            
            # 선택된 영역은 투명하게 만듭니다 (배경을 지웁니다).
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(selection_rect, Qt.transparent)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            
            # 선택 영역의 테두리를 그립니다.
            pen = QPen(Qt.white, 1, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(selection_rect)

    def mousePressEvent(self, event):
        self.start_point = event.position().toPoint()
        self.end_point = self.start_point
        self.update()

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.position().toPoint()
            self.update() # repaint

    def mouseReleaseEvent(self, event):
        if self.start_point and self.end_point:
            selection_rect = QRect(self.start_point, self.end_point).normalized()
            # 0x0 크기의 영역이 선택되는 것을 방지
            if selection_rect.width() > 0 and selection_rect.height() > 0:
                self.region_selected.emit(selection_rect)
        self.close() # 선택이 끝나면 오버레이를 닫습니다.