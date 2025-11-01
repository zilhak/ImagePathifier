// 설정 관리 모듈
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

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

impl Default for Config {
    fn default() -> Self {
        let home_dir = dirs::home_dir().unwrap_or_else(|| PathBuf::from("."));
        Self {
            save_directory: home_dir.join("saved_images"),
            max_images: 20,
            theme: Theme::Dark,
            thumbnail_size: 100,
        }
    }
}

impl Config {
    /// 설정 로드
    pub fn load() -> Self {
        confy::load("image-pathifier", "config").unwrap_or_default()
    }

    /// 설정 저장
    pub fn save(&self) -> anyhow::Result<()> {
        confy::store("image-pathifier", "config", self)?;
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
            Theme::Light => egui::Visuals::light(),
            Theme::Dark => egui::Visuals::dark(),
            Theme::System => {
                // 시스템 테마 감지 (dark를 기본값으로)
                egui::Visuals::dark()
            }
        }
    }
}
