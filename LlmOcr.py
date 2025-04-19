from ollama_ocr import OCRProcessor

# Initialize OCR processor
ocr = OCRProcessor(
    model_name="ZimaBlueAI/Qwen2.5-VL-7B-Instruct",
    base_url="http://127.0.0.1:11434/api/generate",
)  # Revert base_url

# Process an image
result = ocr.process_image(
    image_path="Test1.jpg",  # path to your pdf files "path/to/your/file.pdf"
    format_type="markdown",  # Options: markdown, text, json, structured, key_value
    custom_prompt="Extract all text, focusing on dates and names.",  # Optional custom prompt
    language="Chinese",  # Specify the language of the text (New! 🆕)
)
print(result)
