# Sentiment Analysis API

Bu proje, Türkçe metinler için duygu analizi yapan bir REST API'sidir. Sklearn kullanarak TF-IDF ve Logistic Regression ile eğitilmiş bir model kullanır.

## 🌟 Özellikler

- 🚀 **FastAPI** ile modern REST API
- 🤖 **Sklearn** ile makine öğrenmesi modeli
- 📊 **TF-IDF** vektörizasyonu
- 🎯 **Logistic Regression** sınıflandırıcısı
- 📝 **Türkçe** metin desteği
- 🔄 **Toplu tahmin** desteği
- 💾 **Model kaydetme/yükleme**
- 🧪 **Kapsamlı test** scriptleri
- 🐳 **Docker** desteği

## 🚀 Hızlı Başlangıç

### Docker ile (Önerilen)

```bash
# Repository'yi klonla
git clone https://github.com/YaseminOran/ai-engineer-lab.git
cd ai-engineer-lab

# Docker ile başlat
docker build -t sentiment-analysis-api .
docker run -p 8000:8000 sentiment-analysis-api
```

### Manuel Kurulum

```bash
# Repository'yi klonla
git clone https://github.com/YaseminOran/ai-engineer-lab.git
cd ai-engineer-lab

# Sanal ortam oluştur
conda create -n sentiment_env python=3.9 -y
conda activate sentiment_env

# Bağımlılıkları yükle
pip install -r requirements.txt

# API'yi başlat
python app/main.py
```

## 📚 API Endpoint'leri

### 1. Sağlık Kontrolü
```bash
GET /health
```

### 2. Tek Metin Tahmini
```bash
POST /predict
Content-Type: application/json

{
  "text": "Bu film gerçekten harika!"
}
```

### 3. Toplu Tahmin
```bash
POST /predict/batch
Content-Type: application/json

{
  "texts": [
    "Bu film harika!",
    "Kötü bir deneyim.",
    "Normal bir gün."
  ]
}
```

### 4. Model Bilgileri
```bash
GET /model/info
```

### 5. Model Yeniden Eğitme
```bash
POST /retrain
```

## 🧪 Test Etme

### Docker ile Test
```bash
# API çalışırken test et
curl -X GET "http://localhost:8000/health"

# Tek metin tahmini
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Bu film gerçekten harika!"}'
```

### Python Script ile Test
```bash
python tests/test_api.py
```

### Shell Script ile Test
```bash
chmod +x tests/test_curl.sh
./tests/test_curl.sh
```

## 🐳 Docker Komutları

```bash
# Image oluştur
docker build -t sentiment-analysis-api .

# Container çalıştır
docker run -p 8000:8000 sentiment-analysis-api

# Arka planda çalıştır
docker run -d -p 8000:8000 --name sentiment-api sentiment-analysis-api

# Container'ı durdur
docker stop sentiment-api
```

## 📊 Model Detayları

- **Vektörizer**: TF-IDF (max_features=5000)
- **Sınıflandırıcı**: Logistic Regression
- **Duygu Kategorileri**: 
  - 0: Negatif
  - 1: Pozitif  
  - 2: Nötr

## 🏗️ Proje Yapısı

```
week1/
├── app/
│   ├── main.py                 # FastAPI uygulaması
│   └── sentiment_model.py      # Sentiment analysis modeli
├── tests/
│   ├── test_api.py            # API test scripti
│   └── test_curl.sh           # cURL test scripti
├── requirements.txt           # Python bağımlılıkları
├── Dockerfile                # Docker image tanımı
├── .dockerignore             # Docker ignore dosyası
├── README.md                # Bu dosya
└── sentiment_model.pkl      # Eğitilmiş model
```

## 👤 Geliştirici

**Yasemin ARSLAN** - [GitHub](https://github.com/YaseminOran)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 