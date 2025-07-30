#!/bin/bash

# Model Eğitimi Scripti
echo "🌸 Iris Model Eğitimi Başlatılıyor..."

# Environment variables
export MLFLOW_TRACKING_URI=http://localhost:5003
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Gerekli dizinleri oluştur
mkdir -p mlflow/artifacts
mkdir -p data/processed

# Model eğitimi başlat
echo "Model eğitimi başlatılıyor..."
python -c "
import sys
import os
sys.path.append(os.getcwd())

from app.data_processor import load_iris_data, preprocess_data
from app.training import train_models, compare_models

# Veri yükle
print('📊 Veri yükleniyor...')
data = load_iris_data('data/raw/iris.csv')

# Veri ön işleme
print('🔧 Veri ön işleme...')
X_train, X_test, y_train, y_test = preprocess_data(data)

# Model eğitimi
print('🤖 Model eğitimi başlatılıyor...')
experiment_name = 'iris_baseline_$(date +%Y%m%d_%H%M%S)'
models = train_models(X_train, y_train, X_test, y_test, experiment_name)

# Model karşılaştırması
print('📈 Model karşılaştırması...')
comparison = compare_models(models)

print('✅ Model eğitimi tamamlandı!')
print(f'📊 En iyi model: {max(models.keys(), key=lambda k: models[k]["accuracy"])}')
print(f'🎯 En yüksek accuracy: {max(models[k]["accuracy"] for k in models):.4f}')
"

echo "✅ Model eğitimi tamamlandı!"
echo "🌐 MLflow UI'da sonuçları görün: http://localhost:5003" 