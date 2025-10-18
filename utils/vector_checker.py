"""
Vector ve Token boyutu kontrol araçları
"""
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import sys


class VectorChecker:
    """Vektör boyutu ve token limitleri kontrolü"""
    
    @staticmethod
    def check_model_info(model_name: str) -> Dict:
        """
        Embedding modelinin bilgilerini döndürür
        
        Args:
            model_name: SentenceTransformer model adı
            
        Returns:
            Model bilgileri (vector dimension, max_seq_length, vb.)
        """
        try:
            print(f"🔍 Loading model: {model_name}")
            model = SentenceTransformer(model_name)
            
            # Model bilgilerini al
            info = {
                "model_name": model_name,
                "vector_dimension": model.get_sentence_embedding_dimension(),
                "max_seq_length": model.max_seq_length,
                "tokenizer": type(model.tokenizer).__name__,
            }
            
            # Test embedding
            test_text = "This is a test sentence."
            test_embedding = model.encode(test_text)
            info["test_embedding_shape"] = test_embedding.shape
            
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def print_model_info(model_name: str):
        """Model bilgilerini ekrana yazdırır"""
        print("\n" + "="*60)
        print("📊 EMBEDDING MODEL INFORMATION")
        print("="*60)
        
        info = VectorChecker.check_model_info(model_name)
        
        if "error" in info:
            print(f"❌ Error: {info['error']}")
            return
        
        print(f"Model Name: {info['model_name']}")
        print(f"Vector Dimension: {info['vector_dimension']}")
        print(f"Max Sequence Length: {info['max_seq_length']} tokens")
        print(f"Tokenizer: {info['tokenizer']}")
        print(f"Test Embedding Shape: {info['test_embedding_shape']}")
        print("="*60 + "\n")
        
        return info
    
    @staticmethod
    def estimate_token_count(text: str, model_name: str) -> int:
        """
        Bir metnin yaklaşık token sayısını hesaplar
        
        Args:
            text: Kontrol edilecek metin
            model_name: SentenceTransformer model adı
            
        Returns:
            Yaklaşık token sayısı
        """
        try:
            model = SentenceTransformer(model_name)
            tokens = model.tokenizer.encode(text)
            return len(tokens)
        except Exception as e:
            # Fallback: kelime sayısı * 1.3 (yaklaşık token oranı)
            return int(len(text.split()) * 1.3)
    
    @staticmethod
    def check_text_length(text: str, model_name: str, max_seq_length: int = None) -> Dict:
        """
        Metnin token sayısını kontrol eder ve limit aşımını bildirir
        
        Args:
            text: Kontrol edilecek metin
            model_name: SentenceTransformer model adı
            max_seq_length: Maksimum token limiti (None ise modelden alınır)
            
        Returns:
            Kontrol sonuçları
        """
        token_count = VectorChecker.estimate_token_count(text, model_name)
        
        if max_seq_length is None:
            model = SentenceTransformer(model_name)
            max_seq_length = model.max_seq_length
        
        result = {
            "token_count": token_count,
            "max_seq_length": max_seq_length,
            "exceeds_limit": token_count > max_seq_length,
            "usage_percentage": (token_count / max_seq_length) * 100,
            "text_preview": text[:100] + "..." if len(text) > 100 else text
        }
        
        return result
    
    @staticmethod
    def get_memory_size(text: str) -> str:
        """Metnin bellekteki boyutunu döndürür"""
        size_bytes = sys.getsizeof(text)
        
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
    
    @staticmethod
    def analyze_documents(documents: List[str], model_name: str) -> Dict:
        """
        Belge listesini analiz eder
        
        Args:
            documents: Belge listesi
            model_name: SentenceTransformer model adı
            
        Returns:
            İstatistikler
        """
        if not documents:
            return {"error": "No documents provided"}
        
        model = SentenceTransformer(model_name)
        max_seq_length = model.max_seq_length
        
        token_counts = [VectorChecker.estimate_token_count(doc, model_name) for doc in documents]
        exceeding_docs = [i for i, count in enumerate(token_counts) if count > max_seq_length]
        
        stats = {
            "total_documents": len(documents),
            "total_tokens": sum(token_counts),
            "avg_tokens_per_doc": sum(token_counts) / len(documents),
            "min_tokens": min(token_counts),
            "max_tokens": max(token_counts),
            "max_seq_length": max_seq_length,
            "exceeding_limit_count": len(exceeding_docs),
            "exceeding_limit_indices": exceeding_docs[:5],  # İlk 5 tanesini göster
        }
        
        return stats
    
    @staticmethod
    def print_document_analysis(documents: List[str], model_name: str):
        """Belge analizi sonuçlarını ekrana yazdırır"""
        print("\n" + "="*60)
        print("📄 DOCUMENT ANALYSIS")
        print("="*60)
        
        stats = VectorChecker.analyze_documents(documents, model_name)
        
        if "error" in stats:
            print(f"❌ Error: {stats['error']}")
            return
        
        print(f"Total Documents: {stats['total_documents']}")
        print(f"Total Tokens: {stats['total_tokens']:,}")
        print(f"Average Tokens/Document: {stats['avg_tokens_per_doc']:.2f}")
        print(f"Min Tokens: {stats['min_tokens']}")
        print(f"Max Tokens: {stats['max_tokens']}")
        print(f"Max Sequence Length: {stats['max_seq_length']}")
        
        if stats['exceeding_limit_count'] > 0:
            print(f"\n⚠️  WARNING: {stats['exceeding_limit_count']} documents exceed token limit!")
            print(f"First few indices: {stats['exceeding_limit_indices']}")
        else:
            print("\n✅ All documents are within token limits")
        
        print("="*60 + "\n")
        
        return stats
