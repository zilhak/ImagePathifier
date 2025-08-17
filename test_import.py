#!/usr/bin/env python3
"""
임포트 테스트 스크립트
"""

import sys
import os

print("Python 버전:", sys.version)
print("Python 실행 파일:", sys.executable)
print("\nPython 경로:")
for path in sys.path:
    print(f"  - {path}")

print("\n패키지 임포트 테스트:")

# 1. customtkinter 테스트
try:
    import customtkinter
    print("✓ customtkinter 임포트 성공")
    print(f"  위치: {customtkinter.__file__}")
except ImportError as e:
    print(f"✗ customtkinter 임포트 실패: {e}")

# 2. Pillow 테스트
try:
    from PIL import Image
    print("✓ PIL (Pillow) 임포트 성공")
except ImportError as e:
    print(f"✗ PIL 임포트 실패: {e}")

# 3. pyperclip 테스트
try:
    import pyperclip
    print("✓ pyperclip 임포트 성공")
except ImportError as e:
    print(f"✗ pyperclip 임포트 실패: {e}")

# 4. tkinter 테스트
try:
    import tkinter
    print("✓ tkinter 임포트 성공")
except ImportError as e:
    print(f"✗ tkinter 임포트 실패: {e}")

print("\n설치된 패키지 확인:")
import subprocess
result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
lines = result.stdout.split('\n')
for line in lines:
    if any(pkg in line.lower() for pkg in ['customtkinter', 'pillow', 'pyperclip', 'tkinter']):
        print(f"  {line}")