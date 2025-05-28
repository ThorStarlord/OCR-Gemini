import os
from pathlib import Path

# --- PROJECT STRUCTURE ---
# Base project directory
PROJECT_DIR = Path(__file__).parent
INPUT_DIR = PROJECT_DIR / "input"
OUTPUT_DIR = PROJECT_DIR / "output"
LOGS_DIR = OUTPUT_DIR / "logs"
DEBUG_DIR = OUTPUT_DIR / "debug"

# Create directories if they don't exist
for directory in [INPUT_DIR, OUTPUT_DIR, LOGS_DIR, DEBUG_DIR]:
    directory.mkdir(exist_ok=True)

# --- MANDATORY SETTINGS ---
# Your Google Gemini API Key.
# It's highly recommended to load this from an environment variable for security.
# Example: GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyD6ZJjkhA-XS_LtxcOFbsPdGNhbuuC6f7o")  # Replace with your actual API key

# Gemini Model to use (e.g., 'gemini-pro-vision', 'gemini-1.5-flash-latest', 'gemini-1.5-pro-latest')
# 'gemini-1.5-flash-latest' is generally faster and cheaper for OCR.
GEMINI_MODEL = 'gemini-1.5-flash-latest'

# Updated folder paths
IMAGE_FOLDER = str(INPUT_DIR)  # Input folder for manga images
OUTPUT_FILE = str(OUTPUT_DIR / 'extracted_manga_text.txt')  # Main output file

# Supported image file extensions (case-insensitive).
SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']

# --- OPTIONAL SETTINGS ---

# General Debugging and Logging
DEBUG_MODE = False  # Set to True for verbose logging (e.g., all debug messages)
VERBOSE_OUTPUT = True  # Print progress and results to console
SAVE_ERROR_LOG = True  # Save errors to a separate log file
ERROR_LOG_FILE = str(LOGS_DIR / 'ocr_errors.log')  # Error log in logs folder

# Image Preprocessing
ENABLE_IMAGE_PREPROCESSING = True  # Enable/disable all preprocessing
MAX_IMAGE_SIZE = (2048, 2048)  # Max dimensions for images (width, height)
ENHANCE_CONTRAST = True  # Apply contrast enhancement
CONTRAST_FACTOR = 1.3  # Factor for contrast enhancement (e.g., 1.0 is no change)
ENHANCE_SHARPNESS = True  # Apply sharpness enhancement
SHARPNESS_FACTOR = 1.3  # Factor for sharpness enhancement

# Debugging Image and API Responses (now in debug folder)
SAVE_PROCESSED_IMAGES = False  # Save preprocessed images to disk for inspection
SAVE_API_RESPONSES = False  # Save raw API responses to disk (for debugging model output)
SCRIPT_DIR = str(DEBUG_DIR)  # Debug files go in debug folder

# API Request Control
REQUEST_DELAY = 0.5  # Delay in seconds between API requests to avoid hitting rate limits
CONTINUE_ON_ERROR = True  # Continue processing other images even if one fails

# OCR Prompting
OCR_PROMPTS = {
    'basic': 'Extract all readable text from this image.',
    'japanese': '''This is a Japanese manga page. Extract all Japanese text accurately, including sound effects. 
Please do not translate, just transcribe. Pay close attention to the reading order which is typically 
right-to-left, top-to-bottom for panels, and then within bubbles/text blocks. If text is vertically 
aligned, extract it from top to bottom. If there are multiple speech bubbles or text areas, process 
them in the typical manga reading flow. Provide the text clearly separated for each distinct bubble 
or text block.''',
    'english': '''This is an English manga/comic page. Extract all English text accurately, including 
sound effects and dialogue. Follow the typical left-to-right, top-to-bottom reading order for panels 
and speech bubbles. Separate text from different bubbles or panels clearly.''',
    'detailed': '''Extract all text from this image with high accuracy. Preserve the original formatting 
and reading order. If this is a manga or comic, consider the typical reading flow. Include all text 
types: dialogue, narration, sound effects, and any other visible text.''',
    'structured': '''Extract text from this manga/comic page in a structured format:
1. First list all dialogue in speech bubbles in reading order
2. Then list all sound effects and onomatopoeia
3. Finally list any narration or text boxes
Label each section clearly.'''
}
DEFAULT_PROMPT = 'japanese'  # Choose which prompt to use ('basic', 'japanese', 'english', 'detailed', etc.)

# Manga Specific Settings
MANGA_LANGUAGE = 'Japanese'  # 'Japanese', 'English', etc. (Used by _get_ocr_prompt)
READING_ORDER = 'right-to-left'  # 'left-to-right' or 'right-to-left' (Used by _get_ocr_prompt)

# Output Formatting
SEPARATE_PAGES = True  # Add a separator between extracted text from different pages
INCLUDE_FILENAME = True  # Include the filename in the output for each page
ADD_PAGE_NUMBERS = True  # Add page numbers to the output
INCLUDE_TIMESTAMP = False  # Include a timestamp for each page's processing
IMAGE_QUALITY = 90  # Quality for saved processed images (if SAVE_PROCESSED_IMAGES is True)

# --- NEW FEATURES ---
# Batch processing settings
BATCH_SIZE = 10  # Process images in batches
PROGRESS_SAVE_INTERVAL = 5  # Save progress every N images

# Output options
SAVE_INDIVIDUAL_FILES = False  # Save each page as separate file
INDIVIDUAL_OUTPUT_DIR = str(OUTPUT_DIR / "individual_pages")
JSON_OUTPUT = False  # Also save results as JSON
JSON_OUTPUT_FILE = str(OUTPUT_DIR / 'extracted_text.json')

# Quality control
MIN_TEXT_LENGTH = 5  # Minimum characters to consider valid extraction
CONFIDENCE_THRESHOLD = 0.7  # For future confidence scoring

# --- VALIDATION ---
def validate_config():
    """Validate configuration settings and provide helpful error messages."""
    errors = []
    
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        errors.append("GOOGLE_API_KEY is not set. Please set it in config.py or as an environment variable.")
    
    if not os.path.exists(IMAGE_FOLDER):
        errors.append(f"IMAGE_FOLDER '{IMAGE_FOLDER}' does not exist. Please create it or update the path.")
    
    if DEFAULT_PROMPT not in OCR_PROMPTS:
        errors.append(f"DEFAULT_PROMPT '{DEFAULT_PROMPT}' is not defined in OCR_PROMPTS.")
    
    if errors:
        error_msg = "Configuration errors found:\n" + "\n".join(f"- {error}" for error in errors)
        raise ValueError(error_msg)

# Auto-validate when config is imported (optional - comment out if you prefer manual validation)
# validate_config()
