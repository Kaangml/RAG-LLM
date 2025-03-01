import os

class MetadataHelper:
    @staticmethod
    def generate_metadata(token_chunks, file_path, doc_type, start_index):
        ids = []
        metadatas = []
        for i, chunk in enumerate(token_chunks):
            ids.append(f"{start_index + i}")
            metadata = {
                "source": os.path.basename(file_path),
                "type": doc_type,
                "chunk_index": i
            }
            metadatas.append(metadata)
        return ids, metadatas

