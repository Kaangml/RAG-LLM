from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from chromadb import Client, PersistentClient
from chromadb.utils import embedding_functions

class ChromaDBCreate:
    def __init__(self, chromaDB_path=None):
        self.chromaDB_path = chromaDB_path

    def create_client_and_collection(self, collection_name, model_name):
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
        
        if self.chromaDB_path:
            chroma_client = PersistentClient(
                path=self.chromaDB_path,
                settings=Settings(),
                tenant=DEFAULT_TENANT,
                database=DEFAULT_DATABASE
            )
        else:
            chroma_client = Client()

        chroma_collection = chroma_client.get_or_create_collection(
            collection_name,
            embedding_function=embedding_function
        )

        return chroma_client, chroma_collection
