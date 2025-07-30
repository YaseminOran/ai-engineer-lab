# AI Engineer Lab

Bu repository, AI Engineer eğitimi sırasında geliştirdiğim projeleri içerir. 6 haftalık öğrenme planı takip edilerek, her hafta farklı bir konu üzerinde çalışılmıştır.

## 🎯 Öğrenme Hedefi

Her haftanın amacı, teorik altyapıyı pratiğe dökerek AI Engineer olarak becerilerini adım adım inşa etmektir.

## 📚 6 Haftalık Öğrenme Programı

### ✅ Hafta 1: Yazılım Temelleri + API Tasarımı
- [x] OOP kavramlarını tekrar et (class, inheritance, encapsulation)
- [x] Fonksiyonel ve nesne yönelimli programlama farklarını öğren
- [x] "Clean Code" kitabından ilk 2 bölümü oku
- [x] Python ile basit bir sentiment analysis modeli geliştir (sklearn veya transformers ile)
- [x] FastAPI kullanarak bu modeli REST API olarak yayınla
- [x] Postman veya curl ile API endpoint'lerini test et
- [x] Kodlarını main.py, requirements.txt ve README.md ile temiz şekilde düzenle

**Proje:** [sentiment-analysis-api](./sentiment-analysis-api/)

### ✅ Hafta 2: Model Deployment – FastAPI + Docker
- [x] Docker nedir, ne işe yarar? Temel mimariyi öğren
- [x] Basit bir Dockerfile oluştur ve API uygulamasını konteynerleştir
- [x] Docker üzerinden servisi ayağa kaldır (port yönlendirmesi dahil)
- [x] .env dosyası kullanarak config yönetimi yap
- [x] Docker Compose ile servis yapılandırmasını otomatize et
- [x] Terminalden log izleme ve hata ayıklama pratiği yap

**Proje:** [docker-learning-project](./docker-learning-project/)

### ✅ Hafta 3: MLOps Girişi – MLflow ile Deney Takibi
- [x] ML lifecycle aşamalarını öğren (training, validation, deployment, monitoring)
- [x] MLflow kurulumu ve local UI başlatmayı öğren
- [x] Sklearn ile küçük bir model eğitip log_params, log_metrics ile izlemeyi dene
- [x] Modelin farklı versiyonlarını karşılaştır
- [x] mlflow.log_artifact() ile model ve görselleri kaydet
- [x] MLflow UI üzerinden geçmiş deneyleri analiz et
- [x] Docker ile MLOps pipeline'ı containerize et
- [x] Model deployment ve monitoring süreçlerini otomatize et

**Proje:** [iris-mlops-project](./iris-mlops-project/)

### 🔄 Hafta 4: LLM Tabanlı RAG Sistemi Kurulumu
- [ ] RAG (Retrieval-Augmented Generation) mimarisini kavra: Retriever + Generator + Prompt
- [ ] PDF dosyasını parçalayıp metinleri OpenAI embedding ile vektörleştir
- [ ] ChromaDB (veya FAISS) ile vektör veritabanı oluştur
- [ ] LangChain ile basit bir "dokümana dayalı chatbot" kur
- [ ] Soru-cevap akışını test et, embedding doğruluğunu ölç
- [ ] Farklı chunk size ve overlap değerleriyle deney yap

### 🔄 Hafta 5: Tool + Agent Sistemleri
- [ ] OpenAI Function Calling dökümantasyonunu oku
- [ ] LangChain'de tool nedir, nasıl tanımlanır öğren
- [ ] "calculator tool" gibi basit bir tool entegre et
- [ ] Hava durumu veya haber API'lerini entegre ederek veri çek
- [ ] ReAct agent yapısını kullanarak çok adımlı bir işlem senaryosu kur
- [ ] Tool seçimlerinin neden önemli olduğunu test ederek kavra

### 🔄 Hafta 6: CI/CD + Takip + Güvenlik
- [ ] Git temel komutlarını (commit, branch, merge, rebase) tekrar et
- [ ] GitHub Actions ile her commit sonrası test ve deploy pipeline'ı oluştur
- [ ] Logging altyapısı kur: Python logging modülü ile merkezi loglama yap
- [ ] .env dosyası ile API key ve config bilgilerini güvenli taşı
- [ ] FastAPI ile CORS, rate limiting, hata yönetimi gibi güvenlik önlemleri ekle
- [ ] Docker ile versiyonlanabilir ve izlenebilir dağıtım yapısı kur

## 🛠️ Kullanılan Teknolojiler

### Backend & API
- **FastAPI** - Modern, hızlı web framework
- **Python** - Ana programlama dili
- **Pydantic** - Veri validasyonu

### Machine Learning
- **Scikit-learn** - ML algoritmaları
- **NumPy** - Sayısal işlemler
- **Pandas** - Veri manipülasyonu
- **MLflow** - ML experiment tracking ve model management

### Deployment & DevOps
- **Docker** - Konteynerleştirme
- **Docker Compose** - Multi-service orchestration
- **Git** - Versiyon kontrolü
- **GitHub** - Kod hosting

### Gelecek Teknolojiler
- **LangChain** - LLM entegrasyonu
- **ChromaDB** - Vektör veritabanı
- **GitHub Actions** - CI/CD

## 📁 Repository Yapısı

```
ai-engineer-lab/
├── sentiment-analysis-api/     # Hafta 1: Sentiment Analysis API
│   ├── app/
│   │   ├── main.py
│   │   └── sentiment_model.py
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_curl.sh
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── docker-learning-project/    # Hafta 2: Docker Deployment
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── database.py
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── config/
│   │   └── env.example
│   ├── scripts/
│   │   ├── build.sh
│   │   ├── run.sh
│   │   └── logs.sh
│   ├── docs/
│   │   ├── docker-basics.md
│   │   └── troubleshooting.md
│   ├── requirements.txt
│   └── README.md
├── iris-mlops-project/         # Hafta 3: MLOps with MLflow
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── training.py
│   │   └── data_processor.py
│   ├── data/
│   │   └── processed/
│   ├── mlflow/
│   │   ├── experiments/
│   │   └── README.md
│   ├── notebooks/
│   │   ├── data_exploration.ipynb
│   │   ├── feature_importance.ipynb
│   │   └── model_comparison.ipynb
│   ├── scripts/
│   │   ├── train_models.sh
│   │   ├── start_mlflow.sh
│   │   └── deploy_model.sh
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── docs/
│   │   ├── api_documentation.md
│   │   └── mlops_basics.md
│   ├── requirements.txt
│   └── README.md
├── [gelecek-proje-4]/         # Hafta 4: RAG System
├── [gelecek-proje-5]/         # Hafta 5: Agent Systems
├── [gelecek-proje-6]/         # Hafta 6: CI/CD
└── README.md                   # Bu dosya
```

## 🚀 Hızlı Başlangıç

### Iris MLOps Project (Hafta 3)
```bash
# Iris MLOps projesini çalıştır
cd iris-mlops-project

# MLflow UI'ı başlat
./scripts/start_mlflow.sh

# Model eğitimi
./scripts/train_models.sh

# Docker ile çalıştır
docker-compose up -d
```

### Docker Learning Project (Hafta 2)
```bash
# Docker projesini çalıştır
cd docker-learning-project

# Build ve run
./scripts/build.sh
./scripts/run.sh
```

### Sentiment Analysis API (Hafta 1)
```bash
# API'yi çalıştır
cd sentiment-analysis-api
python -m uvicorn app.main:app --reload
```

## 📊 Proje Durumu

| Hafta | Proje | Durum | Teknolojiler |
|-------|-------|-------|--------------|
| 1 | Sentiment Analysis API | ✅ Tamamlandı | FastAPI, Scikit-learn |
| 2 | Docker Learning Project | ✅ Tamamlandı | Docker, Docker Compose |
| 3 | Iris MLOps Project | ✅ Tamamlandı | MLflow, Docker, Scikit-learn |
| 4 | RAG System | 🔄 Planlanıyor | LangChain, ChromaDB |
| 5 | Agent Systems | 🔄 Planlanıyor | OpenAI, LangChain |
| 6 | CI/CD Pipeline | 🔄 Planlanıyor | GitHub Actions |

## 🎯 Öğrenme Çıktıları

### Hafta 1-3 Tamamlandı ✅
- **API Tasarımı**: FastAPI ile modern REST API'ler
- **Docker Containerization**: Microservices deployment
- **MLOps Pipeline**: MLflow ile experiment tracking
- **Model Management**: Version control ve deployment
- **Documentation**: Comprehensive README ve API docs

### Gelecek Haftalar 🔄
- **RAG Systems**: Retrieval-Augmented Generation
- **Agent Systems**: Tool integration ve automation
- **CI/CD**: Automated testing ve deployment

## 👤 Geliştirici

**Yasemin ARSLAN**
- [GitHub](https://github.com/YaseminOran)

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---

⭐ Bu repository'yi beğendiyseniz yıldız vermeyi unutmayın! 