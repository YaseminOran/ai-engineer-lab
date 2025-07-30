from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class IrisSpecies(str, Enum):
    """Iris türleri"""
    SETOSA = "setosa"
    VERSICOLOR = "versicolor"
    VIRGINICA = "virginica"

class IrisFeatures(BaseModel):
    """Iris çiçeği özellikleri"""
    sepal_length: float = Field(..., ge=0, le=10, description="Sepal uzunluğu (cm)")
    sepal_width: float = Field(..., ge=0, le=10, description="Sepal genişliği (cm)")
    petal_length: float = Field(..., ge=0, le=10, description="Petal uzunluğu (cm)")
    petal_width: float = Field(..., ge=0, le=10, description="Petal genişliği (cm)")
    
    class Config:
        schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }

class PredictionResponse(BaseModel):
    """Tahmin sonucu"""
    prediction: str = Field(..., description="Tahmin edilen tür")
    confidence: float = Field(..., ge=0, le=1, description="Güven skoru")
    confidence_scores: Dict[str, float] = Field(..., description="Her tür için güven skorları")
    model_version: str = Field(..., description="Model versiyonu")
    timestamp: datetime = Field(..., description="Tahmin zamanı")
    
    class Config:
        schema_extra = {
            "example": {
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
        }

class ModelInfo(BaseModel):
    """Model bilgileri"""
    name: str = Field(..., description="Model adı")
    version: str = Field(..., description="Model versiyonu")
    accuracy: float = Field(..., ge=0, le=1, description="Model doğruluğu")
    training_date: str = Field(..., description="Eğitim tarihi")
    status: str = Field(..., description="Model durumu")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "random_forest",
                "version": "1.0.0",
                "accuracy": 0.96,
                "training_date": "2024-01-15T10:00:00",
                "status": "loaded"
            }
        }

class HealthCheck(BaseModel):
    """Sağlık kontrolü"""
    status: str = Field(..., description="Genel durum")
    timestamp: datetime = Field(..., description="Kontrol zamanı")
    model_loaded: bool = Field(..., description="Model yüklü mü?")
    mlflow_connected: bool = Field(..., description="MLflow bağlantısı")
    version: str = Field(..., description="API versiyonu")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00",
                "model_loaded": True,
                "mlflow_connected": True,
                "version": "1.0.0"
            }
        }

class TrainingRequest(BaseModel):
    """Model eğitimi isteği"""
    experiment_name: str = Field(..., description="Deney adı")
    model_type: Optional[str] = Field(None, description="Model türü (logistic_regression, random_forest, svm)")
    hyperparameters: Optional[Dict] = Field(None, description="Hiperparametreler")
    
    class Config:
        schema_extra = {
            "example": {
                "experiment_name": "iris_hyperopt",
                "model_type": "random_forest",
                "hyperparameters": {
                    "n_estimators": 100,
                    "max_depth": 10
                }
            }
        }

class TrainingResponse(BaseModel):
    """Model eğitimi sonucu"""
    message: str = Field(..., description="Sonuç mesajı")
    model_name: str = Field(..., description="Eğitilen model adı")
    accuracy: float = Field(..., description="Model doğruluğu")
    experiment_name: str = Field(..., description="Deney adı")
    training_time: Optional[float] = Field(None, description="Eğitim süresi (saniye)")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Model başarıyla eğitildi",
                "model_name": "random_forest",
                "accuracy": 0.96,
                "experiment_name": "iris_hyperopt",
                "training_time": 2.5
            }
        }

class ExperimentInfo(BaseModel):
    """Deney bilgileri"""
    name: str = Field(..., description="Deney adı")
    experiment_id: str = Field(..., description="Deney ID")
    lifecycle_stage: str = Field(..., description="Yaşam döngüsü aşaması")
    run_count: Optional[int] = Field(None, description="Çalıştırma sayısı")
    last_updated: Optional[str] = Field(None, description="Son güncelleme")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "iris_classification",
                "experiment_id": "123456789",
                "lifecycle_stage": "active",
                "run_count": 15,
                "last_updated": "2024-01-15T10:30:00"
            }
        }

class ModelComparison(BaseModel):
    """Model karşılaştırması"""
    model_name: str = Field(..., description="Model adı")
    accuracy: float = Field(..., description="Doğruluk")
    precision: float = Field(..., description="Kesinlik")
    recall: float = Field(..., description="Duyarlılık")
    f1_score: float = Field(..., description="F1 skoru")
    training_time: float = Field(..., description="Eğitim süresi")
    prediction_time: float = Field(..., description="Tahmin süresi")
    
    class Config:
        schema_extra = {
            "example": {
                "model_name": "random_forest",
                "accuracy": 0.96,
                "precision": 0.95,
                "recall": 0.96,
                "f1_score": 0.95,
                "training_time": 0.5,
                "prediction_time": 0.01
            }
        }

class BatchPredictionRequest(BaseModel):
    """Toplu tahmin isteği"""
    features: List[IrisFeatures] = Field(..., description="Özellik listesi")
    
    class Config:
        schema_extra = {
            "example": {
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
        } 