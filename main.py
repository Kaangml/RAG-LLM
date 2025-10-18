from vector_store.manager import ChromaDBManager
from utils.file_uploader import FileUploader
from file_processing.file_processor import FileProcessor
from query_docs.retrieve_docs import ChromaDBRetriever
from query_docs.result_displayer import ChromaDBResultDisplayer
from chatbot.chatbot import ChatBot

# Ayarlar
chromaDB_path = "./ChromaDBData"
collection_name = "Papers"
model_name = "all-mpnet-base-v2"

# ChromaDB Yöneticisi
db_manager = ChromaDBManager(chromaDB_path)

# ChromaDB Silmek (y/n)
db_manager.delete.delete_all_files_and_folders()

# ChromaDB oluştur
chroma_client, chroma_collection = db_manager.create.create_client_and_collection(
    collection_name, model_name)

# ChromaDBAdd başlat (model ile)
db_manager.initialize_add_with_model(chroma_client, model_name)

# Dosya Yükleme ve İşleme için FileProcessor sınıfı
def main():
    # Dosya Yükleme - PDF veya CSV dosyaları seçebilirsiniz
    print("Select files to process (PDF or CSV).")
    file_paths = FileUploader.select_files(file_types="all")  # "all", "pdf", veya "csv"
    file_paths = FileUploader.validate_files(file_paths)
    
    if not file_paths:
        print("No files selected. Skipping file processing.")
    else:
        print(f"\n{len(file_paths)} file(s) selected for processing.")
        ## FileProcessor sınıfını kullanarak dosyaları işle
        file_processor = FileProcessor(db_manager, model_name, chroma_collection)
        file_processor.process_files(file_paths)

    # ChromaDBRetriever sınıfı ile sorgu yap
    query_executor = ChromaDBRetriever(chroma_collection)
    query = "Nvidia is a fraud ?"
    results = query_executor.retrieve_docs(query, n_results=5)
    
    # ChromaDBResultDisplayer ile sonuçları ekrana yazdır
    result_displayer = ChromaDBResultDisplayer()
    result_displayer.show_results(results, return_only_docs=False)

    #Chatbotu oluştur
    chatbot = ChatBot()
    response = chatbot.generate_answer(prompt=query,context=results)
    generated_response = response.candidates[0].content.parts[0].text

    print("Chatbot response:",generated_response)

if __name__ == "__main__":
    main()
