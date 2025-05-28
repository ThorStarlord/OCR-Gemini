"""
Script to create the complete project folder structure and setup files.
Run this once to set up your OCR project properly.
"""

import os
from pathlib import Path

def create_project_structure():
    """Create the complete project folder structure."""
    
    base_dir = Path(__file__).parent
    
    # Define folder structure
    folders = {
        'input': 'Place your manga images here',
        'output': 'OCR results will be saved here',
        'output/logs': 'Error logs and processing logs',
        'output/debug': 'Debug files (processed images, API responses)',
        'output/individual_pages': 'Individual page results (if enabled)',
        'output/backups': 'Backup files',
        'samples': 'Sample manga images for testing'
    }
    
    # Create folders and README files
    for folder_path, description in folders.items():
        full_path = base_dir / folder_path
        full_path.mkdir(parents=True, exist_ok=True)
        
        # Create README in each folder
        readme_path = full_path / 'README.md'
        if not readme_path.exists():
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# {folder_path.split('/')[-1].title()}\n\n")
                f.write(f"{description}\n\n")
                
                if 'input' in folder_path:
                    f.write("Supported formats: JPG, PNG, TIFF, BMP, WebP\n")
                    f.write("Recommended: High-resolution scans for better OCR accuracy\n")
                elif 'output' in folder_path:
                    f.write("This folder contains OCR processing results.\n")
        
        print(f"✅ Created: {folder_path}/")
    
    # Create sample config template
    create_config_template(base_dir)
    
    # Create startup scripts
    create_startup_scripts(base_dir)
    
    print("\n🎉 Project structure created successfully!")
    print("\n📁 Folder structure:")
    print("├── input/              # Place manga images here")
    print("├── output/             # OCR results")
    print("│   ├── logs/           # Processing logs")
    print("│   ├── debug/          # Debug files")
    print("│   ├── individual_pages/ # Per-page results")
    print("│   └── backups/        # Backup files")
    print("├── samples/            # Test images")
    print("└── scripts/            # Utility scripts")

def create_config_template(base_dir):
    """Create a config template file."""
    template_path = base_dir / 'config_template.py'
    
    if not template_path.exists():
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write('''# Configuration Template for Gemini Manga OCR
# Copy this to config.py and customize your settings

import os
from pathlib import Path

# --- REQUIRED: Set your API key ---
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"  # Get from https://aistudio.google.com/

# --- BASIC SETTINGS ---
GEMINI_MODEL = 'gemini-1.5-flash-latest'  # Fast and cost-effective
MANGA_LANGUAGE = 'Japanese'  # 'Japanese' or 'English'
DEFAULT_PROMPT = 'japanese'  # 'basic', 'japanese', 'english', 'detailed'

# --- PROCESSING OPTIONS ---
ENABLE_IMAGE_PREPROCESSING = True
ENHANCE_CONTRAST = True
ENHANCE_SHARPNESS = True
REQUEST_DELAY = 0.5  # Seconds between API calls

# --- OUTPUT OPTIONS ---
SAVE_INDIVIDUAL_FILES = False  # Save each page separately
INCLUDE_TIMESTAMP = False
DEBUG_MODE = False  # Enable for troubleshooting
''')
        print(f"✅ Created: config_template.py")

def create_startup_scripts(base_dir):
    """Create utility scripts for easy project management."""
    scripts_dir = base_dir / 'scripts'
    scripts_dir.mkdir(exist_ok=True)
    
    # Quick start script
    quick_start = scripts_dir / 'quick_start.py'
    with open(quick_start, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python3
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
''')
    
    # Cleanup script
    cleanup = scripts_dir / 'cleanup.py'
    with open(cleanup, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python3
"""
Cleanup script to clear output folders.
"""

import os
import shutil
from pathlib import Path

def cleanup_outputs():
    """Clean up output folders."""
    base_dir = Path(__file__).parent.parent
    
    folders_to_clean = [
        base_dir / 'output' / 'logs',
        base_dir / 'output' / 'debug',
        base_dir / 'output' / 'individual_pages'
    ]
    
    for folder in folders_to_clean:
        if folder.exists():
            for file in folder.glob('*'):
                if file.is_file():
                    file.unlink()
            print(f"🧹 Cleaned: {folder}")
    
    # Keep main output files but move to backup
    main_output = base_dir / 'output' / 'extracted_manga_text.txt'
    if main_output.exists():
        backup_dir = base_dir / 'output' / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f'extracted_manga_text_{timestamp}.txt'
        shutil.move(str(main_output), str(backup_path))
        print(f"📦 Backed up main output to: {backup_path}")

if __name__ == "__main__":
    cleanup_outputs()
    print("✅ Cleanup complete!")
''')
    
    print(f"✅ Created utility scripts in scripts/")

def main():
    """Main function."""
    print("🔧 Setting up Gemini Manga OCR Project Structure")
    print("=" * 50)
    
    create_project_structure()
    
    print(f"\n📋 Next steps:")
    print(f"1. Copy config_template.py to config.py")
    print(f"2. Set your GOOGLE_API_KEY in config.py")
    print(f"3. Add manga images to the input/ folder")
    print(f"4. Run: python gemini_ocr.py")
    print(f"5. Or run: python scripts/quick_start.py")

if __name__ == "__main__":
    main()
