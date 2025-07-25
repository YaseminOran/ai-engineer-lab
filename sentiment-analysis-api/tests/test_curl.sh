#!/bin/bash

# Sentiment Analysis API Test Script
# Bu script API endpoint'lerini test eder

BASE_URL="http://localhost:8000"

echo "🚀 Sentiment Analysis API Test Başlıyor..."
echo "=========================================="

# 1. Sağlık kontrolü
echo "1. Sağlık Kontrolü:"
curl -X GET "$BASE_URL/health" -H "Content-Type: application/json"
echo -e "\n\n"

# 2. Ana sayfa
echo "2. Ana Sayfa:"
curl -X GET "$BASE_URL/" -H "Content-Type: application/json"
echo -e "\n\n"

# 3. Model bilgileri
echo "3. Model Bilgileri:"
curl -X GET "$BASE_URL/model/info" -H "Content-Type: application/json"
echo -e "\n\n"

# 4. Tek metin tahmini - Pozitif
echo "4. Tek Metin Tahmini (Pozitif):"
curl -X POST "$BASE_URL/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Bu film gerçekten harika! Çok beğendim."}'
echo -e "\n\n"

# 5. Tek metin tahmini - Negatif
echo "5. Tek Metin Tahmini (Negatif):"
curl -X POST "$BASE_URL/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Çok kötü bir deneyimdi, hiç tavsiye etmem."}'
echo -e "\n\n"

# 6. Tek metin tahmini - Nötr
echo "6. Tek Metin Tahmini (Nötr):"
curl -X POST "$BASE_URL/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Orta karar bir ürün, ne iyi ne kötü."}'
echo -e "\n\n"

# 7. Toplu tahmin
echo "7. Toplu Tahmin:"
curl -X POST "$BASE_URL/predict/batch" \
     -H "Content-Type: application/json" \
     -d '{
       "texts": [
         "Bu film harika!",
         "Kötü bir deneyim.",
         "Normal bir gün.",
         "Mükemmel bir hizmet!",
         "Berbat bir yemek."
       ]
     }'
echo -e "\n\n"

# 8. Hata testi - Boş metin
echo "8. Hata Testi (Boş Metin):"
curl -X POST "$BASE_URL/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": ""}'
echo -e "\n\n"

# 9. Model yeniden eğitme
echo "9. Model Yeniden Eğitme:"
curl -X POST "$BASE_URL/retrain" -H "Content-Type: application/json"
echo -e "\n\n"

echo "✅ Tüm testler tamamlandı!" 