# 🌸 Iris Flower Classification - MLOps Project

Bu proje, MLOps (Machine Learning Operations) kavramlarını **Iris çiçeği sınıflandırma** problemi üzerinden öğrenmek için tasarlanmıştır. MLflow kullanarak model lifecycle'ını yönetmeyi, deney takibini ve model deployment'ını pratik edebilirsiniz.

## 🎯 Proje Hedefi

Iris çiçeğinin 4 özelliğini (sepal length, sepal width, petal length, petal width) kullanarak 3 farklı türü (setosa, versicolor, virginica) sınıflandıran bir ML modeli geliştirmek ve MLOps pipeline'ı kurmak.

## 📚 Öğrenme Hedefleri

- [x] **ML lifecycle aşamalarını öğren** - Data → Training → Evaluation → Deployment
- [x] **MLflow kurulumu ve local UI başlatmayı öğren** - Experiment tracking
- [x] **Sklearn ile farklı modeller eğitip log_params, log_metrics ile izlemeyi dene** - Model training
- [x] **Modelin farklı versiyonlarını karşılaştır** - Version comparison
- [x] **mlflow.log_artifact() ile model ve görselleri kaydet** - Artifact management
- [x] **MLflow UI üzerinden geçmiş deneyleri analiz et** - Experiment analysis

## 🏗️ Proje Mimarisi

```
iris-mlops-project/
├── app/                    # Ana uygulama
│   ├── main.py            # FastAPI + MLflow integration
│   ├── models.py          # Pydantic schemas
│   ├── training.py        # Model training pipeline
│   ├── evaluation.py      # Model evaluation logic
│   └── data_processor.py  # Data preprocessing
├── data/                  # Veri setleri
│   ├── raw/              # Ham veriler (iris.csv)
│   └── processed/        # İşlenmiş veriler
├── mlflow/                # MLflow konfigürasyonu
│   └── experiments/       # Deney dosyaları
├── notebooks/             # Jupyter notebooks
│   ├── data_exploration.ipynb
│   ├── model_comparison.ipynb
│   └── feature_importance.ipynb
├── scripts/               # Yardımcı scriptler
│   ├── train_models.sh   # Model training
│   ├── start_mlflow.sh   # MLflow UI
│   └── deploy_model.sh   # Model deployment
├── docker/                # Docker dosyaları
│   ├── Dockerfile        # MLflow + FastAPI
│   └── docker-compose.yml # Multi-service orchestration
├── docs/                  # Dokümantasyon
│   ├── mlflow-basics.md  # MLflow temelleri
│   └── mlops-practices.md # MLOps pratikleri
├── requirements.txt       # Python bağımlılıkları
└── README.md             # Bu dosya
```

## 🚀 Hızlı Başlangıç

### 1. Projeyi Klonlayın
```bash
git clone <repository-url>
cd iris-mlops-project
```

### 2. Environment Hazırlayın
```bash
# Virtual environment oluşturun
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 3. Veri Setini Hazırlayın
```bash
# Iris dataset'ini indirin
python -c "from sklearn.datasets import load_iris; import pandas as pd; iris = load_iris(); df = pd.DataFrame(iris.data, columns=iris.feature_names); df['target'] = iris.target; df['target_name'] = iris.target_names[iris.target]; df.to_csv('data/raw/iris.csv', index=False)"
```

### 4. MLflow UI Başlatın
```bash
./scripts/start_mlflow.sh
```

### 5. Model Eğitin
```bash
./scripts/train_models.sh
```

### 6. FastAPI Uygulamasını Başlatın
```bash
./scripts/deploy_model.sh
```

## 🧪 MLOps Pipeline

### 1. Data Pipeline
```python
# Veri yükleme ve işleme
from app.data_processor import load_iris_data, preprocess_data

# Veri yükle
data = load_iris_data("data/raw/iris.csv")

# Veri işleme
X_train, X_test, y_train, y_test = preprocess_data(data)
```

### 2. Training Pipeline
```python
# Model eğitimi ve MLflow tracking
from app.training import train_models

# Farklı modelleri eğit
models = train_models(X_train, y_train, experiment_name="iris_classification")
```

### 3. Evaluation Pipeline
```python
# Model değerlendirme
from app.evaluation import evaluate_models

# Modelleri değerlendir
results = evaluate_models(models, X_test, y_test)
```

### 4. Deployment Pipeline
```python
# Model deployment
from app.main import load_best_model

# En iyi modeli yükle
model = load_best_model("iris_classifier", "latest")
```

## 🛠️ Kullanılan Teknolojiler

### Machine Learning
- **Scikit-learn** - ML algoritmaları (Logistic Regression, Random Forest, SVM)
- **Pandas** - Veri manipülasyonu
- **NumPy** - Sayısal işlemler
- **Matplotlib/Seaborn** - Görselleştirme

### MLOps Tools
- **MLflow** - Experiment tracking ve model registry
- **FastAPI** - Model serving API
- **Docker** - Containerization
- **PostgreSQL** - MLflow backend

### Development
- **Jupyter Notebook** - Data exploration ve model development
- **Git** - Version control
- **Shell Scripts** - Automation

## 📊 Model Algoritmaları

### 1. Logistic Regression
```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(random_state=42)
mlflow.log_params({"algorithm": "logistic_regression", "random_state": 42})
```

### 2. Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
mlflow.log_params({"algorithm": "random_forest", "n_estimators": 100})
```

### 3. Support Vector Machine
```python
from sklearn.svm import SVC

model = SVC(kernel='rbf', random_state=42)
mlflow.log_params({"algorithm": "svm", "kernel": "rbf"})
```

## 🔧 Kullanım Örnekleri

### Model Eğitimi
```bash
# Tüm modelleri eğit
python app/training.py --experiment-name "iris_baseline"

# Belirli bir modeli eğit
python app/training.py --model logistic_regression --experiment-name "logistic_test"

# Hiperparametre optimizasyonu
python app/training.py --optimize --experiment-name "hyperopt_tuning"
```

### Model Karşılaştırma
```bash
# MLflow UI'da model karşılaştırma
mlflow ui --port 5000

# Programatik karşılaştırma
python notebooks/model_comparison.ipynb
```

### Model Deployment
```bash
# Docker ile deployment
docker-compose up -d

# API test
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

## 📈 Monitoring ve Analytics

### MLflow UI
- **Experiment Tracking**: Deney geçmişi ve parametreler
- **Model Registry**: Model versiyonları ve metadata
- **Artifact Browser**: Model dosyaları ve görseller
- **Metrics Comparison**: Accuracy, precision, recall karşılaştırması

### FastAPI Monitoring
- **Health Endpoints**: Servis sağlığı
- **Performance Metrics**: API response time
- **Request Logging**: Prediction logları
- **Error Tracking**: Model prediction hataları

## 🐳 Docker Orchestration

### Multi-service Architecture
```yaml
services:
  mlflow:
    image: python:3.11-slim
    command: mlflow server --host 0.0.0.0 --port 5000
    ports:
      - "5000:5000"
  
  fastapi:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mlflow
  
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=mlflow
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## 📚 Öğrenme Kaynakları

### MLOps Dokümantasyonu
- [MLflow Official Docs](https://mlflow.org/docs/latest/index.html)
- [MLOps Best Practices](https://ml-ops.org/)
- [Model Deployment Guide](https://mlflow.org/docs/latest/models.html)

### Iris Dataset
- [Iris Dataset Documentation](https://scikit-learn.org/stable/datasets/toy_dataset.html#iris-dataset)
- [Iris Classification Tutorial](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html)

### Video Eğitimler
- [MLflow Tutorial](https://www.youtube.com/watch?v=1ykiI-qcImo)
- [MLOps Fundamentals](https://www.youtube.com/watch?v=9BgIDqAzfuA)

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👨‍💻 Geliştirici

Bu proje MLOps öğrenme amaçlı oluşturulmuştur. Sorularınız için issue açabilirsiniz.

---

**Not**: Bu proje eğitim amaçlıdır ve production ortamında kullanılmadan önce güvenlik ve performans optimizasyonları yapılmalıdır. 