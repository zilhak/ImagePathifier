"""
메인 윈도우 UI 모듈
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from pathlib import Path
from typing import Optional, Callable


class MainWindow:
    """메인 윈도우 UI"""
    
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.thumbnails = {}
        self.on_paste_callback: Optional[Callable] = None
        self.on_settings_callback: Optional[Callable] = None
        self.on_copy_path_callback: Optional[Callable] = None
        
        self.setup_ui()
        self.bind_shortcuts()
    
    def setup_ui(self):
        """UI 구성"""
        # 메뉴 바 프레임
        self._create_menu_bar()
        
        # 안내 프레임
        self._create_instructions()
        
        # 썸네일 그리드
        self._create_thumbnail_grid()
    
    def _create_menu_bar(self):
        """메뉴 바 생성"""
        menu_frame = ctk.CTkFrame(self.root, height=40)
        menu_frame.pack(fill="x", padx=5, pady=5)
        
        # 타이틀
        title_label = ctk.CTkLabel(
            menu_frame, 
            text="Image Pathifier", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # 설정 버튼
        settings_btn = ctk.CTkButton(
            menu_frame,
            text="⚙ 설정",
            width=100,
            command=self._on_settings_click
        )
        settings_btn.pack(side="right", padx=10)
    
    def _create_instructions(self):
        """안내 텍스트 생성"""
        # 메인 컨테이너 (배경 통일)
        instruction_container = ctk.CTkFrame(self.root, fg_color="transparent")
        instruction_container.pack(fill="x", padx=10, pady=(0, 10))
        
        # 버튼과 텍스트를 담을 프레임
        button_frame = ctk.CTkFrame(instruction_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(5, 10))
        
        # 붙여넣기 버튼 (중앙 정렬, 더 크고 눈에 띄게)
        paste_button = ctk.CTkButton(
            button_frame,
            text="📋 클립보드에서 붙여넣기",
            width=200,
            height=40,
            command=self._on_paste,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            hover_color=("#36719F", "#144870")
        )
        paste_button.pack()
        
        # 안내 텍스트 (버튼 아래)
        instruction_label = ctk.CTkLabel(
            instruction_container,
            text="단축키: Cmd+V 또는 Ctrl+V",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60")
        )
        instruction_label.pack(pady=(0, 5))
        
        # 상태 레이블
        self.status_label = ctk.CTkLabel(
            instruction_container,
            text="준비됨",
            font=ctk.CTkFont(size=10),
            text_color=("gray30", "gray70")
        )
        self.status_label.pack()
    
    def _create_thumbnail_grid(self):
        """썸네일 그리드 생성"""
        self.grid_frame = ctk.CTkScrollableFrame(self.root)
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 그리드 컬럼 설정
        for i in range(6):  # 6 컬럼
            self.grid_frame.grid_columnconfigure(i, weight=1)
    
    def bind_shortcuts(self):
        """키보드 단축키 바인딩"""
        import platform
        
        # 모든 플랫폼에서 Ctrl+V 지원
        self.root.bind('<Control-v>', lambda e: self._on_paste())
        self.root.bind('<Control-V>', lambda e: self._on_paste())
        
        # macOS에서만 Cmd+V 추가 지원
        if platform.system() == 'Darwin':
            try:
                self.root.bind('<Command-v>', lambda e: self._on_paste())
                self.root.bind('<Command-V>', lambda e: self._on_paste())
            except:
                # Command 키 바인딩 실패 시 무시
                pass
    
    def update_thumbnail_grid(self, image_files: list, thumbnail_size: int = 100):
        """썸네일 그리드 업데이트"""
        # 기존 썸네일 제거
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.thumbnails.clear()
        
        columns = 6
        
        for idx, img_path in enumerate(image_files):
            if not img_path.exists():
                continue
            
            row = idx // columns
            col = idx % columns
            
            # 썸네일 프레임 생성 (첫 번째 이미지는 강조)
            thumb_frame = ctk.CTkFrame(
                self.grid_frame,
                border_width=2 if idx == 0 else 0,
                border_color="green" if idx == 0 else None
            )
            thumb_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            try:
                # 이미지 로드 및 리사이즈
                img = Image.open(img_path)
                img.thumbnail((thumbnail_size, thumbnail_size), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # 이미지 레이블 생성
                img_label = tk.Label(
                    thumb_frame, 
                    image=photo, 
                    bg=thumb_frame.cget("fg_color")[0]
                )
                img_label.image = photo  # 참조 유지
                img_label.pack(padx=2, pady=2)
                
                # 클릭 이벤트 바인딩
                img_label.bind(
                    "<Button-1>", 
                    lambda e, path=img_path: self._on_thumbnail_click(path)
                )
                
                # 파일명 레이블 추가 (최신 이미지는 표시)
                label_text = f"[최신] {img_path.name}" if idx == 0 else img_path.name
                name_label = ctk.CTkLabel(
                    thumb_frame, 
                    text=label_text, 
                    font=ctk.CTkFont(size=10, weight="bold" if idx == 0 else "normal"),
                    text_color="green" if idx == 0 else None
                )
                name_label.pack()
                
                # 툴팁 (호버 이벤트)
                img_label.bind(
                    "<Enter>", 
                    lambda e, path=img_path: self.update_status(f"클릭하여 복사: {path}")
                )
                img_label.bind(
                    "<Leave>", 
                    lambda e: self.update_status("준비됨")
                )
                
            except Exception as e:
                print(f"썸네일 로드 오류 {img_path}: {e}")
    
    def update_status(self, message: str):
        """상태 메시지 업데이트"""
        self.status_label.configure(text=message, text_color=("gray10", "gray90"))
    
    def update_status_error(self, message: str, duration: int = 3000):
        """에러 상태 메시지 업데이트 (빨간색)
        
        Args:
            message: 표시할 메시지
            duration: 메시지 표시 시간 (밀리초, 기본 3초)
        """
        self.status_label.configure(text=message, text_color="red")
        
        # 일정 시간 후 원래 상태로 복구
        self.root.after(duration, lambda: self.update_status("준비됨"))
    
    def show_error(self, title: str, message: str):
        """에러 메시지 표시"""
        messagebox.showerror(title, message)
    
    def show_warning(self, title: str, message: str):
        """경고 메시지 표시"""
        messagebox.showwarning(title, message)
    
    def show_info(self, title: str, message: str):
        """정보 메시지 표시"""
        messagebox.showinfo(title, message)
    
    def set_paste_callback(self, callback: Callable):
        """붙여넣기 콜백 설정"""
        self.on_paste_callback = callback
    
    def set_settings_callback(self, callback: Callable):
        """설정 콜백 설정"""
        self.on_settings_callback = callback
    
    def set_copy_path_callback(self, callback: Callable):
        """경로 복사 콜백 설정"""
        self.on_copy_path_callback = callback
    
    def _on_paste(self):
        """붙여넣기 이벤트 처리"""
        if self.on_paste_callback:
            self.on_paste_callback()
    
    def _on_settings_click(self):
        """설정 버튼 클릭 처리"""
        if self.on_settings_callback:
            self.on_settings_callback()
    
    def _on_thumbnail_click(self, img_path: Path):
        """썸네일 클릭 처리"""
        if self.on_copy_path_callback:
            self.on_copy_path_callback(img_path)