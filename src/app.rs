// 메인 애플리케이션
use crate::clipboard::ClipboardManager;
use crate::config::{Config, Theme};
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
}

impl ImagePathifierApp {
    pub fn new(cc: &eframe::CreationContext<'_>) -> Self {
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

    /// 썸네일 로드
    fn load_thumbnail(&self, ctx: &egui::Context, path: &PathBuf) -> Option<egui::TextureHandle> {
        if let Ok(img) = image::open(path) {
            let size = self.config.thumbnail_size;
            let thumbnail = img.thumbnail(size, size);
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
}

impl eframe::App for ImagePathifierApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // 키보드 단축키 처리 (Ctrl+V / Cmd+V)
        if ctx.input(|i| i.key_pressed(egui::Key::V) && (i.modifiers.ctrl || i.modifiers.command)) {
            self.handle_paste(ctx);
        }

        // 상단 패널 (붙여넣기 버튼과 설정)
        egui::TopBottomPanel::top("top_panel").show(ctx, |ui| {
            ui.horizontal(|ui| {
                // 붙여넣기 버튼
                if ui.button("📋 붙여넣기").clicked() {
                    self.handle_paste(ctx);
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
                    ui.label(format!("{}/{}", self.image_list.len(), self.config.max_images));

                    // 설정 버튼
                    if ui.button("⚙ 설정").clicked() {
                        self.show_settings = true;
                        self.temp_config = self.config.clone();
                    }
                });
            });

            // 상태 메시지
            ui.horizontal(|ui| {
                ui.colored_label(self.status_color, &self.status_message);
            });
        });

        // 메인 컨텐츠 (썸네일 그리드)
        egui::CentralPanel::default().show(ctx, |ui| {
            egui::ScrollArea::vertical().show(ui, |ui| {
                // 썸네일 로드 (필요한 경우에만)
                if self.thumbnails.len() != self.image_list.len() {
                    self.thumbnails.clear();
                    for path in &self.image_list {
                        if let Some(texture) = self.load_thumbnail(ctx, path) {
                            self.thumbnails.push((path.clone(), texture));
                        }
                    }
                }

                // 그리드 레이아웃
                let available_width = ui.available_width();
                let thumb_size = self.config.thumbnail_size as f32 + 20.0;
                let columns = (available_width / thumb_size).floor().max(2.0) as usize;

                ui.columns(columns.min(self.thumbnails.len()).max(1), |columns_ui| {
                    for (idx, (path, texture)) in self.thumbnails.iter().enumerate() {
                        let col_idx = idx % columns;
                        columns_ui[col_idx].group(|ui| {
                            // 썸네일 이미지
                            let response = ui.add(
                                egui::Image::new(texture)
                                    .fit_to_exact_size(egui::vec2(
                                        self.config.thumbnail_size as f32,
                                        self.config.thumbnail_size as f32,
                                    ))
                                    .sense(egui::Sense::click()),
                            );

                            if response.clicked() {
                                self.clicked_path = Some(path.clone());
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
            });
        });

        // 설정 창
        if self.show_settings {
            egui::Window::new("⚙ 설정")
                .collapsible(false)
                .resizable(false)
                .show(ctx, |ui| {
                    ui.label("저장 디렉토리:");
                    ui.text_edit_singleline(&mut self.temp_config.save_directory.to_string_lossy().to_string());

                    ui.add_space(10.0);

                    ui.label("최대 이미지 수:");
                    ui.add(egui::Slider::new(&mut self.temp_config.max_images, 1..=100));

                    ui.add_space(10.0);

                    ui.label("썸네일 크기:");
                    ui.add(egui::Slider::new(&mut self.temp_config.thumbnail_size, 50..=200));

                    ui.add_space(10.0);

                    ui.label("테마:");
                    ui.horizontal(|ui| {
                        ui.selectable_value(&mut self.temp_config.theme, Theme::System, "시스템");
                        ui.selectable_value(&mut self.temp_config.theme, Theme::Light, "라이트");
                        ui.selectable_value(&mut self.temp_config.theme, Theme::Dark, "다크");
                    });

                    ui.add_space(20.0);

                    ui.horizontal(|ui| {
                        if ui.button("저장").clicked() {
                            self.save_settings();
                            ctx.set_visuals(self.config.theme.to_visuals());
                            self.show_settings = false;
                        }

                        if ui.button("취소").clicked() {
                            self.show_settings = false;
                        }
                    });
                });
        }

        // 클릭된 썸네일 처리
        if let Some(path) = self.clicked_path.take() {
            self.handle_thumbnail_click(&path);
        }
    }
}
