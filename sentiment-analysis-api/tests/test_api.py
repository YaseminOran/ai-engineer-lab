import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Sağlık kontrolü endpoint'ini test et"""
    print("=== Sağlık Kontrolü Testi ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Hata: {e}")
        return False

def test_root_endpoint():
    """Ana endpoint'i test et"""
    print("=== Ana Endpoint Testi ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Hata: {e}")
        return False

def test_model_info():
    """Model bilgilerini test et"""
    print("=== Model Bilgileri Testi ===")
    try:
        response = requests.get(f"{BASE_URL}/model/info")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Hata: {e}")
        return False

def test_single_prediction():
    """Tek metin tahmini test et"""
    print("=== Tek Metin Tahmini Testi ===")
    
    test_cases = [
        "Bu film gerçekten harika! Çok beğendim.",
        "Çok kötü bir deneyimdi, hiç tavsiye etmem.",
        "Orta karar bir ürün, ne iyi ne kötü.",
        "Mükemmel bir hizmet aldık, teşekkürler!",
        "Berbat bir yemek, paramı geri istiyorum."
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"Test {i}: {text}")
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json={"text": text}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Sentiment: {result['sentiment']}")
                print(f"Confidence: {result['confidence']:.3f}")
                print(f"Prediction: {result['prediction']}")
            else:
                print(f"Error: {response.text}")
            print("-" * 50)
        except Exception as e:
            print(f"Hata: {e}")
            print("-" * 50)

def test_batch_prediction():
    """Toplu tahmin test et"""
    print("=== Toplu Tahmin Testi ===")
    
    texts = [
        "Bu film harika!",
        "Kötü bir deneyim.",
        "Normal bir gün.",
        "Mükemmel!",
        "Berbat!"
    ]
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict/batch",
            json={"texts": texts}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Toplam sonuç sayısı: {len(result['results'])}")
            
            for i, item in enumerate(result['results'], 1):
                print(f"Sonuç {i}:")
                print(f"  Metin: {item['text']}")
                print(f"  Sentiment: {item['sentiment']}")
                print(f"  Confidence: {item['confidence']:.3f}")
                print(f"  Prediction: {item['prediction']}")
                print()
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Hata: {e}")

def test_error_cases():
    """Hata durumlarını test et"""
    print("=== Hata Durumları Testi ===")
    
    # Boş metin testi
    print("1. Boş metin testi:")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={"text": ""}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Hata: {e}")
    
    print("-" * 30)
    
    # Boş liste testi
    print("2. Boş liste testi:")
    try:
        response = requests.post(
            f"{BASE_URL}/predict/batch",
            json={"texts": []}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Hata: {e}")

def test_retrain():
    """Model yeniden eğitme test et"""
    print("=== Model Yeniden Eğitme Testi ===")
    try:
        response = requests.post(f"{BASE_URL}/retrain")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Hata: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🚀 Sentiment Analysis API Test Başlıyor...")
    print("=" * 60)
    
    # API'nin çalışıp çalışmadığını kontrol et
    print("API'nin başlatılması bekleniyor...")
    time.sleep(3)
    
    # Temel endpoint testleri
    test_health_endpoint()
    test_root_endpoint()
    test_model_info()
    
    # Tahmin testleri
    test_single_prediction()
    test_batch_prediction()
    
    # Hata durumları
    test_error_cases()
    
    # Model yeniden eğitme
    test_retrain()
    
    print("✅ Tüm testler tamamlandı!")

if __name__ == "__main__":
    main() 