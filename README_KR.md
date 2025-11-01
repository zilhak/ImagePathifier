# Image Pathifier

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)
[![한국어](https://img.shields.io/badge/lang-한국어-green.svg)](README_KR.md)

클립보드 이미지를 파일 경로로 즉시 변환. Rust로 빌드되어 빠르고 안정적입니다.

## 특징

- 🚀 **빠른 시작**: 단일 실행 파일, 의존성 설치 불필요
- 💾 **작은 크기**: 약 10MB 바이너리
- ⚡ **즉각 반응**: 네이티브 Rust 성능
- 🎨 **모던 UI**: 깔끔한 egui 기반 인터페이스
- 🔄 **크로스 플랫폼**: Windows, macOS, Linux 지원
- ⌨️ **키보드 단축키**: Ctrl+V (Windows/Linux), Cmd+V (macOS)
- 🌏 **한글 지원**: 내장 한글 폰트 지원

## 설치

### 옵션 1: 릴리스 다운로드 (권장)

[Releases](https://github.com/zilhak/ImagePathifier/releases) 페이지에서 플랫폼에 맞는 최신 릴리스를 다운로드하세요.

### 옵션 2: 소스에서 빌드

**1. Rust 설치**

Windows:
```powershell
winget install Rustlang.Rust.GNU
```

macOS/Linux:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**2. 클론 및 빌드**

```bash
git clone https://github.com/zilhak/ImagePathifier.git
cd ImagePathifier

# 릴리스 빌드
cargo build --release

# 실행
./target/release/image-pathifier      # macOS/Linux
.\target\release\image-pathifier.exe  # Windows
```

또는 빌드 스크립트 사용:

```bash
./build.sh       # macOS/Linux
build.bat        # Windows
```

## 사용법

1. **이미지 복사** (스크린샷, 파일 복사 등)
2. **Ctrl+V 누르기** (macOS는 Cmd+V) 또는 붙여넣기 버튼 클릭
3. **파일 경로가 자동으로 복사됨**
4. **경로를 CLI 도구에 붙여넣기** (Claude Code 등)

썸네일을 클릭하면 해당 경로를 다시 복사할 수 있습니다.

## 설정

⚙ 설정 버튼을 클릭하여 다음을 구성:
- **저장 디렉토리**: 이미지가 저장될 위치
- **최대 이미지 수**: 보관할 이미지 개수 (1-100)
- **썸네일 크기**: 표시 크기 (50-200px)
- **테마**: 시스템/라이트/다크 모드

설정은 자동으로 저장됩니다.

## 시작 프로그램에 추가 (선택사항)

### Windows

빌드 스크립트(`build.bat`)가 자동으로 시작 프로그램 추가를 제안합니다.

또는 수동으로:
1. `Win+R` 누르고 `shell:startup` 입력
2. `image-pathifier.exe` 바로가기 생성

### macOS

LaunchAgent 생성:

```bash
# ~/Library/LaunchAgents/com.imagepathifier.plist 생성
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.imagepathifier</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/image-pathifier</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

### Linux

autostart 항목 생성:

```bash
# ~/.config/autostart/image-pathifier.desktop 생성
[Desktop Entry]
Type=Application
Name=Image Pathifier
Exec=/path/to/image-pathifier
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

## 기술 스택

- **GUI**: [egui](https://github.com/emilk/egui) - 즉시 모드 GUI
- **클립보드**: [arboard](https://github.com/1Password/arboard) - 크로스 플랫폼 클립보드
- **이미지**: [image](https://github.com/image-rs/image) - 이미지 처리
- **설정**: [confy](https://github.com/rust-cli/confy) - 설정 관리

## 라이선스

MIT
