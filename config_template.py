# Configuration Template for Gemini Manga OCR
# Copy this to config.py and customize your settings

import os
from pathlib import Path

# --- REQUIRED: Set your API key ---
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"  # Get from https://aistudio.google.com/

# --- BASIC SETTINGS ---
GEMINI_MODEL = 'gemini-1.5-flash-latest'  # Fast and cost-effective
MANGA_LANGUAGE = 'English'  # 'Japanese' or 'English'
DEFAULT_PROMPT = 'English'  # 'basic', 'japanese', 'english', 'detailed'

# --- PROCESSING OPTIONS ---
ENABLE_IMAGE_PREPROCESSING = True
ENHANCE_CONTRAST = True
ENHANCE_SHARPNESS = True
REQUEST_DELAY = 0.5  # Seconds between API calls

# --- OUTPUT OPTIONS ---
SAVE_INDIVIDUAL_FILES = False  # Save each page separately
INCLUDE_TIMESTAMP = False
DEBUG_MODE = False  # Enable for troubleshooting
