class ChromaDBCheck:
    def __init__(self, chroma_client):
        self.chroma_client = chroma_client

    def check_collection(self, collection):
        print(f"Collection name: {collection.name}")
        print(f"Number of documents in collection: {collection.count()}")

    def list_collections(self):
        print("All collections in ChromaDB client:")
        for collection in self.chroma_client.list_collections():
            print(collection.name)
