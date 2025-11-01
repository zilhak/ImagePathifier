# ImagePathifier - Rust Edition 프로젝트 명세서

## 프로젝트 개요
클립보드의 이미지를 파일 경로로 변환하는 크로스 플랫폼 데스크톱 애플리케이션. Claude CLI 및 기타 커맨드라인 도구와의 원활한 통합을 위해 특별히 설계됨.

**Python에서 Rust로 전환**: 단일 실행 파일, 빠른 시작, 낮은 메모리 사용량

## 핵심 기능

### 주요 목적
사용자가 클립보드에 이미지를 복사했을 때 (스크린샷, 파일 복사, 애플리케이션에서 복사 등), 이 앱은:
1. 클립보드의 이미지를 감지
2. 순차적 이름으로 지정된 디렉토리에 저장
3. 클립보드 내용을 파일 경로로 자동 교체
4. 저장된 이미지의 시각적 피드백 제공

이는 많은 CLI 도구(Claude CLI 등)가 이미지 데이터를 직접 받을 수 없지만 파일 경로는 처리할 수 있는 문제를 해결합니다.

## 기술 아키텍처

### 기술 스택
- **언어**: Rust 2021 Edition
- **GUI 프레임워크**: egui (즉시 모드 GUI)
- **이미지 처리**: image crate
- **클립보드 관리**: arboard (크로스 플랫폼)
- **설정 관리**: confy (자동 직렬화)
- **플랫폼 지원**: Windows, macOS, Linux

### 프로젝트 구조
```
ImagePathifier/
├── Cargo.toml              # Rust 프로젝트 설정
├── src/
│   ├── main.rs            # 진입점, 폰트 설정
│   ├── app.rs             # 메인 애플리케이션 로직
│   ├── config.rs          # 설정 관리
│   ├── image_manager.rs   # 이미지 파일 작업
│   ├── clipboard.rs       # 클립보드 작업
│   └── ui/
│       ├── mod.rs         # UI 모듈
│       ├── settings_window.rs  # 설정 다이얼로그
│       └── thumbnail_grid.rs   # 썸네일 그리드
├── build.bat              # Windows 빌드 스크립트
├── build.sh               # macOS/Linux 빌드 스크립트
└── saved_images/          # 기본 이미지 저장소
```

## 상세 구현 설명

### 1. 메인 애플리케이션 (`src/app.rs`)

```rust
pub struct ImagePathifierApp {
    config: Config,
    clipboard: Arc<Mutex<ClipboardManager>>,
    image_manager: ImageManager,
    status_message: String,
    status_color: egui::Color32,
    image_list: Vec<PathBuf>,
    thumbnails: Vec<(PathBuf, egui::TextureHandle)>,
    show_settings: bool,
    temp_config: Config,
    clicked_path: Option<PathBuf>,
}
```

**주요 책임**:
- egui 컨텍스트에서 설정 초기화
- 메인 윈도우 렌더링 및 이벤트 처리
- 클립보드 붙여넣기 이벤트 처리 (키보드 단축키와 버튼 클릭 모두)
- 클립보드 관리자와 이미지 관리자 간 조정
- 설정 변경 동적 적용
- 썸네일 그리드 업데이트

**Rust 특징**:
- `Arc<Mutex<ClipboardManager>>`: 스레드 안전한 클립보드 접근
- `clicked_path`: borrowing 규칙 준수를 위한 지연 처리
- `egui::TextureHandle`: GPU 텍스처 관리

### 2. 설정 관리 (`src/config.rs`)

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub save_directory: PathBuf,
    pub max_images: usize,
    pub theme: Theme,
    pub thumbnail_size: u32,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq)]
pub enum Theme {
    System,
    Light,
    Dark,
}
```

**설정 저장**:
- `confy` crate 사용으로 자동 직렬화/역직렬화
- 플랫폼별 설정 경로 자동 관리
- Windows: `%APPDATA%\image-pathifier\config.toml`
- macOS: `~/Library/Application Support/image-pathifier/config.toml`
- Linux: `~/.config/image-pathifier/config.toml`

### 3. 이미지 관리 (`src/image_manager.rs`)

```rust
pub struct ImageManager {
    save_directory: PathBuf,
    max_images: usize,
}
```

**파일 작업**:
- 순차적 명명 (img_0001.png, img_0002.png 등)
- 디렉토리 자동 생성
- PNG 형식으로 이미지 저장
- 기존 이미지 추적 (최신순 정렬)
- max_images 초과 시 오래된 이미지 자동 정리
- `walkdir` crate로 효율적인 파일 시스템 탐색

**중요**: `get_next_image_number()`는 기존 번호가 매겨진 파일을 올바르게 처리하고 다음 사용 가능한 번호를 찾습니다.

### 4. 클립보드 작업 (`src/clipboard.rs`)

```rust
pub struct ClipboardManager {
    clipboard: Clipboard,
}
```

**크로스 플랫폼 처리**:
- `arboard` crate로 플랫폼별 클립보드 API 추상화
- 이미지 데이터 감지 및 추출
- RGBA 형식으로 이미지 변환
- 텍스트 클립보드에 경로 복사

**macOS 고려사항**:
- 클립보드 접근은 `arboard`가 자동 처리
- 권한 문제 시 시스템 환경설정에서 권한 부여 필요

### 5. 메인 진입점 (`src/main.rs`)

**한글 폰트 지원**:
```rust
fn setup_fonts(ctx: &egui::Context) {
    // Windows: 맑은 고딕, 굴림, 바탕
    // macOS: AppleSDGothicNeo
    // Linux: Noto Sans CJK
}
```

**플랫폼별 폰트 로드**:
- 시스템 폰트 디렉토리에서 자동 감지
- egui의 기본 폰트 앞에 한글 폰트 추가
- 한글 우선, 영문은 기본 폰트 사용

### 6. UI 구성

**메인 윈도우 레이아웃**:
```
┌─────────────────────────────────────┐
│ [📋 붙여넣기]  Ctrl+V    0/20  [⚙]  │ <- 상단 패널
│ 상태: 준비됨                         │
├─────────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │
│ │     │ │     │ │     │ │     │    │ <- 썸네일 그리드
│ │ img │ │ img │ │ img │ │ img │    │    (동적 컬럼)
│ │     │ │     │ │     │ │     │    │
│ └─────┘ └─────┘ └─────┘ └─────┘    │
│ [최신] img_0005.png                 │
└─────────────────────────────────────┘
```

**설정 다이얼로그**:
- 모달 윈도우
- 디렉토리 경로 입력
- 슬라이더: 최대 이미지 수 (1-100)
- 슬라이더: 썸네일 크기 (50-200px)
- 테마 선택: System/Light/Dark
- 저장/취소 버튼

## 크로스 플랫폼 고려사항

### Windows
- **폰트**: 맑은 고딕 자동 로드
- **경로**: 백슬래시 자동 처리
- **클립보드**: 네이티브 API 사용
- **키 바인딩**: Ctrl+V
- **콘솔 숨기기**: `#![windows_subsystem = "windows"]`

### macOS
- **폰트**: AppleSDGothicNeo 자동 로드
- **키 바인딩**: Cmd+V
- **권한**: 클립보드 접근 권한 필요 시 시스템 설정에서 부여

### Linux
- **폰트**: Noto Sans CJK 자동 로드
- **X11/Wayland**: arboard가 자동 처리
- **의존성**: 시스템 라이브러리 필요 시 설치
  ```bash
  sudo apt install libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev
  ```

## 빌드 및 배포

### 개발 빌드
```bash
cargo build
cargo run
```

### 릴리스 빌드
```bash
cargo build --release
```

**최적화 옵션**:
```toml
[profile.release]
opt-level = 3        # 최대 최적화
lto = true          # Link Time Optimization
codegen-units = 1   # 단일 코드 생성 유닛
strip = true        # 심볼 제거
```

**바이너리 크기**: 약 10MB (최적화 후)

### 빌드 스크립트
- **Windows**: `build.bat` - 빌드 후 시작 프로그램 등록 제안
- **macOS/Linux**: `build.sh` - 빌드 후 LaunchAgent/autostart 안내

## 사용자 경험 흐름

1. **시작**
   - 설정 로드 (confy 자동 처리)
   - 저장 디렉토리 생성
   - 기존 이미지 로드 및 썸네일 생성
   - 한글 폰트 로드
   - "준비됨" 상태 표시

2. **붙여넣기 작업**
   - 사용자가 Cmd/Ctrl+V 또는 버튼 클릭
   - 클립보드에서 이미지 확인
   - 이미지 있으면:
     - `saved_images/img_XXXX.png`로 저장
     - 절대 경로를 클립보드에 복사
     - 썸네일 그리드 업데이트
     - 성공 메시지 표시 (초록색)
   - 이미지 없으면:
     - 에러 메시지 표시 (빨간색)

3. **썸네일 클릭**
   - 썸네일 클릭 시 해당 경로 복사
   - 상태 메시지 업데이트

4. **설정 변경**
   - 모달 설정 창 열기
   - 저장 시 즉시 적용
   - 테마 변경 시 UI 업데이트
   - 디렉토리 변경 시 이미지 다시 로드

## 에러 처리

- **클립보드에 이미지 없음**: 빨간색 상태 메시지
- **저장 디렉토리 문제**: 자동으로 디렉토리 생성, 실패 시 에러 메시지
- **권한 오류**: 에러 로그 출력
- **잘못된 설정**: 기본값 사용

## 성능 특징

- **시작 시간**: <1초
- **메모리 사용**: ~20-40MB
- **이미지 저장**: 즉각 (수십 ms)
- **썸네일 로드**: 요청 시 (lazy loading)
- **UI 반응**: 60 FPS 유지

## Rust의 장점

1. **메모리 안전성**: Borrowing checker로 메모리 버그 방지
2. **스레드 안전성**: Arc<Mutex<>> 패턴으로 안전한 동시성
3. **제로 비용 추상화**: 고수준 코드에도 C++ 수준 성능
4. **패턴 매칭**: Result/Option으로 명확한 에러 처리
5. **크로스 컴파일**: 단일 코드베이스로 모든 플랫폼 지원

## 향후 개선 사항

- [ ] 이미지 압축 옵션
- [ ] 다양한 이미지 포맷 지원 (JPEG, WebP)
- [ ] 클라우드 스토리지 연동
- [ ] 이미지 편집 기능 (크롭, 리사이즈)
- [ ] 핫키 커스터마이징
- [ ] 다국어 지원 확대

## 라이선스

MIT
