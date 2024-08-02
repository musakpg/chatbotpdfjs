import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return clean_text(text)

def clean_text(text):
    # Implement cleaning steps like removing extra whitespace, fixing OCR errors, etc.
    return text.strip()
