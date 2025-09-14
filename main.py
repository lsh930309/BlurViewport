# main.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory, QSystemSemaphore

from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 중복 실행 방지를 위한 고유 키 설정
    unique_key = "my_awesome_blur_viewport_app"
    
    # 공유 메모리를 확인하여 이미 인스턴스가 실행 중인지 체크
    shared_memory = QSharedMemory(unique_key)
    if shared_memory.attach():
        # 이미 실행 중인 경우, 새로운 인스턴스를 종료
        print("Application is already running.")
        sys.exit(0)
    
    # 실행 중이 아니라면, 공유 메모리를 생성
    if not shared_memory.create(1):
        print("Unable to create shared memory segment.")
        sys.exit(-1)

    # 기본 창 생성 및 표시
    main_win = MainWindow()
    main_win.show()
    
    sys.exit(app.exec())