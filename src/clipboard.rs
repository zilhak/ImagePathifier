// 클립보드 관리 모듈
use arboard::{Clipboard, ImageData};
use image::{DynamicImage, ImageBuffer, Rgba};

pub struct ClipboardManager {
    clipboard: Clipboard,
}

impl ClipboardManager {
    pub fn new() -> anyhow::Result<Self> {
        Ok(Self {
            clipboard: Clipboard::new()?,
        })
    }

    /// 클립보드에서 이미지 가져오기
    pub fn get_image(&mut self) -> anyhow::Result<Option<DynamicImage>> {
        match self.clipboard.get_image() {
            Ok(img_data) => {
                log::info!("클립보드 이미지 감지: {}x{}", img_data.width, img_data.height);
                // arboard ImageData를 image crate DynamicImage로 변환
                let img = self.convert_to_dynamic_image(img_data)?;
                Ok(Some(img))
            }
            Err(arboard::Error::ContentNotAvailable) => {
                log::warn!("클립보드에 이미지 없음 (ContentNotAvailable)");
                Ok(None)
            }
            Err(e) => {
                log::error!("클립보드 읽기 오류: {:?}", e);
                Err(e.into())
            }
        }
    }

    /// 텍스트를 클립보드에 복사
    pub fn copy_text(&mut self, text: &str) -> anyhow::Result<()> {
        self.clipboard.set_text(text)?;
        Ok(())
    }

    /// arboard ImageData를 DynamicImage로 변환
    fn convert_to_dynamic_image(&self, img_data: ImageData) -> anyhow::Result<DynamicImage> {
        let width = img_data.width;
        let height = img_data.height;
        let bytes = img_data.bytes;

        // RGBA 형식으로 가정
        let img_buffer: ImageBuffer<Rgba<u8>, Vec<u8>> =
            ImageBuffer::from_raw(width as u32, height as u32, bytes.into_owned())
                .ok_or_else(|| anyhow::anyhow!("Failed to create image buffer"))?;

        Ok(DynamicImage::ImageRgba8(img_buffer))
    }
}

impl Default for ClipboardManager {
    fn default() -> Self {
        Self::new().expect("Failed to create clipboard manager")
    }
}
