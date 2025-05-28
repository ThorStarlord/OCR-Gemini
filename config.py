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
    # BASIC PROMPT - Simple and fast
    'basic': 'Extract all readable text from this image.',
    # Use this when: You want quick, simple text extraction without special formatting
    # Best for: Simple images, testing, or when you don't need structured output
    
    # JAPANESE MANGA PROMPT - Optimized for traditional manga layout
    'japanese': '''This is a Japanese manga page. Extract all Japanese text accurately, including sound effects and dialogue. 

IMPORTANT READING ORDER: Follow the traditional Japanese manga reading pattern:
1. Start from the TOP-RIGHT panel and move LEFT across the page
2. Within each panel, read speech bubbles from RIGHT to LEFT, TOP to BOTTOM
3. For vertical text, read from TOP to BOTTOM
4. Move down to the next row of panels and repeat

Please extract text in this exact reading order and clearly label each panel/bubble. Format like this:
Panel 1 (top-right): [dialogue/text]
Panel 2 (top-left): [dialogue/text]
Panel 3 (middle-right): [dialogue/text]
And so on...

Include ALL text: dialogue, thoughts, sound effects, and narration.''',
    # Use this when: Processing traditional Japanese manga
    # Best for: Right-to-left manga with complex panel layouts
    # Features: Panel numbering, reading order guidance, includes sound effects
    
    # ENGLISH COMIC PROMPT - Optimized for Western comics/manga
    'english': '''This is an English manga/comic page. Extract all English text accurately, including 
sound effects and dialogue. Follow the typical left-to-right, top-to-bottom reading order for panels 
and speech bubbles. Separate text from different bubbles or panels clearly.''',
    # Use this when: Processing English comics, webtoons, or English-translated manga
    # Best for: Left-to-right reading order, Western comic layouts
    # Features: Left-to-right panel flow, clear bubble separation
    
    # DETAILED PROMPT - Comprehensive extraction with formatting preservation
    'detailed': '''Extract all text from this image with high accuracy. Preserve the original formatting 
and reading order. If this is a manga or comic, consider the typical reading flow. Include all text 
types: dialogue, narration, sound effects, and any other visible text.''',
    # Use this when: You need maximum text extraction with formatting
    # Best for: Complex pages, mixed content, preserving layout information
    # Features: Format preservation, comprehensive text types, adaptive to content
    
    # STRUCTURED PROMPT - Organized output by content type
    'structured': '''Extract text from this manga/comic page in a structured format following RIGHT-TO-LEFT, TOP-TO-BOTTOM reading order:

1. PANELS: Number panels from top-right to bottom-left
2. DIALOGUE: Extract speech bubbles in proper manga reading order (right-to-left within panels)
3. SOUND EFFECTS: List all onomatopoeia and sound effects with their positions
4. NARRATION: Any text boxes or narrative elements

Format example:
=== PANEL 1 (Top-Right) ===
Dialogue: "Text here"
Sound Effect: *CRASH*

=== PANEL 2 (Top-Left) ===
Dialogue: "Next text"

Continue in proper manga reading order...''',
    # Use this when: You want organized output separated by content type
    # Best for: Analysis, translation work, detailed study of manga structure
    # Features: Content categorization, clear organization, position tracking

    # MANGA PRECISE PROMPT - Most detailed spatial awareness (DEFAULT)
    'manga_precise': '''You are reading a Japanese manga page. Extract ALL text following the traditional Japanese reading pattern:

SPATIAL READING RULES:
- Start at TOP-RIGHT corner of the page
- Move LEFT across each row of panels  
- Within each panel: read RIGHT-TO-LEFT, TOP-TO-BOTTOM
- For speech bubbles: follow the flow from right to left
- For vertical text: read from top to bottom
- Include panel transitions and page flow

OUTPUT FORMAT:
Panel Position: [Description of location]
Speaker/Type: [Character name or "Narration" or "Sound Effect"]
Text: [Exact transcription]

Be very precise about the reading order and spatial relationships.'''
    # Use this when: You need the most accurate manga reading order (RECOMMENDED)
    # Best for: Professional manga processing, accurate text extraction
    # Features: Precise spatial instructions, speaker identification, exact positioning
}

# CURRENT DEFAULT - Choose based on your manga type:

# FOR ORIGINAL JAPANESE MANGA (right-to-left reading):
DEFAULT_PROMPT = 'detailed'  # ← RECOMMENDED for Japanese manga
# Alternative: DEFAULT_PROMPT = 'structured'  # If you want organized output

# FOR ENGLISH TRANSLATED MANGA (still right-to-left layout):
# DEFAULT_PROMPT = 'detailed'  # ← RECOMMENDED for English translations
# Alternative: DEFAULT_PROMPT = 'structured'  # If you want categorized output

# Manga Specific Settings - UPDATE THESE BASED ON YOUR CONTENT:

# For Original Japanese Manga:
MANGA_LANGUAGE = 'English'
READING_ORDER = 'right-to-left'

# For English Translated Manga (uncomment these instead):
# MANGA_LANGUAGE = 'English'
# READING_ORDER = 'right-to-left'  # Keep this since layout is still right-to-left

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
