#!/bin/bash

# Docker Learning Project - Logs Script
# Bu script container loglarını yönetir

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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

# Yardım fonksiyonu
show_help() {
    echo "Docker Learning Project - Logs Script"
    echo ""
    echo "Kullanım:"
    echo "  $0 [SERVİS] [OPTION]"
    echo ""
    echo "Servisler:"
    echo "  app     - API uygulaması logları"
    echo "  db      - PostgreSQL veritabanı logları"
    echo "  cache   - Redis cache logları"
    echo "  all     - Tüm servislerin logları"
    echo ""
    echo "Seçenekler:"
    echo "  -f      - Follow (sürekli izle)"
    echo "  -t      - Timestamps göster"
    echo "  -n N    - Son N satır göster"
    echo "  --error - Sadece hata logları"
    echo "  --info  - Sadece info logları"
    echo ""
    echo "Örnekler:"
    echo "  $0 app -f           # API loglarını sürekli izle"
    echo "  $0 db -n 50         # Son 50 DB log satırı"
    echo "  $0 all --error      # Tüm servislerin hata logları"
    echo "  $0 app -f -t        # API loglarını timestamp ile izle"
}

# Ana fonksiyon
main() {
    local service=""
    local follow=false
    local timestamps=false
    local lines=""
    local filter=""
    
    # Argümanları parse et
    while [[ $# -gt 0 ]]; do
        case $1 in
            app|db|cache|all)
                service="$1"
                shift
                ;;
            -f|--follow)
                follow=true
                shift
                ;;
            -t|--timestamps)
                timestamps=true
                shift
                ;;
            -n)
                lines="$2"
                shift 2
                ;;
            --error)
                filter="ERROR"
                shift
                ;;
            --info)
                filter="INFO"
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                error "Bilinmeyen seçenek: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Servis belirtilmemişse yardım göster
    if [ -z "$service" ]; then
        show_help
        exit 1
    fi
    
    # Docker'ın çalışıp çalışmadığını kontrol et
    if ! docker info > /dev/null 2>&1; then
        error "Docker çalışmıyor! Docker Desktop'ı başlatın."
        exit 1
    fi
    
    # Docker Compose dizinine git
    cd docker 2>/dev/null || {
        error "docker/ dizini bulunamadı!"
        exit 1
    }
    
    # Container'ların çalışıp çalışmadığını kontrol et
    if ! docker-compose ps | grep -q "Up"; then
        error "Hiçbir servis çalışmıyor! Önce ./scripts/run.sh çalıştırın."
        exit 1
    fi
    
    # Log komutunu oluştur
    local log_cmd="docker-compose logs"
    
    if [ "$follow" = true ]; then
        log_cmd="$log_cmd -f"
    fi
    
    if [ "$timestamps" = true ]; then
        log_cmd="$log_cmd -t"
    fi
    
    if [ -n "$lines" ]; then
        log_cmd="$log_cmd --tail=$lines"
    fi
    
    # Servis seçimi
    case $service in
        app)
            log "📝 API logları gösteriliyor:"
            if [ -n "$filter" ]; then
                eval "$log_cmd app" | grep -i "$filter"
            else
                eval "$log_cmd app"
            fi
            ;;
        db)
            log "🗄️  Database logları gösteriliyor:"
            if [ -n "$filter" ]; then
                eval "$log_cmd db" | grep -i "$filter"
            else
                eval "$log_cmd db"
            fi
            ;;
        cache)
            log "⚡ Redis logları gösteriliyor:"
            if [ -n "$filter" ]; then
                eval "$log_cmd cache" | grep -i "$filter"
            else
                eval "$log_cmd cache"
            fi
            ;;
        all)
            log "📊 Tüm servislerin logları gösteriliyor:"
            if [ -n "$filter" ]; then
                eval "$log_cmd" | grep -i "$filter"
            else
                eval "$log_cmd"
            fi
            ;;
    esac
    
    cd ..
}

# Script'i çalıştır
main "$@" 