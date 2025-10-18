# manager.py
from .create import ChromaDBCreate
from .delete import ChromaDBDelete
from .check import ChromaDBCheck
from .metadata import MetadataHelper
from .add import ChromaDBAdd

class ChromaDBManager:
    def __init__(self, chromaDB_path=None):
        self.create = ChromaDBCreate(chromaDB_path)
        self.delete = ChromaDBDelete(chromaDB_path)
        self.metadata = MetadataHelper
        self.add = None  # ChromaDBAdd sınıfını dinamik olarak tanımlamak için

    def initialize_add(self, chroma_client):
        """
        ChromaDBAdd sınıfını başlatır.

        Args:
            chroma_client (object): ChromaDB istemcisi.
        """
        # Default model name can be provided later; initialize without model by default
        self.add = ChromaDBAdd(chroma_client)

    def initialize_add_with_model(self, chroma_client, model_name: str):
        """
        Initialize ChromaDBAdd with a specific embedding model.
        """
        self.add = ChromaDBAdd(chroma_client, model_name=model_name)

    def check(self, chroma_client, chroma_collection):
        checker = ChromaDBCheck(chroma_client)
        checker.check_collection(chroma_collection)
        checker.list_collections()
