"""
설정 윈도우 UI 모듈
"""

import customtkinter as ctk
from tkinter import filedialog
from typing import Dict, Any, Callable


class SettingsWindow:
    """설정 윈도우"""
    
    def __init__(self, parent_window, current_settings: Dict[str, Any], on_save: Callable):
        self.parent_window = parent_window
        self.settings = current_settings.copy()
        self.on_save_callback = on_save
        
        # 윈도우 생성
        self.window = ctk.CTkToplevel(parent_window)
        self.window.title("설정")
        self.window.geometry("500x350")
        self.window.transient(parent_window)
        self.window.grab_set()
        
        # 윈도우 중앙 배치
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (350 // 2)
        self.window.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        self.window.focus()
    
    def setup_ui(self):
        """설정 UI 구성"""
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 저장 디렉토리 설정
        self._create_directory_setting(main_frame, 0)
        
        # 최대 이미지 수 설정
        self._create_max_images_setting(main_frame, 1)
        
        # 테마 설정
        self._create_theme_setting(main_frame, 2)
        
        # 썸네일 크기 설정
        self._create_thumbnail_setting(main_frame, 3)
        
        # 그리드 가중치 설정
        main_frame.grid_columnconfigure(1, weight=1)
        
        # 버튼 프레임
        self._create_buttons()
    
    def _create_directory_setting(self, parent, row):
        """디렉토리 설정 UI 생성"""
        dir_label = ctk.CTkLabel(parent, text="저장 디렉토리:", font=ctk.CTkFont(size=14))
        dir_label.grid(row=row, column=0, sticky="w", pady=(0, 10))
        
        dir_frame = ctk.CTkFrame(parent)
        dir_frame.grid(row=row, column=1, sticky="ew", pady=(0, 10), padx=(10, 0))
        
        self.dir_entry = ctk.CTkEntry(dir_frame, width=250)
        self.dir_entry.pack(side="left", padx=(0, 10))
        self.dir_entry.insert(0, self.settings['save_directory'])
        
        browse_btn = ctk.CTkButton(
            dir_frame, 
            text="찾아보기", 
            width=70, 
            command=self.browse_directory
        )
        browse_btn.pack(side="right")
    
    def _create_max_images_setting(self, parent, row):
        """최대 이미지 수 설정 UI 생성"""
        max_label = ctk.CTkLabel(parent, text="최대 이미지 수:", font=ctk.CTkFont(size=14))
        max_label.grid(row=row, column=0, sticky="w", pady=(10, 10))
        
        max_frame = ctk.CTkFrame(parent)
        max_frame.grid(row=row, column=1, sticky="w", pady=(10, 10), padx=(10, 0))
        
        self.max_slider = ctk.CTkSlider(
            max_frame, 
            from_=5, 
            to=50, 
            number_of_steps=45, 
            width=200
        )
        self.max_slider.pack(side="left", padx=(0, 10))
        self.max_slider.set(self.settings['max_images'])
        self.max_slider.configure(command=self.update_max_label)
        
        self.max_value_label = ctk.CTkLabel(max_frame, text=str(int(self.settings['max_images'])))
        self.max_value_label.pack(side="left")
    
    def _create_theme_setting(self, parent, row):
        """테마 설정 UI 생성"""
        theme_label = ctk.CTkLabel(parent, text="테마:", font=ctk.CTkFont(size=14))
        theme_label.grid(row=row, column=0, sticky="w", pady=(10, 10))
        
        self.theme_var = ctk.StringVar(value=self.settings['theme'])
        theme_menu = ctk.CTkOptionMenu(
            parent, 
            values=["dark", "light"], 
            variable=self.theme_var, 
            width=150
        )
        theme_menu.grid(row=row, column=1, sticky="w", pady=(10, 10), padx=(10, 0))
    
    def _create_thumbnail_setting(self, parent, row):
        """썸네일 크기 설정 UI 생성"""
        thumb_label = ctk.CTkLabel(parent, text="썸네일 크기:", font=ctk.CTkFont(size=14))
        thumb_label.grid(row=row, column=0, sticky="w", pady=(10, 10))
        
        thumb_frame = ctk.CTkFrame(parent)
        thumb_frame.grid(row=row, column=1, sticky="w", pady=(10, 10), padx=(10, 0))
        
        self.thumb_slider = ctk.CTkSlider(
            thumb_frame, 
            from_=50, 
            to=200, 
            number_of_steps=15, 
            width=200
        )
        self.thumb_slider.pack(side="left", padx=(0, 10))
        self.thumb_slider.set(self.settings.get('thumbnail_size', 100))
        self.thumb_slider.configure(command=self.update_thumb_label)
        
        self.thumb_value_label = ctk.CTkLabel(
            thumb_frame, 
            text=f"{int(self.settings.get('thumbnail_size', 100))}px"
        )
        self.thumb_value_label.pack(side="left")
    
    def _create_buttons(self):
        """버튼 생성"""
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        save_btn = ctk.CTkButton(button_frame, text="저장", command=self.save_settings)
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ctk.CTkButton(button_frame, text="취소", command=self.window.destroy)
        cancel_btn.pack(side="right")
    
    def browse_directory(self):
        """디렉토리 찾아보기"""
        directory = filedialog.askdirectory(initialdir=self.dir_entry.get())
        if directory:
            self.dir_entry.delete(0, 'end')
            self.dir_entry.insert(0, directory)
    
    def update_max_label(self, value):
        """최대 이미지 수 레이블 업데이트"""
        self.max_value_label.configure(text=str(int(value)))
    
    def update_thumb_label(self, value):
        """썸네일 크기 레이블 업데이트"""
        self.thumb_value_label.configure(text=f"{int(value)}px")
    
    def save_settings(self):
        """설정 저장 및 닫기"""
        self.settings['save_directory'] = self.dir_entry.get()
        self.settings['max_images'] = int(self.max_slider.get())
        self.settings['theme'] = self.theme_var.get()
        self.settings['thumbnail_size'] = int(self.thumb_slider.get())
        
        # 콜백 호출
        if self.on_save_callback:
            self.on_save_callback(self.settings)
        
        self.window.destroy()