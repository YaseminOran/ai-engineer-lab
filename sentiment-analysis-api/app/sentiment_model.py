import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import re

class SentimentAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = LogisticRegression(random_state=42)
        self.is_trained = False
    
    def preprocess_text(self, text):
        """Basit metin ön işleme"""
        if isinstance(text, str):
            # Küçük harfe çevir
            text = text.lower()
            # Özel karakterleri temizle
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            # Fazla boşlukları temizle
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        return ""
    
    def create_sample_data(self):
        """Örnek veri seti oluştur"""
        positive_texts = [
            "Bu film harika! Çok beğendim.",
            "Mükemmel bir deneyimdi, kesinlikle tavsiye ederim.",
            "Çok güzel bir gün geçirdik.",
            "Bu ürün gerçekten kaliteli.",
            "Harika bir hizmet aldık.",
            "Çok memnun kaldım, teşekkürler.",
            "Bu kitap gerçekten etkileyici.",
            "Mükemmel bir performans sergiledi.",
            "Çok lezzetli bir yemek.",
            "Harika bir konser oldu."
        ]
        
        negative_texts = [
            "Bu film berbat! Hiç beğenmedim.",
            "Kötü bir deneyimdi, tavsiye etmem.",
            "Çok kötü bir gün geçirdik.",
            "Bu ürün gerçekten kalitesiz.",
            "Berbat bir hizmet aldık.",
            "Hiç memnun kalmadım.",
            "Bu kitap gerçekten sıkıcı.",
            "Kötü bir performans sergiledi.",
            "Çok kötü bir yemek.",
            "Berbat bir konser oldu."
        ]
        
        neutral_texts = [
            "Bu film orta karar.",
            "Normal bir deneyimdi.",
            "Sıradan bir gün geçirdik.",
            "Bu ürün orta kalitede.",
            "Standart bir hizmet aldık.",
            "Ne memnun ne de memnun değilim.",
            "Bu kitap orta seviyede.",
            "Normal bir performans sergiledi.",
            "Orta karar bir yemek.",
            "Normal bir konser oldu."
        ]
        
        texts = positive_texts + negative_texts + neutral_texts
        labels = [1] * len(positive_texts) + [0] * len(negative_texts) + [2] * len(neutral_texts)
        
        return texts, labels
    
    def train(self, texts=None, labels=None):
        """Modeli eğit"""
        if texts is None or labels is None:
            texts, labels = self.create_sample_data()
        
        # Metinleri ön işle
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # TF-IDF vektörlerini oluştur
        X = self.vectorizer.fit_transform(processed_texts)
        
        # Modeli eğit
        self.model.fit(X, labels)
        self.is_trained = True
        
        # Eğitim performansını değerlendir
        y_pred = self.model.predict(X)
        accuracy = accuracy_score(labels, y_pred)
        
        print(f"Model eğitildi. Doğruluk: {accuracy:.2f}")
        print(classification_report(labels, y_pred, 
                                  target_names=['Negatif', 'Pozitif', 'Nötr']))
        
        return accuracy
    
    def predict(self, text):
        """Tek bir metin için tahmin yap"""
        if not self.is_trained:
            raise ValueError("Model henüz eğitilmemiş!")
        
        processed_text = self.preprocess_text(text)
        X = self.vectorizer.transform([processed_text])
        prediction = self.model.predict(X)[0]
        probability = np.max(self.model.predict_proba(X))
        
        sentiment_map = {0: "negatif", 1: "pozitif", 2: "nötr"}
        sentiment = sentiment_map.get(prediction, "bilinmiyor")
        
        return {
            "text": text,
            "sentiment": sentiment,
            "confidence": float(probability),
            "prediction": int(prediction)
        }
    
    def predict_batch(self, texts):
        """Birden fazla metin için tahmin yap"""
        if not self.is_trained:
            raise ValueError("Model henüz eğitilmemiş!")
        
        processed_texts = [self.preprocess_text(text) for text in texts]
        X = self.vectorizer.transform(processed_texts)
        predictions = self.model.predict(X)
        probabilities = np.max(self.model.predict_proba(X), axis=1)
        
        sentiment_map = {0: "negatif", 1: "pozitif", 2: "nötr"}
        
        results = []
        for i, (text, pred, prob) in enumerate(zip(texts, predictions, probabilities)):
            sentiment = sentiment_map.get(pred, "bilinmiyor")
            results.append({
                "text": text,
                "sentiment": sentiment,
                "confidence": float(prob),
                "prediction": int(pred)
            })
        
        return results
    
    def save_model(self, filepath):
        """Modeli kaydet"""
        if not self.is_trained:
            raise ValueError("Model henüz eğitilmemiş!")
        
        model_data = {
            'vectorizer': self.vectorizer,
            'model': self.model,
            'is_trained': self.is_trained
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model {filepath} dosyasına kaydedildi.")
    
    def load_model(self, filepath):
        """Modeli yükle"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vectorizer = model_data['vectorizer']
        self.model = model_data['model']
        self.is_trained = model_data['is_trained']
        print(f"Model {filepath} dosyasından yüklendi.")

if __name__ == "__main__":
    # Model oluştur ve eğit
    analyzer = SentimentAnalyzer()
    accuracy = analyzer.train()
    
    # Test et
    test_texts = [
        "Bu film gerçekten harika!",
        "Çok kötü bir deneyimdi.",
        "Orta karar bir ürün."
    ]
    
    for text in test_texts:
        result = analyzer.predict(text)
        print(f"Metin: {result['text']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Güven: {result['confidence']:.2f}")
        print("-" * 50)
    
    # Modeli kaydet
    analyzer.save_model('sentiment_model.pkl') 