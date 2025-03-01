from pypdf import PdfReader

class PDFReader:
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        reader = PdfReader(pdf_path)
        pdf_texts = [p.extract_text().strip() for p in reader.pages]
        return [text for text in pdf_texts if text]
