#!/usr/bin/env python3
"""
Image Pathifier - 진입점
"""

import sys
from pathlib import Path

# 현재 디렉토리가 src이므로 상위 디렉토리를 경로에 추가
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

from src.app import ImagePathifierApp


def main():
    """메인 함수"""
    try:
        app = ImagePathifierApp()
        app.run()
    except ImportError as e:
        print(f"필요한 패키지가 설치되지 않았습니다: {e}")
        print("다음 명령어로 설치해주세요:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"애플리케이션 실행 중 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()