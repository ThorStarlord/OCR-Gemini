#!/usr/bin/env python3
"""
Quick start script for OCR processing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from gemini_ocr import GeminiMangaOCR
import config

def main():
    print("🚀 Quick Start OCR Processing")
    print("=" * 40)
    
    # Check if images exist
    import os
    if not os.listdir(config.IMAGE_FOLDER):
        print(f"⚠️  No images found in {config.IMAGE_FOLDER}")
        print("Please add some manga images to the input folder.")
        return
    
    # Run OCR
    ocr = GeminiMangaOCR()
    success = ocr.process_manga_folder()
    
    if success:
        print(f"✅ Processing complete! Check {config.OUTPUT_FILE}")
    else:
        print("❌ Processing failed. Check the logs for details.")

if __name__ == "__main__":
    main()
