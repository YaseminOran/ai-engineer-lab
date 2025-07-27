 # 🐳 Docker Öğrenme Projesi

Bu proje, Docker'ın temel kavramlarını öğrenmek için tasarlanmış kapsamlı bir öğrenme deneyimidir. Basit bir REST API uygulaması üzerinden Docker'ın tüm temel özelliklerini pratik edebilirsiniz.

## 📚 Öğrenme Hedefleri

- [x] **Docker nedir, ne işe yarar?** - Temel mimariyi öğren
- [x] **Basit bir Dockerfile oluştur** - API uygulamasını konteynerleştir
- [x] **Docker üzerinden servisi ayağa kaldır** - Port yönlendirmesi dahil
- [x] **.env dosyası kullanarak config yönetimi** - Environment variables
- [x] **Docker Compose ile servis yapılandırması** - Otomatize et
- [x] **Terminalden log izleme ve hata ayıklama** - Pratik et

## 🏗️ Proje Mimarisi

```
docker-learning-project/
├── app/                    # Ana uygulama
│   ├── main.py            # FastAPI uygulaması
│   ├── models.py          # Veri modelleri
│   └── database.py        # Veritabanı işlemleri
├── docker/                # Docker dosyaları
│   ├── Dockerfile         # Ana uygulama container'ı
│   └── docker-compose.yml # Multi-service yapılandırma
├── config/                # Konfigürasyon dosyaları
│   └── .env.example       # Environment variables örneği
├── scripts/               # Yardımcı scriptler
│   ├── build.sh           # Build script'i
│   ├── run.sh             # Çalıştırma script'i
│   └── logs.sh            # Log izleme script'i
└── docs/                  # Dokümantasyon
    ├── docker-basics.md   # Docker temelleri
    └── troubleshooting.md # Sorun giderme
```

## 🚀 Hızlı Başlangıç

### 1. Projeyi Klonlayın
```bash
git clone <repository-url>
cd docker-learning-project
```

### 2. Environment Dosyasını Hazırlayın
```bash
cp config/.env.example config/.env
# .env dosyasını düzenleyin
```

### 3. Docker Compose ile Başlatın
```bash
docker-compose up -d
```

### 4. Uygulamayı Test Edin
```bash
curl http://localhost:8000/health
```

## 📖 Docker Temelleri

### Docker Nedir?
Docker, uygulamaları konteynerler içinde çalıştırmaya yarayan bir platformdur. Konteynerler, uygulamanızı ve tüm bağımlılıklarını izole bir ortamda çalıştırır.

### Temel Kavramlar
- **Image**: Uygulamanızın çalışması için gereken dosyaların snapshot'ı
- **Container**: Image'ın çalışan bir instance'ı
- **Dockerfile**: Image oluşturmak için kullanılan talimatlar
- **Docker Compose**: Birden fazla servisi yönetmek için kullanılan araç

### Docker Mimarisi
```
┌─────────────────┐
│   Docker Host   │
├─────────────────┤
│  Docker Engine  │
├─────────────────┤
│   Containers    │
│  ┌─────────────┐│
│  │   App 1     ││
│  └─────────────┘│
│  ┌─────────────┐│
│  │   App 2     ││
│  └─────────────┘│
└─────────────────┘
```

## 🛠️ Proje Özellikleri

### API Endpoints
- `GET /health` - Sağlık kontrolü
- `GET /users` - Kullanıcı listesi
- `POST /users` - Yeni kullanıcı ekleme
- `GET /users/{id}` - Kullanıcı detayı
- `PUT /users/{id}` - Kullanıcı güncelleme
- `DELETE /users/{id}` - Kullanıcı silme

### Veritabanı
- **PostgreSQL** - Ana veritabanı
- **Redis** - Cache ve session yönetimi
- **Persistent Storage** - Veri kalıcılığı

### Monitoring
- **Health Checks** - Otomatik sağlık kontrolü
- **Logging** - Yapılandırılabilir log sistemi
- **Metrics** - Performans metrikleri

## 📋 Öğrenme Adımları

### 1. Docker Temelleri
```bash
# Docker kurulumu kontrolü
docker --version
docker-compose --version

# İlk container'ı çalıştırma
docker run hello-world
```

### 2. Dockerfile Oluşturma
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Environment Variables
```bash
# .env dosyası
APP_NAME=Docker Learning API
DEBUG=true
DATABASE_URL=postgresql://user:pass@db:5432/dbname
REDIS_URL=redis://cache:6379
```

### 4. Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - db
      - cache
```

### 5. Log İzleme
```bash
# Container loglarını izleme
docker-compose logs -f app

# Belirli bir servisin logları
docker logs -f container_name

# Real-time log izleme
docker-compose logs -f --tail=100
```

## 🔧 Geliştirme Komutları

### Build ve Run
```bash
# Image build etme
docker build -t docker-learning-api .

# Container çalıştırma
docker run -p 8000:8000 docker-learning-api

# Docker Compose ile çalıştırma
docker-compose up -d
```

### Debug ve Troubleshooting
```bash
# Container'a bağlanma
docker exec -it container_name bash

# Container durumunu kontrol etme
docker ps
docker-compose ps

# Resource kullanımını izleme
docker stats
```

### Cleanup
```bash
# Container'ları durdurma
docker-compose down

# Image'ları temizleme
docker system prune -a

# Volume'ları temizleme
docker volume prune
```

## 📊 Monitoring ve Debugging

### Health Checks
```bash
# API sağlık kontrolü
curl http://localhost:8000/health

# Container sağlık kontrolü
docker inspect container_name | grep Health
```

### Log Analysis
```bash
# Hata loglarını filtreleme
docker-compose logs app | grep ERROR

# Son 100 log satırı
docker-compose logs --tail=100 app
```

### Performance Monitoring
```bash
# Container resource kullanımı
docker stats

# Disk kullanımı
docker system df
```

## 🐛 Yaygın Sorunlar ve Çözümler

### Port Çakışması
```bash
# Port kullanımını kontrol etme
lsof -i :8000

# Farklı port kullanma
docker run -p 8001:8000 docker-learning-api
```

### Permission Issues
```bash
# Docker group'a kullanıcı ekleme
sudo usermod -aG docker $USER

# Container içinde dosya izinleri
chmod 755 /app
```

### Memory Issues
```bash
# Memory limiti ayarlama
docker run --memory=512m docker-learning-api

# Swap kullanımı
docker run --memory=512m --memory-swap=1g docker-learning-api
```

## 📚 Ek Kaynaklar

### Docker Dokümantasyonu
- [Docker Official Docs](https://docs.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Video Eğitimler
- [Docker Tutorial for Beginners](https://www.youtube.com/watch?v=fqMOX6JJhGo)
- [Docker Compose Tutorial](https://www.youtube.com/watch?v=HG6yIjZapSA)

### Kitaplar
- "Docker in Action" - Jeff Nickoloff
- "The Docker Book" - James Turnbull

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👨‍💻 Geliştirici

Bu proje Docker öğrenme amaçlı oluşturulmuştur. Sorularınız için issue açabilirsiniz.

---

**Not**: Bu proje eğitim amaçlıdır ve production ortamında kullanılmadan önce güvenlik ve performans optimizasyonları yapılmalıdır.