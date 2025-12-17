"""
Topshiriq: FastAPI Application with .env Configuration using environs
Bajarilgan topshiriqlar:
- .env fayl yaratish va environment variables saqlash
- environs kutubxonasidan foydalanish (env.str, env.list, env.int, env.bool)
- FastAPI da .env o'zgaruvchilaridan foydalanish
- Settings class yaratish (environs bilan)
- Database, Security, CORS, Email, Redis konfiguratsiyalari
- Professional darajada environment variables boshqarish
"""

import os
import asyncio
from typing import List, Optional
from functools import lru_cache
from environs import Env
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import uvloop

# Env instance yaratish va .env faylni yuklash
env = Env()
env.read_env()

# uvloop event loop policy
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Settings:
    """Application Settings - .env fayldan environs orqali o'qiladi"""
    
    def __init__(self):
        # Application
        self.app_name: str = env.str("APP_NAME", default="FastAPI Application")
        self.app_version: str = env.str("APP_VERSION", default="1.0.0")
        self.debug: bool = env.bool("DEBUG", default=True)
        self.environment: str = env.str("ENVIRONMENT", default="development")
        
        # Server
        self.host: str = env.str("HOST", default="0.0.0.0")
        self.port: int = env.int("PORT", default=8000)
        
        # Database
        self.database_url: str = env.str(
            "DATABASE_URL", 
            default="postgresql://user:password@localhost:5432/mydb"
        )
        self.database_pool_size: int = env.int("DATABASE_POOL_SIZE", default=10)
        self.database_max_overflow: int = env.int("DATABASE_MAX_OVERFLOW", default=20)
        
        # Security
        self.secret_key: str = env.str("SECRET_KEY", default="your-secret-key-change-this")
        self.algorithm: str = env.str("ALGORITHM", default="HS256")
        self.access_token_expire_minutes: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
        self.refresh_token_expire_days: int = env.int("REFRESH_TOKEN_EXPIRE_DAYS", default=7)
        
        # CORS - list sifatida o'qiladi
        self.cors_origins: List[str] = env.list("CORS_ORIGINS", default=["http://localhost:3000"])
        self.cors_allow_credentials: bool = env.bool("CORS_ALLOW_CREDENTIALS", default=True)
        self.cors_allow_methods: List[str] = env.list(
            "CORS_ALLOW_METHODS", 
            default=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        )
        self.cors_allow_headers: List[str] = env.list("CORS_ALLOW_HEADERS", default=["*"])
        
        # API Keys
        self.api_key_openai: Optional[str] = env.str("API_KEY_OPENAI", default=None)
        self.api_key_stripe: Optional[str] = env.str("API_KEY_STRIPE", default=None)
        self.api_key_sendgrid: Optional[str] = env.str("API_KEY_SENDGRID", default=None)
        
        # Email
        self.smtp_host: str = env.str("SMTP_HOST", default="smtp.gmail.com")
        self.smtp_port: int = env.int("SMTP_PORT", default=587)
        self.smtp_user: str = env.str("SMTP_USER", default="")
        self.smtp_password: str = env.str("SMTP_PASSWORD", default="")
        self.smtp_tls: bool = env.bool("SMTP_TLS", default=True)
        self.email_from: str = env.str("EMAIL_FROM", default="noreply@example.com")
        
        # Redis
        self.redis_host: str = env.str("REDIS_HOST", default="localhost")
        self.redis_port: int = env.int("REDIS_PORT", default=6379)
        self.redis_password: Optional[str] = env.str("REDIS_PASSWORD", default=None)
        self.redis_db: int = env.int("REDIS_DB", default=0)
        
        # Logging
        self.log_level: str = env.str("LOG_LEVEL", default="INFO")
        self.log_file: str = env.str("LOG_FILE", default="app.log")
        self.log_format: str = env.str("LOG_FORMAT", default="json")
        
        # File Upload
        self.max_upload_size: int = env.int("MAX_UPLOAD_SIZE", default=10485760)  # 10MB
        self.upload_dir: str = env.str("UPLOAD_DIR", default="uploads")
        # Allowed extensions - list sifatida o'qiladi
        self.allowed_extensions: List[str] = env.list(
            "ALLOWED_EXTENSIONS", 
            default=["jpg", "jpeg", "png", "pdf", "doc", "docx"]
        )
        
        # Rate Limiting
        self.rate_limit_per_minute: int = env.int("RATE_LIMIT_PER_MINUTE", default=60)
        self.rate_limit_per_hour: int = env.int("RATE_LIMIT_PER_HOUR", default=1000)
        
        # Cache
        self.cache_ttl: int = env.int("CACHE_TTL", default=3600)
        self.cache_enabled: bool = env.bool("CACHE_ENABLED", default=True)
    
    @property
    def cors_origins_list(self) -> List[str]:
        """CORS origins list (allaqachon list)"""
        return self.cors_origins
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Allowed extensions list (allaqachon list)"""
        return self.allowed_extensions
    
    @property
    def database_config(self) -> dict:
        """Database konfiguratsiyasi"""
        return {
            "url": self.database_url,
            "pool_size": self.database_pool_size,
            "max_overflow": self.database_max_overflow
        }
    
    @property
    def redis_config(self) -> dict:
        """Redis konfiguratsiyasi"""
        return {
            "host": self.redis_host,
            "port": self.redis_port,
            "password": self.redis_password,
            "db": self.redis_db
        }
    
    @property
    def email_config(self) -> dict:
        """Email konfiguratsiyasi"""
        return {
            "host": self.smtp_host,
            "port": self.smtp_port,
            "user": self.smtp_user,
            "password": self.smtp_password,
            "tls": self.smtp_tls,
            "from": self.email_from
        }


@lru_cache()
def get_settings() -> Settings:
    """Settings singleton"""
    return Settings()


# Settings instance
settings = get_settings()

# FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="FastAPI application with .env configuration using environs"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"🚀 {settings.app_name} v{settings.app_version} ishga tushmoqda...")
    print(f"📝 Environment: {settings.environment}")
    print(f"🔧 Debug mode: {settings.debug}")
    print(f"🌐 Server: {settings.host}:{settings.port}")
    print(f"📊 Database: {settings.database_url.split('@')[-1] if '@' in settings.database_url else 'Not configured'}")
    print(f"🔐 Secret key: {'*' * 20} (hidden)")
    print(f"📧 Email: {settings.email_from}")
    print(f"💾 Redis: {settings.redis_host}:{settings.redis_port}")
    print(f"🌍 CORS Origins: {', '.join(settings.cors_origins_list)}")
    
    # Uploads papkasini yaratish
    os.makedirs(settings.upload_dir, exist_ok=True)
    
    app.state.settings = settings
    app.state.db_connection = "connected"
    
    yield
    
    # Shutdown
    print("🛑 Server to'xtatilmoqda...")
    if hasattr(app.state, "db_connection"):
        app.state.db_connection = None
    print("✅ Server to'xtatildi")


app.router.lifespan_context = lifespan


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if hasattr(app.state, "db_connection") else "disconnected",
        "environment": settings.environment
    }


@app.get("/config")
async def get_config(current_settings: Settings = Depends(get_settings)):
    """Konfiguratsiyani ko'rish (faqat development muhitida)"""
    if current_settings.environment != "development":
        raise HTTPException(status_code=403, detail="Config endpoint faqat development muhitida mavjud")
    
    return {
        "app": {
            "name": current_settings.app_name,
            "version": current_settings.app_version,
            "environment": current_settings.environment,
            "debug": current_settings.debug
        },
        "server": {
            "host": current_settings.host,
            "port": current_settings.port
        },
        "database": {
            "url": current_settings.database_url.split("@")[-1] if "@" in current_settings.database_url else "hidden",
            "pool_size": current_settings.database_pool_size
        },
        "security": {
            "algorithm": current_settings.algorithm,
            "token_expire_minutes": current_settings.access_token_expire_minutes
        },
        "cors": {
            "origins": current_settings.cors_origins_list,
            "allow_credentials": current_settings.cors_allow_credentials
        },
        "redis": current_settings.redis_config,
        "email": {
            "host": current_settings.smtp_host,
            "port": current_settings.smtp_port,
            "from": current_settings.email_from
        },
        "upload": {
            "max_size": current_settings.max_upload_size,
            "allowed_extensions": current_settings.allowed_extensions_list
        },
        "rate_limiting": {
            "per_minute": current_settings.rate_limit_per_minute,
            "per_hour": current_settings.rate_limit_per_hour
        },
        "cache": {
            "enabled": current_settings.cache_enabled,
            "ttl": current_settings.cache_ttl
        }
    }


@app.get("/env-example")
async def env_example():
    """.env fayl misoli"""
    return {
        "message": "Quyidagi o'zgaruvchilar .env faylga qo'shilishi kerak:",
        "variables": {
            "APP_NAME": "FastAPI Application",
            "DEBUG": "True",
            "HOST": "0.0.0.0",
            "PORT": "8000",
            "DATABASE_URL": "postgresql://user:password@localhost:5432/mydb",
            "SECRET_KEY": "your-secret-key-here",
            "CORS_ORIGINS": "http://localhost:3000,http://localhost:8080",
            "SMTP_HOST": "smtp.gmail.com",
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "ALLOWED_EXTENSIONS": "jpg,jpeg,png,pdf"
        },
        "note": "environs kutubxonasi env.str(), env.list(), env.int(), env.bool() metodlaridan foydalanadi"
    }


def main():
    """Asosiy funksiya - uvicorn serverni ishga tushiradi"""
    print("\n" + "="*50)
    print(f"  {settings.app_name} v{settings.app_version}")
    print("="*50 + "\n")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()
