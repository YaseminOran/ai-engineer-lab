import asyncpg
import os
import logging
from typing import List, Optional
from datetime import datetime
from .models import User, UserCreate, UserUpdate

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.database_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/docker_learning")
    
    async def connect(self):
        """Veritabanı bağlantısını kur"""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=10
            )
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    async def disconnect(self):
        """Veritabanı bağlantısını kapat"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection closed")
    
    async def check_connection(self) -> bool:
        """Veritabanı bağlantısını kontrol et"""
        try:
            if self.pool:
                async with self.pool.acquire() as conn:
                    await conn.execute("SELECT 1")
                return True
            return False
        except Exception as e:
            logger.error(f"Database connection check failed: {e}")
            return False
    
    async def create_tables(self):
        """Veritabanı tablolarını oluştur"""
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    async def get_all_users(self) -> List[User]:
        """Tüm kullanıcıları getir"""
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch("""
                    SELECT id, email, name, is_active, created_at, updated_at
                    FROM users
                    ORDER BY created_at DESC
                """)
                
                users = []
                for row in rows:
                    users.append(User(
                        id=row['id'],
                        email=row['email'],
                        name=row['name'],
                        is_active=row['is_active'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    ))
                return users
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            raise
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """ID'ye göre kullanıcı getir"""
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT id, email, name, is_active, created_at, updated_at
                    FROM users
                    WHERE id = $1
                """, user_id)
                
                if row:
                    return User(
                        id=row['id'],
                        email=row['email'],
                        name=row['name'],
                        is_active=row['is_active'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                return None
        except Exception as e:
            logger.error(f"Error getting user by id {user_id}: {e}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Email'e göre kullanıcı getir"""
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT id, email, name, is_active, created_at, updated_at
                    FROM users
                    WHERE email = $1
                """, email)
                
                if row:
                    return User(
                        id=row['id'],
                        email=row['email'],
                        name=row['name'],
                        is_active=row['is_active'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                return None
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise
    
    async def create_user(self, user: UserCreate) -> User:
        """Yeni kullanıcı oluştur"""
        try:
            async with self.pool.acquire() as conn:
                # Basit password hash (production'da bcrypt kullanın)
                password_hash = f"hashed_{user.password}"
                
                row = await conn.fetchrow("""
                    INSERT INTO users (email, name, password_hash, is_active)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id, email, name, is_active, created_at, updated_at
                """, user.email, user.name, password_hash, True)
                
                return User(
                    id=row['id'],
                    email=row['email'],
                    name=row['name'],
                    is_active=row['is_active'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """Kullanıcı bilgilerini güncelle"""
        try:
            async with self.pool.acquire() as conn:
                # Güncellenecek alanları belirle
                update_fields = []
                values = []
                param_count = 1
                
                if user_update.email is not None:
                    update_fields.append(f"email = ${param_count}")
                    values.append(user_update.email)
                    param_count += 1
                
                if user_update.name is not None:
                    update_fields.append(f"name = ${param_count}")
                    values.append(user_update.name)
                    param_count += 1
                
                if user_update.is_active is not None:
                    update_fields.append(f"is_active = ${param_count}")
                    values.append(user_update.is_active)
                    param_count += 1
                
                if not update_fields:
                    # Güncellenecek alan yoksa mevcut kullanıcıyı getir
                    return await self.get_user_by_id(user_id)
                
                # updated_at alanını ekle
                update_fields.append(f"updated_at = CURRENT_TIMESTAMP")
                
                values.append(user_id)
                
                query = f"""
                    UPDATE users 
                    SET {', '.join(update_fields)}
                    WHERE id = ${param_count}
                    RETURNING id, email, name, is_active, created_at, updated_at
                """
                
                row = await conn.fetchrow(query, *values)
                
                return User(
                    id=row['id'],
                    email=row['email'],
                    name=row['name'],
                    is_active=row['is_active'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            raise
    
    async def delete_user(self, user_id: int):
        """Kullanıcıyı sil"""
        try:
            async with self.pool.acquire() as conn:
                result = await conn.execute("""
                    DELETE FROM users
                    WHERE id = $1
                """, user_id)
                
                if result == "DELETE 0":
                    raise ValueError("User not found")
                
                logger.info(f"User {user_id} deleted successfully")
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            raise 