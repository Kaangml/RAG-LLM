from vector_store.manager import ChromaDBManager
from utils.file_uploader import FileUploader
from file_processing.file_processor import FileProcessor
from query_docs.retrieve_docs import ChromaDBRetriever
from query_docs.result_displayer import ChromaDBResultDisplayer
from chatbot.chatbot import ChatBot

# Ayarlar
chromaDB_path = "./ChromaDBData"
collection_name = "Papers"
model_name = "distiluse-base-multilingual-cased-v1"

# ChromaDB Yöneticisi
db_manager = ChromaDBManager(chromaDB_path)

# ChromaDB Silmek (y/n)
db_manager.delete.delete_all_files_and_folders()

# ChromaDB oluştur
chroma_client, chroma_collection = db_manager.create.create_client_and_collection(
    collection_name, model_name)

# ChromaDBAdd başlat
db_manager.initialize_add(chroma_client)

# Dosya Yükleme ve İşleme için FileProcessor sınıfı
def main():
    # Dosya Yükleme
    print("Select PDF files to process.")
    #file_paths = FileUploader.select_files()
    #file_paths = FileUploader.validate_files(file_paths)

    

    ## FileProcessor sınıfını kullanarak dosyaları işle
    #file_processor = FileProcessor(db_manager, model_name, chroma_collection)
    #file_processor.process_files(file_paths)

    # ChromaDBRetriever sınıfı ile sorgu yap
    query_executor = ChromaDBRetriever(chroma_collection)
    query = "Why does deep learning perform better with large datasets?"
    results = query_executor.retrieve_docs(query, n_results=5)
    
    # ChromaDBResultDisplayer ile sonuçları ekrana yazdır
    result_displayer = ChromaDBResultDisplayer()
    result_displayer.show_results(results, return_only_docs=False)

    prompt = "Why does deep learning perform better with large datasets?"

    #Chatbotu oluştur
    chatbot = ChatBot()
    response = chatbot.generate_answer(prompt=prompt,context=results)
    print(response)

if __name__ == "__main__":
    main()
