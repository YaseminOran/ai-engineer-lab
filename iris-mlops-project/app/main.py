from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
from datetime import datetime
from typing import List, Optional
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
import json

from .models import IrisFeatures, PredictionResponse, ModelInfo, HealthCheck
from .data_processor import load_iris_data, preprocess_data
from .training import train_models, get_best_model

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Iris Flower Classification API",
    description="MLOps projesi - Iris çiçeği sınıflandırma API'si",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MLflow setup
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5001")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Global variables
current_model = None
model_info = None

@app.on_event("startup")
async def startup_event():
    """Uygulama başlatıldığında çalışır"""
    global current_model, model_info
    
    logger.info("Iris Classification API başlatılıyor...")
    
    try:
        # MLflow bağlantısını kontrol et
        mlflow.get_tracking_uri()
        logger.info(f"MLflow tracking URI: {MLFLOW_TRACKING_URI}")
        
        # En iyi modeli yükle
        current_model, model_info = await load_best_model()
        
        if current_model:
            logger.info(f"Model yüklendi: {model_info['model_name']} v{model_info['version']}")
        else:
            logger.warning("Model bulunamadı, yeni model eğitilecek...")
            await train_initial_model()
            
    except Exception as e:
        logger.error(f"Startup hatası: {e}")
        await train_initial_model()

async def train_initial_model():
    """İlk model eğitimi"""
    global current_model, model_info
    
    try:
        logger.info("İlk model eğitimi başlatılıyor...")
        
        # Veri yükle
        data = load_iris_data("data/raw/iris.csv")
        X_train, X_test, y_train, y_test = preprocess_data(data)
        
        # Model eğit
        models = train_models(X_train, y_train, X_test, y_test, experiment_name="iris_initial")
        
        # En iyi modeli seç
        best_model_name = "random_forest"  # Default olarak Random Forest
        current_model = models[best_model_name]['model']
        model_info = {
            'model_name': best_model_name,
            'version': '1.0.0',
            'accuracy': models[best_model_name]['accuracy'],
            'training_date': datetime.now().isoformat()
        }
        
        logger.info(f"İlk model eğitimi tamamlandı: {best_model_name}")
        
    except Exception as e:
        logger.error(f"Model eğitimi hatası: {e}")
        raise

async def load_best_model():
    """En iyi modeli MLflow'dan yükle"""
    try:
        # Model registry'den en son modeli al
        model_name = "iris_classifier"
        
        # MLflow'dan model yükle
        model_uri = f"models:/{model_name}/latest"
        model = mlflow.sklearn.load_model(model_uri)
        
        # Model bilgilerini al
        client = mlflow.tracking.MlflowClient()
        latest_version = client.get_latest_versions(model_name, stages=["Production"])[0]
        
        model_info = {
            'model_name': model_name,
            'version': latest_version.version,
            'run_id': latest_version.run_id,
            'status': latest_version.status,
            'last_updated': latest_version.last_updated_timestamp
        }
        
        return model, model_info
        
    except Exception as e:
        logger.warning(f"Model yükleme hatası: {e}")
        return None, None

@app.get("/", response_model=dict)
async def root():
    """Ana endpoint"""
    return {
        "message": "🌸 Iris Flower Classification API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "predict_batch": "/predict/batch",
            "model_info": "/model/info",
            "retrain": "/model/retrain",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Sağlık kontrolü"""
    try:
        model_status = current_model is not None
        mlflow_status = mlflow.get_tracking_uri() is not None
        
        return HealthCheck(
            status="healthy" if model_status and mlflow_status else "unhealthy",
            timestamp=datetime.now(),
            model_loaded=model_status,
            mlflow_connected=mlflow_status,
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check hatası: {e}")
        return HealthCheck(
            status="unhealthy",
            timestamp=datetime.now(),
            model_loaded=False,
            mlflow_connected=False,
            version="1.0.0"
        )

@app.post("/predict", response_model=PredictionResponse)
async def predict_iris(features: IrisFeatures):
    """Tekil tahmin"""
    try:
        if current_model is None:
            raise HTTPException(status_code=503, detail="Model yüklenemedi")
        
        # Özellikleri numpy array'e çevir
        input_data = np.array([[
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]])
        
        # Tahmin yap
        prediction = current_model.predict(input_data)[0]
        probabilities = current_model.predict_proba(input_data)[0]
        
        # Sınıf isimlerini al
        class_names = ['setosa', 'versicolor', 'virginica']
        predicted_class = class_names[prediction]
        
        # Güven skorları
        confidence_scores = {
            'setosa': float(probabilities[0]),
            'versicolor': float(probabilities[1]),
            'virginica': float(probabilities[2])
        }
        
        return PredictionResponse(
            prediction=predicted_class,
            confidence=float(max(probabilities)),
            confidence_scores=confidence_scores,
            model_version=model_info['version'] if model_info else "unknown",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Tahmin hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")

@app.post("/predict/batch", response_model=List[PredictionResponse])
async def predict_batch(features_list: List[IrisFeatures]):
    """Toplu tahmin"""
    try:
        if current_model is None:
            raise HTTPException(status_code=503, detail="Model yüklenemedi")
        
        predictions = []
        
        for features in features_list:
            input_data = np.array([[
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width
            ]])
            
            prediction = current_model.predict(input_data)[0]
            probabilities = current_model.predict_proba(input_data)[0]
            
            class_names = ['setosa', 'versicolor', 'virginica']
            predicted_class = class_names[prediction]
            
            confidence_scores = {
                'setosa': float(probabilities[0]),
                'versicolor': float(probabilities[1]),
                'virginica': float(probabilities[2])
            }
            
            predictions.append(PredictionResponse(
                prediction=predicted_class,
                confidence=float(max(probabilities)),
                confidence_scores=confidence_scores,
                model_version=model_info['version'] if model_info else "unknown",
                timestamp=datetime.now()
            ))
        
        return predictions
        
    except Exception as e:
        logger.error(f"Toplu tahmin hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Toplu tahmin hatası: {str(e)}")

@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Model bilgilerini getir"""
    if model_info is None:
        raise HTTPException(status_code=404, detail="Model bilgisi bulunamadı")
    
    return ModelInfo(
        name=model_info['model_name'],
        version=model_info['version'],
        accuracy=model_info.get('accuracy', 0.0),
        training_date=model_info.get('training_date', datetime.now().isoformat()),
        status="loaded" if current_model else "not_loaded"
    )

@app.post("/model/retrain")
async def retrain_model():
    """Modeli yeniden eğit"""
    try:
        logger.info("Model yeniden eğitimi başlatılıyor...")
        
        # Veri yükle
        data = load_iris_data("data/raw/iris.csv")
        X_train, X_test, y_train, y_test = preprocess_data(data)
        
        # Yeni experiment ile eğit
        experiment_name = f"iris_retrain_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        models = train_models(X_train, y_train, experiment_name=experiment_name)
        
        # En iyi modeli seç
        best_model_name = max(models.keys(), key=lambda k: models[k]['accuracy'])
        global current_model, model_info
        
        current_model = models[best_model_name]['model']
        model_info = {
            'model_name': best_model_name,
            'version': f"{model_info['version']}.1" if model_info else "1.0.0",
            'accuracy': models[best_model_name]['accuracy'],
            'training_date': datetime.now().isoformat(),
            'experiment_name': experiment_name
        }
        
        logger.info(f"Model yeniden eğitimi tamamlandı: {best_model_name}")
        
        return {
            "message": "Model başarıyla yeniden eğitildi",
            "model_name": best_model_name,
            "accuracy": models[best_model_name]['accuracy'],
            "experiment_name": experiment_name
        }
        
    except Exception as e:
        logger.error(f"Model yeniden eğitimi hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Model yeniden eğitimi hatası: {str(e)}")

@app.get("/experiments")
async def list_experiments():
    """MLflow deneylerini listele"""
    try:
        experiments = mlflow.list_experiments()
        
        return {
            "experiments": [
                {
                    "name": exp.name,
                    "experiment_id": exp.experiment_id,
                    "lifecycle_stage": exp.lifecycle_stage
                }
                for exp in experiments
            ]
        }
        
    except Exception as e:
        logger.error(f"Deney listesi hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Deney listesi hatası: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 