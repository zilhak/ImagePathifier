// 설정 관리 모듈
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub save_directory: PathBuf,
    pub max_images: usize,
    pub theme: Theme,
    pub thumbnail_size: u32,
    #[cfg(target_os = "windows")]
    pub wsl_mode: bool,
    #[cfg(target_os = "macos")]
    pub show_macos_tip: bool,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq)]
pub enum Theme {
    System,
    Light,
    Dark,
}

impl Default for Config {
    fn default() -> Self {
        // exe가 있는 폴더/saved_images를 기본값으로
        let exe_dir = std::env::current_exe()
            .ok()
            .and_then(|p| p.parent().map(|p| p.to_path_buf()))
            .unwrap_or_else(|| PathBuf::from("."));

        Self {
            save_directory: exe_dir.join("saved_images"),
            max_images: 20,
            theme: Theme::Dark,
            thumbnail_size: 100,
            #[cfg(target_os = "windows")]
            wsl_mode: false,
            #[cfg(target_os = "macos")]
            show_macos_tip: true, // 기본값은 팁 표시
        }
    }
}

impl Config {
    /// exe 폴더의 settings.json 경로 가져오기
    fn get_config_path() -> PathBuf {
        let exe_dir = std::env::current_exe()
            .ok()
            .and_then(|p| p.parent().map(|p| p.to_path_buf()))
            .unwrap_or_else(|| PathBuf::from("."));

        exe_dir.join("settings.json")
    }

    /// 설정 로드 (exe폴더/settings.json)
    pub fn load() -> Self {
        let config_path = Self::get_config_path();

        if config_path.exists() {
            // 파일이 있으면 로드
            if let Ok(contents) = std::fs::read_to_string(&config_path) {
                if let Ok(config) = serde_json::from_str(&contents) {
                    return config;
                }
            }
        }

        // 파일이 없거나 파싱 실패 시 기본값
        Self::default()
    }

    /// 설정 저장 (exe폴더/settings.json)
    pub fn save(&self) -> anyhow::Result<()> {
        let config_path = Self::get_config_path();
        let json = serde_json::to_string_pretty(self)?;
        std::fs::write(config_path, json)?;
        Ok(())
    }

    /// 저장 디렉토리 생성
    pub fn ensure_save_directory(&self) -> anyhow::Result<()> {
        if !self.save_directory.exists() {
            std::fs::create_dir_all(&self.save_directory)?;
        }
        Ok(())
    }
}

impl Theme {
    pub fn to_visuals(&self) -> egui::Visuals {
        match self {
            Theme::Light => {
                let mut visuals = egui::Visuals::light();
                // 배경색을 RGB(240, 240, 240)으로 변경
                visuals.panel_fill = egui::Color32::from_rgb(240, 240, 240);
                visuals.window_fill = egui::Color32::from_rgb(240, 240, 240);
                visuals.extreme_bg_color = egui::Color32::from_rgb(230, 230, 230);

                // 버튼 배경색을 더 어둡게
                visuals.widgets.inactive.weak_bg_fill = egui::Color32::from_rgb(210, 210, 210);
                visuals.widgets.inactive.bg_fill = egui::Color32::from_rgb(210, 210, 210);
                visuals.widgets.hovered.weak_bg_fill = egui::Color32::from_rgb(190, 190, 190);
                visuals.widgets.hovered.bg_fill = egui::Color32::from_rgb(190, 190, 190);
                visuals.widgets.active.weak_bg_fill = egui::Color32::from_rgb(170, 170, 170);
                visuals.widgets.active.bg_fill = egui::Color32::from_rgb(170, 170, 170);

                visuals
            }
            Theme::Dark => egui::Visuals::dark(),
            Theme::System => {
                // 시스템 테마 감지 (dark를 기본값으로)
                egui::Visuals::dark()
            }
        }
    }
}
