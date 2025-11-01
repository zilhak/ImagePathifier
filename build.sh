#!/bin/bash
# macOS/Linux 빌드 스크립트

set -e

echo "========================================"
echo "ImagePathifier Rust Build Script"
echo "========================================"
echo

# Rust 설치 확인
if ! command -v cargo &> /dev/null; then
    echo "[ERROR] Rust가 설치되어 있지 않습니다."
    echo
    echo "Rust 설치:"
    echo "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

echo "[1/3] Rust 버전 확인..."
cargo --version
rustc --version
echo

echo "[2/3] 릴리스 빌드 시작..."
cargo build --release
echo

echo "[3/3] 빌드 완료!"
echo
echo "실행 파일 위치: target/release/image-pathifier"
echo "실행: ./target/release/image-pathifier"
echo

# 실행 파일 크기 확인
if [[ "$OSTYPE" == "darwin"* ]]; then
    size=$(stat -f%z target/release/image-pathifier)
else
    size=$(stat -c%s target/release/image-pathifier)
fi
sizeMB=$((size / 1048576))
echo "파일 크기: ${sizeMB} MB"
echo

# 시작 프로그램 등록 안내
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS 시작 프로그램 등록:"
    echo "1. '시스템 환경설정 > 사용자 및 그룹 > 로그인 항목'으로 이동"
    echo "2. '+' 버튼을 클릭하고 실행 파일 선택"
    echo
    echo "또는 LaunchAgent 사용 (README-rust.md 참조)"
else
    echo "Linux 시작 프로그램 등록:"
    echo "~/.config/autostart/image-pathifier.desktop 파일 생성"
    echo "(README-rust.md 참조)"
fi

echo
echo "완료!"
