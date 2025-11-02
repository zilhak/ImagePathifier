// 썸네일 그리드 UI 모듈
use eframe::egui;
use std::path::PathBuf;

/// 썸네일 그리드 렌더링
///
/// Returns: clicked_path (썸네일 클릭 시)
pub fn render(
    ui: &mut egui::Ui,
    thumbnails: &[(PathBuf, egui::TextureHandle)],
    thumbnail_size: u32,
) -> Option<PathBuf> {
    let mut clicked_path = None;

    // 그리드 레이아웃
    let available_width = ui.available_width();
    let thumb_size = thumbnail_size as f32 + 20.0;
    let columns = (available_width / thumb_size).floor().max(2.0) as usize;

    ui.columns(columns.min(thumbnails.len()).max(1), |columns_ui| {
        for (idx, (path, texture)) in thumbnails.iter().enumerate() {
            let col_idx = idx % columns;
            columns_ui[col_idx].group(|ui| {
                // 썸네일 이미지
                let response = ui.add(
                    egui::Image::new(texture)
                        .fit_to_exact_size(egui::vec2(
                            thumbnail_size as f32,
                            thumbnail_size as f32,
                        ))
                        .sense(egui::Sense::click()),
                );

                if response.clicked() {
                    clicked_path = Some(path.clone());
                }

                // 파일명
                let filename = path.file_name().unwrap().to_string_lossy();
                ui.label(if idx == 0 {
                    format!("[최신] {}", filename)
                } else {
                    filename.to_string()
                });
            });
        }
    });

    clicked_path
}

/// 썸네일 로드
pub fn load_thumbnail(
    ctx: &egui::Context,
    path: &PathBuf,
    thumbnail_size: u32,
) -> Option<egui::TextureHandle> {
    if let Ok(img) = image::open(path) {
        let thumbnail = img.thumbnail(thumbnail_size, thumbnail_size);
        let rgba = thumbnail.to_rgba8();
        let pixels = rgba.as_flat_samples();

        let color_image = egui::ColorImage::from_rgba_unmultiplied(
            [thumbnail.width() as usize, thumbnail.height() as usize],
            pixels.as_slice(),
        );

        let texture = ctx.load_texture(
            path.to_string_lossy(),
            color_image,
            Default::default(),
        );

        return Some(texture);
    }
    None
}
