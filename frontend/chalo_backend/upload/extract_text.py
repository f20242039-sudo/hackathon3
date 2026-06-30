"""
chalo_backend/upload/extract_text.py

Plain functions for pulling raw text out of an uploaded PDF or screenshot,
for use directly from Streamlit's st.file_uploader -- no FastAPI involved.

- PDFs: pypdf (pure Python, no network).
- Images: pytesseract wrapping Tesseract OCR (CPU-only, local). Tesseract
  must be installed on the host -- on Streamlit Cloud this is handled by
  packages.txt (tesseract-ocr); locally see backend README.
"""
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(file_bytes))
    text_chunks = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(text_chunks).strip()


def extract_text_from_image(file_bytes: bytes) -> str:
    import pytesseract
    from PIL import Image

    image = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(image).strip()
