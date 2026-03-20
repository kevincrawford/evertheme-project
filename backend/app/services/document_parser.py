import io
from pathlib import Path


SUPPORTED_TYPES = {".docx", ".pdf", ".txt", ".md"}


def parse_document(content: bytes, filename: str) -> str:
    """Extract plain text from an uploaded document."""
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported file type: {suffix}. Supported: {', '.join(SUPPORTED_TYPES)}")

    if suffix == ".docx":
        return _parse_docx(content)
    elif suffix == ".pdf":
        return _parse_pdf(content)
    else:
        return content.decode("utf-8", errors="replace")


def _parse_docx(content: bytes) -> str:
    from docx import Document
    doc = Document(io.BytesIO(content))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    # Also extract table cells
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    paragraphs.append(cell.text.strip())
    return "\n\n".join(paragraphs)


def _parse_pdf(content: bytes) -> str:
    import pdfplumber
    pages = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
    return "\n\n".join(pages)
