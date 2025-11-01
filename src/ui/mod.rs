// UI 모듈
pub mod settings_window;
pub mod thumbnail_grid;

use egui::{Context, Ui};

pub trait UiComponent {
    fn show(&mut self, ctx: &Context, ui: &mut Ui);
}
