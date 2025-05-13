# RAG-LLM

RAG-LLM, belgelere dayalı bir chatbot oluşturmayı hedefleyen bir projedir. Proje, farklı bileşenleri yönetmek için çeşitli modüller içermektedir.

## Proje Yapısı

### 1. **chatbot/**
Bu klasör, chatbot'un temel bileşenlerini içerir:
- **API anahtarı yönetimi**
- **Sistem talimatları (System Instructions)**
- **Sohbet geçmişi işleme**

### 2. **file_processing/**
Bu klasör, PDF veya Word belgelerini işlemek için kullanılan kodları içerir:
- **Belgeleri okuma**
- **Bölme ve parçalama**
- **Düzenleme ve ön işleme**

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
1. Gerekli bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
2. API anahtarlarını `chatbot/` klasöründe uygun şekilde yapılandırın.
3. Projeyi çalıştırmak için:
   ```bash
   python main.py
   ```

## Katkıda Bulunma
Katkıda bulunmak isterseniz lütfen bir **pull request (PR)** açın veya bir **issue** oluşturun.

## Lisans
Bu proje açık kaynak olup, lisans bilgileri **LICENSE** dosyasında mevcuttur.

