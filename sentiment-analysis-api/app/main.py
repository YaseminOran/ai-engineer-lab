from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from app.sentiment_model import SentimentAnalyzer
import os

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Sentiment Analysis API",
    description="Türkçe metinler için duygu analizi API'si",
    version="1.0.0"
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic modelleri
class TextRequest(BaseModel):
    text: str

class BatchTextRequest(BaseModel):
    texts: List[str]

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    prediction: int

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]

class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool

# Global sentiment analyzer
analyzer = SentimentAnalyzer()

@app.on_event("startup")
async def startup_event():
    """Uygulama başladığında modeli yükle"""
    global analyzer
    
    # Eğer kaydedilmiş model varsa yükle, yoksa eğit
    if os.path.exists('sentiment_model.pkl'):
        try:
            analyzer.load_model('sentiment_model.pkl')
            print("Kaydedilmiş model yüklendi.")
        except Exception as e:
            print(f"Model yüklenirken hata: {e}")
            print("Yeni model eğitiliyor...")
            analyzer.train()
            analyzer.save_model('sentiment_model.pkl')
    else:
        print("Model dosyası bulunamadı. Yeni model eğitiliyor...")
        analyzer.train()
        analyzer.save_model('sentiment_model.pkl')

@app.get("/", response_model=HealthResponse)
async def root():
    """Ana endpoint - API durumu"""
    return HealthResponse(
        status="success",
        message="Sentiment Analysis API çalışıyor!",
        model_loaded=analyzer.is_trained
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return HealthResponse(
        status="healthy",
        message="API sağlıklı çalışıyor",
        model_loaded=analyzer.is_trained
    )

@app.post("/predict", response_model=SentimentResponse)
async def predict_sentiment(request: TextRequest):
    """Tek metin için duygu analizi"""
    try:
        if not analyzer.is_trained:
            raise HTTPException(status_code=500, detail="Model henüz eğitilmemiş")
        
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Metin boş olamaz")
        
        result = analyzer.predict(request.text)
        return SentimentResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")

@app.post("/predict/batch", response_model=BatchSentimentResponse)
async def predict_sentiment_batch(request: BatchTextRequest):
    """Birden fazla metin için duygu analizi"""
    try:
        if not analyzer.is_trained:
            raise HTTPException(status_code=500, detail="Model henüz eğitilmemiş")
        
        if not request.texts:
            raise HTTPException(status_code=400, detail="Metin listesi boş olamaz")
        
        # Boş metinleri filtrele
        valid_texts = [text for text in request.texts if text.strip()]
        if not valid_texts:
            raise HTTPException(status_code=400, detail="Geçerli metin bulunamadı")
        
        results = analyzer.predict_batch(valid_texts)
        return BatchSentimentResponse(results=[SentimentResponse(**result) for result in results])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Toplu tahmin hatası: {str(e)}")

@app.post("/retrain")
async def retrain_model():
    """Modeli yeniden eğit"""
    try:
        accuracy = analyzer.train()
        analyzer.save_model('sentiment_model.pkl')
        return {
            "status": "success",
            "message": "Model başarıyla yeniden eğitildi",
            "accuracy": accuracy
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model eğitme hatası: {str(e)}")

@app.get("/model/info")
async def model_info():
    """Model bilgilerini getir"""
    return {
        "is_trained": analyzer.is_trained,
        "model_type": "LogisticRegression",
        "vectorizer_type": "TfidfVectorizer",
        "max_features": 5000,
        "supported_sentiments": ["negatif", "pozitif", "nötr"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 