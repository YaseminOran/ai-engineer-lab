import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import seaborn as sns
import os

logger = logging.getLogger(__name__)

def train_models(X_train: np.ndarray, y_train: np.ndarray, 
                 X_test: np.ndarray, y_test: np.ndarray,
                 experiment_name: str = "iris_classification") -> Dict[str, Any]:
    """
    Farklı modelleri eğit ve MLflow ile takip et
    
    Args:
        X_train: Eğitim özellikleri
        y_train: Eğitim hedefleri
        X_test: Test özellikleri
        y_test: Test hedefleri
        experiment_name: MLflow deney adı
        
    Returns:
        Dict: Eğitilen modeller ve metrikleri
    """
    try:
        logger.info(f"Model eğitimi başlatılıyor: {experiment_name}")
        
        # MLflow experiment'i ayarla
        mlflow.set_experiment(experiment_name)
        
        models = {}
        
        # 1. Logistic Regression
        with mlflow.start_run(run_name="logistic_regression"):
            logger.info("Logistic Regression eğitiliyor...")
            
            start_time = time.time()
            
            model = LogisticRegression(random_state=42, max_iter=1000)
            model.fit(X_train, y_train)
            
            training_time = time.time() - start_time
            
            # Tahminler
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            # Metrikler
            accuracy = accuracy_score(y_test, y_pred)
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            
            # MLflow'a log
            mlflow.log_params({
                "algorithm": "logistic_regression",
                "random_state": 42,
                "max_iter": 1000
            })
            
            mlflow.log_metrics({
                "accuracy": accuracy,
                "cv_mean": cv_scores.mean(),
                "cv_std": cv_scores.std(),
                "training_time": training_time
            })
            
            # Model kaydet
            mlflow.sklearn.log_model(model, "model")
            
            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            plot_confusion_matrix(cm, "logistic_regression", experiment_name)
            
            models["logistic_regression"] = {
                "model": model,
                "accuracy": accuracy,
                "cv_mean": cv_scores.mean(),
                "training_time": training_time,
                "run_id": mlflow.active_run().info.run_id
            }
            
            logger.info(f"Logistic Regression tamamlandı - Accuracy: {accuracy:.4f}")
        
        # 2. Random Forest
        with mlflow.start_run(run_name="random_forest"):
            logger.info("Random Forest eğitiliyor...")
            
            start_time = time.time()
            
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            training_time = time.time() - start_time
            
            # Tahminler
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            # Metrikler
            accuracy = accuracy_score(y_test, y_pred)
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            
            # Feature importance
            feature_importance = model.feature_importances_
            
            # MLflow'a log
            mlflow.log_params({
                "algorithm": "random_forest",
                "n_estimators": 100,
                "random_state": 42
            })
            
            mlflow.log_metrics({
                "accuracy": accuracy,
                "cv_mean": cv_scores.mean(),
                "cv_std": cv_scores.std(),
                "training_time": training_time
            })
            
            # Feature importance log
            for i, importance in enumerate(feature_importance):
                mlflow.log_metric(f"feature_importance_{i}", importance)
            
            # Model kaydet
            mlflow.sklearn.log_model(model, "model")
            
            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            plot_confusion_matrix(cm, "random_forest", experiment_name)
            
            # Feature importance plot
            plot_feature_importance(feature_importance, "random_forest", experiment_name)
            
            models["random_forest"] = {
                "model": model,
                "accuracy": accuracy,
                "cv_mean": cv_scores.mean(),
                "training_time": training_time,
                "feature_importance": feature_importance,
                "run_id": mlflow.active_run().info.run_id
            }
            
            logger.info(f"Random Forest tamamlandı - Accuracy: {accuracy:.4f}")
        
        # 3. Support Vector Machine
        with mlflow.start_run(run_name="svm"):
            logger.info("SVM eğitiliyor...")
            
            start_time = time.time()
            
            model = SVC(kernel='rbf', random_state=42, probability=True)
            model.fit(X_train, y_train)
            
            training_time = time.time() - start_time
            
            # Tahminler
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            # Metrikler
            accuracy = accuracy_score(y_test, y_pred)
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            
            # MLflow'a log
            mlflow.log_params({
                "algorithm": "svm",
                "kernel": "rbf",
                "random_state": 42
            })
            
            mlflow.log_metrics({
                "accuracy": accuracy,
                "cv_mean": cv_scores.mean(),
                "cv_std": cv_scores.std(),
                "training_time": training_time
            })
            
            # Model kaydet
            mlflow.sklearn.log_model(model, "model")
            
            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            plot_confusion_matrix(cm, "svm", experiment_name)
            
            models["svm"] = {
                "model": model,
                "accuracy": accuracy,
                "cv_mean": cv_scores.mean(),
                "training_time": training_time,
                "run_id": mlflow.active_run().info.run_id
            }
            
            logger.info(f"SVM tamamlandı - Accuracy: {accuracy:.4f}")
        
        # En iyi modeli seç
        best_model_name = max(models.keys(), key=lambda k: models[k]['accuracy'])
        best_model = models[best_model_name]['model']
        best_accuracy = models[best_model_name]['accuracy']
        
        logger.info(f"En iyi model: {best_model_name} - Accuracy: {best_accuracy:.4f}")
        
        # En iyi modeli MLflow Model Registry'ye kaydet
        with mlflow.start_run(run_name=f"best_model_{best_model_name}"):
            mlflow.log_params({
                "best_model": best_model_name,
                "best_accuracy": best_accuracy
            })
            
            mlflow.sklearn.log_model(best_model, "model")
            
            # Model Registry'ye kaydet
            model_name = "iris_classifier"
            mlflow.sklearn.log_model(
                best_model, 
                "model",
                registered_model_name=model_name
            )
        
        return models
        
    except Exception as e:
        logger.error(f"Model eğitimi hatası: {e}")
        raise

def plot_confusion_matrix(cm: np.ndarray, model_name: str, experiment_name: str):
    """Confusion matrix çiz ve MLflow'a kaydet"""
    try:
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # MLflow'a kaydet
        plot_path = f"confusion_matrix_{model_name}.png"
        plt.savefig(plot_path)
        mlflow.log_artifact(plot_path)
        plt.close()
        
        # Dosyayı sil
        os.remove(plot_path)
        
    except Exception as e:
        logger.error(f"Confusion matrix çizim hatası: {e}")

def plot_feature_importance(importance: np.ndarray, model_name: str, experiment_name: str):
    """Feature importance çiz ve MLflow'a kaydet"""
    try:
        feature_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        
        plt.figure(figsize=(10, 6))
        plt.bar(feature_names, importance)
        plt.title(f'Feature Importance - {model_name}')
        plt.xlabel('Features')
        plt.ylabel('Importance')
        plt.xticks(rotation=45)
        
        # MLflow'a kaydet
        plot_path = f"feature_importance_{model_name}.png"
        plt.savefig(plot_path, bbox_inches='tight')
        mlflow.log_artifact(plot_path)
        plt.close()
        
        # Dosyayı sil
        os.remove(plot_path)
        
    except Exception as e:
        logger.error(f"Feature importance çizim hatası: {e}")

def get_best_model(model_name: str = "iris_classifier") -> Optional[Any]:
    """MLflow'dan en iyi modeli yükle"""
    try:
        # Model Registry'den model yükle
        model_uri = f"models:/{model_name}/latest"
        model = mlflow.sklearn.load_model(model_uri)
        
        logger.info(f"Model yüklendi: {model_name}")
        return model
        
    except Exception as e:
        logger.warning(f"Model yükleme hatası: {e}")
        return None

def compare_models(models: Dict[str, Any]) -> pd.DataFrame:
    """Modelleri karşılaştır"""
    try:
        comparison_data = []
        
        for model_name, model_info in models.items():
            comparison_data.append({
                'model': model_name,
                'accuracy': model_info['accuracy'],
                'cv_mean': model_info['cv_mean'],
                'cv_std': model_info['cv_std'],
                'training_time': model_info['training_time']
            })
        
        df = pd.DataFrame(comparison_data)
        df = df.sort_values('accuracy', ascending=False)
        
        logger.info("Model karşılaştırması:")
        logger.info(df.to_string(index=False))
        
        return df
        
    except Exception as e:
        logger.error(f"Model karşılaştırma hatası: {e}")
        raise

def log_model_performance(model: Any, X_test: np.ndarray, y_test: np.ndarray, 
                         model_name: str, run_name: str):
    """Model performansını MLflow'a log et"""
    try:
        with mlflow.start_run(run_name=run_name):
            # Tahminler
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            # Metrikler
            accuracy = accuracy_score(y_test, y_pred)
            
            # Classification report
            report = classification_report(y_test, y_pred, output_dict=True)
            
            # MLflow'a log
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision_macro", report['macro avg']['precision'])
            mlflow.log_metric("recall_macro", report['macro avg']['recall'])
            mlflow.log_metric("f1_macro", report['macro avg']['f1-score'])
            
            # Model kaydet
            mlflow.sklearn.log_model(model, "model")
            
            logger.info(f"Model performansı log edildi: {model_name}")
            
    except Exception as e:
        logger.error(f"Model performans log hatası: {e}")
        raise 