#!/bin/bash

# Docker Learning Project - Build Script
# Bu script Docker image'ını build eder ve test eder

set -e  # Hata durumunda script'i durdur

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log fonksiyonu
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Script başlangıcı
log "🚀 Docker Learning Project - Build Script başlatılıyor..."

# Docker'ın çalışıp çalışmadığını kontrol et
if ! docker info > /dev/null 2>&1; then
    error "Docker çalışmıyor! Docker Desktop'ı başlatın."
    exit 1
fi

success "Docker çalışıyor"

# Eski container'ları temizle
log "🧹 Eski container'lar temizleniyor..."
docker-compose down --remove-orphans 2>/dev/null || true

# Eski image'ları temizle (opsiyonel)
if [ "$1" = "--clean" ]; then
    log "🗑️  Eski image'lar temizleniyor..."
    docker system prune -f
fi

# Docker Compose ile build et
log "🔨 Docker image'ları build ediliyor..."
cd docker
docker-compose build --no-cache

if [ $? -eq 0 ]; then
    success "Image'lar başarıyla build edildi"
else
    error "Image build hatası!"
    exit 1
fi

# Image'ları listele
log "📋 Build edilen image'lar:"
docker images | grep docker-learning || true

# Basit test
log "🧪 Basit test yapılıyor..."
docker-compose up -d db cache

# Veritabanının hazır olmasını bekle
log "⏳ Veritabanı başlatılıyor..."
sleep 10

# Health check
if docker-compose exec -T db pg_isready -U user -d docker_learning > /dev/null 2>&1; then
    success "PostgreSQL hazır"
else
    warning "PostgreSQL henüz hazır değil, biraz daha bekleniyor..."
    sleep 10
fi

# Redis test
if docker-compose exec -T cache redis-cli ping > /dev/null 2>&1; then
    success "Redis hazır"
else
    warning "Redis henüz hazır değil"
fi

# Servisleri durdur
log "🛑 Test servisleri durduruluyor..."
docker-compose down

# Sonuç
success "✅ Build işlemi tamamlandı!"
log "📋 Sonraki adımlar:"
echo "  1. ./scripts/run.sh - Uygulamayı çalıştır"
echo "  2. ./scripts/logs.sh - Logları izle"
echo "  3. curl http://localhost:8003/health - API test et"

cd .. 