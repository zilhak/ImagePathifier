// 설정 다이얼로그 UI 모듈
use crate::config::{Config, Theme};
use eframe::egui;

/// 설정 다이얼로그 렌더링
///
/// Returns: (should_save, should_close)
pub fn render(
    ctx: &egui::Context,
    temp_config: &mut Config,
) -> (bool, bool) {
    let mut should_save = false;
    let mut should_close = false;

    egui::Window::new("⚙ 설정")
        .collapsible(false)
        .resizable(false)
        .default_width(500.0)
        .show(ctx, |ui| {
            ui.label("저장 디렉토리:");
            ui.horizontal(|ui| {
                // 경로 표시 (Frame으로 감싸서 텍스트 입력처럼 보이게)
                let path_str = temp_config.save_directory.to_string_lossy().to_string();
                egui::Frame::none()
                    .fill(ui.visuals().extreme_bg_color)
                    .inner_margin(egui::Margin::same(4.0))
                    .rounding(egui::Rounding::same(2.0))
                    .show(ui, |ui| {
                        ui.set_width(350.0);
                        ui.label(
                            egui::RichText::new(path_str)
                                .font(egui::FontId::monospace(12.0))
                                .color(ui.visuals().text_color())
                        );
                    });

                // 찾기 버튼
                if ui.button("📁 찾기").clicked() {
                    if let Some(folder) = rfd::FileDialog::new()
                        .set_directory(&temp_config.save_directory)
                        .pick_folder()
                    {
                        temp_config.save_directory = folder;
                    }
                }
            });

            ui.add_space(10.0);

            ui.label("최대 이미지 수:");
            ui.add(egui::Slider::new(&mut temp_config.max_images, 1..=100));

            ui.add_space(10.0);

            ui.label("썸네일 크기:");
            ui.add(egui::Slider::new(&mut temp_config.thumbnail_size, 50..=200));

            ui.add_space(10.0);

            ui.label("테마:");
            ui.horizontal(|ui| {
                ui.selectable_value(&mut temp_config.theme, Theme::System, "시스템");
                ui.selectable_value(&mut temp_config.theme, Theme::Light, "라이트");
                ui.selectable_value(&mut temp_config.theme, Theme::Dark, "다크");
            });

            ui.add_space(20.0);

            ui.horizontal(|ui| {
                if ui.button("저장").clicked() {
                    should_save = true;
                    should_close = true;
                }

                if ui.button("취소").clicked() {
                    should_close = true;
                }
            });
        });

    (should_save, should_close)
}
