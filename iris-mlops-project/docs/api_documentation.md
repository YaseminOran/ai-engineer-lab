# Iris Classification API Dokümantasyonu

## Genel Bakış

Iris Classification API, makine öğrenmesi modellerini kullanarak Iris çiçeği türlerini sınıflandırmak için geliştirilmiş bir REST API'dir. API, MLflow ile entegre çalışarak model versiyonlama ve deney takibi sağlar.

## Base URL

```
http://localhost:8006
```

## Endpoints

### 1. Health Check

**GET** `/health`

API'nin sağlık durumunu kontrol eder.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "model_loaded": true,
  "mlflow_connected": true,
  "version": "1.0.0"
}
```

### 2. Root Endpoint

**GET** `/`

API hakkında genel bilgi verir.

**Response:**
```json
{
  "message": "Iris Classification API",
  "version": "1.0.0",
  "description": "MLOps projesi - Iris çiçeği sınıflandırma API'si"
}
```

### 3. Single Prediction

**POST** `/predict`

Tek bir Iris çiçeği için tahmin yapar.

**Request Body:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response:**
```json
{
  "prediction": "setosa",
  "confidence": 0.95,
  "confidence_scores": {
    "setosa": 0.95,
    "versicolor": 0.03,
    "virginica": 0.02
  },
  "model_version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 4. Batch Prediction

**POST** `/predict/batch`

Birden fazla Iris çiçeği için toplu tahmin yapar.

**Request Body:**
```json
{
  "features": [
    {
      "sepal_length": 5.1,
      "sepal_width": 3.5,
      "petal_length": 1.4,
      "petal_width": 0.2
    },
    {
      "sepal_length": 6.3,
      "sepal_width": 3.3,
      "petal_length": 4.7,
      "petal_width": 1.6
    }
  ]
}
```

**Response:**
```json
[
  {
    "prediction": "setosa",
    "confidence": 0.95,
    "confidence_scores": {
      "setosa": 0.95,
      "versicolor": 0.03,
      "virginica": 0.02
    },
    "model_version": "1.0.0",
    "timestamp": "2024-01-15T10:30:00"
  },
  {
    "prediction": "versicolor",
    "confidence": 0.87,
    "confidence_scores": {
      "setosa": 0.01,
      "versicolor": 0.87,
      "virginica": 0.12
    },
    "model_version": "1.0.0",
    "timestamp": "2024-01-15T10:30:01"
  }
]
```

### 5. Model Information

**GET** `/model/info`

Mevcut model hakkında bilgi verir.

**Response:**
```json
{
  "name": "random_forest",
  "version": "1.0.0",
  "accuracy": 0.96,
  "training_date": "2024-01-15T10:00:00",
  "status": "loaded"
}
```

### 6. Model Retraining

**POST** `/model/retrain`

Yeni bir model eğitir ve MLflow'a kaydeder.

**Request Body:**
```json
{
  "experiment_name": "iris_retraining",
  "model_type": "random_forest",
  "hyperparameters": {
    "n_estimators": 100,
    "max_depth": 10
  }
}
```

**Response:**
```json
{
  "message": "Model başarıyla eğitildi",
  "model_name": "random_forest",
  "accuracy": 0.97,
  "experiment_name": "iris_retraining",
  "training_time": 2.5
}
```

### 7. Experiments List

**GET** `/experiments`

MLflow'daki deneyleri listeler.

**Response:**
```json
[
  {
    "name": "iris_initial",
    "experiment_id": "1",
    "lifecycle_stage": "active",
    "run_count": 3,
    "last_updated": "2024-01-15T10:00:00"
  },
  {
    "name": "iris_retraining",
    "experiment_id": "2",
    "lifecycle_stage": "active",
    "run_count": 1,
    "last_updated": "2024-01-15T11:00:00"
  }
]
```

## Data Models

### IrisFeatures
```json
{
  "sepal_length": "float (0-10)",
  "sepal_width": "float (0-10)",
  "petal_length": "float (0-10)",
  "petal_width": "float (0-10)"
}
```

### PredictionResponse
```json
{
  "prediction": "string (setosa|versicolor|virginica)",
  "confidence": "float (0-1)",
  "confidence_scores": "object",
  "model_version": "string",
  "timestamp": "datetime"
}
```

### ModelInfo
```json
{
  "name": "string",
  "version": "string",
  "accuracy": "float (0-1)",
  "training_date": "string",
  "status": "string"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

## Kullanım Örnekleri

### cURL ile Test

**Health Check:**
```bash
curl -X GET "http://localhost:8006/health"
```

**Single Prediction:**
```bash
curl -X POST "http://localhost:8006/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

**Batch Prediction:**
```bash
curl -X POST "http://localhost:8006/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
      },
      {
        "sepal_length": 6.3,
        "sepal_width": 3.3,
        "petal_length": 4.7,
        "petal_width": 1.6
      }
    ]
  }'
```

### Python ile Test

```python
import requests
import json

# Health check
response = requests.get("http://localhost:8006/health")
print(response.json())

# Single prediction
data = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
response = requests.post("http://localhost:8006/predict", json=data)
print(response.json())
```

## Monitoring

### Health Check Endpoints
- `/health`: API sağlık durumu
- `/model/info`: Model bilgileri

### Metrics
- Model doğruluğu
- Tahmin güven skorları
- API response time
- Model yükleme durumu

### Logging
API tüm istekleri ve hataları loglar:
- Request/response logları
- Model eğitimi logları
- Error logları

## Güvenlik

### Input Validation
- Tüm input'lar Pydantic ile validate edilir
- Özellik değerleri 0-10 arasında olmalı
- Required field'lar kontrol edilir

### Error Handling
- Validation hataları 400 döner
- Model hataları 500 döner
- Detaylı error mesajları

## Deployment

### Docker ile Çalıştırma
```bash
docker build -t iris-api .
docker run -p 8006:8006 iris-api
```

### Environment Variables
```bash
MLFLOW_TRACKING_URI=http://localhost:5001
MODEL_NAME=iris_classifier
API_PORT=8006
```

## Troubleshooting

### Yaygın Hatalar

1. **Model yüklenemiyor**
   - MLflow server'ın çalıştığından emin olun
   - Model registry'de model olduğunu kontrol edin

2. **MLflow bağlantı hatası**
   - MLflow tracking URI'yi kontrol edin
   - Network bağlantısını test edin

3. **Validation hatası**
   - Input değerlerinin 0-10 arasında olduğunu kontrol edin
   - Tüm required field'ların dolu olduğunu kontrol edin

### Debug Commands
```bash
# API loglarını kontrol et
docker logs iris-api

# MLflow server durumunu kontrol et
curl http://localhost:5001/health

# Model registry'yi kontrol et
mlflow models list
``` 