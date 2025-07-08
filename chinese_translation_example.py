"""
Dedicated script to test Chinese to English translation functionality.
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

def test_translation_modes():
    """Test different translation modes and styles."""
    
    print("🔤 Testing Chinese Translation Modes")
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
            'name': 'Chinese Extraction Only',
            'prompt': 'chinese',
            'translation': False,
            'mode': 'none',
            'style': 'natural'
        },
        {
            'name': 'Chinese with Inline Translation',
            'prompt': 'chinese_translate',
            'translation': True,
            'mode': 'inline',
            'style': 'natural'
        },
        {
            'name': 'Chinese with Separate Translation',
            'prompt': 'chinese_translate', 
            'translation': True,
            'mode': 'separate',
            'style': 'natural'
        },
        {
            'name': 'Chinese Literal Translation',
            'prompt': 'chinese_translate',
            'translation': True,
            'mode': 'inline',
            'style': 'literal'
        }
    ]
    
    results = {}
    
    for test_config in test_configs:
        print(f"\n🧪 Testing: {test_config['name']}")
        
        # Set configuration
        config.DEFAULT_PROMPT = test_config['prompt']
        config.MANGA_LANGUAGE = 'Chinese'
        config.READING_ORDER = 'right-to-left'
        config.ENABLE_TRANSLATION = test_config['translation']
        config.TRANSLATION_MODE = test_config['mode']
        config.TRANSLATION_STYLE = test_config['style']
        config.SOURCE_LANGUAGE = 'Chinese'
        config.TARGET_LANGUAGE = 'English'
        
        # Create new OCR instance with updated config
        test_ocr = GeminiMangaOCR()
        
        try:
            extracted_text = test_ocr.extract_text_from_image(test_image)
            
            if extracted_text:
                results[test_config['name']] = extracted_text
                print(f"   ✅ Success ({len(extracted_text)} characters)")
                
                # Save individual result
                safe_name = test_config['name'].lower().replace(' ', '_')
                output_file = config.OUTPUT_DIR / f"test_{safe_name}_{filename}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"Chinese Translation Test: {test_config['name']}\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(f"Configuration:\n")
                    f.write(f"- Prompt: {test_config['prompt']}\n")
                    f.write(f"- Translation: {test_config['translation']}\n")
                    f.write(f"- Mode: {test_config['mode']}\n")
                    f.write(f"- Style: {test_config['style']}\n\n")
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
    comparison_file = config.OUTPUT_DIR / f"chinese_translation_comparison_{filename}.txt"
    with open(comparison_file, 'w', encoding='utf-8') as f:
        f.write(f"Chinese Translation Comparison Report\n")
        f.write(f"{'='*70}\n\n")
        f.write(f"Test Image: {filename}\n")
        f.write(f"Generated: {os.path.basename(__file__)}\n\n")
        
        for name, result in results.items():
            f.write(f"\n{'='*50}\n")
            f.write(f"Configuration: {name}\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Result Preview (first 300 chars):\n")
            preview = result[:300] + "..." if len(result) > 300 else result
            f.write(f"{preview}\n\n")
            f.write(f"Full Length: {len(result)} characters\n")
    
    print(f"\n📊 Comparison Complete!")
    print(f"📄 Full comparison saved to: {comparison_file}")

def main():
    """Main function."""
    print("🔧 Chinese Translation Test & Optimization")
    print("=" * 60)
    
    try:
        test_translation_modes()
        
        print(f"\n💡 Tips for Chinese translation:")
        print(f"   1. Use 'chinese_translate' prompt for best translation results")
        print(f"   2. Set MANGA_LANGUAGE = 'Chinese' in config")
        print(f"   3. Enable ENABLE_TRANSLATION = True for translation")
        print(f"   4. Choose translation mode: 'inline', 'separate', or 'both'")
        print(f"   5. Select style: 'natural', 'literal', or 'localized'")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
