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
        self.current_images = []  # 현재 이미지 목록 저장
        self.current_thumbnail_size = 100  # 현재 썸네일 크기 저장
        self.current_columns = 0  # 현재 컬럼 수 저장
        self.last_width = 0  # 마지막 창 너비 저장
        
        self.setup_ui()
        self.bind_shortcuts()
        self.bind_resize_event()
    
    def setup_ui(self):
        """UI 구성"""
        # 상단 컨트롤 패널
        self._create_control_panel()
        
        # 썸네일 그리드
        self._create_thumbnail_grid()
    
    def _create_control_panel(self):
        """상단 컨트롤 패널 생성"""
        # 메인 컨테이너 (배경색 통일)
        control_frame = ctk.CTkFrame(self.root, fg_color="transparent", height=60)
        control_frame.pack(fill="x", padx=10, pady=(5, 10))
        control_frame.pack_propagate(False)
        
        # 왼쪽 영역 (붙여넣기 버튼과 단축키)
        left_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=(10, 0))
        
        # 붙여넣기 버튼 (작게)
        paste_button = ctk.CTkButton(
            left_frame,
            text="📋 붙여넣기",
            width=100,
            height=28,
            command=self._on_paste,
            font=ctk.CTkFont(size=12)
        )
        paste_button.pack(pady=(0, 2))
        
        # 단축키 안내 (버튼 아래)
        import platform
        shortcut_text = "Cmd+V" if platform.system() == 'Darwin' else "Ctrl+V"
        shortcut_label = ctk.CTkLabel(
            left_frame,
            text=shortcut_text,
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60")
        )
        shortcut_label.pack()
        
        # 오른쪽 영역 (설정 버튼과 카운터)
        right_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=(0, 10))
        
        # 설정 버튼 (작게)
        settings_btn = ctk.CTkButton(
            right_frame,
            text="⚙ 설정",
            width=80,
            height=28,
            command=self._on_settings_click,
            font=ctk.CTkFont(size=12)
        )
        settings_btn.pack(pady=(0, 2))
        
        # 이미지 카운터 (설정 버튼 아래)
        self.counter_label = ctk.CTkLabel(
            right_frame,
            text="0/20",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60")
        )
        self.counter_label.pack()
        
        # 중앙 상태 레이블 (숨김 처리, 필요시 표시)
        self.status_label = ctk.CTkLabel(
            control_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray30", "gray70")
        )
    
    def _create_thumbnail_grid(self):
        """썸네일 그리드 생성"""
        # 썸네일 영역에 다른 배경색 적용 가능
        self.grid_frame = ctk.CTkScrollableFrame(self.root)
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 초기에는 컬럼 설정하지 않음 (동적으로 설정됨)
    
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
        # 현재 이미지와 썸네일 크기 저장
        self.current_images = image_files
        self.current_thumbnail_size = thumbnail_size
        
        # 기존 썸네일 제거
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.thumbnails.clear()
        
        # 창 너비에 따른 동적 컬럼 수 계산
        columns = self._calculate_columns(thumbnail_size)
        self.current_columns = columns  # 현재 컬럼 수 저장
        
        # 그리드 컬럼 재설정 (기존 설정 모두 제거 후 재설정)
        for i in range(20):  # 충분히 큰 수로 기존 컬럼 설정 제거
            self.grid_frame.grid_columnconfigure(i, weight=0)
        for i in range(columns):
            self.grid_frame.grid_columnconfigure(i, weight=1)
        
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
                    lambda e, path=img_path: self.update_status(f"📋 {path.name}")
                )
                img_label.bind(
                    "<Leave>", 
                    lambda e: self.update_status("")
                )
                
            except Exception as e:
                print(f"썸네일 로드 오류 {img_path}: {e}")
    
    def update_status(self, message: str):
        """상태 메시지 업데이트"""
        self.status_label.configure(text=message, text_color=("gray10", "gray90"))
    
    def update_counter(self, current: int, max_count: int):
        """이미지 카운터 업데이트"""
        self.counter_label.configure(text=f"{current}/{max_count}")
    
    def update_status_error(self, message: str, duration: int = 3000):
        """에러 상태 메시지 업데이트 (빨간색)
        
        Args:
            message: 표시할 메시지
            duration: 메시지 표시 시간 (밀리초, 기본 3초)
        """
        self.status_label.configure(text=message, text_color="red")
        
        # 일정 시간 후 비우기
        self.root.after(duration, lambda: self.update_status(""))
    
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
    
    def _calculate_columns(self, thumbnail_size: int) -> int:
        """창 너비에 따른 최적 컬럼 수 계산"""
        # grid_frame의 실제 너비 가져오기
        available_width = self.grid_frame.winfo_width()
        if available_width <= 1:  # 아직 렌더링되지 않은 경우
            available_width = self.root.winfo_width() - 40  # 패딩 고려
        
        # 스크롤바 너비와 여백 고려
        available_width -= 30  # 스크롤바 + 여백
        
        # 각 썸네일이 차지하는 실제 너비 (썸네일 + 패딩 + 테두리 + 레이블)
        thumb_total_width = thumbnail_size + 20  # 패딩과 여백 포함
        
        # 최소 2개, 최대 10개 컬럼
        columns = max(2, min(10, available_width // thumb_total_width))
        
        return columns
    
    def bind_resize_event(self):
        """창 크기 변경 이벤트 바인딩"""
        # 디바운싱을 위한 타이머
        self.resize_timer = None
        
        def on_resize(event):
            # root 윈도우의 이벤트만 처리 (자식 위젯 이벤트 무시)
            if event.widget != self.root:
                return
            
            # 너비가 실제로 변경된 경우만 처리
            current_width = event.width
            if abs(current_width - self.last_width) < 50:  # 50픽셀 미만 변경은 무시
                return
            
            self.last_width = current_width
            
            # 이전 타이머 취소
            if self.resize_timer:
                self.root.after_cancel(self.resize_timer)
            
            # 500ms 후에 리사이즈 처리 (디바운싱 시간 증가)
            self.resize_timer = self.root.after(500, self._handle_resize)
        
        # Configure 이벤트는 창 크기가 변경될 때 발생
        self.root.bind('<Configure>', on_resize)
    
    def _handle_resize(self):
        """창 크기 변경 처리"""
        if self.current_images:
            # 새로운 컬럼 수 계산
            new_columns = self._calculate_columns(self.current_thumbnail_size)
            
            # 컬럼 수가 변경된 경우에만 그리드 업데이트
            if new_columns != self.current_columns:
                self.current_columns = new_columns
                self.update_thumbnail_grid(self.current_images, self.current_thumbnail_size)
    
    def _on_thumbnail_click(self, img_path: Path):
        """썸네일 클릭 처리"""
        if self.on_copy_path_callback:
            self.on_copy_path_callback(img_path)