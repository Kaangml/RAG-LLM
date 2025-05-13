from vector_store.manager import ChromaDBManager
from query_docs.retrieve_docs import ChromaDBRetriever
from query_docs.result_displayer import ChromaDBResultDisplayer
from chatbot.chatbot_ollama import ChatBotOllama

chromaDB_path = "./ChromaDBData"
collection_name = "Papers"
tokenizer_model_name = "distiluse-base-multilingual-cased-v1"

db_manager = ChromaDBManager(chromaDB_path)
chroma_client, chroma_collection = db_manager.create.create_client_and_collection(
    collection_name, tokenizer_model_name)

# ChromaDBAdd başlat
db_manager.initialize_add(chroma_client)

def main():
    # ChromaDBRetriever sınıfı ile sorgu yap
    query_executor = ChromaDBRetriever(chroma_collection)
    query = "Why does deep learning perform better with large datasets?"
    results = query_executor.retrieve_docs(query, n_results=5)
    
    # ChromaDBResultDisplayer ile sonuçları ekrana yazdır
    result_displayer = ChromaDBResultDisplayer()
    result_displayer.show_results(results, return_only_docs=False)

    # ChatbotOllama'yı oluştur
    chatbot = ChatBotOllama(model_name="qwen3:0.6b")
    response = chatbot.generate_answer(prompt=query, context=results)

    # Cevabı ekrana yazdır
    print("Generated Response:", response)

if __name__ == "__main__":
    main()