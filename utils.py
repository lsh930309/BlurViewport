# utils.py
import sys
import ctypes

def apply_blur(hwnd):
    """ctypes를 사용해 주어진 창(hwnd)에 네이티브 블러 효과를 적용합니다."""
    if sys.platform != 'win32':
        return

    class ACCENT_POLICY(ctypes.Structure):
        _fields_ = [
            ("AccentState", ctypes.c_uint),
            ("AccentFlags", ctypes.c_uint),
            ("GradientColor", ctypes.c_uint),
            ("AnimationId", ctypes.c_uint)
        ]

    class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
        _fields_ = [
            ("Attribute", ctypes.c_int),
            ("Data", ctypes.POINTER(ACCENT_POLICY)),
            ("SizeOfData", ctypes.c_size_t)
        ]
    
    ACCENT_ENABLE_BLURBEHIND = 3
    
    accent = ACCENT_POLICY()
    accent.AccentState = ACCENT_ENABLE_BLURBEHIND
    
    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = 19
    data.SizeOfData = ctypes.sizeof(accent)
    data.Data = ctypes.cast(ctypes.pointer(accent), ctypes.POINTER(ACCENT_POLICY))
    
    user32 = ctypes.windll.user32
    user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))