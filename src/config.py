"""
설정 관리 모듈
"""

import json
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """애플리케이션 설정 관리자"""
    
    DEFAULT_SETTINGS = {
        'save_directory': './saved_images',
        'max_images': 20,
        'theme': 'dark',
        'thumbnail_size': 100
    }
    
    def __init__(self, config_file: str = 'settings.json'):
        self.config_file = Path(config_file)
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """JSON 파일에서 설정 로드"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # 기본값과 병합하여 모든 키가 존재하도록 보장
                    settings = self.DEFAULT_SETTINGS.copy()
                    settings.update(loaded)
                    return settings
            except (json.JSONDecodeError, IOError) as e:
                print(f"설정 파일 로드 오류: {e}")
                return self.DEFAULT_SETTINGS.copy()
        return self.DEFAULT_SETTINGS.copy()
    
    def save_settings(self, settings: Dict[str, Any] = None) -> bool:
        """설정을 JSON 파일에 저장"""
        if settings:
            self.settings = settings
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"설정 파일 저장 오류: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """설정 값 가져오기"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """설정 값 설정"""
        self.settings[key] = value
    
    def update(self, settings: Dict[str, Any]) -> None:
        """여러 설정 값 업데이트"""
        self.settings.update(settings)