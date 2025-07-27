#!/bin/bash

# Docker Learning Project - Run Script
# Bu script uygulamayı çalıştırır ve test eder

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
log "🚀 Docker Learning Project - Run Script başlatılıyor..."

# Docker'ın çalışıp çalışmadığını kontrol et
if ! docker info > /dev/null 2>&1; then
    error "Docker çalışmıyor! Docker Desktop'ı başlatın."
    exit 1
fi

success "Docker çalışıyor"

# Eski container'ları durdur
log "🛑 Eski container'lar durduruluyor..."
cd docker
docker-compose down 2>/dev/null || true

# Environment dosyasını kontrol et
if [ ! -f "../config/.env" ]; then
    log "📝 Environment dosyası oluşturuluyor..."
    cp ../config/env.example ../config/.env
    warning "config/.env dosyasını düzenleyin!"
fi

# Docker Compose ile başlat
log "🚀 Servisler başlatılıyor..."
docker-compose up -d

# Servislerin başlamasını bekle
log "⏳ Servislerin başlaması bekleniyor..."
sleep 15

# Health check'leri kontrol et
log "🏥 Health check'ler kontrol ediliyor..."

# PostgreSQL health check
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U user -d docker_learning > /dev/null 2>&1; then
        success "PostgreSQL hazır"
        break
    fi
    if [ $i -eq 30 ]; then
        error "PostgreSQL başlatılamadı!"
        docker-compose logs db
        exit 1
    fi
    sleep 2
done

# Redis health check
for i in {1..30}; do
    if docker-compose exec -T cache redis-cli ping > /dev/null 2>&1; then
        success "Redis hazır"
        break
    fi
    if [ $i -eq 30 ]; then
        error "Redis başlatılamadı!"
        docker-compose logs cache
        exit 1
    fi
    sleep 2
done

# API health check
for i in {1..60}; do
    if curl -f http://localhost:8003/health > /dev/null 2>&1; then
        success "API hazır"
        break
    fi
    if [ $i -eq 60 ]; then
        error "API başlatılamadı!"
        docker-compose logs app
        exit 1
    fi
    sleep 2
done

# API test'leri
log "🧪 API test'leri yapılıyor..."

# Ana endpoint test
if curl -s http://localhost:8003/ | grep -q "Docker Learning API"; then
    success "Ana endpoint çalışıyor"
else
    error "Ana endpoint hatası!"
fi

# Health endpoint test
if curl -s http://localhost:8003/health | grep -q "healthy"; then
    success "Health endpoint çalışıyor"
else
    error "Health endpoint hatası!"
fi

# Kullanıcı listesi test
if curl -s http://localhost:8003/users | grep -q "\[\]"; then
    success "Users endpoint çalışıyor"
else
    error "Users endpoint hatası!"
fi

# Yeni kullanıcı oluşturma test
TEST_USER=$(curl -s -X POST http://localhost:8003/users \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","name":"Test User","password":"password123"}')

if echo "$TEST_USER" | grep -q "test@example.com"; then
    success "User creation endpoint çalışıyor"
else
    error "User creation endpoint hatası!"
fi

# Servis durumunu göster
log "📊 Servis durumu:"
docker-compose ps

# Başarı mesajı
success "🎉 Uygulama başarıyla çalışıyor!"
echo ""
echo "📋 Servis Bilgileri:"
echo "  API: http://localhost:8003"
echo "  Docs: http://localhost:8003/docs"
echo "  Health: http://localhost:8003/health"
echo "  Database: localhost:5432"
echo "  Redis: localhost:6380"
echo ""
echo "🔧 Kullanışlı Komutlar:"
echo "  docker-compose logs -f app    # API logları"
echo "  docker-compose logs -f db     # Database logları"
echo "  docker-compose logs -f cache  # Redis logları"
echo "  docker-compose exec app bash  # Container'a bağlan"
echo "  docker-compose down           # Servisleri durdur"
echo ""
echo "📊 Monitoring:"
echo "  docker stats                  # Resource kullanımı"
echo "  docker-compose ps             # Servis durumu"

cd .. 