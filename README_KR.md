# Image Pathifier

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)
[![한국어](https://img.shields.io/badge/lang-한국어-green.svg)](README_KR.md)

클립보드 이미지를 파일 경로로 즉시 변환. Claude CLI용으로 제작.

## 기능

1. 이미지를 클립보드에 복사 (스크린샷 등)
2. 앱에서 `Ctrl+V` 누르기
3. 파일 경로가 클립보드에 복사됨

끝.

## 설치

```bash
git clone https://github.com/yourusername/ImagePathifier.git
cd ImagePathifier

# 설정 (처음 한 번만)
./setup_venv.sh    # Mac/Linux
setup_venv.bat     # Windows

# 실행
./run_with_venv.sh    # Mac/Linux  
run_with_venv.bat     # Windows
```

## 필요 사항

- Python 3.7+
- `pip install -r requirements.txt`

## 사용법

```bash
python ImagePathifier.py
```

이미지가 클립보드에 있을 때 `Ctrl+V` 누르면 됩니다.

## 라이선스

MIT