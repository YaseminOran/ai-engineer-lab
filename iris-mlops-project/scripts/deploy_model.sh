#!/bin/bash

# Model Deployment Scripti
echo "🌸 Iris Model Deployment Başlatılıyor..."

# Environment variables
export MLFLOW_TRACKING_URI=http://localhost:5001
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# FastAPI uygulamasını başlat
echo "🚀 FastAPI uygulaması başlatılıyor..."
echo "📊 Model yükleniyor..."
echo "🔗 API endpoints:"
echo "   - Health: http://localhost:8001/health"
echo "   - Predict: http://localhost:8001/predict"
echo "   - Model Info: http://localhost:8001/model/info"
echo "   - Docs: http://localhost:8001/docs"

# FastAPI uygulamasını başlat
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

echo "✅ Model deployment tamamlandı!"
echo "🌐 API dokümantasyonu: http://localhost:8001/docs" 