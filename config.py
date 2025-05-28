import os

# --- Gemini API Configuration ---

# Google API Key - Set this as an environment variable GOOGLE_API_KEY
# Or set it directly here (not recommended for production)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Gemini model to use
# Options: 'gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro'
GEMINI_MODEL = 'gemini-2.0-flash-exp'

# --- File and Directory Configuration ---

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Input folder for manga images
IMAGE_FOLDER = SCRIPT_DIR

# Output file for extracted text
OUTPUT_FILE_NAME = 'extracted_manga_text_gemini.txt'
OUTPUT_FILE = os.path.join(SCRIPT_DIR, OUTPUT_FILE_NAME)

# Supported image extensions
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif', '.webp')

# --- OCR Configuration ---

# Language settings for manga
MANGA_LANGUAGE = 'English'  # Change to 'Japanese' for Japanese manga
READING_ORDER = 'right-to-left'  # 'right-to-left' for manga, 'left-to-right' for western comics

# OCR prompts for different scenarios
OCR_PROMPTS = {
    'basic': "Extract all text from this manga page image. Return only the text content without descriptions.",
    'detailed': "Carefully extract all text from this manga page including dialogue, sound effects, and any written text. Preserve the reading order and format the output clearly.",
    'structured': "Extract text from this manga page and organize it as follows:\n- Dialogue: [character dialogue]\n- Sound effects: [onomatopoeia and sound effects]\n- Other text: [signs, captions, etc.]",
    'japanese': "この漫画ページから全てのテキストを抽出してください。対話、効果音、その他の文字を含めて、読み順を保って明確に整理してください。"
}

# Default prompt to use
DEFAULT_PROMPT = 'detailed'

# --- Image Processing Configuration ---

# Image preprocessing options
ENABLE_IMAGE_PREPROCESSING = True
MAX_IMAGE_SIZE = (1920, 1920)  # Resize large images to this max size
IMAGE_QUALITY = 95  # JPEG quality when saving processed images
SAVE_PROCESSED_IMAGES = False  # Save preprocessed images for debugging

# Image enhancement options
ENHANCE_CONTRAST = True
ENHANCE_SHARPNESS = True
CONTRAST_FACTOR = 1.2
SHARPNESS_FACTOR = 1.1

# --- Output Configuration ---

# Output formatting options
INCLUDE_FILENAME = True
INCLUDE_TIMESTAMP = True
SEPARATE_PAGES = True  # Add separators between different pages
ADD_PAGE_NUMBERS = True

# Error handling
CONTINUE_ON_ERROR = True  # Continue processing other images if one fails
SAVE_ERROR_LOG = True
ERROR_LOG_FILE = os.path.join(SCRIPT_DIR, 'gemini_ocr_errors.log')

# --- Performance Configuration ---

# API rate limiting
MAX_REQUESTS_PER_MINUTE = 60
REQUEST_DELAY = 1.0  # Seconds between requests

# Parallel processing
ENABLE_PARALLEL_PROCESSING = False  # Set to True for faster processing (if API limits allow)
MAX_WORKERS = 3

# --- Debugging Configuration ---

# Debug options
DEBUG_MODE = False
VERBOSE_OUTPUT = True
SAVE_API_RESPONSES = False  # Save raw API responses for debugging
```
