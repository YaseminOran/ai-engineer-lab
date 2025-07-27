# 🐳 Docker Temelleri

Bu dokümantasyon, Docker'ın temel kavramlarını ve kullanımını açıklar.

## Docker Nedir?

Docker, uygulamaları konteynerler içinde çalıştırmaya yarayan bir platformdur. Konteynerler, uygulamanızı ve tüm bağımlılıklarını izole bir ortamda çalıştırır.

### Avantajları

- **Taşınabilirlik**: "Benim makinemde çalışıyor" sorunu çözülür
- **İzolasyon**: Her uygulama kendi ortamında çalışır
- **Hızlı Deployment**: Image'lar önceden hazırlanır
- **Kaynak Verimliliği**: VM'lere göre daha az kaynak kullanır
- **Versiyonlama**: Her image versiyonlanabilir

## Temel Kavramlar

### 1. Image (Görüntü)
- Uygulamanızın çalışması için gereken dosyaların snapshot'ı
- Değişmez (immutable) yapıdadır
- Katmanlı (layered) mimari kullanır

### 2. Container (Konteyner)
- Image'ın çalışan bir instance'ı
- Geçici (ephemeral) yapıdadır
- İzole bir ortamda çalışır

### 3. Dockerfile
- Image oluşturmak için kullanılan talimatlar
- Her satır bir katman oluşturur
- En iyi pratikler vardır

### 4. Docker Compose
- Birden fazla servisi yönetmek için kullanılan araç
- YAML formatında yapılandırma
- Servisler arası iletişimi kolaylaştırır

## Docker Mimarisi

```
┌─────────────────────────────────────┐
│           Docker Host              │
├─────────────────────────────────────┤
│         Docker Engine              │
│  ┌─────────────┐ ┌─────────────┐  │
│  │   Images    │ │ Containers  │  │
│  │             │ │             │  │
│  │ • app:v1    │ │ • app-1     │  │
│  │ • db:v2     │ │ • app-2     │  │
│  │ • cache:v1  │ │ • db-1      │  │
│  └─────────────┘ └─────────────┘  │
└─────────────────────────────────────┘
```

## Temel Komutlar

### Image Yönetimi

```bash
# Image listesi
docker images

# Image build etme
docker build -t myapp:v1 .

# Image çekme
docker pull nginx:alpine

# Image silme
docker rmi myapp:v1
```

### Container Yönetimi

```bash
# Container çalıştırma
docker run -d -p 8080:80 nginx:alpine

# Çalışan container'ları listeleme
docker ps

# Tüm container'ları listeleme
docker ps -a

# Container durdurma
docker stop container_id

# Container silme
docker rm container_id

# Container'a bağlanma
docker exec -it container_id bash
```

### Docker Compose

```bash
# Servisleri başlatma
docker-compose up -d

# Servisleri durdurma
docker-compose down

# Logları izleme
docker-compose logs -f

# Servis durumu
docker-compose ps
```

## Dockerfile En İyi Pratikleri

### 1. Base Image Seçimi
```dockerfile
# Kötü
FROM ubuntu:latest

# İyi
FROM python:3.11-slim
```

### 2. Katman Optimizasyonu
```dockerfile
# Kötü
COPY . /app/
RUN pip install -r requirements.txt

# İyi
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app/
```

### 3. Güvenlik
```dockerfile
# Non-root kullanıcı
RUN useradd --create-home app
USER app
```

### 4. Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/health || exit 1
```

## Docker Compose Yapılandırması

### Temel Yapı
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/db
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Environment Variables
```yaml
services:
  app:
    environment:
      - DEBUG=true
      - DATABASE_URL=${DATABASE_URL}
    env_file:
      - .env
```

### Networks
```yaml
services:
  app:
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## Monitoring ve Debugging

### Container İzleme
```bash
# Resource kullanımı
docker stats

# Container detayları
docker inspect container_id

# Logları izleme
docker logs -f container_id
```

### Debugging
```bash
# Container'a bağlanma
docker exec -it container_id bash

# Port mapping kontrolü
docker port container_id

# Network kontrolü
docker network ls
docker network inspect network_name
```

## Yaygın Sorunlar ve Çözümler

### 1. Port Çakışması
```bash
# Port kullanımını kontrol etme
lsof -i :8080

# Farklı port kullanma
docker run -p 8081:80 nginx
```

### 2. Permission Issues
```bash
# Docker group'a kullanıcı ekleme
sudo usermod -aG docker $USER

# Container içinde dosya izinleri
chmod 755 /app
```

### 3. Disk Space
```bash
# Kullanılmayan kaynakları temizleme
docker system prune -a

# Disk kullanımını kontrol etme
docker system df
```

## Güvenlik En İyi Pratikleri

### 1. Non-root Kullanıcı
```dockerfile
RUN useradd --create-home app
USER app
```

### 2. Minimal Base Image
```dockerfile
FROM python:3.11-slim
```

### 3. Multi-stage Build
```dockerfile
FROM node:alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:alpine
COPY --from=builder /app/node_modules ./node_modules
COPY . .
```

### 4. Secrets Yönetimi
```yaml
services:
  app:
    secrets:
      - db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Performance Optimizasyonu

### 1. Image Boyutu
```dockerfile
# .dockerignore kullanın
node_modules
.git
*.log
```

### 2. Layer Caching
```dockerfile
# Sık değişmeyen dosyaları önce kopyalayın
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 3. Resource Limits
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

## CI/CD Entegrasyonu

### GitHub Actions Örneği
```yaml
name: Docker Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build image
        run: docker build -t myapp .
      - name: Run tests
        run: docker run myapp npm test
```

## Kaynaklar

### Dokümantasyon
- [Docker Official Docs](https://docs.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### Video Eğitimler
- [Docker Tutorial for Beginners](https://www.youtube.com/watch?v=fqMOX6JJhGo)
- [Docker Compose Tutorial](https://www.youtube.com/watch?v=HG6yIjZapSA)

### Kitaplar
- "Docker in Action" - Jeff Nickoloff
- "The Docker Book" - James Turnbull

---

Bu dokümantasyon Docker öğrenme sürecinizde size yardımcı olacaktır. Sorularınız için issue açabilirsiniz. 