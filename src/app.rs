// 메인 애플리케이션
use crate::clipboard::ClipboardManager;
use crate::config::Config;
use crate::image_manager::ImageManager;
use eframe::egui;
use std::path::PathBuf;
use std::sync::Arc;
use std::sync::Mutex;

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
    paste_requested: bool, // Ctrl+V 플래그
}

impl ImagePathifierApp {
    pub fn new(cc: &eframe::CreationContext<'_>) -> Self {
        // 빌드 확인용 로그
        println!("=== ImagePathifierApp 초기화 - 빌드 버전: 2024-11-02-06:19 ===");

        // 설정 로드
        let config = Config::load();

        // 저장 디렉토리 확인/생성
        if let Err(e) = config.ensure_save_directory() {
            eprintln!("Failed to create save directory: {}", e);
        }

        // 테마 적용
        cc.egui_ctx.set_visuals(config.theme.to_visuals());

        let image_manager = ImageManager::new(config.save_directory.clone(), config.max_images);
        let clipboard = Arc::new(Mutex::new(
            ClipboardManager::new().expect("Failed to initialize clipboard"),
        ));

        // 기존 이미지 로드
        let image_list = image_manager.list_images().unwrap_or_default();

        Self {
            temp_config: config.clone(),
            config,
            clipboard,
            image_manager,
            status_message: String::from("준비됨"),
            status_color: egui::Color32::GRAY,
            image_list,
            thumbnails: Vec::new(),
            show_settings: false,
            clicked_path: None,
            paste_requested: false,
        }
    }

    /// 붙여넣기 작업 처리
    fn handle_paste(&mut self, ctx: &egui::Context) {
        let clipboard = Arc::clone(&self.clipboard);
        let mut clipboard_guard = clipboard.lock().unwrap();

        match clipboard_guard.get_image() {
            Ok(Some(img)) => {
                // 이미지 저장
                match self.image_manager.save_image(&img) {
                    Ok(path) => {
                        // 경로를 문자열로 변환
                        let path_str = path.to_string_lossy().to_string();

                        // WSL 모드가 활성화되어 있으면 경로 변환 (Windows만)
                        #[cfg(target_os = "windows")]
                        let path_str = if self.config.wsl_mode {
                            Self::convert_to_wsl_path(&path_str)
                        } else {
                            path_str
                        };

                        #[cfg(not(target_os = "windows"))]
                        let path_str = path_str;

                        // 경로를 클립보드에 복사
                        if let Err(e) = clipboard_guard.copy_text(&path_str) {
                            self.set_status_error(format!("클립보드 복사 실패: {}", e));
                        } else {
                            self.set_status_success(format!("저장됨: {}", path.file_name().unwrap().to_string_lossy()));
                            // 이미지 목록 갱신
                            self.refresh_images();
                        }
                    }
                    Err(e) => {
                        self.set_status_error(format!("이미지 저장 실패: {}", e));
                    }
                }
            }
            Ok(None) => {
                self.set_status_error("클립보드에 이미지가 없습니다".to_string());
            }
            Err(e) => {
                self.set_status_error(format!("클립보드 읽기 실패: {}", e));
            }
        }

        ctx.request_repaint();
    }

    /// 썸네일 클릭 처리
    fn handle_thumbnail_click(&mut self, path: &PathBuf) {
        let clipboard = Arc::clone(&self.clipboard);
        let mut clipboard_guard = clipboard.lock().unwrap();

        // 경로를 문자열로 변환
        let path_str = path.to_string_lossy().to_string();

        // WSL 모드가 활성화되어 있으면 경로 변환 (Windows만)
        #[cfg(target_os = "windows")]
        let path_str = if self.config.wsl_mode {
            Self::convert_to_wsl_path(&path_str)
        } else {
            path_str
        };

        #[cfg(not(target_os = "windows"))]
        let path_str = path_str;

        if let Err(e) = clipboard_guard.copy_text(&path_str) {
            self.set_status_error(format!("클립보드 복사 실패: {}", e));
        } else {
            self.set_status_success(format!("경로 복사됨: {}", path.file_name().unwrap().to_string_lossy()));
        }
    }

    /// 이미지 목록 갱신
    fn refresh_images(&mut self) {
        self.image_list = self.image_manager.list_images().unwrap_or_default();
        // 썸네일은 다음 렌더링에서 로드됨
        self.thumbnails.clear();
    }

    /// 설정 저장
    fn save_settings(&mut self) {
        self.config = self.temp_config.clone();
        if let Err(e) = self.config.save() {
            self.set_status_error(format!("설정 저장 실패: {}", e));
        } else {
            // 이미지 매니저 설정 업데이트
            self.image_manager.update_settings(
                self.config.save_directory.clone(),
                self.config.max_images,
            );
            self.refresh_images();
            self.set_status_success("설정 저장됨".to_string());
        }
    }

    /// 성공 상태 메시지 설정
    fn set_status_success(&mut self, message: String) {
        self.status_message = message;
        self.status_color = egui::Color32::GREEN;
    }

    /// 오류 상태 메시지 설정
    fn set_status_error(&mut self, message: String) {
        self.status_message = message;
        self.status_color = egui::Color32::RED;
    }

    /// Windows 경로를 WSL 경로로 변환 (Windows에서만 컴파일됨)
    /// 예: E:\workspace\img.png -> /mnt/e/workspace/img.png
    #[cfg(target_os = "windows")]
    fn convert_to_wsl_path(windows_path: &str) -> String {
        let mut path = windows_path.to_string();

        // Windows UNC 경로 처리 (\\?\E:\... 형식)
        if path.starts_with(r"\\?\") {
            path = path[4..].to_string();
        }

        // 백슬래시를 슬래시로 변환
        path = path.replace('\\', "/");

        // 드라이브 문자 추출 (C:, E: 등)
        if let Some(colon_pos) = path.find(':') {
            if colon_pos > 0 && colon_pos <= 2 {
                let drive = &path[..colon_pos].to_lowercase();
                let rest = &path[colon_pos + 1..];
                return format!("/mnt/{}{}", drive, rest);
            }
        }

        // 드라이브 문자가 없으면 그대로 반환
        path
    }

}

impl eframe::App for ImagePathifierApp {
    fn raw_input_hook(&mut self, _ctx: &egui::Context, raw_input: &mut egui::RawInput) {
        // Ctrl+V / Cmd+V 감지 (키를 뗐을 때)
        let has_paste = raw_input.events.iter().any(|event| {
            match event {
                egui::Event::Key {
                    key: egui::Key::V,
                    pressed: false, // 키를 뗐을 때
                    modifiers,
                    ..
                } if modifiers.ctrl || modifiers.command => true,
                _ => false,
            }
        });

        if has_paste {
            self.paste_requested = true;
        }
    }

    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // raw_input_hook에서 설정한 플래그 확인
        if self.paste_requested {
            log::info!("이미지 붙여넣기 처리 시작");
            self.paste_requested = false;
            self.handle_paste(ctx);
        }

        // 상단 패널
        let mut on_paste = false;
        let mut on_settings = false;

        egui::TopBottomPanel::top("top_panel").show(ctx, |ui| {
            #[cfg(target_os = "windows")]
            let mut wsl_mode = self.config.wsl_mode;

            #[cfg(not(target_os = "windows"))]
            let mut wsl_mode = false;

            crate::ui::top_panel::render(
                ui,
                &self.status_message,
                self.status_color,
                self.image_list.len(),
                self.config.max_images,
                &mut wsl_mode,
                &mut on_paste,
                &mut on_settings,
            );

            #[cfg(target_os = "windows")]
            {
                self.config.wsl_mode = wsl_mode;
            }
        });

        // 상단 패널 이벤트 처리
        if on_paste {
            self.handle_paste(ctx);
        }
        if on_settings {
            self.show_settings = true;
            self.temp_config = self.config.clone();
        }

        // 메인 컨텐츠 (썸네일 그리드)
        egui::CentralPanel::default().show(ctx, |ui| {
            egui::ScrollArea::vertical().show(ui, |ui| {
                // 썸네일 로드 (필요한 경우에만)
                if self.thumbnails.len() != self.image_list.len() {
                    self.thumbnails.clear();
                    for path in &self.image_list {
                        if let Some(texture) = crate::ui::thumbnail_grid::load_thumbnail(
                            ctx,
                            path,
                            self.config.thumbnail_size,
                        ) {
                            self.thumbnails.push((path.clone(), texture));
                        }
                    }
                }

                // 썸네일 그리드 렌더링
                if let Some(clicked) = crate::ui::thumbnail_grid::render(
                    ui,
                    &self.thumbnails,
                    self.config.thumbnail_size,
                ) {
                    self.clicked_path = Some(clicked);
                }
            });
        });

        // 설정 창
        if self.show_settings {
            let (should_save, should_close) = crate::ui::settings_dialog::render(
                ctx,
                &mut self.temp_config,
            );

            if should_save {
                self.save_settings();
                ctx.set_visuals(self.config.theme.to_visuals());
            }

            if should_close {
                self.show_settings = false;
            }
        }

        // macOS 팁 모달
        #[cfg(target_os = "macos")]
        if self.config.show_macos_tip {
            egui::Window::new("💡 Tip")
                .collapsible(false)
                .resizable(false)
                .anchor(egui::Align2::CENTER_CENTER, [0.0, 0.0])
                .show(ctx, |ui| {
                    ui.set_width(450.0);
                    ui.vertical_centered(|ui| {
                        ui.add_space(10.0);
                        ui.label(
                            egui::RichText::new(
                                "macOS 이용자를 위한 팁"
                            )
                            .size(16.0)
                            .strong()
                        );
                        ui.add_space(5.0);
                        ui.label(
                            egui::RichText::new(
                                "Claude Code 또는 Codex 사용자"
                            )
                            .size(14.0)
                            .color(egui::Color32::GRAY)
                        );
                        ui.add_space(15.0);
                    });

                    ui.label(
                        egui::RichText::new(
                            "Claude Code나 Codex CLI에서 이미지를 직접 붙여넣을 수 있습니다."
                        )
                        .size(14.0)
                    );

                    ui.add_space(10.0);

                    ui.horizontal(|ui| {
                        ui.label("단축키:");
                        ui.label(
                            egui::RichText::new("Ctrl + V")
                                .strong()
                                .color(egui::Color32::from_rgb(100, 150, 255))
                        );
                        ui.label(
                            egui::RichText::new("(Cmd + V가 아닙니다)")
                                .italics()
                                .color(egui::Color32::GRAY)
                        );
                    });

                    ui.add_space(20.0);

                    ui.horizontal(|ui| {
                        if ui.button("확인").clicked() {
                            self.config.show_macos_tip = false;
                        }

                        ui.add_space(10.0);

                        if ui.button("더이상 보지 않기").clicked() {
                            self.config.show_macos_tip = false;
                            if let Err(e) = self.config.save() {
                                self.set_status_error(format!("설정 저장 실패: {}", e));
                            }
                        }
                    });

                    ui.add_space(5.0);
                });
        }

        // 클릭된 썸네일 처리
        if let Some(path) = self.clicked_path.take() {
            self.handle_thumbnail_click(&path);
        }
    }
}
