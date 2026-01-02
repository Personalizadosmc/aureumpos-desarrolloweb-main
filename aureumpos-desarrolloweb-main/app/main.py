from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api.routes import auth, categories, products, carts, quotations
from app.models import User, Category, Product, Cart, CartItem, Quotation, QuotationItem
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from app.database import SessionLocal

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AureumPOS API",
    description="Sistema de punto de venta para productos personalizados",
    version="1.0.0"
)

# CORS
# Definimos manualmente quién puede entrar
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://github.com/Personalizadosmc",
    "https://personalizadosmc.github.io/Aureumpos.Web/" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # <--- Aquí usamos la lista que acabamos de crear
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(carts.router)
app.include_router(quotations.router)


@app.on_event("startup")
async def startup_event():
    """Crear usuario administrador si no existe"""
    db: Session = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin:
            # Asegurar que la contraseña no exceda 72 bytes (límite de bcrypt)
            password = settings.ADMIN_PASSWORD[:72] if len(settings.ADMIN_PASSWORD.encode('utf-8')) > 72 else settings.ADMIN_PASSWORD
            admin = User(
                email=settings.ADMIN_EMAIL,
                hashed_password=get_password_hash(password),
                first_name="Admin",
                last_name="AureumPOS",
                is_admin=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"✅ Usuario administrador creado: {settings.ADMIN_EMAIL}")
        else:
            print(f"✅ Usuario administrador ya existe: {settings.ADMIN_EMAIL}")
    except Exception as e:
        print(f"⚠️ Error al crear usuario administrador: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "message": "Bienvenido a AureumPOS API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

