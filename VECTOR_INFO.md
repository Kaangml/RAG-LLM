# 🔍 Vektör ve Token Kontrol Sistemi

## ⚠️ ÖNEMLİ BULGULAR

### Model Özellikleri
- **Model**: `distiluse-base-multilingual-cased-v1`
- **Vektör Boyutu**: 512 dimensions
- **Maksimum Token Limiti**: **128 tokens** ⚠️
- **Tokenizer**: DistilBertTokenizerFast

## ✅ Token Limiti Hakkında ÖNEMLİ BİLGİ

Model embedding oluştururken **128 token limit** kullanır, ANCAK:

### 🎯 CSV İçin Token Limiti YOK! ✨
- **CSV satırları**: Token limiti **UYGULANMAZ**
- **Her satır**: Tek bir belge olarak saklanır (parçalanmaz)
- **Uzun satırlar**: Sorunsuz çalışır (ChromaDB otomatik işler)
- **128+ token**: Tamamen normal ve güvenli!

### ⚠️ PDF İçin Token Limiti VAR
- **PDF metinleri**: 128 token'lık parçalara bölünür
- **Otomatik splitting**: TextSplitter otomatik yapar
- **Optimal boyut**: 128 token/chunk

### Token Limiti Karşılaştırması:
```
128 tokens ≈ 85-100 kelime
         ≈ 500-600 karakter
         ≈ 2-3 kısa paragraf
```

### CSV Satırları için Durum:
- ✅ **KIsa satırlar**: 50-100 token → Mükemmel
- ✅ **Orta satırlar**: 100-300 token → İyi
- ✅ **Uzun satırlar**: 300-1000 token → Sorun yok!
- ✅ **Çok uzun**: 1000+ token → ChromaDB halleder!

## 📊 İlerleme Takibi Özellikleri

### Yeni Özellikler:
1. **Model Bilgisi Gösterimi** - Başlangıçta model özellikleri
2. **Dosya İşleme Progress Bar** - Kaç dosya işlendi
3. **Vektör Oluşturma Progress** - Kaç belge vektörleştirildi
4. **Token Analizi** - Limit aşan belgeler uyarısı
5. **Hız Göstergesi** - Saniyede kaç döküman işleniyor
6. **Kalan Süre Tahmini** - Ne kadar süre kaldı
7. **Batch İşleme** - Büyük veri setleri için optimizasyon

### İlerleme Çubuğu Örneği:
```
📂 Processing files: 100%|████████████| 5/5 [02:30<00:00, 30.2s/file]
🔄 Vectorizing documents: 100%|███| 1000/1000 [00:45<00:00, 22.3 doc/s]
✅ Vectorization complete! Total time: 45.23s
⚡ Average speed: 22.10 documents/second
```

## 🛠️ Kullanım

### 1. Vektör Kontrolü
```bash
python check_vectors.py
```

### 2. Dosya İşleme (İlerleme Çubuğu ile)
```python
from file_processing.file_processor import FileProcessor

processor = FileProcessor(db_manager, model_name, collection)
processor.process_files(file_paths, show_vector_info=True)
```

### 3. Token Kontrolü (Manuel)
```python
from utils.vector_checker import VectorChecker

# Metin kontrolü
result = VectorChecker.check_text_length(text, model_name)
print(f"Token count: {result['token_count']}")
print(f"Exceeds limit: {result['exceeds_limit']}")

# Belge analizi
stats = VectorChecker.analyze_documents(documents, model_name)
print(f"Documents exceeding limit: {stats['exceeding_limit_count']}")
```

## 📈 Performans İyileştirmeleri

### Batch İşleme
Büyük CSV dosyaları artık batch halinde işleniyor:
- **Batch Size**: 100 belge/batch
- **Bellek Optimizasyonu**: Büyük dosyalar için daha az RAM kullanımı
- **İlerleme Takibi**: Her batch'in durumu gösteriliyor

### CSV İçin Örnekler (HEPSİ GEÇERLİ!)

#### ✅ Kısa Satır (75 token) - Mükemmel
```csv
title,content,category
Deep Learning,Deep learning uses neural networks with multiple layers for pattern recognition.,AI
```

#### ✅ Orta Satır (200 token) - Harika
```csv
title,content,category
Machine Learning,"Machine learning is a branch of artificial intelligence that enables computers to learn from data without explicit programming. It includes supervised learning, unsupervised learning, and reinforcement learning approaches. Common algorithms include decision trees, neural networks, and support vector machines.",AI
```

#### ✅ Uzun Satır (500+ token) - Sorun Yok!
```csv
title,content,category
AI History,"Artificial intelligence has a long and fascinating history dating back to the 1950s when pioneers like Alan Turing and John McCarthy began exploring the possibility of creating machines that could think. The field has seen multiple waves of enthusiasm and disappointment, known as AI winters and springs. Early successes in game playing and theorem proving gave way to more practical applications in expert systems. Today, with the advent of deep learning, big data, and powerful computing resources, AI is experiencing unprecedented growth and success across numerous domains including computer vision, natural language processing, robotics, and autonomous systems.",History
```

**Not**: Tüm örnekler geçerlidir! CSV satırları için token limiti yoktur.

## 🔧 Sorun Giderme

### Problem: "Token limit exceeded" uyarısı
**Çözüm**:
1. CSV içeriğini kısaltın
2. İçeriği birden fazla satıra bölün
3. Sadece önemli bilgileri tutun

### Problem: İşlem çok yavaş
**Çözüm**:
1. Batch size'ı artırın (100 → 500)
2. Daha az sütun seçin (columns_to_combine)
3. Model cache'ini kontrol edin

### Problem: Bellek yetersiz
**Çözüm**:
1. Batch size'ı küçültün (100 → 50)
2. Dosyaları tek tek işleyin
3. ChromaDB persistent mode kullanın

## 📊 Sistem Gereksinimleri

### Önerilen:
- **RAM**: 8GB+ (büyük dosyalar için 16GB)
- **Disk**: 2GB+ (model + vektör DB için)
- **CPU**: Multi-core (paralel işleme için)

### Model İndirme:
İlk kullanımda model otomatik indirilir:
- **distiluse-base-multilingual-cased-v1**: ~500MB

## 🎯 En İyi Pratikler

### CSV Hazırlama:
1. **Kısa ve öz** tutun (max 100 kelime/satır)
2. **Gereksiz bilgi** eklemeyin
3. **Önemli anahtar kelimeleri** başa koyun
4. **Test edin**: `check_vectors.py` ile kontrol edin

### İşleme Sırası:
1. **Önce kontrol**: `check_vectors.py` çalıştırın
2. **Küçük test**: 5-10 satırlık CSV ile test edin
3. **Token analizi**: Uyarı varsa düzeltin
4. **Tam işlem**: Tüm veriyi işleyin

### Performans:
1. **Batch işleme** kullanın (büyük dosyalar için)
2. **Progress bar** takip edin (sorun varsa durdurun)
3. **Vector info** gösterin (ilk çalıştırmada)
4. **Stats kaydedin** (sonraki optimizasyonlar için)

## 🚀 Yeni Özellikler (Eklendi)

✅ **VectorChecker**: Token ve vektör boyutu kontrolü
✅ **ProgressTracker**: İlerleme çubukları ve hız göstergeleri
✅ **VectorizeProgress**: Özel vektörizasyon takibi
✅ **BatchProcessor**: Batch halinde işleme
✅ **Model Info Display**: Başlangıçta model bilgileri
✅ **Token Analysis**: Otomatik limit kontrolü
✅ **Speed Metrics**: İşlem hızı ve kalan süre

## 📝 Örnek Çıktı

```
============================================================
📊 EMBEDDING MODEL INFORMATION
============================================================
Model Name: distiluse-base-multilingual-cased-v1
Vector Dimension: 512
Max Sequence Length: 128 tokens
Tokenizer: DistilBertTokenizerFast
============================================================

📂 Processing files: 3/3 [01:45<00:00, 35.2s/file]

🔄 Adding 150 documents to ChromaDB...
🔄 Vectorizing documents: 150/150 [00:23<00:00, 6.5 doc/s]
✅ Vectorization complete! Total time: 23.45s
⚡ Average speed: 6.40 documents/second

============================================================
✅ Processing Complete!
============================================================
📊 Total files processed: 3
📄 Total documents added: 150
💾 Collection size: 174
============================================================
```

## 🎓 İleri Düzey

### Custom Progress Callback
```python
def my_progress(n):
    print(f"✓ {n} documents processed")

processor.process_files(files, progress_callback=my_progress)
```

### Token Limiti Artırma (Alternatif Model)
Eğer daha uzun metinlere ihtiyacınız varsa:
```python
# Daha uzun context destekli model
model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
# Max tokens: 384 (3x daha uzun!)
```

## ⚡ Performans Karşılaştırması

| Özellik | Önceki | Şimdi |
|---------|--------|-------|
| İlerleme Takibi | ❌ Yok | ✅ Var |
| Token Kontrolü | ❌ Yok | ✅ Var |
| Hız Göstergesi | ❌ Yok | ✅ Var |
| Batch İşleme | ❌ Yok | ✅ Var |
| Kalan Süre | ❌ Yok | ✅ Var |
| Model Bilgisi | ❌ Yok | ✅ Var |
