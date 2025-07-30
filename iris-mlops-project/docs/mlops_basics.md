# MLOps Temelleri

## MLOps Nedir?

MLOps (Machine Learning Operations), makine öğrenmesi modellerinin yaşam döngüsünü yönetmek için kullanılan bir yaklaşımdır. DevOps'un ML dünyasına uyarlanmış halidir.

## MLOps Yaşam Döngüsü

### 1. Veri Yönetimi (Data Management)
- **Veri Toplama**: Ham verilerin toplanması
- **Veri Temizleme**: Eksik değerler, aykırı değerler
- **Veri Doğrulama**: Veri kalitesi kontrolü
- **Veri Versiyonlama**: DVC, Git LFS gibi araçlar

### 2. Model Geliştirme (Model Development)
- **Deney Tasarımı**: Farklı algoritmaların test edilmesi
- **Hiperparametre Optimizasyonu**: Grid search, Bayesian optimization
- **Model Değerlendirme**: Cross-validation, metrikler
- **Model Versiyonlama**: Model kayıtları

### 3. Model Deployment (Model Deployment)
- **Model Paketleme**: Docker, model formatları
- **API Geliştirme**: REST API, gRPC
- **A/B Testing**: Farklı modellerin karşılaştırılması
- **Canary Deployment**: Kademeli yayınlama

### 4. Model Monitoring (Model Monitoring)
- **Performans İzleme**: Drift detection
- **Veri Kalitesi**: Input validation
- **Sistem Sağlığı**: Uptime, latency
- **Alerting**: Anomali tespiti

## MLOps Araçları

### Deney Takibi
- **MLflow**: Deney yönetimi ve model registry
- **Weights & Biases**: Deney takibi ve görselleştirme
- **TensorBoard**: TensorFlow deney takibi

### Model Deployment
- **Kubernetes**: Container orchestration
- **Docker**: Konteynerleştirme
- **FastAPI**: API geliştirme
- **Flask**: Web framework

### Monitoring
- **Prometheus**: Metrik toplama
- **Grafana**: Görselleştirme
- **Evidently**: ML model monitoring
- **Great Expectations**: Veri validasyonu

## MLOps Best Practices

### 1. Otomasyon
- CI/CD pipeline'ları
- Otomatik model eğitimi
- Otomatik deployment

### 2. Versiyonlama
- Kod versiyonlama (Git)
- Veri versiyonlama (DVC)
- Model versiyonlama (MLflow)

### 3. Monitoring
- Model drift detection
- Performans metrikleri
- Sistem sağlığı

### 4. Güvenlik
- API key yönetimi
- Veri şifreleme
- Access control

## Iris Projesi MLOps Uygulaması

### Proje Yapısı
```
iris-mlops-project/
├── app/                    # FastAPI uygulaması
├── data/                   # Veri setleri
├── mlflow/                 # MLflow artifacts
├── notebooks/              # Jupyter notebooks
├── scripts/                # Otomasyon scriptleri
├── docker/                 # Docker yapılandırması
└── docs/                   # Dokümantasyon
```

### MLOps Pipeline
1. **Veri Yükleme**: `data_processor.py`
2. **Model Eğitimi**: `training.py`
3. **Deney Takibi**: MLflow
4. **API Deployment**: FastAPI
5. **Monitoring**: Health checks

### Kullanılan Teknolojiler
- **MLflow**: Deney takibi ve model registry
- **FastAPI**: REST API
- **Scikit-learn**: ML algoritmaları
- **Docker**: Konteynerleştirme
- **PostgreSQL**: Model metadata

## Öğrenme Hedefleri

### Temel Kavramlar
- [x] MLOps yaşam döngüsü
- [x] Deney takibi (MLflow)
- [x] Model registry
- [x] API deployment
- [x] Monitoring

### Pratik Uygulamalar
- [x] Iris sınıflandırma projesi
- [x] MLflow deney yönetimi
- [x] FastAPI ile model serving
- [x] Docker containerization
- [x] Health monitoring

### İleri Seviye
- [ ] CI/CD pipeline
- [ ] A/B testing
- [ ] Model drift detection
- [ ] AutoML
- [ ] Kubernetes deployment

## Kaynaklar

### Dokümantasyon
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)

### Makaleler
- [MLOps: Continuous delivery and automation pipelines in machine learning](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- [The State of MLOps](https://mlops.community/state-of-mlops/)

### Kurslar
- [MLOps Fundamentals](https://www.coursera.org/specializations/mlops)
- [Machine Learning Engineering for Production](https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops) 