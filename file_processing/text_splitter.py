from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter

class TextSplitter:
    @staticmethod
    def split_by_characters(texts, chunk_size=1500, chunk_overlap=0):
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", " ", ""],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return splitter.split_text("\n\n".join(texts))

    @staticmethod
    def split_by_tokens(chunks, model_name, tokens_per_chunk=128):
        splitter = SentenceTransformersTokenTextSplitter(
            model_name=model_name,
            tokens_per_chunk=tokens_per_chunk
        )
        tokenized_chunks = []
        for chunk in chunks:
            tokenized_chunks.extend(splitter.split_text(chunk))
        return tokenized_chunks
