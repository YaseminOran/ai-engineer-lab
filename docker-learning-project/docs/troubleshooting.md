# 🔧 Docker Sorun Giderme Rehberi

Bu dokümantasyon, Docker kullanımında karşılaşabileceğiniz yaygın sorunları ve çözümlerini içerir.

## 🚨 Yaygın Sorunlar

### 1. Port Çakışması

**Sorun**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Çözüm**:
```bash
# Port kullanımını kontrol et
lsof -i :8000

# Çakışan process'i bul ve durdur
sudo kill -9 $(lsof -t -i:8000)

# Veya farklı port kullan
docker run -p 8001:8000 myapp
```

**Docker Compose'da**:
```yaml
services:
  app:
    ports:
      - "8001:8000"  # Host port'u değiştir
```

### 2. Permission Denied

**Sorun**: `Got permission denied while trying to connect to the Docker daemon`

**Çözüm**:
```bash
# Kullanıcıyı docker group'a ekle
sudo usermod -aG docker $USER

# Yeni terminal aç veya logout/login yap
newgrp docker

# Docker service'ini yeniden başlat
sudo systemctl restart docker
```

### 3. Disk Space Sorunu

**Sorun**: `no space left on device`

**Çözüm**:
```bash
# Kullanılmayan Docker kaynaklarını temizle
docker system prune -a

# Disk kullanımını kontrol et
docker system df

# Belirli volume'ları temizle
docker volume prune
```

### 4. Container Başlatılamıyor

**Sorun**: Container sürekli restart oluyor

**Çözüm**:
```bash
# Container loglarını kontrol et
docker logs container_name

# Container detaylarını incele
docker inspect container_name

# Health check'i kontrol et
docker inspect container_name | grep -A 10 Health
```

### 5. Network Bağlantı Sorunu

**Sorun**: Container'lar birbirini bulamıyor

**Çözüm**:
```bash
# Network'leri listele
docker network ls

# Network detaylarını incele
docker network inspect network_name

# Container'ı network'e bağla
docker network connect network_name container_name
```

## 🔍 Debugging Teknikleri

### 1. Container İçine Bağlanma

```bash
# Çalışan container'a bağlan
docker exec -it container_name bash

# Root olarak bağlan
docker exec -it --user root container_name bash

# Belirli bir shell ile bağlan
docker exec -it container_name sh
```

### 2. Log İzleme

```bash
# Tüm logları izle
docker logs -f container_name

# Son N satır
docker logs --tail=100 container_name

# Timestamp ile
docker logs -t container_name

# Belirli bir tarihten itibaren
docker logs --since="2023-01-01T00:00:00" container_name
```

### 3. Resource Kullanımı

```bash
# Real-time resource kullanımı
docker stats

# Belirli container'ların stats'ı
docker stats container1 container2

# Detaylı resource bilgisi
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### 4. Network Debugging

```bash
# Container'ın network bilgileri
docker inspect container_name | grep -A 20 "NetworkSettings"

# Port mapping kontrolü
docker port container_name

# Network connectivity test
docker exec container_name ping google.com
```

## 🐛 Docker Compose Sorunları

### 1. Service Bağımlılıkları

**Sorun**: Servisler sırayla başlamıyor

**Çözüm**:
```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 2. Environment Variables

**Sorun**: Environment variables çalışmıyor

**Çözüm**:
```yaml
services:
  app:
    environment:
      - DATABASE_URL=${DATABASE_URL}
    env_file:
      - .env
      - .env.local
```

### 3. Volume Mount Sorunları

**Sorun**: Dosyalar container'da görünmüyor

**Çözüm**:
```yaml
services:
  app:
    volumes:
      - ./app:/app:ro  # Read-only
      - ./logs:/app/logs  # Read-write
      - app_data:/app/data  # Named volume
```

## 🔧 Performance Sorunları

### 1. Yavaş Build

**Çözüm**:
```dockerfile
# .dockerignore kullan
node_modules
.git
*.log

# Multi-stage build kullan
FROM node:alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:alpine
COPY --from=builder /app/node_modules ./node_modules
COPY . .
```

### 2. Yüksek Memory Kullanımı

**Çözüm**:
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

### 3. Disk I/O Sorunları

**Çözüm**:
```yaml
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data
    tmpfs:
      - /tmp
      - /var/tmp
```

## 🛡️ Güvenlik Sorunları

### 1. Root Kullanıcı

**Sorun**: Container root olarak çalışıyor

**Çözüm**:
```dockerfile
# Non-root kullanıcı oluştur
RUN useradd --create-home --shell /bin/bash app
USER app
```

### 2. Exposed Ports

**Sorun**: Gereksiz portlar expose edilmiş

**Çözüm**:
```dockerfile
# Sadece gerekli portları expose et
EXPOSE 8000
```

### 3. Secrets Yönetimi

**Sorun**: Hassas bilgiler environment variables'da

**Çözüm**:
```yaml
services:
  app:
    secrets:
      - db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## 📊 Monitoring ve Alerting

### 1. Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

### 2. Log Aggregation

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 3. Resource Monitoring

```bash
# Container metrics
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Disk usage
docker system df

# Network usage
docker network ls
```

## 🔄 Recovery Procedures

### 1. Container Crash Recovery

```bash
# Container'ı yeniden başlat
docker restart container_name

# Yeni container oluştur
docker run --name new_container image_name

# Data recovery
docker cp container_name:/app/data ./backup/
```

### 2. Database Recovery

```bash
# Database backup
docker exec container_name pg_dump -U user dbname > backup.sql

# Database restore
docker exec -i container_name psql -U user dbname < backup.sql
```

### 3. Volume Recovery

```bash
# Volume backup
docker run --rm -v volume_name:/data -v $(pwd):/backup alpine tar czf /backup/volume_backup.tar.gz -C /data .

# Volume restore
docker run --rm -v volume_name:/data -v $(pwd):/backup alpine tar xzf /backup/volume_backup.tar.gz -C /data
```

## 🆘 Emergency Procedures

### 1. Tüm Container'ları Durdurma

```bash
# Tüm container'ları durdur
docker stop $(docker ps -q)

# Tüm container'ları sil
docker rm $(docker ps -aq)

# Docker service'ini yeniden başlat
sudo systemctl restart docker
```

### 2. Docker Daemon Reset

```bash
# Docker daemon'ı yeniden başlat
sudo systemctl stop docker
sudo systemctl start docker

# Docker daemon loglarını kontrol et
sudo journalctl -u docker.service
```

### 3. Complete Cleanup

```bash
# Tüm Docker kaynaklarını temizle
docker system prune -a --volumes

# Docker daemon'ı reset et
sudo systemctl stop docker
sudo rm -rf /var/lib/docker
sudo systemctl start docker
```

## 📞 Destek

### Log Dosyaları

```bash
# Docker daemon logları
sudo journalctl -u docker.service

# Container logları
docker logs container_name

# Docker Compose logları
docker-compose logs
```

### Debug Mode

```bash
# Docker daemon debug mode
sudo dockerd --debug

# Container debug info
docker inspect container_name
```

### Community Resources

- [Docker Community Forums](https://forums.docker.com/)
- [Stack Overflow - Docker](https://stackoverflow.com/questions/tagged/docker)
- [GitHub Issues](https://github.com/docker/docker-ce/issues)

---

Bu rehber Docker sorunlarınızı çözmenize yardımcı olacaktır. Sorununuz burada yoksa, lütfen issue açın. 