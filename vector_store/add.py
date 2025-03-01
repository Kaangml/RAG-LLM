class ChromaDBAdd:
    def __init__(self, chroma_client):
        self.chroma_client = chroma_client

    def add_documents_to_collection(self, ids, metadatas, token_chunks, chroma_collection):
        """
        ChromaDB koleksiyonuna belgeleri ekler.

        Args:
            ids (list): Belge ID'leri.
            metadatas (list): Metadata bilgileri.
            token_chunks (list): Bölünmüş metinler.
            chroma_collection (object): ChromaDB koleksiyonu.
        """
        if not ids or not metadatas or not token_chunks:
            print("No documents to add.")
            return

        try:
            chroma_collection.add(
                documents=token_chunks,
                metadatas=metadatas,
                ids=ids
            )
            print(f"{len(ids)} documents added to collection.")
        except Exception as e:
            print(f"Error adding documents to collection: {e}")
