class ChromaDBRetriever:
    def __init__(self, chroma_collection):
        """
        ChromaDB koleksiyonunu başlatır.
        :param chroma_collection: ChromaDB koleksiyonu (örneğin, ChromaDBCollection nesnesi)
        """
        self.chroma_collection = chroma_collection

    def retrieve_docs(self, query, n_results=5, return_only_docs=False):
        """
        Belirli bir sorgu için ChromaDB koleksiyonundan belgeleri alır.
        :param query: Sorgu metni
        :param n_results: Döndürülecek sonuç sayısı
        :param return_only_docs: Sadece belgeleri mi döndürsün, yoksa tam sonuçları mı?
        :return: İlgili belgeler veya tam sonuçlar (belgeler, metadata, mesafe)
        """
        # ChromaDB sorgusu
        results = self.chroma_collection.query(query_texts=[query],
                                                include=["documents", "metadatas", 'distances'],
                                                n_results=n_results)
        
        # Sadece belgeleri döndürmek için
        if return_only_docs:
            return results['documents'][0]
        else:
            return results
        
