#!/bin/bash

# MLflow UI Başlatma Scripti
echo "🌸 MLflow UI başlatılıyor..."

# MLflow tracking URI'yi ayarla
export MLFLOW_TRACKING_URI=http://localhost:5003

# MLflow server'ı başlat
echo "MLflow server başlatılıyor..."
mlflow server \
    --host 0.0.0.0 \
    --port 5003 \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlflow/artifacts

echo "✅ MLflow UI başlatıldı!"
echo "🌐 Tarayıcıda açın: http://localhost:5003" 