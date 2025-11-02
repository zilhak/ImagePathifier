// ImagePathifier - Rust Edition
// 클립보드 이미지를 파일 경로로 변환하는 데스크톱 앱

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // Windows에서 콘솔 창 숨기기

mod app;
mod clipboard;
mod config;
mod image_manager;
mod ui;

use eframe::egui;

fn main() -> Result<(), eframe::Error> {
    // 로깅 초기화 (기본 레벨: info)
    env_logger::Builder::from_default_env()
        .filter_level(log::LevelFilter::Info)
        .filter_module("egui_winit::clipboard", log::LevelFilter::Off) // egui_winit 클립보드 에러 숨기기
        .init();

    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([800.0, 600.0])
            .with_min_inner_size([600.0, 400.0])
            .with_icon(load_icon()),
        ..Default::default()
    };

    eframe::run_native(
        "Image Pathifier",
        options,
        Box::new(|cc| {
            setup_fonts(&cc.egui_ctx);
            Ok(Box::new(app::ImagePathifierApp::new(cc)))
        }),
    )
}

fn setup_fonts(ctx: &egui::Context) {
    let mut fonts = egui::FontDefinitions::default();

    // Windows 시스템 한글 폰트 로드 시도
    #[cfg(target_os = "windows")]
    {
        let font_paths = vec![
            r"C:\Windows\Fonts\malgun.ttf",      // 맑은 고딕
            r"C:\Windows\Fonts\gulim.ttc",       // 굴림
            r"C:\Windows\Fonts\batang.ttc",      // 바탕
        ];

        for font_path in font_paths {
            if let Ok(font_data) = std::fs::read(font_path) {
                fonts.font_data.insert(
                    "korean".to_owned(),
                    egui::FontData::from_owned(font_data),
                );

                // 모든 텍스트 스타일에 한글 폰트 추가
                fonts
                    .families
                    .entry(egui::FontFamily::Proportional)
                    .or_default()
                    .insert(0, "korean".to_owned());

                fonts
                    .families
                    .entry(egui::FontFamily::Monospace)
                    .or_default()
                    .insert(0, "korean".to_owned());

                break; // 첫 번째로 찾은 폰트 사용
            }
        }
    }

    // macOS
    #[cfg(target_os = "macos")]
    {
        let font_paths = vec![
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/Library/Fonts/AppleGothic.ttf",
        ];

        for font_path in font_paths {
            if let Ok(font_data) = std::fs::read(font_path) {
                fonts.font_data.insert(
                    "korean".to_owned(),
                    egui::FontData::from_owned(font_data),
                );

                fonts
                    .families
                    .entry(egui::FontFamily::Proportional)
                    .or_default()
                    .insert(0, "korean".to_owned());

                break;
            }
        }
    }

    // Linux
    #[cfg(target_os = "linux")]
    {
        let font_paths = vec![
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        ];

        for font_path in font_paths {
            if let Ok(font_data) = std::fs::read(font_path) {
                fonts.font_data.insert(
                    "korean".to_owned(),
                    egui::FontData::from_owned(font_data),
                );

                fonts
                    .families
                    .entry(egui::FontFamily::Proportional)
                    .or_default()
                    .insert(0, "korean".to_owned());

                break;
            }
        }
    }

    ctx.set_fonts(fonts);
}

fn load_icon() -> egui::IconData {
    // TODO: 아이콘 로드 구현
    // 기본 빈 아이콘 반환
    egui::IconData {
        rgba: vec![],
        width: 0,
        height: 0,
    }
}
