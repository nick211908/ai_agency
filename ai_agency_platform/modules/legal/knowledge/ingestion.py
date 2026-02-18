import os
from typing import List
import pypdf
from docx import Document

class DocumentParser:
    """
    Parses various document formats into text chunks.
    Supported: PDF, DOCX, TXT.
    """

    def parse_file(self, file_path: str) -> List[str]:
        """
        Reads a file and returns a list of text chunks.
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".pdf":
            return self._parse_pdf(file_path)
        elif ext == ".docx":
            return self._parse_docx(file_path)
        elif ext == ".txt":
            return self._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _parse_pdf(self, path: str) -> List[str]:
        print(f"[DocumentParser] Parsing PDF: {path}")
        chunks = []
        try:
            reader = pypdf.PdfReader(path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    # Naive chunking by page for MVP
                    chunks.append(f"[Page {i+1}] {text}")
        except Exception as e:
            print(f"Error parsing PDF: {e}")
        return chunks

    def _parse_docx(self, path: str) -> List[str]:
        print(f"[DocumentParser] Parsing DOCX: {path}")
        chunks = []
        try:
            doc = Document(path)
            current_chunk = ""
            for para in doc.paragraphs:
                if len(current_chunk) > 1000:
                    chunks.append(current_chunk)
                    current_chunk = ""
                current_chunk += para.text + "\n"
            if current_chunk:
                chunks.append(current_chunk)
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
        return chunks

    def _parse_txt(self, path: str) -> List[str]:
        print(f"[DocumentParser] Parsing TXT: {path}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
                # Naive chunking by 1000 chars
                return [text[i:i+1000] for i in range(0, len(text), 1000)]
        except Exception as e:
            print(f"Error parsing TXT: {e}")
            return []
