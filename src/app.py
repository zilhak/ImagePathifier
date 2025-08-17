"""
메인 애플리케이션 클래스
"""

import customtkinter as ctk
from pathlib import Path
from typing import Optional

try:
    from .config import ConfigManager
    from .image_manager import ImageManager
    from .ui.main_window import MainWindow
    from .ui.settings_window import SettingsWindow
    from .utils.clipboard import ClipboardManager
except ImportError:
    # 직접 실행 시 절대 임포트 사용
    from config import ConfigManager
    from image_manager import ImageManager
    from ui.main_window import MainWindow
    from ui.settings_window import SettingsWindow
    from utils.clipboard import ClipboardManager


class ImagePathifierApp:
    """Image Pathifier 애플리케이션"""
    
    def __init__(self):
        # 설정 관리자 초기화
        self.config_manager = ConfigManager()
        
        # 이미지 관리자 초기화
        self.image_manager = ImageManager(
            save_directory=self.config_manager.get('save_directory'),
            max_images=self.config_manager.get('max_images')
        )
        
        # 클립보드 관리자 초기화
        self.clipboard_manager = ClipboardManager()
        
        # 윈도우 설정
        self.root = ctk.CTk()
        self.root.title("Image Pathifier")
        
        # 테마 설정
        ctk.set_appearance_mode(self.config_manager.get('theme'))
        ctk.set_default_color_theme("blue")
        
        # 윈도우 크기 설정
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 윈도우 중앙 배치
        self.center_window(800, 600)
        
        # 메인 윈도우 UI 초기화
        self.main_window = MainWindow(self.root)
        
        # 콜백 설정
        self.main_window.set_paste_callback(self.handle_paste)
        self.main_window.set_settings_callback(self.open_settings)
        self.main_window.set_copy_path_callback(self.copy_image_path)
        
        # 초기 UI 업데이트
        self.update_ui()
    
    def center_window(self, width: int, height: int):
        """윈도우를 화면 중앙에 배치"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def handle_paste(self):
        """붙여넣기 이벤트 처리"""
        try:
            # 클립보드에서 이미지 가져오기
            image = self.clipboard_manager.get_image_from_clipboard()
            
            if image:
                # 이미지 저장
                filepath = self.image_manager.save_image(image)
                
                if filepath:
                    # 경로를 클립보드에 복사
                    path_str = str(filepath.absolute())
                    if self.clipboard_manager.copy_text_to_clipboard(path_str):
                        self.main_window.update_status(
                            f"저장됨: {filepath.name} - 경로가 클립보드에 복사되었습니다!"
                        )
                        self.update_ui()
                    else:
                        self.main_window.show_error(
                            "클립보드 오류", 
                            "경로를 클립보드에 복사할 수 없습니다."
                        )
                else:
                    self.main_window.show_error(
                        "저장 오류", 
                        "이미지를 저장할 수 없습니다."
                    )
            else:
                self.main_window.update_status("클립보드에 이미지가 없습니다")
                self.main_window.show_warning(
                    "이미지 없음", 
                    "클립보드에서 이미지를 찾을 수 없습니다."
                )
                
        except Exception as e:
            self.main_window.update_status(f"오류: {e}")
            self.main_window.show_error("오류", f"이미지 처리 실패: {e}")
    
    def copy_image_path(self, img_path: Path):
        """이미지 경로를 클립보드에 복사"""
        path_str = str(img_path.absolute())
        if self.clipboard_manager.copy_text_to_clipboard(path_str):
            self.main_window.update_status(f"복사됨: {path_str}")
        else:
            self.main_window.show_error(
                "클립보드 오류", 
                "경로를 클립보드에 복사할 수 없습니다."
            )
    
    def open_settings(self):
        """설정 윈도우 열기"""
        SettingsWindow(
            self.root,
            self.config_manager.settings,
            self.apply_settings
        )
    
    def apply_settings(self, new_settings: dict):
        """새 설정 적용"""
        # 이전 설정과 비교
        theme_changed = self.config_manager.get('theme') != new_settings['theme']
        dir_changed = self.config_manager.get('save_directory') != new_settings['save_directory']
        max_changed = self.config_manager.get('max_images') != new_settings['max_images']
        
        # 설정 저장
        self.config_manager.update(new_settings)
        self.config_manager.save_settings()
        
        # 테마 변경 적용
        if theme_changed:
            ctk.set_appearance_mode(new_settings['theme'])
        
        # 이미지 관리자 설정 업데이트
        if dir_changed or max_changed:
            self.image_manager.update_settings(
                save_directory=new_settings['save_directory'] if dir_changed else None,
                max_images=new_settings['max_images'] if max_changed else None
            )
        
        # UI 업데이트
        self.update_ui()
    
    def update_ui(self):
        """UI 업데이트"""
        # 정렬된 이미지 목록 가져오기
        images = self.image_manager.get_sorted_images()
        
        # 썸네일 그리드 업데이트
        self.main_window.update_thumbnail_grid(
            images,
            self.config_manager.get('thumbnail_size', 100)
        )
        
        # 상태 업데이트
        save_dir = self.image_manager.save_dir
        max_images = self.image_manager.max_images
        current_count = len(images)
        
        self.main_window.update_status(
            f"이미지: {current_count}/{max_images} | 저장 위치: {save_dir}"
        )
    
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n프로그램이 종료되었습니다.")
        except Exception as e:
            print(f"예기치 않은 오류: {e}")
        finally:
            # 정리 작업 (필요한 경우)
            pass