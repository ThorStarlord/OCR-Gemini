"""
Example setup script to help users get started with the OCR system.
Run this script to create example folders and check your configuration.
"""

import os
import sys
from pathlib import Path

def create_example_structure():
    """Create example folder structure for the OCR system."""
    
    # Check the new folder structure
    folders_to_check = [
        ("input", "Place your manga image files here"),
        ("output", "OCR results will be saved here"),
        ("output/logs", "Processing logs and errors"),
        ("output/debug", "Debug files (processed images, API responses)"),
        ("output/individual_pages", "Individual page results (if enabled)"),
    ]
    
    for folder_path, description in folders_to_check:
        folder = Path(folder_path)
        if folder.exists():
            print(f"✅ '{folder}' folder exists - {description}")
        else:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created '{folder}' folder - {description}")
    
    # Check for image files in input folder
    input_folder = Path("input")
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_folder.glob(f"*{ext}"))
        image_files.extend(input_folder.glob(f"*{ext.upper()}"))
    
    if image_files:
        print(f"✅ Found {len(image_files)} image files in input folder")
        for img in image_files[:3]:  # Show first 3 files
            print(f"   📷 {img.name}")
        if len(image_files) > 3:
            print(f"   ... and {len(image_files) - 3} more files")
    else:
        print(f"⚠️  No image files found in input folder")
        print("   📷 Add some manga images to input/ folder to get started")

def test_gemini_api():
    """Test if the Gemini API is working."""
    try:
        import config
        api_key = getattr(config, 'GOOGLE_API_KEY', '')
        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            print("⚠️  Cannot test API - API key not configured")
            return False
        
        import google.generativeai as genai
        
        # Test API configuration
        genai.configure(api_key=api_key)
        
        # Try to create a model instance
        model_name = getattr(config, 'GEMINI_MODEL', 'gemini-1.5-flash')
        model = genai.GenerativeModel(model_name)
        print("✅ Gemini API connection successful")
        print(f"   📡 Using model: {model_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        print("   🔑 Check your API key and internet connection")
        return False

def check_config():
    """Check if config.py exists and is properly configured."""
    try:
        import config
        print("✅ config.py found and imported successfully")
        
        # Check API key
        api_key = getattr(config, 'GOOGLE_API_KEY', '')
        if api_key and api_key != "YOUR_GEMINI_API_KEY_HERE":
            print("✅ API key appears to be configured")
        else:
            print("⚠️  API key not configured in config.py")
            print("   🔑 Set GOOGLE_API_KEY in config.py or as environment variable")
        
        # Check required settings
        required_settings = ['GEMINI_MODEL', 'IMAGE_FOLDER', 'OUTPUT_FILE', 'SUPPORTED_EXTENSIONS']
        for setting in required_settings:
            if hasattr(config, setting):
                print(f"✅ {setting} configured")
            else:
                print(f"❌ {setting} missing from config.py")
                
    except ImportError:
        print("❌ config.py not found")
        print("   📝 Create config.py with your settings")
        return False
    
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = {
        'google.generativeai': 'google-generativeai',
        'PIL': 'Pillow'
    }
    
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
            if module == 'google.generativeai':
                # Special handling for google.generativeai
                import google.generativeai as genai
                # Test if configure is available
                if hasattr(genai, 'configure'):
                    print(f"✅ {package} is installed and working")
                else:
                    print(f"⚠️  {package} installed but configure function not found")
                    print("   📦 Try: pip install --upgrade google-generativeai")
            else:
                __import__(module)
                print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_project_structure():
    """Check if the project structure is properly set up."""
    print("\n📁 Checking project structure...")
    
    required_files = [
        "config.py",
        "gemini_ocr.py", 
        "requirements.txt",
        "README.md"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
    
    # Check folder structure
    required_folders = ["input", "output", "output/logs", "output/debug"]
    for folder in required_folders:
        if Path(folder).exists():
            print(f"✅ {folder}/ folder exists")
        else:
            print(f"❌ {folder}/ folder missing")

def provide_next_steps():
    """Provide clear next steps for the user."""
    print(f"\n{'='*60}")
    print("🎯 NEXT STEPS")
    print(f"{'='*60}")
    
    # Check what's ready
    has_images = len(list(Path("input").glob("*.*"))) > 0
    has_config = Path("config.py").exists()
    
    if not has_config:
        print("1. 📝 Create config.py with your API key")
        print("   Copy from config_template.py or use the existing config.py")
        return
    
    if not has_images:
        print("1. 📷 Add manga images to the input/ folder")
        print("   Supported formats: JPG, PNG, TIFF, BMP, WebP")
        print("\n2. 🚀 Run your first OCR:")
        print("   python gemini_ocr.py")
        return
    
    # Everything looks ready
    print("🎉 Everything looks ready! Here's what you can do:")
    print("\n📚 Basic Usage:")
    print("   python gemini_ocr.py")
    print("   (Processes all images in input/ folder)")
    
    print("\n🧪 Try Examples:")
    print("   python run_example.py")
    print("   (Demonstrates different OCR features)")
    
    print("\n⚙️  Customize Settings:")
    print("   Edit config.py to:")
    print("   - Change language (Japanese/English)")
    print("   - Adjust image processing")
    print("   - Modify output format")
    
    print("\n📊 Check Results:")
    print("   - Main results: output/extracted_manga_text.txt")
    print("   - Logs: output/logs/ocr_errors.log")
    print("   - Debug files: output/debug/ (if enabled)")

def main():
    """Run the setup check."""
    print("🔧 OCR-Gemini Setup Check & Next Steps")
    print("=" * 50)
    
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n📝 Checking configuration...")
    config_ok = check_config()
    
    check_project_structure()
    
    print("\n📁 Setting up folder structure...")
    create_example_structure()
    
    if deps_ok and config_ok:
        print("\n🧪 Testing Gemini API connection...")
        api_ok = test_gemini_api()
    else:
        api_ok = False
    
    # Provide next steps
    provide_next_steps()
    
    print(f"\n{'='*50}")
    if deps_ok and config_ok and api_ok:
        print("🎉 Setup complete! Ready to start OCR processing!")
    else:
        print("⚠️  Please fix the issues above before proceeding")

if __name__ == "__main__":
    main()
