from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
from datetime import datetime
from typing import List, Optional
import redis
import json

from .models import User, UserCreate, UserUpdate, HealthCheck, ServiceInfo, MetricsResponse
from .database import DatabaseManager

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI uygulaması
app = FastAPI(
    title="Docker Learning API",
    description="Docker öğrenme projesi için REST API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global değişkenler
db_manager = DatabaseManager()
redis_client = None

@app.on_event("startup")
async def startup_event():
    """Uygulama başlangıcında çalışacak fonksiyonlar"""
    global redis_client
    
    logger.info("Starting Docker Learning API v1.0.0")
    
    # Veritabanı bağlantısı
    await db_manager.connect()
    await db_manager.create_tables()
    
    # Redis bağlantısı
    try:
        redis_url = os.getenv("REDIS_URL", "redis://cache:6379")
        redis_client = redis.from_url(redis_url)
        redis_client.ping()  # Bağlantı testi
        logger.info("Redis connection established")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")
        redis_client = None
    
    logger.info("Application started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Uygulama kapanışında çalışacak fonksiyonlar"""
    await db_manager.disconnect()
    if redis_client:
        redis_client.close()
    logger.info("Application shutdown complete")

@app.get("/", response_model=dict)
async def root():
    """Ana endpoint - API bilgileri"""
    return {
        "message": "Hoş geldiniz! Docker Learning API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "users": "/users",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    try:
        # Veritabanı bağlantı kontrolü
        db_status = await db_manager.check_connection()
        
        # Redis bağlantı kontrolü
        redis_status = False
        if redis_client:
            try:
                redis_client.ping()
                redis_status = True
            except:
                pass
        
        return HealthCheck(
            status="healthy" if db_status and redis_status else "unhealthy",
            timestamp=datetime.now(),
            database=db_status,
            cache=redis_status,
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthCheck(
            status="unhealthy",
            timestamp=datetime.now(),
            database=False,
            cache=False,
            version="1.0.0"
        )

@app.get("/users", response_model=List[User])
async def get_users():
    """Tüm kullanıcıları getir"""
    try:
        users = await db_manager.get_all_users()
        return users
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """Yeni kullanıcı oluştur"""
    try:
        # Email kontrolü
        existing_user = await db_manager.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Kullanıcı oluştur
        new_user = await db_manager.create_user(user)
        
        # Cache'e kaydet
        if redis_client:
            try:
                redis_client.setex(
                    f"user:{new_user.id}",
                    3600,  # 1 saat
                    json.dumps(new_user.dict())
                )
            except:
                pass
        
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Belirli bir kullanıcıyı getir"""
    try:
        # Önce cache'den kontrol et
        if redis_client:
            try:
                cached_user = redis_client.get(f"user:{user_id}")
                if cached_user:
                    return User(**json.loads(cached_user))
            except:
                pass
        
        # Veritabanından getir
        user = await db_manager.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Cache'e kaydet
        if redis_client:
            try:
                redis_client.setex(
                    f"user:{user_id}",
                    3600,
                    json.dumps(user.dict())
                )
            except:
                pass
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """Kullanıcı bilgilerini güncelle"""
    try:
        # Kullanıcının var olup olmadığını kontrol et
        existing_user = await db_manager.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Güncelle
        updated_user = await db_manager.update_user(user_id, user_update)
        
        # Cache'i temizle
        if redis_client:
            try:
                redis_client.delete(f"user:{user_id}")
            except:
                pass
        
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Kullanıcıyı sil"""
    try:
        # Kullanıcının var olup olmadığını kontrol et
        existing_user = await db_manager.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Sil
        await db_manager.delete_user(user_id)
        
        # Cache'i temizle
        if redis_client:
            try:
                redis_client.delete(f"user:{user_id}")
            except:
                pass
        
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Sistem metriklerini getir"""
    try:
        # Kullanıcı sayısı
        users = await db_manager.get_all_users()
        user_count = len(users)
        
        # Redis durumu
        cache_status = False
        if redis_client:
            try:
                redis_client.ping()
                cache_status = True
            except:
                pass
        
        return MetricsResponse(
            timestamp=datetime.now(),
            user_count=user_count,
            cache_status=cache_status,
            uptime="running"
        )
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/info", response_model=ServiceInfo)
async def get_service_info():
    """Servis bilgilerini getir"""
    return ServiceInfo(
        name="Docker Learning API",
        version="1.0.0",
        description="Docker öğrenme projesi için REST API",
        environment=os.getenv("ENVIRONMENT", "development"),
        database_url=os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/dbname"),
        redis_url=os.getenv("REDIS_URL", "redis://cache:6379")
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 