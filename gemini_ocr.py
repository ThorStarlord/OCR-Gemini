import os
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

# Import with error handling for type checking
try:
    import google.generativeai as genai  # type: ignore[reportPrivateImportUsage]
except ImportError as e:
    print(f"Error importing google.generativeai: {e}")
    print("Please install with: pip install google-generativeai")
    exit(1)

from PIL import Image, ImageEnhance
import config

class GeminiMangaOCR:
    def __init__(self):
        """Initialize the Gemini OCR system."""
        self._validate_config()
        self.setup_logging()
        self.setup_gemini()
        self.processed_count = 0
        self.error_count = 0
        
    def _validate_config(self) -> None:
        """Validate required configuration settings."""
        if not hasattr(config, 'GOOGLE_API_KEY') or not config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in config.py or as an environment variable.")
        
        required_attrs = ['GEMINI_MODEL', 'IMAGE_FOLDER', 'OUTPUT_FILE', 'SUPPORTED_EXTENSIONS']
        for attr in required_attrs:
            if not hasattr(config, attr):
                raise ValueError(f"Required configuration '{attr}' not found in config.py")
        
    def setup_logging(self) -> None:
        """Setup logging configuration."""
        handlers = []
        
        if getattr(config, 'SAVE_ERROR_LOG', False):
            handlers.append(logging.FileHandler(config.ERROR_LOG_FILE))
        
        if getattr(config, 'VERBOSE_OUTPUT', True):
            handlers.append(logging.StreamHandler())
        
        if not handlers:
            handlers.append(logging.NullHandler())
            
        logging.basicConfig(
            level=logging.DEBUG if getattr(config, 'DEBUG_MODE', False) else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_gemini(self) -> None:
        """Setup Gemini API configuration."""
        try:
            # Use the configure function directly from genai module
            genai.configure(api_key=config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(config.GEMINI_MODEL)
            self.logger.info(f"Initialized Gemini model: {config.GEMINI_MODEL}")
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini API: {e}")
        
    def _enhance_image(self, img: Image.Image) -> Image.Image:
        """Apply image enhancements for better OCR results."""
        if not getattr(config, 'ENABLE_IMAGE_PREPROCESSING', False):
            return img
            
        # Enhance contrast
        if getattr(config, 'ENHANCE_CONTRAST', False):
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(getattr(config, 'CONTRAST_FACTOR', 1.2))
        
        # Enhance sharpness
        if getattr(config, 'ENHANCE_SHARPNESS', False):
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(getattr(config, 'SHARPNESS_FACTOR', 1.2))
            
        return img
        
    def _resize_image(self, img: Image.Image) -> Image.Image:
        """Resize image if it exceeds maximum dimensions."""
        max_size = getattr(config, 'MAX_IMAGE_SIZE', (2048, 2048))
        
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            self.logger.info(f"Resized image to {img.size}")
            
        return img
        
    def _save_debug_image(self, img: Image.Image, image_path: str) -> None:
        """Save processed image for debugging purposes."""
        if not getattr(config, 'SAVE_PROCESSED_IMAGES', False):
            return
            
        try:
            script_dir = getattr(config, 'SCRIPT_DIR', os.path.dirname(__file__))
            processed_path = os.path.join(script_dir, f"processed_{os.path.basename(image_path)}")
            quality = getattr(config, 'IMAGE_QUALITY', 95)
            img.save(processed_path, quality=quality)
            self.logger.debug(f"Saved processed image: {processed_path}")
        except Exception as e:
            self.logger.warning(f"Failed to save debug image: {e}")

    def preprocess_image(self, image_path: str) -> Optional[Image.Image]:
        """Preprocess image for better OCR results."""
        try:
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if too large
            img = self._resize_image(img)
            
            # Apply enhancements
            img = self._enhance_image(img)
            
            # Save processed image if debugging
            self._save_debug_image(img, image_path)
            
            return img
            
        except Exception as e:
            self.logger.error(f"Error preprocessing image {image_path}: {e}")
            return None
    
    def _get_ocr_prompt(self) -> str:
        """Get the appropriate OCR prompt based on configuration."""
        prompts = getattr(config, 'OCR_PROMPTS', {})
        default_prompt = getattr(config, 'DEFAULT_PROMPT', 'basic')
        prompt = prompts.get(default_prompt, prompts.get('basic', 'Extract all text from this image.'))
        
        # Add language-specific instructions
        manga_language = getattr(config, 'MANGA_LANGUAGE', '')
        
        # Handle Chinese language settings
        if manga_language == 'Chinese':
            if getattr(config, 'ENABLE_TRANSLATION', False):
                # Use translation prompt if translation is enabled
                if 'chinese_translate' in prompts:
                    prompt = prompts['chinese_translate']
                elif 'chinese' in prompts:
                    prompt = prompts['chinese']
            elif default_prompt == 'basic' and 'chinese' in prompts:
                # Override basic with Chinese if language is set
                prompt = prompts['chinese']
        elif manga_language == 'Japanese' and 'japanese' in prompts:
            if default_prompt == 'basic':
                prompt = prompts['japanese']
        
        # Add translation instructions if enabled
        if getattr(config, 'ENABLE_TRANSLATION', False) and not default_prompt.endswith('_translate'):
            translation_instructions = self._get_translation_instructions()
            prompt += translation_instructions
        
        # Add reading order instructions based on configuration
        reading_order = getattr(config, 'READING_ORDER', '')
        if reading_order == 'right-to-left':
            spatial_instructions = """

CRITICAL SPATIAL INSTRUCTIONS FOR MANGA:
- The page flows from RIGHT to LEFT, TOP to BOTTOM
- Panel 1 is at the TOP-RIGHT corner
- Panel 2 is to the LEFT of Panel 1
- Continue LEFT across the top row
- Drop down to the next row and start again from the RIGHT
- Within each panel, speech bubbles follow RIGHT-TO-LEFT flow
- Vertical text reads TOP-TO-BOTTOM
- Pay attention to panel borders and speech bubble tails to determine reading sequence

Please number and extract text in this precise order, indicating the spatial position of each text element."""
            
            prompt += spatial_instructions
        
        return prompt
    
    def _get_translation_instructions(self) -> str:
        """Get translation instructions based on configuration."""
        if not getattr(config, 'ENABLE_TRANSLATION', False):
            return ""
        
        source_lang = getattr(config, 'SOURCE_LANGUAGE', 'Chinese') or 'Chinese'
        target_lang = getattr(config, 'TARGET_LANGUAGE', 'English') or 'English'
        translation_mode = getattr(config, 'TRANSLATION_MODE', 'inline') or 'inline'
        translation_style = getattr(config, 'TRANSLATION_STYLE', 'natural') or 'natural'
        preserve_original = getattr(config, 'PRESERVE_ORIGINAL', True)
        
        instructions = f"""

TRANSLATION INSTRUCTIONS:
- Translate all extracted {source_lang} text to {target_lang}
- Translation style: {translation_style}
- Preserve original text: {'Yes' if preserve_original else 'No'}
- Output mode: {translation_mode}

Translation Guidelines:
- For 'natural' style: Provide fluent, contextual translations
- For 'literal' style: Stay close to original meaning and structure
- For 'localized' style: Adapt cultural references and idioms
- Maintain the emotional tone and character personality
- Keep sound effects descriptive but culturally appropriate"""

        if translation_mode == 'inline':
            instructions += """

OUTPUT FORMAT (Inline):
Panel X: [Original text] → [Translation]"""
        elif translation_mode == 'separate':
            instructions += """

OUTPUT FORMAT (Separate):
=== ORIGINAL TEXT ===
[All original text in reading order]

=== ENGLISH TRANSLATION ===
[All translations in same order]"""
        elif translation_mode == 'both':
            instructions += """

OUTPUT FORMAT (Both):
=== DETAILED EXTRACTION ===
Panel X: [Original] → [Translation]

=== ORIGINAL TEXT ONLY ===
[All original text]

=== TRANSLATIONS ONLY ===
[All translations]"""
        
        return instructions
    
    def _save_api_response(self, response_text: str, image_path: str) -> None:
        """Save API response for debugging purposes."""
        if not getattr(config, 'SAVE_API_RESPONSES', False):
            return
            
        try:
            script_dir = getattr(config, 'SCRIPT_DIR', os.path.dirname(__file__))
            response_file = os.path.join(script_dir, f"response_{os.path.basename(image_path)}.txt")
            with open(response_file, 'w', encoding='utf-8') as f:
                f.write(response_text)
        except Exception as e:
            self.logger.warning(f"Failed to save API response: {e}")
    
    def extract_text_from_image(self, image_path: str) -> Optional[str]:
        """Extract text from a single image using Gemini."""
        try:
            # Preprocess image
            img = self.preprocess_image(image_path)
            if img is None:
                return None
            
            # Get the appropriate prompt
            prompt = self._get_ocr_prompt()
            
            self.logger.info(f"Processing image: {os.path.basename(image_path)}")
            
            # Generate content with Gemini
            response = self.model.generate_content([prompt, img])
            
            # Add delay to respect rate limits
            delay = getattr(config, 'REQUEST_DELAY', 1.0)
            time.sleep(delay)
            
            if response.text:
                self.processed_count += 1
                self.logger.info(f"Successfully extracted text from {os.path.basename(image_path)}")
                
                # Save API response if debugging
                self._save_api_response(response.text, image_path)
                
                return response.text
            else:
                self.logger.warning(f"No text extracted from {os.path.basename(image_path)}")
                return None
                
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Error processing {image_path}: {e}")
            
            continue_on_error = getattr(config, 'CONTINUE_ON_ERROR', True)
            if not continue_on_error:
                raise
            return None
    
    def translate_text(self, text: str, source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> Optional[str]:
        """Translate extracted text using Gemini."""
        if not getattr(config, 'ENABLE_TRANSLATION', False):
            return None
        
        source_lang = source_lang or getattr(config, 'SOURCE_LANGUAGE', 'Chinese') or 'Chinese'
        target_lang = target_lang or getattr(config, 'TARGET_LANGUAGE', 'English') or 'English'
        translation_style = getattr(config, 'TRANSLATION_STYLE', 'natural') or 'natural'
        
        translation_prompt = f"""Translate the following {source_lang} text to {target_lang}.

Translation style: {translation_style}
- For 'natural': Provide fluent, contextual translations
- For 'literal': Stay close to original meaning  
- For 'localized': Adapt cultural references

Text to translate:
{text}

Provide only the translation, maintaining the original formatting and structure."""
        
        try:
            response = self.model.generate_content(translation_prompt)
            
            # Add delay to respect rate limits
            delay = getattr(config, 'REQUEST_DELAY', 1.0)
            time.sleep(delay)
            
            if response.text:
                self.logger.info("Successfully translated text")
                return response.text.strip()
            else:
                self.logger.warning("No translation generated")
                return None
                
        except Exception as e:
            self.logger.error(f"Error translating text: {e}")
            return None
    
    def get_image_files(self, folder_path: str) -> List[str]:
        """Get all supported image files from the folder."""
        folder = Path(folder_path)
        if not folder.exists():
            self.logger.error(f"Folder not found: {folder_path}")
            return []
            
        image_files = []
        supported_extensions = getattr(config, 'SUPPORTED_EXTENSIONS', ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'])
        
        for ext in supported_extensions:
            # Check both lowercase and uppercase extensions
            for case_ext in [ext.lower(), ext.upper()]:
                pattern = f"*{case_ext}"
                image_files.extend(folder.glob(pattern))
        
        # Sort files naturally and convert to strings
        image_files = sorted([str(f) for f in set(image_files)])
        self.logger.info(f"Found {len(image_files)} image files")
        return image_files
    
    def format_output(self, filename: str, text: str, page_number: int) -> str:
        """Format the extracted text for output."""
        output_parts = []
        
        # Page separator
        if getattr(config, 'SEPARATE_PAGES', True) and page_number > 1:
            output_parts.append("\n" + "="*80)
        
        # File information
        if getattr(config, 'INCLUDE_FILENAME', True):
            output_parts.append(f"File: {filename}")
        
        if getattr(config, 'ADD_PAGE_NUMBERS', True):
            output_parts.append(f"Page: {page_number}")
        
        if getattr(config, 'INCLUDE_TIMESTAMP', False):
            output_parts.append(f"Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Content separator and text
        output_parts.append("-"*40)
        output_parts.append(text)
        
        return "\n".join(output_parts) + "\n"
    
    def _create_output_header(self, total_images: int) -> str:
        """Create the header for the output file."""
        return (
            f"Manga OCR Results - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Model: {config.GEMINI_MODEL}\n"
            f"Total Images Processed: {total_images}\n"
            f"Successful Extractions: {self.processed_count}\n"
            f"Errors: {self.error_count}\n"
            f"{'='*80}\n\n"
        )
    
    def _save_results(self, all_text: List[str], total_images: int) -> bool:
        """Save the OCR results to the output file."""
        try:
            with open(config.OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(self._create_output_header(total_images))
                f.write("\n".join(all_text))
            return True
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")
            return False

    def process_manga_folder(self, folder_path: Optional[str] = None) -> bool:
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
        
        return self._process_images(image_files)
    
    def _process_images(self, image_files: List[str]) -> bool:
        """Process the list of image files."""
        self.logger.info(f"Starting OCR processing of {len(image_files)} images...")
        
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
        
        return self._finalize_processing(all_text, len(image_files), start_time)
    
    def _finalize_processing(self, all_text: List[str], total_images: int, start_time: float) -> bool:
        """Finalize the processing and save results."""
        if not all_text:
            self.logger.warning("No text was extracted from any images")
            return False
        
        # Save results
        if not self._save_results(all_text, total_images):
            return False
        
        # Log completion statistics
        end_time = time.time()
        processing_time = end_time - start_time
        
        self.logger.info(f"OCR processing completed!")
        self.logger.info(f"Results saved to: {config.OUTPUT_FILE}")
        self.logger.info(f"Processing time: {processing_time:.2f} seconds")
        self.logger.info(f"Successfully processed: {self.processed_count}/{total_images} images")
        
        if self.error_count > 0:
            self.logger.warning(f"Errors encountered: {self.error_count}")
        
        return True

def main():
    """Main function to run the OCR process."""
    try:
        # Validate configuration before starting
        if hasattr(config, 'validate_config'):
            config.validate_config()
        
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
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n📋 Setup checklist:")
        print("1. Set your GOOGLE_API_KEY in config.py or as environment variable")
        print("2. Create an 'images' folder with your manga files")
        print("3. Install required packages: pip install google-generativeai Pillow")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.error(f"Fatal error in main: {e}")

if __name__ == "__main__":
    main()
