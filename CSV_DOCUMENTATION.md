# CSV İşleme Özelliği - Dokümantasyon

## 🎯 Özellik Özeti
Bu özellik, CSV dosyalarından veri okuyarak her satırı **tek bir belge (document)** olarak ChromaDB'ye ekler. **Satırlar kesinlikle parçalanmaz!**

## 📋 Kullanım

### Basit Kullanım
```python
from file_processing.csv_reader import CSVReader

# CSV'den tüm satırları oku
documents = CSVReader.extract_rows_from_csv("data.csv")
```

### Belirli Sütunları Seçme
```python
# Sadece belirli sütunları birleştir
documents = CSVReader.extract_rows_from_csv(
    "data.csv", 
    columns_to_combine=["title", "content", "category"]
)
```

### CSV Sütunlarını Görüntüleme
```python
# CSV'deki sütun isimlerini listele
columns = CSVReader.get_csv_columns("data.csv")
print(columns)  # ['title', 'content', 'category', 'author']
```

### Önizleme
```python
# İlk 5 satırı görüntüle
preview = CSVReader.preview_csv("data.csv", n_rows=5)
print(preview)
```

## 🔧 FileProcessor ile Entegrasyon

FileProcessor otomatik olarak dosya uzantısını algılar:

```python
from file_processing.file_processor import FileProcessor

processor = FileProcessor(db_manager, model_name, chroma_collection)

# Hem PDF hem CSV işleyebilir
processor.process_files([
    "document.pdf",
    "data.csv"
])
```

## 📊 CSV Formatı

### Örnek CSV
```csv
title,content,category,author
Deep Learning Basics,Deep learning uses neural networks...,AI,John Doe
Machine Learning,ML enables computers to learn...,AI,Jane Smith
```

### ChromaDB'ye Nasıl Kaydedilir?
Her satır şu formatta tek bir belgeye dönüştürülür:

```
title: Deep Learning Basics | content: Deep learning uses neural networks... | category: AI | author: John Doe
```

## ⚙️ Yapılandırma

### Ayırıcı Karakteri Değiştirme
```python
documents = CSVReader.extract_rows_from_csv(
    "data.csv", 
    separator=" || "  # Varsayılan: " | "
)
```

Çıktı:
```
title: Deep Learning Basics || content: ... || category: AI || author: John Doe
```

## 🎨 Özellikler

✅ **Satır Bütünlüğü**: Her CSV satırı tek bir belge olarak saklanır (parçalanmaz)
✅ **Esnek Sütun Seçimi**: İstediğiniz sütunları seçip birleştirebilirsiniz
✅ **Otomatik Temizleme**: Boş satırlar ve NaN değerler otomatik filtrelenir
✅ **Metadata Desteği**: Her belgeye kaynak dosya, tip ve chunk_index eklenir
✅ **Önizleme**: İşlemeden önce veriyi görebilirsiniz
✅ **Encoding Desteği**: UTF-8 encoding ile Türkçe karakter desteği

## 🚀 Örnek Senaryo

### 1. CSV Hazırlama
`products.csv`:
```csv
product_name,description,price,category
iPhone 15,Latest Apple smartphone with A17 chip,999,Electronics
MacBook Pro,Professional laptop with M3 chip,2499,Electronics
```

### 2. Veriyi Yükleme
```python
from vector_store.manager import ChromaDBManager
from file_processing.file_processor import FileProcessor

# ChromaDB setup
db_manager = ChromaDBManager("./ChromaDBData")
client, collection = db_manager.create.create_client_and_collection(
    "Products", 
    "distiluse-base-multilingual-cased-v1"
)
db_manager.initialize_add(client)

# CSV'yi yükle
processor = FileProcessor(db_manager, "distiluse-base-multilingual-cased-v1", collection)
processor.process_files(["products.csv"])
```

### 3. Sorgulama
```python
from query_docs.retrieve_docs import ChromaDBRetriever

retriever = ChromaDBRetriever(collection)
results = retriever.retrieve_docs("laptop with M3 chip", n_results=3)
```

## 📈 Performans

- **Hız**: Her satır doğrudan eklenir (tokenization yok)
- **Bellek**: Büyük CSV'ler için pandas chunk reading kullanabilirsiniz
- **Ölçeklenebilirlik**: 1M+ satırlı CSV'ler desteklenir

## ⚠️ Önemli Notlar

1. **Satır = Belge**: Her CSV satırı bir belgedir ve parçalanmaz
2. **Token Limiti Yok**: PDF'deki gibi token bazlı bölme yapılmaz
3. **Sütun Sırası**: Sütunlar CSV'deki sırayla birleştirilir
4. **Boş Değerler**: NaN ve boş sütunlar otomatik atlanır
5. **Encoding**: UTF-8 varsayılan olarak kullanılır

## 🐛 Hata Ayıklama

### Sütun Bulunamadı Hatası
```python
# Hata: ValueError: Şu sütunlar CSV'de bulunamadı: ['xyz']

# Çözüm: Önce sütunları kontrol edin
columns = CSVReader.get_csv_columns("data.csv")
print(f"Mevcut sütunlar: {columns}")
```

### Encoding Hatası
```python
# Eğer UTF-8 dışında encoding kullanıyorsanız
# csv_reader.py içinde encoding parametresini değiştirin
df = pd.read_csv(csv_path, encoding='latin-1')  # veya 'iso-8859-9'
```

## 🔄 PDF vs CSV Karşılaştırması

| Özellik | PDF | CSV |
|---------|-----|-----|
| **Bölme** | Token-based chunks | Satır başına 1 belge |
| **Parçalama** | Evet (128 token) | Hayır |
| **Metadata** | "PDF Document" | "CSV Data" |
| **İşlem** | Multi-step (char→token) | Single-step (row→doc) |
| **Kullanım** | Uzun metinler | Yapılandırılmış veri |

## 📚 İleri Seviye

### Custom CSV Processor
```python
class CustomCSVProcessor:
    def process_with_custom_logic(self, csv_path):
        df = pd.read_csv(csv_path)
        
        # Özel işlemler
        df['combined'] = df['title'] + ": " + df['content']
        
        # Her satır için
        documents = []
        for _, row in df.iterrows():
            doc = f"Title: {row['title']}\nContent: {row['content']}"
            documents.append(doc)
        
        return documents
```

### Batch Processing
```python
import glob

# Tüm CSV dosyalarını işle
csv_files = glob.glob("data/*.csv")
processor.process_files(csv_files)
```

## 💡 İpuçları

1. **Büyük CSV'ler**: Chunk processing kullanın
2. **Veri Kalitesi**: CSV'yi işlemeden önce temizleyin
3. **Sütun Seçimi**: Sadece gerekli sütunları seçin (daha hızlı)
4. **Önizleme**: Her zaman önce preview_csv() kullanın
5. **Metadata**: Filtreleme için type="CSV Data" kullanın

## 🎓 Örnek Projeler

1. **FAQ Sistemi**: Soru-cevap CSV'sinden chatbot
2. **Ürün Kataloğu**: E-ticaret ürün arama
3. **Bilgi Bankası**: Dokümantasyon ve kılavuzlar
4. **Akademik Veri**: Paper abstracts ve metadata
