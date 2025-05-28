"""
Dedicated script to test and optimize manga reading order detection.
"""

import sys
import os
from pathlib import Path

try:
    import config
    from gemini_ocr import GeminiMangaOCR
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_reading_orders():
    """Test different reading order configurations."""
    
    print("🔍 Testing Manga Reading Order Configurations")
    print("=" * 60)
    
    # Get first image for testing
    ocr = GeminiMangaOCR()
    image_files = ocr.get_image_files(config.IMAGE_FOLDER)
    
    if not image_files:
        print("❌ No images found in input folder")
        return
    
    test_image = image_files[0]
    filename = os.path.basename(test_image)
    print(f"📖 Testing with: {filename}")
    
    # Test configurations
    test_configs = [
        {
            'name': 'Basic Manga',
            'prompt': 'japanese',
            'reading_order': 'right-to-left',
            'language': 'Japanese'
        },
        {
            'name': 'Precise Manga',
            'prompt': 'manga_precise',
            'reading_order': 'right-to-left', 
            'language': 'Japanese'
        },
        {
            'name': 'Structured Manga',
            'prompt': 'structured',
            'reading_order': 'right-to-left',
            'language': 'Japanese'
        }
    ]
    
    results = {}
    
    for test_config in test_configs:
        print(f"\n🧪 Testing: {test_config['name']}")
        
        # Set configuration
        config.DEFAULT_PROMPT = test_config['prompt']
        config.READING_ORDER = test_config['reading_order']
        config.MANGA_LANGUAGE = test_config['language']
        
        # Create new OCR instance with updated config
        test_ocr = GeminiMangaOCR()
        
        try:
            extracted_text = test_ocr.extract_text_from_image(test_image)
            
            if extracted_text:
                results[test_config['name']] = extracted_text
                print(f"   ✅ Success ({len(extracted_text)} characters)")
                
                # Save individual result
                output_file = config.OUTPUT_DIR / f"test_{test_config['name'].lower().replace(' ', '_')}_{filename}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"Reading Order Test: {test_config['name']}\n")
                    f.write(f"{'='*40}\n\n")
                    f.write(f"Configuration:\n")
                    f.write(f"- Prompt: {test_config['prompt']}\n")
                    f.write(f"- Reading Order: {test_config['reading_order']}\n")
                    f.write(f"- Language: {test_config['language']}\n\n")
                    f.write(f"Extracted Text:\n")
                    f.write(f"{'-'*30}\n\n")
                    f.write(extracted_text)
                    
            else:
                results[test_config['name']] = "No text extracted"
                print(f"   ❌ Failed")
                
        except Exception as e:
            results[test_config['name']] = f"Error: {e}"
            print(f"   ❌ Error: {e}")
    
    # Create comparison report
    comparison_file = config.OUTPUT_DIR / f"reading_order_comparison_{filename}.txt"
    with open(comparison_file, 'w', encoding='utf-8') as f:
        f.write(f"Manga Reading Order Comparison Report\n")
        f.write(f"{'='*60}\n\n")
        f.write(f"Test Image: {filename}\n")
        f.write(f"Generated: {os.path.basename(__file__)}\n\n")
        
        for name, result in results.items():
            f.write(f"\n{'='*40}\n")
            f.write(f"Configuration: {name}\n")
            f.write(f"{'='*40}\n\n")
            f.write(f"Result Preview (first 200 chars):\n")
            preview = result[:200] + "..." if len(result) > 200 else result
            f.write(f"{preview}\n\n")
            f.write(f"Full Length: {len(result)} characters\n")
    
    print(f"\n📊 Comparison Complete!")
    print(f"📄 Full comparison saved to: {comparison_file}")
    
    # Show best result
    if results:
        best_config = max(results.items(), key=lambda x: len(x[1]) if isinstance(x[1], str) else 0)
        print(f"\n🏆 Best Configuration: {best_config[0]}")
        print(f"   📝 Extracted {len(best_config[1])} characters")

def main():
    """Main function."""
    print("🔧 Manga Reading Order Test & Optimization")
    print("=" * 50)
    
    try:
        test_reading_orders()
        
        print(f"\n💡 Tips for better manga reading order:")
        print(f"   1. Use 'manga_precise' prompt for best spatial awareness")
        print(f"   2. Set READING_ORDER = 'right-to-left' in config")  
        print(f"   3. Set MANGA_LANGUAGE = 'Japanese' for Japanese manga")
        print(f"   4. Check the generated comparison files to see differences")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
