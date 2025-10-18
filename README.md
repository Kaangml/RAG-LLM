# RAG-LLM

RAG-LLM, belgelere dayalı bir chatbot oluşturmayı hedefleyen bir projedir. Proje, farklı bileşenleri yönetmek için çeşitli modüller içermektedir.

## Proje Yapısı

### 1. **chatbot/**
Bu klasör, chatbot'un temel bileşenlerini içerir:
- **API anahtarı yönetimi**
- **Sistem talimatları (System Instructions)**
- **Sohbet geçmişi işleme**

### 2. **file_processing/**
Bu klasör, farklı dosya formatlarını işlemek için kullanılan kodları içerir:
- **PDF Okuma**: PDF belgelerini okuma ve işleme
- **CSV Okuma**: CSV dosyalarından veri okuma (her satır tek bir belge olarak işlenir)
- **Metin Bölme**: Büyük metinleri daha küçük parçalara bölme
- **Düzenleme ve ön işleme**: Veriyi ChromaDB için hazırlama

**Önemli**: CSV dosyalarında her satır tek bir belge (document) olarak eklenir ve parçalanmaz!

### 3. **query_docs/**
Bu klasör, belirli bir sorguya yönelik olarak ChromaDB koleksiyonundan belgeleri alır ve işleyerek en uygun sonuçları belirler:
- **Sorgu tabanlı belge getirme**
- **Uzaklık/yakınlık hesaplama**
- **Sonuç düzenleme ve gösterim**

### 4. **utils/**
Bu klasör, dosya yükleme işlemleri ile ilgili yardımcı fonksiyonları içerir.

### 5. **vector_store/**
Bu klasör, vektör veri tabanı yönetimi için kullanılır:
- **Veri ekleme (add)**
- **Veri kontrolü (check)**
- **Konfigürasyon ayarları (config)**
- **Veri tabanı oluşturma (create)**
- **Veri silme (delete)**
- **Veri tabanı yönetimi (manager, metadata)**

### 6. **main.py**
Bu dosya, projeyi nasıl kullanacağınızı belirleyen ana betiktir. Kullanım senaryolarına göre özelleştirilebilir.

## Kurulum

### 1. Virtual Environment Oluşturma (uv ile - önerilen)
```bash
# uv kurulumu (eğer kurulu değilse)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Virtual environment oluştur
uv venv

# Virtual environment'ı aktive et
source .venv/bin/activate  # Linux/Mac
# veya
.venv\Scripts\activate  # Windows
```

### 2. Bağımlılıkları Yükleme
```bash
# uv ile (hızlı)
uv pip install -r requirements.txt

# veya standart pip ile
pip install -r requirements.txt
```

### 3. API Anahtarı Yapılandırması
Proje kök dizininde `.env` dosyası oluşturun:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Projeyi Çalıştırma
```bash
# Ana program (GUI ile dosya seçimi)
python main.py

# CSV test örneği
python test_csv.py
```

## Desteklenen Dosya Formatları
- **PDF**: Akademik makaleler, raporlar, dökümanlar
- **CSV**: Veri setleri, tablolar (her satır bir belge olarak işlenir)

## CSV Kullanımı
CSV dosyalarında her satır **tek bir belge** olarak eklenir ve **parçalanmaz**. Örnek CSV yapısı:
```csv
title,content,category,author
Başlık 1,İçerik metni buraya...,Kategori,Yazar Adı
Başlık 2,Diğer içerik...,Kategori,Yazar Adı
```

Her satır şu formatta tek bir dokümana dönüştürülür:
```
title: Başlık 1 | content: İçerik metni buraya... | category: Kategori | author: Yazar Adı
```

## Katkıda Bulunma
Katkıda bulunmak isterseniz lütfen bir **pull request (PR)** açın veya bir **issue** oluşturun.

## Lisans
Bu proje açık kaynak olup, lisans bilgileri **LICENSE** dosyasında mevcuttur.

