@echo off
REM Windows 빌드 스크립트

echo ========================================
echo ImagePathifier Rust Build Script
echo ========================================
echo.

REM Rust 설치 확인
cargo --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Rust가 설치되어 있지 않습니다.
    echo.
    echo Rust 설치: https://rustup.rs/
    echo 또는: winget install Rustlang.Rust.GNU
    pause
    exit /b 1
)

echo [1/3] Rust 버전 확인...
cargo --version
rustc --version
echo.

echo [2/3] 릴리스 빌드 시작...
cargo build --release
if %errorlevel% neq 0 (
    echo [ERROR] 빌드 실패!
    pause
    exit /b 1
)
echo.

echo [3/3] 빌드 완료!
echo.
echo 실행 파일 위치: target\release\image-pathifier.exe
echo 실행: .\target\release\image-pathifier.exe
echo.

REM 실행 파일 크기 확인
for %%A in (target\release\image-pathifier.exe) do (
    set size=%%~zA
    set /a sizeMB=!size! / 1048576
    echo 파일 크기: !sizeMB! MB
)

echo.
echo 시작 프로그램에 추가하시겠습니까? (Y/N)
set /p choice="선택: "
if /i "%choice%"=="Y" (
    set "targetPath=%cd%\target\release\image-pathifier.exe"
    set "startupFolder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
    powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%startupFolder%\ImagePathifier.lnk'); $s.TargetPath='%targetPath%'; $s.Save()"
    echo 시작 프로그램에 추가되었습니다!
)

echo.
pause
