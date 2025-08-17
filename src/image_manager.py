"""
이미지 관리 모듈
"""

from pathlib import Path
from typing import List, Optional
from PIL import Image
import shutil


class ImageManager:
    """이미지 파일 관리자"""
    
    def __init__(self, save_directory: str, max_images: int = 20):
        self.save_dir = Path(save_directory)
        self.max_images = max_images
        self.image_files: List[Path] = []
        
        # 디렉토리 생성
        self.save_dir.mkdir(exist_ok=True, parents=True)
        
        # 기존 이미지 로드
        self.load_existing_images()
    
    def load_existing_images(self) -> None:
        """저장 디렉토리에서 기존 이미지 로드"""
        self.image_files = []
        if self.save_dir.exists():
            # 번호가 매겨진 이미지 찾기
            for i in range(1, self.max_images + 1):
                img_path = self.save_dir / f"img_{i:04d}.png"
                if img_path.exists():
                    self.image_files.append(img_path)
    
    def get_next_filename(self) -> str:
        """다음 순차 파일명 가져오기"""
        # 가장 높은 번호 찾기
        max_num = 0
        for img_path in self.image_files:
            try:
                parts = img_path.stem.split('_')
                if len(parts) >= 2:
                    num = int(parts[1])
                    max_num = max(max_num, num)
            except (ValueError, IndexError):
                continue
        
        # 다음 번호
        next_num = max_num + 1
        
        # max_images를 초과하면 1로 순환
        if next_num > self.max_images:
            next_num = 1
            
        return f"img_{next_num:04d}.png"
    
    def save_image(self, image: Image.Image) -> Optional[Path]:
        """이미지 저장 및 경로 반환"""
        try:
            filename = self.get_next_filename()
            filepath = self.save_dir / filename
            
            # 파일이 존재하고 덮어써야 하는 경우
            if filepath.exists() and filepath in self.image_files:
                self.image_files.remove(filepath)
            
            # 이미지 저장
            image.save(filepath, 'PNG')
            
            # 목록에 추가
            self.image_files.append(filepath)
            
            # 오래된 이미지 정리
            self.cleanup_old_images()
            
            return filepath
            
        except Exception as e:
            print(f"이미지 저장 오류: {e}")
            return None
    
    def cleanup_old_images(self) -> None:
        """max_images 제한을 초과하는 이미지 제거"""
        while len(self.image_files) > self.max_images:
            # 가장 오래된 것(목록의 첫 번째) 제거
            old_file = self.image_files.pop(0)
            try:
                if old_file.exists():
                    old_file.unlink()
            except OSError as e:
                print(f"파일 삭제 오류: {e}")
    
    def get_sorted_images(self) -> List[Path]:
        """번호순으로 정렬된 이미지 목록 반환"""
        def get_image_number(path: Path) -> int:
            try:
                if path.stem.startswith('img_'):
                    return int(path.stem.split('_')[1])
            except (ValueError, IndexError):
                pass
            return 0
        
        self.image_files.sort(key=get_image_number)
        return self.image_files
    
    def update_settings(self, save_directory: str = None, max_images: int = None) -> None:
        """설정 업데이트"""
        if save_directory and save_directory != str(self.save_dir):
            # 새 디렉토리로 이미지 이동
            new_dir = Path(save_directory)
            new_dir.mkdir(exist_ok=True, parents=True)
            
            # 기존 이미지 복사
            new_files = []
            for old_path in self.image_files:
                if old_path.exists():
                    try:
                        new_path = new_dir / old_path.name
                        shutil.copy2(old_path, new_path)
                        new_files.append(new_path)
                    except Exception as e:
                        print(f"파일 이동 오류: {e}")
            
            self.save_dir = new_dir
            self.image_files = new_files
        
        if max_images is not None:
            self.max_images = max_images
            self.cleanup_old_images()