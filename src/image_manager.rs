// 이미지 파일 관리 모듈
use image::DynamicImage;
use std::path::PathBuf;
use walkdir::WalkDir;

pub struct ImageManager {
    save_directory: PathBuf,
    max_images: usize,
}

impl ImageManager {
    pub fn new(save_directory: PathBuf, max_images: usize) -> Self {
        Self {
            save_directory,
            max_images,
        }
    }

    /// 이미지를 저장하고 경로 반환
    pub fn save_image(&self, img: &DynamicImage) -> anyhow::Result<PathBuf> {
        // 저장 디렉토리 확인/생성
        if !self.save_directory.exists() {
            std::fs::create_dir_all(&self.save_directory)?;
        }

        // 다음 사용 가능한 번호 찾기
        let next_num = self.get_next_image_number()?;
        let filename = format!("img_{:04}.png", next_num);
        let filepath = self.save_directory.join(&filename);

        // 이미지 저장
        img.save(&filepath)?;

        // 최대 이미지 수 초과 시 오래된 이미지 삭제
        self.cleanup_old_images()?;

        // 절대 경로 반환
        Ok(filepath.canonicalize()?)
    }

    /// 다음 사용 가능한 이미지 번호 찾기
    fn get_next_image_number(&self) -> anyhow::Result<u32> {
        let mut max_num = 0;

        if self.save_directory.exists() {
            for entry in WalkDir::new(&self.save_directory)
                .max_depth(1)
                .into_iter()
                .filter_map(|e| e.ok())
            {
                let path = entry.path();
                if let Some(filename) = path.file_name() {
                    let filename_str = filename.to_string_lossy();
                    // img_XXXX.png 형식에서 번호 추출
                    if filename_str.starts_with("img_") && filename_str.ends_with(".png") {
                        if let Some(num_str) = filename_str.strip_prefix("img_").and_then(|s| s.strip_suffix(".png")) {
                            if let Ok(num) = num_str.parse::<u32>() {
                                max_num = max_num.max(num);
                            }
                        }
                    }
                }
            }
        }

        Ok(max_num + 1)
    }

    /// 오래된 이미지 정리 (max_images 초과 시)
    fn cleanup_old_images(&self) -> anyhow::Result<()> {
        let mut images = self.list_images()?;

        // 최대 개수 초과 시 오래된 이미지 삭제
        while images.len() > self.max_images {
            if let Some(oldest) = images.pop() {
                std::fs::remove_file(oldest)?;
            }
        }

        Ok(())
    }

    /// 저장된 이미지 목록 가져오기 (최신순)
    pub fn list_images(&self) -> anyhow::Result<Vec<PathBuf>> {
        if !self.save_directory.exists() {
            return Ok(Vec::new());
        }

        let mut images: Vec<(PathBuf, std::time::SystemTime)> = Vec::new();

        for entry in WalkDir::new(&self.save_directory)
            .max_depth(1)
            .into_iter()
            .filter_map(|e| e.ok())
        {
            let path = entry.path();
            if path.is_file() {
                if let Some(ext) = path.extension() {
                    if ext == "png" || ext == "jpg" || ext == "jpeg" {
                        if let Ok(metadata) = path.metadata() {
                            if let Ok(modified) = metadata.modified() {
                                images.push((path.to_path_buf(), modified));
                            }
                        }
                    }
                }
            }
        }

        // 최신순으로 정렬
        images.sort_by(|a, b| b.1.cmp(&a.1));

        Ok(images.into_iter().map(|(path, _)| path).collect())
    }

    /// 설정 업데이트
    pub fn update_settings(&mut self, save_directory: PathBuf, max_images: usize) {
        self.save_directory = save_directory;
        self.max_images = max_images;
    }
}
