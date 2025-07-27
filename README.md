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

### 🔄 Hafta 3: MLOps Girişi – MLflow ile Deney Takibi
- [ ] ML lifecycle aşamalarını öğren (training, validation, deployment, monitoring)
- [ ] MLflow kurulumu ve local UI başlatmayı öğren
- [ ] Sklearn ile küçük bir model eğitip log_params, log_metrics ile izlemeyi dene
- [ ] Modelin farklı versiyonlarını karşılaştır
- [ ] mlflow.log_artifact() ile model ve görselleri kaydet
- [ ] MLflow UI üzerinden geçmiş deneyleri analiz et

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

### Deployment & DevOps
- **Docker** - Konteynerleştirme
- **Docker Compose** - Multi-service orchestration
- **Git** - Versiyon kontrolü
- **GitHub** - Kod hosting

### Gelecek Teknolojiler
- **MLflow** - ML deney takibi
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
<<<<<<< HEAD
├── docker-learning-project/    # Hafta 2: Docker Learning Project
=======
├── docker-learning-project/    # Hafta 2: Docker Deployment
>>>>>>> fdaca2c0aa3c8f9b89adffbbfe594abef5262f88
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── database.py
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
<<<<<<< HEAD
│   ├── config/
│   │   └── env.example
=======
>>>>>>> fdaca2c0aa3c8f9b89adffbbfe594abef5262f88
│   ├── scripts/
│   │   ├── build.sh
│   │   ├── run.sh
│   │   └── logs.sh
│   ├── docs/
│   │   ├── docker-basics.md
│   │   └── troubleshooting.md
<<<<<<< HEAD
│   ├── requirements.txt
│   └── README.md
├── [gelecek-proje-3]/         # Hafta 3: MLflow
├── [gelecek-proje-4]/         # Hafta 4: RAG System
├── [gelecek-proje-5]/         # Hafta 5: Agent Systems
├── [gelecek-proje-6]/         # Hafta 6: CI/CD
=======
│   └── README.md
├── [gelecek-proje-1]/         # Hafta 3: MLflow
├── [gelecek-proje-2]/         # Hafta 4: RAG System
├── [gelecek-proje-3]/         # Hafta 5: Agent Systems
├── [gelecek-proje-4]/         # Hafta 6: CI/CD
>>>>>>> fdaca2c0aa3c8f9b89adffbbfe594abef5262f88
└── README.md                   # Bu dosya
```

## 👤 Geliştirici

**Yasemin ARSLAN**
- [GitHub](https://github.com/YaseminOran)

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---

⭐ Bu repository'yi beğendiyseniz yıldız vermeyi unutmayın! 