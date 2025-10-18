from typing import List, Optional, Callable
from sentence_transformers import SentenceTransformer
import math
import numpy as np


class ChromaDBAdd:
    def __init__(self, chroma_client, model_name: str = "all-mpnet-base-v2", chunk_tokens: int = 256):
        self.chroma_client = chroma_client
        self.model_name = model_name
        self.chunk_tokens = chunk_tokens
        # load model lazily
        self._embedder = None

    def _get_embedder(self):
        if self._embedder is None:
            self._embedder = SentenceTransformer(self.model_name)
        return self._embedder

    def _chunk_text(self, text: str) -> List[str]:
        """Chunk long text into token-aware windows using the model tokenizer"""
        embedder = self._get_embedder()
        tokenizer = embedder.tokenizer
        # temporarily increase model_max_length to avoid tokenizer warnings on very long inputs
        orig_max = getattr(tokenizer, 'model_max_length', None)
        try:
            if orig_max is not None and orig_max < 100000:
                tokenizer.model_max_length = 100000
        except Exception:
            pass

        token_ids = tokenizer.encode(text)
        if len(token_ids) <= self.chunk_tokens:
            return [text]

        chunks = []
        # create overlapping windows to preserve context
        stride = int(self.chunk_tokens * 0.8)
        for i in range(0, len(token_ids), stride):
            window_ids = token_ids[i:i + self.chunk_tokens]
            if not window_ids:
                break
            chunk_text = tokenizer.decode(window_ids)
            chunks.append(chunk_text)
            if i + self.chunk_tokens >= len(token_ids):
                break
        # restore original max length
        try:
            if orig_max is not None:
                tokenizer.model_max_length = orig_max
        except Exception:
            pass

        return chunks

    def _embed_texts(self, texts: List[str]) -> np.ndarray:
        embedder = self._get_embedder()
        embeddings = embedder.encode(texts, show_progress_bar=False)
        return np.array(embeddings)

    def add_documents_to_collection(self, ids: List[str], metadatas: List[dict], documents: List[str], chroma_collection,
                                    progress_callback: Optional[Callable] = None, batch_size: int = 64):
        """
        Robustly add documents to ChromaDB by chunking long texts for embedding and averaging embeddings per document.

        Args:
            ids: list of document ids
            metadatas: list of metadata dicts
            documents: list of full document strings (one per id)
            chroma_collection: chroma collection object
            progress_callback: optional callable taking processed_count (int)
            batch_size: number of documents to process per batch
        """
        if not ids or not metadatas or not documents:
            print("No documents to add.")
            return

        total = len(ids)
        all_embeddings = []
        processed = 0

        for start in range(0, total, batch_size):
            end = min(start + batch_size, total)
            batch_ids = ids[start:end]
            batch_meta = metadatas[start:end]
            batch_docs = documents[start:end]

            # For each doc, chunk if needed and compute embeddings then average
            batch_embeddings = []
            for doc in batch_docs:
                chunks = self._chunk_text(doc)
                embs = self._embed_texts(chunks)
                # average chunk embeddings to get single vector per document
                avg = np.mean(embs, axis=0)
                batch_embeddings.append(avg)

            # convert to list of lists for chroma
            embeddings_lists = [emb.tolist() for emb in batch_embeddings]

            try:
                chroma_collection.add(
                    documents=batch_docs,
                    metadatas=batch_meta,
                    ids=batch_ids,
                    embeddings=embeddings_lists
                )
            except TypeError:
                # Older chroma versions might not accept embeddings param; fallback to documents-only add
                chroma_collection.add(
                    documents=batch_docs,
                    metadatas=batch_meta,
                    ids=batch_ids
                )

            processed += len(batch_ids)
            if progress_callback:
                progress_callback(len(batch_ids))

        print(f"✅ {total} documents added to collection.")
