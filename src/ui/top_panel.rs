// 상단 패널 UI 모듈
use eframe::egui;

/// 상단 패널 렌더링
pub fn render(
    ui: &mut egui::Ui,
    status_message: &str,
    status_color: egui::Color32,
    image_count: usize,
    max_images: usize,
    on_paste: &mut bool,
    on_settings: &mut bool,
) {
    ui.horizontal(|ui| {
        // 붙여넣기 버튼
        if ui.button("📋 붙여넣기").clicked() {
            *on_paste = true;
        }

        // 단축키 안내
        let shortcut = if cfg!(target_os = "macos") {
            "Cmd+V"
        } else {
            "Ctrl+V"
        };
        ui.label(format!("단축키: {}", shortcut));

        ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
            // 이미지 카운터
            ui.label(format!("{}/{}", image_count, max_images));

            // 설정 버튼
            if ui.button("⚙ 설정").clicked() {
                *on_settings = true;
            }
        });
    });

    // 상태 메시지
    ui.horizontal(|ui| {
        ui.colored_label(status_color, status_message);
    });
}
