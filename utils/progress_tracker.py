"""
İlerleme çubuğu ve işlem takibi araçları
"""
from tqdm import tqdm
from typing import List, Callable, Any
import time


class ProgressTracker:
    """Dosya işleme ve vektör oluşturma için ilerleme takibi"""
    
    @staticmethod
    def track_file_processing(files: List[str], process_func: Callable, *args, **kwargs) -> List[Any]:
        """
        Dosya işleme için ilerleme çubuğu
        
        Args:
            files: İşlenecek dosya listesi
            process_func: Her dosya için çağrılacak fonksiyon
            *args, **kwargs: process_func'a iletilecek ek parametreler
            
        Returns:
            İşlem sonuçları listesi
        """
        results = []
        
        with tqdm(total=len(files), desc="📂 Processing files", unit="file") as pbar:
            for file in files:
                pbar.set_description(f"📂 Processing: {file.split('/')[-1][:30]}")
                result = process_func(file, *args, **kwargs)
                results.append(result)
                pbar.update(1)
        
        return results
    
    @staticmethod
    def track_chunks(chunks: List[Any], desc: str = "Processing chunks") -> tqdm:
        """
        Chunk işleme için ilerleme çubuğu döndürür
        
        Args:
            chunks: İşlenecek chunk listesi
            desc: İlerleme çubuğu açıklaması
            
        Returns:
            tqdm progress bar
        """
        return tqdm(chunks, desc=desc, unit="chunk")
    
    @staticmethod
    def track_documents(total: int, desc: str = "Adding documents") -> tqdm:
        """
        Belge ekleme için ilerleme çubuğu
        
        Args:
            total: Toplam belge sayısı
            desc: İlerleme çubuğu açıklaması
            
        Returns:
            tqdm progress bar
        """
        return tqdm(total=total, desc=desc, unit="doc")
    
    @staticmethod
    def simple_progress(iterable, desc: str = "Processing", unit: str = "item"):
        """
        Basit ilerleme çubuğu
        
        Args:
            iterable: İterasyon yapılacak nesne
            desc: Açıklama
            unit: Birim adı
            
        Returns:
            tqdm wrapped iterable
        """
        return tqdm(iterable, desc=desc, unit=unit)
    
    @staticmethod
    def print_stats(stage: str, count: int, time_elapsed: float = None):
        """
        İşlem istatistiklerini yazdırır
        
        Args:
            stage: İşlem aşaması adı
            count: İşlenen öğe sayısı
            time_elapsed: Geçen süre (saniye)
        """
        print(f"\n{'='*60}")
        print(f"📊 {stage} - Completed")
        print(f"{'='*60}")
        print(f"✅ Processed: {count} items")
        
        if time_elapsed:
            print(f"⏱️  Time: {time_elapsed:.2f} seconds")
            if count > 0:
                print(f"⚡ Speed: {count/time_elapsed:.2f} items/sec")
        
        print(f"{'='*60}\n")


class BatchProcessor:
    """Batch işleme ile bellek optimizasyonu"""
    
    @staticmethod
    def process_in_batches(items: List[Any], batch_size: int, process_func: Callable, 
                          desc: str = "Processing batches") -> List[Any]:
        """
        Öğeleri batch'ler halinde işler
        
        Args:
            items: İşlenecek öğeler
            batch_size: Her batch'teki öğe sayısı
            process_func: Batch işleme fonksiyonu (batch alır, sonuç listesi döner)
            desc: İlerleme açıklaması
            
        Returns:
            Tüm sonuçlar
        """
        results = []
        total_batches = (len(items) + batch_size - 1) // batch_size
        
        with tqdm(total=total_batches, desc=desc, unit="batch") as pbar:
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                pbar.set_description(f"{desc} [{i+1}-{min(i+batch_size, len(items))}/{len(items)}]")
                
                batch_results = process_func(batch)
                results.extend(batch_results)
                
                pbar.update(1)
        
        return results
    
    @staticmethod
    def estimate_processing_time(sample_items: List[Any], process_func: Callable, 
                                 total_items: int) -> float:
        """
        İşlem süresini tahmin eder
        
        Args:
            sample_items: Örnek öğeler (ilk birkaç)
            process_func: İşlem fonksiyonu
            total_items: Toplam öğe sayısı
            
        Returns:
            Tahmini toplam süre (saniye)
        """
        if not sample_items:
            return 0
        
        start_time = time.time()
        for item in sample_items:
            process_func(item)
        elapsed = time.time() - start_time
        
        avg_time_per_item = elapsed / len(sample_items)
        estimated_total = avg_time_per_item * total_items
        
        return estimated_total


class VectorizeProgress:
    """Vektör oluşturma için özel ilerleme takibi"""
    
    def __init__(self, total_documents: int):
        self.total = total_documents
        self.pbar = None
        self.current = 0
        self.start_time = None
    
    def start(self, desc: str = "🔄 Vectorizing documents"):
        """İlerleme çubuğunu başlat"""
        self.start_time = time.time()
        self.pbar = tqdm(total=self.total, desc=desc, unit="doc")
    
    def update(self, n: int = 1):
        """İlerleme çubuğunu güncelle"""
        if self.pbar:
            self.current += n
            self.pbar.update(n)
            
            # Kalan süre tahmini
            if self.current > 0:
                elapsed = time.time() - self.start_time
                avg_time = elapsed / self.current
                remaining = (self.total - self.current) * avg_time
                self.pbar.set_postfix({
                    'remaining': f'{remaining:.1f}s',
                    'speed': f'{self.current/elapsed:.1f} doc/s'
                })
    
    def close(self):
        """İlerleme çubuğunu kapat"""
        if self.pbar:
            self.pbar.close()
            total_time = time.time() - self.start_time
            print(f"\n✅ Vectorization complete! Total time: {total_time:.2f}s")
            print(f"⚡ Average speed: {self.total/total_time:.2f} documents/second\n")
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
