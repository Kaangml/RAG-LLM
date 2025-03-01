from .pdf_reader import PDFReader
from .text_splitter import TextSplitter


class FileProcessor:
    def __init__(self, db_manager, model_name, chroma_collection):
        self.db_manager = db_manager
        self.model_name = model_name
        self.chroma_collection = chroma_collection

    def process_files(self, file_paths):
        current_id = self.chroma_collection.count()

        for file_path in file_paths:
            print(f"Processing: {file_path}")
            pdf_texts = PDFReader.extract_text_from_pdf(file_path)

            # Metni böl
            char_chunks = TextSplitter.split_by_characters(pdf_texts)
            print(f'Char chunks: {len(char_chunks)}')
            token_chunks = TextSplitter.split_by_tokens(char_chunks, self.model_name)
            print(f'Token chunks: {len(token_chunks)}')  

            # Metadata ekle
            ids, metadatas = self.db_manager.metadata.generate_metadata(
                token_chunks, file_path, "Journal Paper", current_id)
            print(f'ids: {ids}')
            
            # Koleksiyona ekle
            self.db_manager.add.add_documents_to_collection(ids, metadatas, token_chunks, self.chroma_collection)

        print("Processing complete!")

