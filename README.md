# Gemini Manga OCR

A Python application that uses Google's Gemini multimodal AI models to extract text from manga pages and comic images.

## Features

- 🤖 **AI-Powered OCR**: Uses Google Gemini's advanced multimodal capabilities
- 📚 **Manga Optimized**: Specifically designed for manga and comic book pages
- 🌍 **Multi-Language**: Supports both English and Japanese text extraction
- 🔧 **Configurable**: Extensive configuration options for different use cases
- 📄 **Batch Processing**: Process entire folders of images at once
- 🖼️ **Image Enhancement**: Automatic image preprocessing for better results
- 📊 **Detailed Output**: Organized text extraction with metadata

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key (free tier available)
3. Set your API key as an environment variable:

**Windows:**
```cmd
set GOOGLE_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY=your_api_key_here
```

**Or** edit `config.py` and set `GOOGLE_API_KEY` directly (not recommended for production).

### 3. Configure Settings

Edit `config.py` to customize:

- **Language**: Set `MANGA_LANGUAGE` to 'English' or 'Japanese'
- **Reading Order**: Set `READING_ORDER` for manga layout
- **OCR Prompts**: Choose from different extraction styles
- **Image Processing**: Enable/disable image enhancements
- **Output Format**: Customize how results are saved

## Usage

### Basic Usage

1. Place your manga images in the same folder as the script
2. Run the OCR:

```bash
python gemini_ocr.py
```

3. Results will be saved to `extracted_manga_text_gemini.txt`

### Advanced Configuration

#### OCR Prompts

Choose from different extraction styles in `config.py`:

- **basic**: Simple text extraction
- **detailed**: Comprehensive extraction with formatting
- **structured**: Organized by dialogue, sound effects, etc.
- **japanese**: Japanese-optimized prompts

#### Image Processing

Enable automatic image enhancements:

```python
ENABLE_IMAGE_PREPROCESSING = True
ENHANCE_CONTRAST = True
ENHANCE_SHARPNESS = True
```

#### Output Formatting

Customize the output format:

```python
INCLUDE_FILENAME = True      # Include source filename
INCLUDE_TIMESTAMP = True     # Add processing timestamp
SEPARATE_PAGES = True        # Add separators between pages
ADD_PAGE_NUMBERS = True      # Number the pages
```

## Supported Formats

- PNG, JPG, JPEG, TIFF, TIF, BMP, GIF, WebP
- Images are automatically resized if too large
- RGB conversion for optimal processing

## Output Example

```
Manga OCR Results - Generated on 2024-01-15 14:30:22
Model: gemini-2.0-flash-exp
Total Images Processed: 5
Successful Extractions: 5
Errors: 0
================================================================================

File: page_001.jpg
Page: 1
Processed: 2024-01-15 14:30:25
----------------------------------------
"What are you doing here?"
"I came to see you."
*THUMP*
```

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure `GOOGLE_API_KEY` is set correctly
2. **Rate Limits**: Adjust `REQUEST_DELAY` in config.py if hitting limits
3. **No Text Found**: Try different `OCR_PROMPTS` or enable image preprocessing
4. **Large Images**: Images are automatically resized, but very large files may cause issues

### Debug Mode

Enable detailed logging:

```python
DEBUG_MODE = True
VERBOSE_OUTPUT = True
SAVE_API_RESPONSES = True  # Save raw API responses
```

### Error Logging

Errors are automatically logged to `gemini_ocr_errors.log` when `SAVE_ERROR_LOG = True`.

## Performance Tips

- Use `gemini-2.0-flash-exp` for fastest processing
- Enable `ENHANCE_CONTRAST` and `ENHANCE_SHARPNESS` for better accuracy
- Adjust `REQUEST_DELAY` based on your API limits
- Process images in smaller batches for large collections

## Model Comparison

| Model | Speed | Accuracy | Cost |
|-------|-------|----------|------|
| gemini-2.0-flash-exp | Fastest | High | Lowest |
| gemini-1.5-flash | Fast | High | Low |
| gemini-1.5-pro | Slower | Highest | Higher |

## License

This project is for educational and personal use. Please respect the terms of service for the Google Gemini API and any copyright restrictions on the manga/comic content you process.
```
