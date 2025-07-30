import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import logging
import os
from typing import Tuple

logger = logging.getLogger(__name__)

def load_iris_data(file_path: str = "data/raw/iris.csv") -> pd.DataFrame:
    """
    Iris veri setini yükle
    
    Args:
        file_path: CSV dosya yolu
        
    Returns:
        DataFrame: Iris veri seti
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"Dosya bulunamadı: {file_path}")
            # Sklearn'dan iris dataset'ini yükle
            from sklearn.datasets import load_iris
            iris = load_iris()
            df = pd.DataFrame(iris.data, columns=iris.feature_names)
            df['target'] = iris.target
            df['target_name'] = iris.target_names[iris.target]
            
            # Dosyayı kaydet
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df.to_csv(file_path, index=False)
            logger.info(f"Iris dataset'i oluşturuldu: {file_path}")
        else:
            df = pd.read_csv(file_path)
            logger.info(f"Iris dataset'i yüklendi: {file_path}")
        
        return df
        
    except Exception as e:
        logger.error(f"Veri yükleme hatası: {e}")
        raise

def preprocess_data(data: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Veriyi ön işleme
    
    Args:
        data: Ham veri
        test_size: Test seti oranı
        random_state: Rastgele durum
        
    Returns:
        Tuple: (X_train, X_test, y_train, y_test)
    """
    try:
        logger.info("Veri ön işleme başlatılıyor...")
        
        # Özellikler ve hedef değişkeni ayır
        feature_columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        X = data[feature_columns].values
        y = data['target'].values
        
        # Veriyi train/test olarak böl
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Standardizasyon
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        logger.info(f"Veri ön işleme tamamlandı:")
        logger.info(f"  - Train seti: {X_train_scaled.shape}")
        logger.info(f"  - Test seti: {X_test_scaled.shape}")
        logger.info(f"  - Sınıf dağılımı: {np.bincount(y_train)}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
        
    except Exception as e:
        logger.error(f"Veri ön işleme hatası: {e}")
        raise

def get_feature_names() -> list:
    """Özellik isimlerini döndür"""
    return ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

def get_target_names() -> list:
    """Hedef sınıf isimlerini döndür"""
    return ['setosa', 'versicolor', 'virginica']

def analyze_data(data: pd.DataFrame) -> dict:
    """
    Veri analizi yap
    
    Args:
        data: Veri seti
        
    Returns:
        dict: Analiz sonuçları
    """
    try:
        analysis = {
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': data.dtypes.to_dict(),
            'missing_values': data.isnull().sum().to_dict(),
            'target_distribution': data['target_name'].value_counts().to_dict(),
            'numeric_summary': data.describe().to_dict()
        }
        
        logger.info("Veri analizi tamamlandı")
        return analysis
        
    except Exception as e:
        logger.error(f"Veri analizi hatası: {e}")
        raise

def save_processed_data(X_train: np.ndarray, X_test: np.ndarray, 
                       y_train: np.ndarray, y_test: np.ndarray,
                       output_dir: str = "data/processed") -> None:
    """
    İşlenmiş veriyi kaydet
    
    Args:
        X_train: Eğitim özellikleri
        X_test: Test özellikleri
        y_train: Eğitim hedefleri
        y_test: Test hedefleri
        output_dir: Çıktı dizini
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Numpy array'leri kaydet
        np.save(f"{output_dir}/X_train.npy", X_train)
        np.save(f"{output_dir}/X_test.npy", X_test)
        np.save(f"{output_dir}/y_train.npy", y_train)
        np.save(f"{output_dir}/y_test.npy", y_test)
        
        logger.info(f"İşlenmiş veri kaydedildi: {output_dir}")
        
    except Exception as e:
        logger.error(f"Veri kaydetme hatası: {e}")
        raise

def load_processed_data(data_dir: str = "data/processed") -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    İşlenmiş veriyi yükle
    
    Args:
        data_dir: Veri dizini
        
    Returns:
        Tuple: (X_train, X_test, y_train, y_test)
    """
    try:
        X_train = np.load(f"{data_dir}/X_train.npy")
        X_test = np.load(f"{data_dir}/X_test.npy")
        y_train = np.load(f"{data_dir}/y_train.npy")
        y_test = np.load(f"{data_dir}/y_test.npy")
        
        logger.info(f"İşlenmiş veri yüklendi: {data_dir}")
        return X_train, X_test, y_train, y_test
        
    except Exception as e:
        logger.error(f"İşlenmiş veri yükleme hatası: {e}")
        raise 