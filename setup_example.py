"""
Example setup script to help users get started with the OCR system.
Run this script to create example folders and check your configuration.
"""

import os
import sys
from pathlib import Path

def create_example_structure():
    """Create example folder structure for the OCR system."""
    
    # Create images folder if it doesn't exist
    images_folder = Path("images")
    if not images_folder.exists():
        images_folder.mkdir()
        print(f"✅ Created '{images_folder}' folder")
        print("   📁 Place your manga image files in this folder")
    else:
        print(f"✅ '{images_folder}' folder already exists")
    
    # Check for image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(images_folder.glob(f"*{ext}"))
        image_files.extend(images_folder.glob(f"*{ext.upper()}"))
    
    if image_files:
        print(f"✅ Found {len(image_files)} image files in '{images_folder}'")
    else:
        print(f"⚠️  No image files found in '{images_folder}'")
        print("   📷 Add some manga images to get started")

def check_config():
    """Check if config.py exists and is properly configured."""
    try:
        import config
        print("✅ config.py found and imported successfully")
        
        # Check API key
        if hasattr(config, 'GOOGLE_API_KEY'):
            if config.GOOGLE_API_KEY and config.GOOGLE_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
                print("✅ API key appears to be configured")
            else:
                print("⚠️  API key not configured in config.py")
                print("   🔑 Set GOOGLE_API_KEY in config.py or as environment variable")
        else:
            print("❌ GOOGLE_API_KEY not found in config.py")
        
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

def test_gemini_api():
    """Test if the Gemini API is working."""
    try:
        import config
        if not hasattr(config, 'GOOGLE_API_KEY') or config.GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            print("⚠️  Cannot test API - API key not configured")
            return False
        
        import google.generativeai as genai
        
        # Test API configuration
        genai.configure(api_key=config.GOOGLE_API_KEY)
        
        # Try to create a model instance
        model = genai.GenerativeModel(getattr(config, 'GEMINI_MODEL', 'gemini-1.5-flash'))
        print("✅ Gemini API connection successful")
        print(f"   📡 Using model: {getattr(config, 'GEMINI_MODEL', 'gemini-1.5-flash')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        print("   🔑 Check your API key and internet connection")
        return False

def main():
    """Run the setup check."""
    print("🔧 OCR-Gemini Setup Check")
    print("=" * 40)
    
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n📝 Checking configuration...")
    config_ok = check_config()
    
    print("\n📁 Setting up folder structure...")
    create_example_structure()
    
    if deps_ok and config_ok:
        print("\n🧪 Testing Gemini API connection...")
        api_ok = test_gemini_api()
    else:
        api_ok = False
    
    print("\n" + "=" * 40)
    if deps_ok and config_ok and api_ok:
        print("🎉 Setup looks good! You can now run:")
        print("   python gemini_ocr.py")
    else:
        print("⚠️  Please fix the issues above before running the OCR system")
        print("\n📋 Quick fixes:")
        if not deps_ok:
            print("   pip install google-generativeai Pillow")
        if not config_ok:
            print("   Create config.py with your API key")
        if not api_ok and deps_ok and config_ok:
            print("   Check your GOOGLE_API_KEY is valid")

if __name__ == "__main__":
    main()
