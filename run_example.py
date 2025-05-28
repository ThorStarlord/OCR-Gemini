"""
Example script demonstrating how to use the Gemini Manga OCR system.
This script shows different ways to use the OCR functionality.
"""

import os
import config
from gemini_ocr import GeminiMangaOCR

def example_basic_usage():
    """Example of basic OCR usage."""
    print("=== Basic OCR Example ===")
    
    # Create OCR instance
    ocr = GeminiMangaOCR()
    
    # Process all images in the current folder
    success = ocr.process_manga_folder()
    
    if success:
        print("✅ OCR completed successfully!")
        print(f"📄 Check results in: {config.OUTPUT_FILE}")
    else:
        print("❌ OCR failed")

def example_single_image():
    """Example of processing a single image."""
    print("\n=== Single Image OCR Example ===")
    
    # Find the first image file in the folder
    ocr = GeminiMangaOCR()
    image_files = ocr.get_image_files(config.IMAGE_FOLDER)
    
    if not image_files:
        print("No image files found in the folder")
        return
    
    # Process just the first image
    first_image = image_files[0]
    print(f"Processing single image: {os.path.basename(first_image)}")
    
    extracted_text = ocr.extract_text_from_image(first_image)
    
    if extracted_text:
        print("✅ Text extracted successfully!")
        print("📄 Extracted text:")
        print("-" * 40)
        print(extracted_text)
        print("-" * 40)
    else:
        print("❌ No text extracted")

def example_custom_config():
    """Example of using custom configuration."""
    print("\n=== Custom Configuration Example ===")
    
    # Temporarily modify config for this example
    original_prompt = config.DEFAULT_PROMPT
    original_enhance = config.ENHANCE_CONTRAST
    
    # Use structured output format
    config.DEFAULT_PROMPT = 'structured'
    config.ENHANCE_CONTRAST = True
    
    print(f"Using prompt style: {config.DEFAULT_PROMPT}")
    print(f"Contrast enhancement: {config.ENHANCE_CONTRAST}")
    
    # Process images
    ocr = GeminiMangaOCR()
    success = ocr.process_manga_folder()
    
    # Restore original config
    config.DEFAULT_PROMPT = original_prompt
    config.ENHANCE_CONTRAST = original_enhance
    
    if success:
        print("✅ Custom OCR completed!")
    else:
        print("❌ Custom OCR failed")

def example_error_handling():
    """Example of proper error handling."""
    print("\n=== Error Handling Example ===")
    
    try:
        # Create OCR instance
        ocr = GeminiMangaOCR()
        
        # Try to process a non-existent folder
        fake_folder = os.path.join(config.SCRIPT_DIR, "non_existent_folder")
        success = ocr.process_manga_folder(fake_folder)
        
        if not success:
            print("Expected failure for non-existent folder handled correctly")
        
        # Process the real folder
        print("Now processing the actual image folder...")
        success = ocr.process_manga_folder()
        
        if success:
            print("✅ Real processing completed successfully!")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("This shows how to handle exceptions properly")

def main():
    """Run all examples."""
    print("Gemini Manga OCR - Examples")
    print("=" * 50)
    
    # Check if API key is set
    if not config.GOOGLE_API_KEY:
        print("❌ GOOGLE_API_KEY not found!")
        print("Please set your API key in config.py or as an environment variable")
        print("Example: set GOOGLE_API_KEY=your_api_key_here")
        return
    
    print(f"Using Gemini model: {config.GEMINI_MODEL}")
    print(f"Image folder: {config.IMAGE_FOLDER}")
    print(f"Output file: {config.OUTPUT_FILE}")
    print()
    
    # Run examples
    try:
        # Example 1: Basic usage
        example_basic_usage()
        
        # Example 2: Single image (commented out to avoid duplicate processing)
        # example_single_image()
        
        # Example 3: Custom configuration (commented out to avoid overwriting results)
        # example_custom_config()
        
        # Example 4: Error handling
        example_error_handling()
        
        print("\n🎉 All examples completed!")
        print(f"📄 Check your results in: {config.OUTPUT_FILE}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
```
