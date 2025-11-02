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
                        // 경로를 클립보드에 복사
                        let path_str = path.to_string_lossy().to_string();
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

        let path_str = path.to_string_lossy().to_string();
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
            crate::ui::top_panel::render(
                ui,
                &self.status_message,
                self.status_color,
                self.image_list.len(),
                self.config.max_images,
                &mut on_paste,
                &mut on_settings,
            );
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

        // 클릭된 썸네일 처리
        if let Some(path) = self.clicked_path.take() {
            self.handle_thumbnail_click(&path);
        }
    }
}
