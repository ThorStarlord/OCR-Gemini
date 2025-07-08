"""
Example script demonstrating how to use the Gemini Manga OCR system.
This script shows different ways to use the OCR functionality with proper error handling.
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
import traceback

try:
    import config
    from gemini_ocr import GeminiMangaOCR
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure config.py and gemini_ocr.py are in the same directory")
    sys.exit(1)

class OCRExamples:
    """Class containing various OCR usage examples."""
    
    def __init__(self):
        """Initialize the examples class."""
        self.ocr: Optional[GeminiMangaOCR] = None
        self._validate_setup()
    
    def _validate_setup(self) -> None:
        """Validate that the setup is correct before running examples."""
        # Check API key
        if not config.GOOGLE_API_KEY or config.GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            raise ValueError("GOOGLE_API_KEY not configured. Please set it in config.py or as environment variable")
        
        # Check image folder exists
        if not os.path.exists(config.IMAGE_FOLDER):
            raise FileNotFoundError(f"Image folder '{config.IMAGE_FOLDER}' not found")
        
        print(f"✅ Setup validated")
        print(f"   🤖 Model: {config.GEMINI_MODEL}")
        print(f"   📁 Images: {config.IMAGE_FOLDER}")
        print(f"   📄 Output: {config.OUTPUT_FILE}")
    
    def _get_ocr_instance(self) -> GeminiMangaOCR:
        """Get or create OCR instance."""
        if self.ocr is None:
            self.ocr = GeminiMangaOCR()
        return self.ocr
    
    def _print_section_header(self, title: str) -> None:
        """Print a formatted section header."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def _print_result_summary(self, success: bool, processed: int = 0, errors: int = 0) -> None:
        """Print a formatted result summary."""
        if success:
            print(f"✅ Success! Processed: {processed}, Errors: {errors}")
        else:
            print(f"❌ Failed! Processed: {processed}, Errors: {errors}")
    
    def example_basic_usage(self) -> bool:
        """Example 1: Basic OCR usage with default settings."""
        self._print_section_header("Example 1: Basic OCR Processing")
        
        try:
            ocr = self._get_ocr_instance()
            
            print("📊 Processing all images in the default folder...")
            success = ocr.process_manga_folder()
            
            self._print_result_summary(success, ocr.processed_count, ocr.error_count)
            
            if success:
                print(f"📄 Results saved to: {config.OUTPUT_FILE}")
            
            return success
            
        except Exception as e:
            print(f"❌ Error in basic usage example: {e}")
            return False
    
    def example_single_image(self) -> bool:
        """Example 2: Process a single image."""
        self._print_section_header("Example 2: Single Image Processing")
        
        try:
            ocr = self._get_ocr_instance()
            image_files = ocr.get_image_files(config.IMAGE_FOLDER)
            
            if not image_files:
                print("⚠️  No image files found")
                return False
            
            # Process the first image
            first_image = image_files[0]
            filename = os.path.basename(first_image)
            
            print(f"🖼️  Processing: {filename}")
            extracted_text = ocr.extract_text_from_image(first_image)
            
            if extracted_text:
                print("✅ Text extracted successfully!")
                print(f"\n📄 Extracted text preview (first 200 chars):")
                print("-" * 50)
                preview = extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
                print(preview)
                print("-" * 50)
                
                # Save single result
                single_output = f"single_image_result_{filename}.txt"
                with open(single_output, 'w', encoding='utf-8') as f:
                    f.write(f"Single Image OCR Result\n")
                    f.write(f"File: {filename}\n")
                    f.write(f"{'='*40}\n\n")
                    f.write(extracted_text)
                
                print(f"💾 Single result saved to: {single_output}")
                return True
            else:
                print("❌ No text extracted")
                return False
                
        except Exception as e:
            print(f"❌ Error in single image example: {e}")
            return False
    
    def example_custom_prompt(self) -> bool:
        """Example 3: Using different OCR prompts."""
        self._print_section_header("Example 3: Custom Prompt Testing")
        
        try:
            # Test different prompts
            prompts_to_test = ['basic', 'detailed', 'english']
            available_prompts = [p for p in prompts_to_test if p in config.OCR_PROMPTS]
            
            if not available_prompts:
                print("⚠️  No test prompts available")
                return False
            
            ocr = self._get_ocr_instance()
            image_files = ocr.get_image_files(config.IMAGE_FOLDER)
            
            if not image_files:
                print("⚠️  No image files found")
                return False
            
            # Use first image for testing
            test_image = image_files[0]
            filename = os.path.basename(test_image)
            
            print(f"🧪 Testing different prompts on: {filename}")
            
            # Store original settings
            original_prompt = config.DEFAULT_PROMPT
            original_save_responses = getattr(config, 'SAVE_API_RESPONSES', False)
            
            results = {}
            
            try:
                # Enable response saving for comparison
                config.SAVE_API_RESPONSES = True
                
                for prompt_name in available_prompts:
                    print(f"\n🔄 Testing prompt: {prompt_name}")
                    config.DEFAULT_PROMPT = prompt_name
                    
                    # Create new OCR instance with updated config
                    test_ocr = GeminiMangaOCR()
                    extracted_text = test_ocr.extract_text_from_image(test_image)
                    
                    if extracted_text:
                        results[prompt_name] = extracted_text[:100] + "..." if len(extracted_text) > 100 else extracted_text
                        print(f"   ✅ Success ({len(extracted_text)} characters)")
                    else:
                        results[prompt_name] = "No text extracted"
                        print(f"   ❌ Failed")
                
                # Save comparison results
                comparison_file = "prompt_comparison_results.txt"
                with open(comparison_file, 'w', encoding='utf-8') as f:
                    f.write(f"Prompt Comparison Results\n")
                    f.write(f"Test Image: {filename}\n")
                    f.write(f"{'='*50}\n\n")
                    
                    for prompt_name, result in results.items():
                        f.write(f"Prompt: {prompt_name}\n")
                        f.write(f"Result: {result}\n")
                        f.write(f"{'-'*30}\n\n")
                
                print(f"\n💾 Comparison saved to: {comparison_file}")
                
            finally:
                # Restore original settings
                config.DEFAULT_PROMPT = original_prompt
                config.SAVE_API_RESPONSES = original_save_responses
            
            return len(results) > 0
            
        except Exception as e:
            print(f"❌ Error in custom prompt example: {e}")
            return False
    
    def example_batch_processing(self) -> bool:
        """Example 4: Batch processing with progress tracking."""
        self._print_section_header("Example 4: Batch Processing with Progress")
        
        try:
            ocr = self._get_ocr_instance()
            image_files = ocr.get_image_files(config.IMAGE_FOLDER)
            
            if not image_files:
                print("⚠️  No image files found")
                return False
            
            total_files = len(image_files)
            print(f"📦 Processing {total_files} images...")
            
            # Process with manual progress tracking
            successful_extractions = []
            failed_extractions = []
            
            for i, image_path in enumerate(image_files, 1):
                filename = os.path.basename(image_path)
                print(f"🔄 [{i}/{total_files}] Processing: {filename}")
                
                try:
                    extracted_text = ocr.extract_text_from_image(image_path)
                    
                    if extracted_text:
                        successful_extractions.append({
                            'filename': filename,
                            'text_length': len(extracted_text),
                            'preview': extracted_text[:50] + "..." if len(extracted_text) > 50 else extracted_text
                        })
                        print(f"   ✅ Success ({len(extracted_text)} chars)")
                    else:
                        failed_extractions.append(filename)
                        print(f"   ❌ No text extracted")
                        
                except Exception as e:
                    failed_extractions.append(filename)
                    print(f"   ❌ Error: {e}")
            
            # Generate detailed report
            report_file = "batch_processing_report.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"Batch Processing Report\n")
                f.write(f"{'='*50}\n\n")
                f.write(f"Total Files: {total_files}\n")
                f.write(f"Successful: {len(successful_extractions)}\n")
                f.write(f"Failed: {len(failed_extractions)}\n\n")
                
                if successful_extractions:
                    f.write("Successful Extractions:\n")
                    f.write("-" * 30 + "\n")
                    for item in successful_extractions:
                        f.write(f"File: {item['filename']}\n")
                        f.write(f"Length: {item['text_length']} characters\n")
                        f.write(f"Preview: {item['preview']}\n\n")
                
                if failed_extractions:
                    f.write("Failed Extractions:\n")
                    f.write("-" * 30 + "\n")
                    for filename in failed_extractions:
                        f.write(f"- {filename}\n")
            
            print(f"\n📊 Batch processing completed!")
            print(f"   ✅ Successful: {len(successful_extractions)}")
            print(f"   ❌ Failed: {len(failed_extractions)}")
            print(f"   📄 Report saved to: {report_file}")
            
            return len(successful_extractions) > 0
            
        except Exception as e:
            print(f"❌ Error in batch processing example: {e}")
            return False
    
    def example_error_handling(self) -> bool:
        """Example 5: Demonstrate proper error handling."""
        self._print_section_header("Example 5: Error Handling Demonstration")
        
        print("🧪 Testing various error scenarios...")
        
        # Test 1: Non-existent folder
        print("\n🔍 Test 1: Non-existent folder")
        try:
            ocr = self._get_ocr_instance()
            fake_folder = os.path.join(config.SCRIPT_DIR, "non_existent_folder")
            success = ocr.process_manga_folder(fake_folder)
            print(f"   Result: {'Success' if success else 'Failed as expected'} ✅")
        except Exception as e:
            print(f"   Exception handled: {type(e).__name__}")
        
        # Test 2: Invalid image file
        print("\n🔍 Test 2: Invalid image processing")
        try:
            ocr = self._get_ocr_instance()
            # Try to process this script file as an image
            invalid_image = __file__
            result = ocr.extract_text_from_image(invalid_image)
            print(f"   Result: {'Text extracted' if result else 'Failed as expected'} ✅")
        except Exception as e:
            print(f"   Exception handled: {type(e).__name__}")
        
        # Test 3: Recovery after error
        print("\n🔍 Test 3: Processing continues after errors")
        try:
            ocr = self._get_ocr_instance()
            # This should work normally
            success = ocr.process_manga_folder()
            print(f"   Normal processing after errors: {'Success' if success else 'Failed'}")
            print(f"   Processed: {ocr.processed_count}, Errors: {ocr.error_count}")
        except Exception as e:
            print(f"   Unexpected error: {e}")
        
        print("\n✅ Error handling tests completed")
        return True
    
    def example_chinese_translation(self) -> bool:
        """Example 7: Test Chinese to English translation."""
        self._print_section_header("Example 7: Chinese Translation Test")
        
        try:
            ocr = self._get_ocr_instance()
            image_files = ocr.get_image_files(config.IMAGE_FOLDER)
            
            if not image_files:
                print("⚠️  No image files found")
                return False
            
            # Store original settings
            original_prompt = getattr(config, 'DEFAULT_PROMPT', 'basic')
            original_language = getattr(config, 'MANGA_LANGUAGE', 'English')
            original_translation = getattr(config, 'ENABLE_TRANSLATION', False)
            original_source = getattr(config, 'SOURCE_LANGUAGE', 'Chinese')
            original_target = getattr(config, 'TARGET_LANGUAGE', 'English')
            original_reading_order = getattr(config, 'READING_ORDER', 'right-to-left')
            
            try:
                # Set Chinese translation settings
                config.DEFAULT_PROMPT = 'chinese_translate'
                config.MANGA_LANGUAGE = 'Chinese'
                config.ENABLE_TRANSLATION = True
                config.SOURCE_LANGUAGE = 'Chinese'
                config.TARGET_LANGUAGE = 'English'
                config.READING_ORDER = 'right-to-left'
                
                print(f"🔄 Testing Chinese to English translation...")
                print(f"   🇨🇳 Source: {config.SOURCE_LANGUAGE}")
                print(f"   🇺🇸 Target: {config.TARGET_LANGUAGE}")
                print(f"   📖 Reading order: {config.READING_ORDER}")
                print(f"   📝 Prompt: {config.DEFAULT_PROMPT}")
                
                # Process first image with translation settings
                test_image = image_files[0]
                filename = os.path.basename(test_image)
                
                test_ocr = GeminiMangaOCR()
                extracted_text = test_ocr.extract_text_from_image(test_image)
                
                if extracted_text:
                    # Save Chinese translation result
                    output_dir = getattr(config, 'OUTPUT_DIR', 'output')
                    translation_output = os.path.join(str(output_dir), f"chinese_translation_{filename}.txt")
                    
                    with open(translation_output, 'w', encoding='utf-8') as f:
                        f.write(f"Chinese to English Translation Test Results\n")
                        f.write(f"{'='*60}\n\n")
                        f.write(f"Image: {filename}\n")
                        f.write(f"Source Language: {config.SOURCE_LANGUAGE}\n")
                        f.write(f"Target Language: {config.TARGET_LANGUAGE}\n")
                        f.write(f"Reading Order: {config.READING_ORDER}\n")
                        f.write(f"Translation Mode: {getattr(config, 'TRANSLATION_MODE', 'inline')}\n")
                        f.write(f"Prompt Type: {config.DEFAULT_PROMPT}\n\n")
                        f.write(f"Extracted Text with Translation:\n")
                        f.write(f"{'-'*50}\n\n")
                        f.write(extracted_text)
                    
                    print(f"✅ Chinese translation test completed!")
                    print(f"📄 Results saved to: {translation_output}")
                    
                    # Show preview
                    print(f"\n🔤 Translation preview:")
                    print("-" * 60)
                    preview = extracted_text[:400] + "..." if len(extracted_text) > 400 else extracted_text
                    print(preview)
                    print("-" * 60)
                    
                    return True
                else:
                    print("❌ No text extracted")
                    return False
                    
            finally:
                # Restore original settings
                config.DEFAULT_PROMPT = original_prompt
                config.MANGA_LANGUAGE = original_language
                config.ENABLE_TRANSLATION = original_translation
                config.SOURCE_LANGUAGE = original_source
                config.TARGET_LANGUAGE = original_target
                config.READING_ORDER = original_reading_order
                
        except Exception as e:
            print(f"❌ Error in Chinese translation test: {e}")
            return False

    def example_manga_reading_order(self) -> bool:
        """Example 6: Test manga reading order specifically."""
        self._print_section_header("Example 6: Manga Reading Order Test")
        
        try:
            ocr = self._get_ocr_instance()
            image_files = ocr.get_image_files(config.IMAGE_FOLDER)
            
            if not image_files:
                print("⚠️  No image files found")
                return False
            
            # Test with manga-specific settings
            original_prompt = getattr(config, 'DEFAULT_PROMPT', 'basic')
            original_reading_order = getattr(config, 'READING_ORDER', 'right-to-left')
            original_language = getattr(config, 'MANGA_LANGUAGE', 'Japanese')
            
            try:
                # Set optimal manga settings
                config.DEFAULT_PROMPT = 'manga_precise'
                config.READING_ORDER = 'right-to-left'
                config.MANGA_LANGUAGE = 'Japanese'
                
                print(f"🔄 Testing manga reading order on first image...")
                print(f"   📖 Reading order: {config.READING_ORDER}")
                print(f"   🗾 Language: {config.MANGA_LANGUAGE}")
                print(f"   📝 Prompt: {config.DEFAULT_PROMPT}")
                
                # Process first image with manga settings
                test_image = image_files[0]
                filename = os.path.basename(test_image)
                
                test_ocr = GeminiMangaOCR()
                extracted_text = test_ocr.extract_text_from_image(test_image)
                
                if extracted_text:
                    # Save manga reading order result
                    output_dir = getattr(config, 'OUTPUT_DIR', 'output')
                    manga_output = os.path.join(str(output_dir), f"manga_reading_order_{filename}.txt")
                    
                    with open(manga_output, 'w', encoding='utf-8') as f:
                        f.write(f"Manga Reading Order Test Results\n")
                        f.write(f"{'='*50}\n\n")
                        f.write(f"Image: {filename}\n")
                        f.write(f"Reading Order: {config.READING_ORDER}\n")
                        f.write(f"Language: {config.MANGA_LANGUAGE}\n")
                        f.write(f"Prompt Type: {config.DEFAULT_PROMPT}\n\n")
                        f.write(f"Extracted Text (in proper manga order):\n")
                        f.write(f"{'-'*40}\n\n")
                        f.write(extracted_text)
                    
                    print(f"✅ Manga reading order test completed!")
                    print(f"📄 Results saved to: {manga_output}")
                    
                    # Show preview
                    print(f"\n📖 Text preview (showing reading order):")
                    print("-" * 50)
                    preview = extracted_text[:300] + "..." if len(extracted_text) > 300 else extracted_text
                    print(preview)
                    print("-" * 50)
                    
                    return True
                else:
                    print("❌ No text extracted")
                    return False
                    
            finally:
                # Restore original settings
                config.DEFAULT_PROMPT = original_prompt
                config.READING_ORDER = original_reading_order
                config.MANGA_LANGUAGE = original_language
                
        except Exception as e:
            print(f"❌ Error in manga reading order test: {e}")
            return False

def run_all_examples() -> None:
    """Run all available examples."""
    print("🚀 Gemini Manga OCR - Examples & Demonstrations")
    print("=" * 60)
    
    try:
        examples = OCRExamples()
        
        # Run examples in sequence
        example_methods = [
            ('Basic Usage', examples.example_basic_usage),
            ('Single Image', examples.example_single_image),
            ('Custom Prompts', examples.example_custom_prompt),
            ('Manga Reading Order', examples.example_manga_reading_order),
            ('Chinese Translation', examples.example_chinese_translation),
            ('Batch Processing', examples.example_batch_processing),
            ('Error Handling', examples.example_error_handling)
        ]
        
        results = {}
        
        for name, method in example_methods:
            try:
                print(f"\n⏳ Running: {name}")
                success = method()
                results[name] = success
                
                if success:
                    print(f"✅ {name} completed successfully")
                else:
                    print(f"⚠️  {name} completed with issues")
                    
            except KeyboardInterrupt:
                print(f"\n⏹️  Process interrupted by user")
                break
            except Exception as e:
                print(f"❌ {name} failed: {e}")
                if config.DEBUG_MODE:
                    traceback.print_exc()
                results[name] = False
        
        # Final summary
        print(f"\n{'='*60}")
        print("📊 FINAL SUMMARY")
        print(f"{'='*60}")
        
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        for name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {status} {name}")
        
        print(f"\n🎯 Overall: {successful}/{total} examples passed")
        
        if successful == total:
            print("🎉 All examples completed successfully!")
        elif successful > 0:
            print("⚠️  Some examples had issues - check the output above")
        else:
            print("❌ All examples failed - check your configuration")
        
        print(f"\n📄 Check output files for detailed results")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if config.DEBUG_MODE:
            traceback.print_exc()

def main():
    """Main function."""
    try:
        run_all_examples()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
