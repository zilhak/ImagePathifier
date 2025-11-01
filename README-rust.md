# ImagePathifier - Rust Edition

클립보드의 이미지를 파일 경로로 변환하는 크로스 플랫폼 데스크톱 애플리케이션 (Rust 버전)

## 특징

- 🚀 **빠른 시작**: 단일 실행 파일, 의존성 설치 불필요
- 💾 **작은 크기**: 약 5-10MB (Python 버전 대비 훨씬 작음)
- ⚡ **빠른 성능**: Rust의 성능으로 즉각적인 반응
- 🎨 **모던 UI**: egui 기반의 깔끔한 디자인
- 🔄 **크로스 플랫폼**: Windows, macOS, Linux 지원
- ⌨️ **키보드 단축키**: Ctrl+V (Windows/Linux), Cmd+V (macOS)

## 설치 및 빌드

### 1. Rust 설치

**Windows:**
```powershell
winget install Rustlang.Rust.GNU
```

**macOS/Linux:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 2. 프로젝트 빌드

```bash
# 디버그 빌드
cargo build

# 릴리스 빌드 (최적화)
cargo build --release
```

### 3. 실행

```bash
# 디버그 모드
cargo run

# 릴리스 모드
cargo run --release

# 또는 직접 실행 파일 실행
./target/release/image-pathifier  # Linux/macOS
.\target\release\image-pathifier.exe  # Windows
```

## 사용법

1. **스크린샷 또는 이미지 복사**
   - 스크린샷 캡처 또는 이미지 파일 복사

2. **붙여넣기**
   - `Ctrl+V` (Windows/Linux) 또는 `Cmd+V` (macOS) 단축키 사용
   - 또는 "📋 붙여넣기" 버튼 클릭

3. **파일 경로 자동 복사**
   - 이미지가 저장되고 파일 경로가 클립보드에 복사됨
   - CLI 도구에 바로 붙여넣기 가능

4. **썸네일 클릭**
   - 저장된 이미지 썸네일 클릭 시 해당 경로 복사

## 설정

⚙️ 설정 버튼을 클릭하여 다음 항목 조정 가능:

- **저장 디렉토리**: 이미지 저장 위치
- **최대 이미지 수**: 보관할 최대 이미지 개수 (1-100)
- **썸네일 크기**: 썸네일 표시 크기 (50-200px)
- **테마**: 시스템/라이트/다크 모드

설정은 자동으로 저장되며 다음 실행 시 유지됩니다.

## 시작 프로그램 등록

### Windows

```powershell
# 시작 폴더에 바로가기 생성
$startupFolder = [Environment]::GetFolderPath("Startup")
$targetPath = "경로\to\image-pathifier.exe"
$shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut("$startupFolder\ImagePathifier.lnk")
$shortcut.TargetPath = $targetPath
$shortcut.Save()
```

### macOS

LaunchAgent 생성:

```bash
# ~/Library/LaunchAgents/com.imagepathifier.plist
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

autostart .desktop 파일 생성:

```bash
# ~/.config/autostart/image-pathifier.desktop
[Desktop Entry]
Type=Application
Name=Image Pathifier
Exec=/path/to/image-pathifier
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

## 프로젝트 구조

```
ImagePathifier/
├── Cargo.toml              # Rust 프로젝트 설정
├── src/
│   ├── main.rs            # 진입점
│   ├── app.rs             # 메인 애플리케이션
│   ├── config.rs          # 설정 관리
│   ├── clipboard.rs       # 클립보드 작업
│   ├── image_manager.rs   # 이미지 파일 관리
│   └── ui/                # UI 컴포넌트
│       ├── mod.rs
│       ├── settings_window.rs
│       └── thumbnail_grid.rs
├── saved_images/          # 기본 이미지 저장소
└── README-rust.md         # 이 문서
```

## 기술 스택

- **GUI**: [egui](https://github.com/emilk/egui) - 즉시 모드 GUI 프레임워크
- **클립보드**: [arboard](https://github.com/1Password/arboard) - 크로스 플랫폼 클립보드
- **이미지 처리**: [image](https://github.com/image-rs/image) - 이미지 인코딩/디코딩
- **설정**: [confy](https://github.com/rust-cli/confy) - 설정 관리
- **에러 처리**: [anyhow](https://github.com/dtolnay/anyhow) - 에러 처리

## Python 버전과의 비교

| 항목 | Python | Rust |
|------|--------|------|
| 실행 파일 크기 | ~50-100MB | ~5-10MB |
| 시작 시간 | ~2-3초 | <1초 |
| 메모리 사용량 | ~80-100MB | ~20-40MB |
| 배포 | 가상환경/의존성 필요 | 단일 실행 파일 |
| 개발 속도 | 빠름 | 보통 |
| 성능 | 보통 | 빠름 |

## 문제 해결

### Windows에서 클립보드 접근 오류
- 관리자 권한으로 실행 시도
- 바이러스 백신 소프트웨어 확인

### macOS에서 권한 오류
- "시스템 환경설정 > 보안 및 개인 정보 보호"에서 권한 부여

### Linux에서 X11/Wayland 오류
- 필요한 라이브러리 설치:
  ```bash
  sudo apt install libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev
  ```

## 라이선스

MIT License

## 기여

버그 리포트, 기능 제안, PR 환영합니다!
