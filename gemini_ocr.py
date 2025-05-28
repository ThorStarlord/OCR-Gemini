import os
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
import google.generativeai as genai
from PIL import Image, ImageEnhance
import config

class GeminiMangaOCR:
    def __init__(self):
        """Initialize the Gemini OCR system."""
        self.setup_logging()
        self.setup_gemini()
        self.processed_count = 0
        self.error_count = 0
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.DEBUG if config.DEBUG_MODE else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(config.ERROR_LOG_FILE) if config.SAVE_ERROR_LOG else logging.NullHandler(),
                logging.StreamHandler() if config.VERBOSE_OUTPUT else logging.NullHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_gemini(self):
        """Setup Gemini API configuration."""
        if not config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in config.py or as an environment variable.")
        
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        self.logger.info(f"Initialized Gemini model: {config.GEMINI_MODEL}")
        
    def preprocess_image(self, image_path: str) -> Optional[Image.Image]:
        """Preprocess image for better OCR results."""
        try:
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if too large
            if img.size[0] > config.MAX_IMAGE_SIZE[0] or img.size[1] > config.MAX_IMAGE_SIZE[1]:
                img.thumbnail(config.MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
                self.logger.info(f"Resized image to {img.size}")
            
            if config.ENABLE_IMAGE_PREPROCESSING:
                # Enhance contrast
                if config.ENHANCE_CONTRAST:
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(config.CONTRAST_FACTOR)
                
                # Enhance sharpness
                if config.ENHANCE_SHARPNESS:
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(config.SHARPNESS_FACTOR)
            
            # Save processed image if debugging
            if config.SAVE_PROCESSED_IMAGES:
                processed_path = os.path.join(config.SCRIPT_DIR, f"processed_{os.path.basename(image_path)}")
                img.save(processed_path, quality=config.IMAGE_QUALITY)
                self.logger.debug(f"Saved processed image: {processed_path}")
            
            return img
            
        except Exception as e:
            self.logger.error(f"Error preprocessing image {image_path}: {e}")
            return None
    
    def extract_text_from_image(self, image_path: str) -> Optional[str]:
        """Extract text from a single image using Gemini."""
        try:
            # Preprocess image
            img = self.preprocess_image(image_path)
            if img is None:
                return None
            
            # Get the appropriate prompt
            prompt = config.OCR_PROMPTS.get(config.DEFAULT_PROMPT, config.OCR_PROMPTS['basic'])
            
            # Add language-specific instructions
            if config.MANGA_LANGUAGE == 'Japanese':
                prompt = config.OCR_PROMPTS.get('japanese', prompt)
            
            if config.READING_ORDER == 'right-to-left':
                prompt += "\nNote: This is a manga page, please consider right-to-left reading order."
            
            self.logger.info(f"Processing image: {os.path.basename(image_path)}")
            
            # Generate content with Gemini
            response = self.model.generate_content([prompt, img])
            
            # Add delay to respect rate limits
            time.sleep(config.REQUEST_DELAY)
            
            if response.text:
                self.processed_count += 1
                self.logger.info(f"Successfully extracted text from {os.path.basename(image_path)}")
                
                # Save API response if debugging
                if config.SAVE_API_RESPONSES:
                    response_file = os.path.join(config.SCRIPT_DIR, f"response_{os.path.basename(image_path)}.txt")
                    with open(response_file, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                
                return response.text
            else:
                self.logger.warning(f"No text extracted from {os.path.basename(image_path)}")
                return None
                
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Error processing {image_path}: {e}")
            if not config.CONTINUE_ON_ERROR:
                raise
            return None
    
    def get_image_files(self, folder_path: str) -> List[str]:
        """Get all supported image files from the folder."""
        image_files = []
        for ext in config.SUPPORTED_EXTENSIONS:
            pattern = f"*{ext}"
            image_files.extend(Path(folder_path).glob(pattern))
            # Also check uppercase extensions
            pattern = f"*{ext.upper()}"
            image_files.extend(Path(folder_path).glob(pattern))
        
        # Sort files naturally
        image_files = sorted([str(f) for f in image_files])
        self.logger.info(f"Found {len(image_files)} image files")
        return image_files
    
    def format_output(self, filename: str, text: str, page_number: int) -> str:
        """Format the extracted text for output."""
        output = ""
        
        if config.SEPARATE_PAGES and page_number > 1:
            output += "\n" + "="*80 + "\n"
        
        if config.INCLUDE_FILENAME:
            output += f"File: {filename}\n"
        
        if config.ADD_PAGE_NUMBERS:
            output += f"Page: {page_number}\n"
        
        if config.INCLUDE_TIMESTAMP:
            output += f"Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        output += f"{'-'*40}\n"
        output += text + "\n"
        
        return output
    
    def process_manga_folder(self, folder_path: str = None) -> bool:
        """Process all manga images in the folder."""
        if folder_path is None:
            folder_path = config.IMAGE_FOLDER
        
        if not os.path.exists(folder_path):
            self.logger.error(f"Folder not found: {folder_path}")
            return False
        
        # Get all image files
        image_files = self.get_image_files(folder_path)
        
        if not image_files:
            self.logger.warning(f"No supported image files found in {folder_path}")
            return False
        
        self.logger.info(f"Starting OCR processing of {len(image_files)} images...")
        
        # Process images
        all_text = []
        start_time = time.time()
        
        for i, image_path in enumerate(image_files, 1):
            self.logger.info(f"Processing {i}/{len(image_files)}: {os.path.basename(image_path)}")
            
            extracted_text = self.extract_text_from_image(image_path)
            
            if extracted_text:
                formatted_text = self.format_output(
                    os.path.basename(image_path),
                    extracted_text,
                    i
                )
                all_text.append(formatted_text)
        
        # Save results
        if all_text:
            try:
                with open(config.OUTPUT_FILE, 'w', encoding='utf-8') as f:
                    f.write(f"Manga OCR Results - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Model: {config.GEMINI_MODEL}\n")
                    f.write(f"Total Images Processed: {len(image_files)}\n")
                    f.write(f"Successful Extractions: {self.processed_count}\n")
                    f.write(f"Errors: {self.error_count}\n")
                    f.write("="*80 + "\n\n")
                    f.write("\n".join(all_text))
                
                end_time = time.time()
                processing_time = end_time - start_time
                
                self.logger.info(f"OCR processing completed!")
                self.logger.info(f"Results saved to: {config.OUTPUT_FILE}")
                self.logger.info(f"Processing time: {processing_time:.2f} seconds")
                self.logger.info(f"Successfully processed: {self.processed_count}/{len(image_files)} images")
                
                if self.error_count > 0:
                    self.logger.warning(f"Errors encountered: {self.error_count}")
                
                return True
                
            except Exception as e:
                self.logger.error(f"Error saving results: {e}")
                return False
        else:
            self.logger.warning("No text was extracted from any images")
            return False

def main():
    """Main function to run the OCR process."""
    try:
        ocr = GeminiMangaOCR()
        success = ocr.process_manga_folder()
        
        if success:
            print(f"\n✅ OCR processing completed successfully!")
            print(f"📄 Results saved to: {config.OUTPUT_FILE}")
            print(f"📊 Processed: {ocr.processed_count} images")
            if ocr.error_count > 0:
                print(f"⚠️  Errors: {ocr.error_count}")
        else:
            print("❌ OCR processing failed or no text was extracted")
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.error(f"Fatal error in main: {e}")

if __name__ == "__main__":
    main()
```
