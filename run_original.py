#!/usr/bin/env python3
"""
원본 파일 실행 스크립트
"""

import sys
import os

# 백업된 원본 파일이 있는지 확인
if os.path.exists('image_pathifier_old.py'):
    print("백업된 원본 파일을 실행합니다...")
    # 원본 파일을 모듈로 임포트
    import importlib.util
    spec = importlib.util.spec_from_file_location("image_pathifier", "image_pathifier_old.py")
    image_pathifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(image_pathifier)
    
    # main 함수 실행
    if hasattr(image_pathifier, 'main'):
        image_pathifier.main()
    else:
        print("원본 파일에 main 함수가 없습니다.")
else:
    print("백업된 원본 파일(image_pathifier_old.py)을 찾을 수 없습니다.")
    print("\n원본 파일이 필요하시면 다음 명령을 실행하세요:")
    print("git checkout image_pathifier.py")