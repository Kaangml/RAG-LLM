from .pdf_reader import PDFReader
from .csv_reader import CSVReader
from .text_splitter import TextSplitter
from tqdm import tqdm
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.progress_tracker import VectorizeProgress


class FileProcessor:
    def __init__(self, db_manager, model_name, chroma_collection):
        self.db_manager = db_manager
        self.model_name = model_name
        self.chroma_collection = chroma_collection

    def process_files(self, file_paths):
        """PDF ve CSV dosyalarını işler ve ChromaDB'ye ekler"""
        
        current_id = self.chroma_collection.count()
        total_chunks_added = 0

        # Dosyaları ilerleme çubuğu ile işle
        with tqdm(total=len(file_paths), desc="📂 Processing files", unit="file") as file_pbar:
            for file_path in file_paths:
                file_name = os.path.basename(file_path)
                file_pbar.set_description(f"📂 {file_name[:40]}")
                
                file_extension = os.path.splitext(file_path)[1].lower()
                
                if file_extension == '.pdf':
                    chunks = self._process_pdf(file_path)
                    doc_type = "PDF Document"
                elif file_extension == '.csv':
                    chunks = self._process_csv(file_path)
                    doc_type = "CSV Data"
                else:
                    print(f"⚠️  Unsupported file type: {file_extension}")
                    file_pbar.update(1)
                    continue
                
                # Metadata ekle
                ids, metadatas = self.db_manager.metadata.generate_metadata(
                    chunks, file_path, doc_type, current_id)
                
                # Koleksiyona ekle (ilerleme çubuğu ile)
                print(f"\n🔄 Adding {len(chunks)} documents to ChromaDB...")
                with VectorizeProgress(len(chunks)) as progress:
                    self.db_manager.add.add_documents_to_collection(
                        ids, metadatas, chunks, self.chroma_collection, progress_callback=progress.update
                    )
                
                # İstatistikleri güncelle
                total_chunks_added += len(chunks)
                current_id += len(chunks)
                file_pbar.update(1)

        print(f"\n{'='*60}")
        print(f"✅ Processing Complete!")
        print(f"{'='*60}")
        print(f"📊 Total files processed: {len(file_paths)}")
        print(f"📄 Total documents added: {total_chunks_added}")
        print(f"💾 Collection size: {self.chroma_collection.count()}")
        print(f"{'='*60}\n")

    def _process_pdf(self, file_path):
        """PDF dosyasını işler ve parçalara böler"""
        pdf_texts = PDFReader.extract_text_from_pdf(file_path)

        # Metni böl
        char_chunks = TextSplitter.split_by_characters(pdf_texts)
        print(f'  - Character-based chunks: {len(char_chunks)}')
        token_chunks = TextSplitter.split_by_tokens(char_chunks, self.model_name)
        print(f'  - Token-based chunks: {len(token_chunks)}')
        
        return token_chunks
    
    def _process_csv(self, file_path, columns_to_combine=None):
        """
        CSV dosyasını işler. Her satır tek bir belge olarak eklenir ve PARÇALANMAZ!
        
        Args:
            file_path: CSV dosyasının yolu
            columns_to_combine: Birleştirilecek sütunlar (None ise tüm sütunlar)
        """
        # CSV sütunlarını göster
        columns = CSVReader.get_csv_columns(file_path)
        print(f"  - CSV columns found: {columns}")
        
        # Önizleme göster
        print(f"  - CSV preview (first 3 rows):")
        preview = CSVReader.preview_csv(file_path, n_rows=3)
        print(preview.to_string())
        
        # Her satırı tek bir belge olarak oku (PARÇALANMADAN!)
        documents = CSVReader.extract_rows_from_csv(file_path, columns_to_combine=columns_to_combine)
        print(f'  - CSV rows extracted: {len(documents)} (each row is ONE document)')
        
        return documents

