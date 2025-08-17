#!/usr/bin/env python3
"""
Image Pathifier - 메인 실행 파일
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 메인 애플리케이션 실행
from src.app import ImagePathifierApp

def main():
    """메인 함수"""
    try:
        app = ImagePathifierApp()
        app.run()
    except ImportError as e:
        print(f"필요한 패키지가 설치되지 않았습니다: {e}")
        print("\n다음 명령어로 설치해주세요:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"애플리케이션 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()