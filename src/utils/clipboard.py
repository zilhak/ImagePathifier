"""
클립보드 관련 유틸리티
"""

from typing import Optional
from PIL import Image, ImageGrab
import pyperclip


class ClipboardManager:
    """클립보드 작업 관리자"""
    
    @staticmethod
    def get_image_from_clipboard() -> Optional[Image.Image]:
        """클립보드에서 이미지 가져오기"""
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                return img
            return None
        except Exception as e:
            print(f"클립보드에서 이미지 가져오기 오류: {e}")
            return None
    
    @staticmethod
    def copy_text_to_clipboard(text: str) -> bool:
        """텍스트를 클립보드에 복사"""
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"클립보드에 텍스트 복사 오류: {e}")
            return False
    
    @staticmethod
    def has_image() -> bool:
        """클립보드에 이미지가 있는지 확인"""
        try:
            img = ImageGrab.grabclipboard()
            return isinstance(img, Image.Image)
        except:
            return False