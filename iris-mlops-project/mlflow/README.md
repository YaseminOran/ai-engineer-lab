# MLflow Directory

Bu klasör, MLflow tracking server'ının tüm verilerini ve artifacts'larını içerir.

## Klasör Yapısı

```
mlflow/
├── README.md                    # Bu dosya
├── artifacts/                   # Model artifacts'ları
│   ├── README.md              # Artifacts açıklaması
│   ├── models/                # Kaydedilen modeller
│   ├── experiments/           # Deney sonuçları
│   └── metrics/              # Model metrikleri
├── experiments/               # Deney metadata'ları
│   ├── README.md             # Experiments açıklaması
│   ├── iris_initial/         # İlk deney
│   ├── iris_manual_training/ # Manuel eğitim deneyi
│   └── iris_retraining/      # Yeniden eğitim deneyi
└── mlflow.db                 # SQLite veritabanı
```

## MLflow Bileşenleri

### 1. Tracking Server
- **Port**: 5001
- **Backend**: SQLite
- **Artifact Store**: Local filesystem
- **Model Registry**: Aktif

### 2. Model Registry
- **Model Name**: iris_classifier
- **Versiyonlar**: 3
- **En Son Versiyon**: 3 (SVM, 0.97 accuracy)

### 3. Experiments
- **iris_initial**: İlk model eğitimi
- **iris_manual_training**: Manuel eğitim
- **iris_retraining**: Yeniden eğitim

## Kullanım

### MLflow Server Başlatma
```bash
# Varsayılan port (5001)
mlflow server --host 0.0.0.0 --port 5001 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlflow/artifacts

# Farklı port
mlflow server --host 0.0.0.0 --port 5002 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlflow/artifacts
```

### MLflow UI Erişimi
```bash
# Web tarayıcısında açın
http://localhost:5001
```

### Programatik Erişim
```python
import mlflow

# Tracking URI ayarlama
mlflow.set_tracking_uri("http://localhost:5001")

# Deney listesi
experiments = mlflow.list_experiments()
print(experiments)

# Model registry
models = mlflow.list_registered_models()
print(models)

# Model yükleme
model = mlflow.sklearn.load_model("models:/iris_classifier/latest")
```

## Model Registry

### Kayıtlı Modeller
1. **iris_classifier**
   - Versiyon 1: Random Forest (0.96 accuracy)
   - Versiyon 2: SVM (0.97 accuracy)
   - Versiyon 3: SVM (0.97 accuracy)

### Model Deployment
```python
# En son modeli yükleme
model = mlflow.sklearn.load_model("models:/iris_classifier/latest")

# Belirli bir versiyonu yükleme
model = mlflow.sklearn.load_model("models:/iris_classifier/2")

# Model tahmin
prediction = model.predict([[5.1, 3.5, 1.4, 0.2]])
```

## Deney Takibi

### Metrikler
- **Accuracy**: Model doğruluğu
- **Precision**: Kesinlik
- **Recall**: Duyarlılık
- **F1-Score**: F1 skoru
- **Training Time**: Eğitim süresi

### Parametreler
- **Model Type**: Algoritma türü
- **Hyperparameters**: Hiperparametreler
- **Random State**: Rastgele durum

### Artifacts
- **Models**: Eğitilmiş modeller
- **Plots**: Görselleştirmeler
- **Metrics**: Detaylı metrikler

## Monitoring

### Health Check
```bash
# MLflow server durumu
curl http://localhost:5001/health

# Model registry durumu
mlflow models list
```

### Logs
```bash
# MLflow server logları
tail -f mlflow.log

# Model registry logları
mlflow models describe iris_classifier
```

## Backup ve Restore

### Backup
```bash
# Veritabanı yedekleme
cp mlflow.db mlflow_backup.db

# Artifacts yedekleme
tar -czf mlflow_artifacts_backup.tar.gz artifacts/
```

### Restore
```bash
# Veritabanı geri yükleme
cp mlflow_backup.db mlflow.db

# Artifacts geri yükleme
tar -xzf mlflow_artifacts_backup.tar.gz
```

## Troubleshooting

### Yaygın Sorunlar

1. **Port çakışması**
   ```bash
   # Kullanılan portları kontrol et
   lsof -i :5001
   
   # Farklı port kullan
   mlflow server --port 5002
   ```

2. **Artifact bulunamıyor**
   ```bash
   # Artifact path'ini kontrol et
   ls -la artifacts/
   
   # MLflow server'ı yeniden başlat
   mlflow server --default-artifact-root ./mlflow/artifacts
   ```

3. **Model yüklenemiyor**
   ```python
   # Model registry'yi kontrol et
   mlflow.list_registered_models()
   
   # Model versiyonlarını kontrol et
   mlflow.list_model_versions("iris_classifier")
   ```

### Debug Commands
```bash
# MLflow server durumu
ps aux | grep mlflow

# Port kullanımı
netstat -tulpn | grep 5001

# Disk kullanımı
du -sh mlflow/

# Veritabanı boyutu
ls -lh mlflow.db
```

## Notlar

- MLflow server'ı production'da PostgreSQL kullanmalı
- Artifacts büyükse external storage kullanın
- Düzenli backup alın
- Model registry'yi düzenli temizleyin
- Monitoring ve alerting ekleyin 