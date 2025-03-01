import textwrap
from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

class ChromaDBResultDisplayer:
    def __init__(self):
        pass

    def show_results(self, results, return_only_docs=False):
        """
        Sonuçları ekrana yazdırır.
        :param results: ChromaDB'den dönen sonuçlar
        :param return_only_docs: Yalnızca belgeleri mi gösterelim, yoksa tam sonuçları mı?
        """
        if return_only_docs:
            # Yalnızca belgeleri döndür
            retrieved_documents = results
            if len(retrieved_documents) == 0:
                print("No results found.")
                return
            for i, doc in enumerate(retrieved_documents):
                print(f"Document {i+1}:")
                print("\tDocument Text: ")
                display(to_markdown(doc))  # Markdown olarak belgeyi görüntüle
        else:
            # Belgeler, metadata ve mesafelerle tam sonuçları döndür
            retrieved_documents = results['documents'][0]
            if len(retrieved_documents) == 0:
                print("No results found.")
                return
            retrieved_documents_metadata = results['metadatas'][0]
            retrieved_documents_distances = results['distances'][0]
            
            # Debugging: metadata'nın yapısını kontrol et
            print("------- Retrieved Documents -------\n")
            print(f"Metadata Structure: {retrieved_documents_metadata}")  # Debugging

            for i, doc in enumerate(retrieved_documents):
                print(f"Document {i+1}:")
                print("\tDocument Text: ")
                display(to_markdown(doc))  # Markdown olarak belgeyi görüntüle

                # metadata'dan doğru anahtarları kullanın
                print(f"\tDocument Source: {retrieved_documents_metadata[i].get('source', 'N/A')}")
                print(f"\tDocument Source Type: {retrieved_documents_metadata[i].get('type', 'N/A')}")
                print(f"\tDocument Distance: {retrieved_documents_distances[i]}")
