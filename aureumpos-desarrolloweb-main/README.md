# AureumPOS - Backend API

Sistema de punto de venta diseñado para negocios de productos personalizados. Backend desarrollado con FastAPI, PostgreSQL y autenticación JWT.

## Características

- **Autenticación JWT**: Sistema seguro de autenticación con tokens
- **Gestión de Usuarios**: Registro e inicio de sesión para clientes y administradores
- **CRUD de Categorías**: Administración completa de categorías de productos
- **CRUD de Productos**: Gestión de productos con actualización automática de precios en carritos
- **Carritos de Compras**: Carritos personalizados por usuario con persistencia
- **Cotizaciones**: Generación de cotizaciones en formato PDF
- **API REST**: Endpoints RESTful bien documentados
- **Docker Compose**: Configuración lista para deployment

## Requisitos Previos

- Docker y Docker Compose instalados
- Git (opcional, para clonar el repositorio)

## Instalación y Configuración

### 1. Clonar o descargar el repositorio

```bash
git clone <url-del-repositorio>
cd aureumpos-backend
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (puedes copiar de `.env.example`):

```bash
# Database
DATABASE_URL=postgresql://aureumpos_user:aureumpos_password@db:5432/aureumpos_db

# JWT
SECRET_KEY=tu-clave-secreta-minimo-32-caracteres-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin User
ADMIN_EMAIL=admin@aureumpos.com
ADMIN_PASSWORD=admin123

# CORS (agregar los orígenes de tu frontend)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://127.0.0.1:5500
```

**IMPORTANTE**: Cambia el `SECRET_KEY` por una clave segura en producción.

### 3. Levantar los servicios con Docker Compose

```bash
docker-compose up -d
```

Este comando:
- Descarga e instala PostgreSQL
- Construye la imagen del backend
- Crea las tablas en la base de datos
- Crea el usuario administrador automáticamente

### 4. Verificar que todo esté funcionando

```bash
# Ver logs del backend
docker-compose logs -f backend

# Verificar que la API responde
curl http://localhost:8000/health
```

Deberías ver: `{"status":"ok"}`

### 5. Acceder a la documentación interactiva

Abre tu navegador en: **http://localhost:8000/docs**

Aquí encontrarás:
- Documentación completa de todos los endpoints
- Interfaz para probar la API directamente
- Esquemas de datos y validaciones

## Endpoints Principales

### Autenticación
- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Iniciar sesión (obtener token JWT)
- `GET /auth/me` - Obtener información del usuario actual

### Categorías (Requiere autenticación de administrador)
- `GET /categories` - Listar todas las categorías
- `GET /categories/{id}` - Obtener categoría por ID
- `POST /categories` - Crear nueva categoría
- `PUT /categories/{id}` - Actualizar categoría
- `DELETE /categories/{id}` - Eliminar categoría

### Productos (Requiere autenticación de administrador para crear/editar/eliminar)
- `GET /products` - Listar productos (filtros: `category_id`, `search`)
- `GET /products/{id}` - Obtener producto por ID
- `POST /products` - Crear nuevo producto
- `PUT /products/{id}` - Actualizar producto
- `DELETE /products/{id}` - Eliminar producto

### Carritos (Requiere autenticación)
- `GET /carts` - Obtener carrito del usuario actual
- `POST /carts/items` - Agregar producto al carrito
- `PUT /carts/items/{id}` - Actualizar cantidad de item
- `DELETE /carts/items/{id}` - Eliminar item del carrito
- `DELETE /carts` - Vaciar carrito completo

### Cotizaciones (Requiere autenticación)
- `POST /quotations` - Crear cotización desde el carrito
- `GET /quotations` - Listar cotizaciones del usuario
- `GET /quotations/{id}` - Obtener cotización por ID
- `GET /quotations/{id}/pdf` - Descargar cotización en PDF

## Autenticación

La API usa autenticación basada en tokens JWT. Para usar endpoints protegidos:

1. Inicia sesión con `POST /auth/login`
2. Copia el `access_token` de la respuesta
3. En las siguientes peticiones, incluye el header:
   ```
   Authorization: Bearer <tu-token>
   ```

### Usuario Administrador por Defecto

Al iniciar el sistema, se crea automáticamente un usuario administrador:
- **Email**: `admin@aureumpos.com` (configurable en `.env`)
- **Password**: `admin123` (configurable en `.env`)

**IMPORTANTE**: Cambia estas credenciales en producción.

## Estructura de la Base de Datos

### Tablas Principales

- **users**: Usuarios del sistema (clientes y administradores)
- **categories**: Categorías de productos
- **products**: Productos del catálogo
- **carts**: Carritos de compra (uno por usuario)
- **cart_items**: Items en los carritos
- **quotations**: Cotizaciones generadas
- **quotation_items**: Items de las cotizaciones

## Comandos Docker Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
docker-compose logs -f db

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (elimina la base de datos)
docker-compose down -v

# Reconstruir imágenes
docker-compose build --no-cache

# Ejecutar comandos en el contenedor del backend
docker-compose exec backend bash

# Acceder a PostgreSQL
docker-compose exec db psql -U aureumpos_user -d aureumpos_db
```

## Desarrollo Local (sin Docker)

Si prefieres desarrollar sin Docker:

### 1. Instalar PostgreSQL localmente

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` con la URL de tu base de datos local:

```
DATABASE_URL=postgresql://usuario:password@localhost:5432/aureumpos_db
```

### 5. Crear tablas

```bash
# Las tablas se crean automáticamente al iniciar la aplicación
# O puedes usar Alembic:
alembic upgrade head
```

### 6. Ejecutar servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Migraciones de Base de Datos

El proyecto usa Alembic para gestionar migraciones:

```bash
# Crear nueva migración
docker-compose exec backend alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
docker-compose exec backend alembic upgrade head

# Revertir última migración
docker-compose exec backend alembic downgrade -1
```

## Probar la API

### Usando la documentación interactiva

1. Ve a http://localhost:8000/docs
2. Haz clic en "Authorize" e ingresa tu token JWT
3. Prueba los endpoints directamente desde el navegador

### Usando curl

```bash
# Registrar usuario
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cliente@example.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "address": "Calle 123",
    "phone": "555-1234"
  }'

# Iniciar sesión
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cliente@example.com",
    "password": "password123"
  }'

# Obtener categorías (con token)
curl -X GET "http://localhost:8000/categories" \
  -H "Authorization: Bearer <tu-token>"
```

## Deployment en Máquina Virtual

### Opción 1: Docker Compose (Recomendado)

1. Copia todo el proyecto a la VM
2. Asegúrate de tener Docker y Docker Compose instalados
3. Configura el archivo `.env` con los valores apropiados
4. Ejecuta `docker-compose up -d`
5. La API estará disponible en `http://<ip-de-la-vm>:8000`

### Opción 2: Instalación Directa

1. Instala PostgreSQL en la VM
2. Instala Python 3.11+
3. Crea un entorno virtual e instala dependencias
4. Configura variables de entorno
5. Ejecuta con `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Configurar Firewall

Asegúrate de abrir el puerto 8000 en el firewall de la VM:

```bash
# Ubuntu/Debian
sudo ufw allow 8000/tcp

# CentOS/RHEL
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

## Solución de Problemas

### La base de datos no se conecta

- Verifica que el contenedor de PostgreSQL esté corriendo: `docker-compose ps`
- Revisa los logs: `docker-compose logs db`
- Verifica la URL en `.env`

### Error al crear usuario administrador

- Verifica que las variables `ADMIN_EMAIL` y `ADMIN_PASSWORD` estén en `.env`
- Revisa los logs del backend: `docker-compose logs backend`

### CORS errors en el frontend

- Agrega la URL de tu frontend a `CORS_ORIGINS` en `.env`
- Reinicia el backend: `docker-compose restart backend`

## Licencia

Este proyecto es parte de un trabajo académico para la Universidad Abierta para Adultos.

## Autores

- Edgar Eduardo Arias Rosado - 100044023
- Jean Carlos Ortiz Paulino - 100064397
- Joel Antonio Alcántara Breton - 100070754
- Lenny Badil González Peña - 100056907
- Pavel Fernando González Medina - 100061480

## Soporte

Para problemas o preguntas, contacta al equipo de desarrollo.

---

**¡Listo para usar!**

El backend está completamente funcional y listo para que tus compañeros implementen el frontend. Todos los endpoints están documentados en `/docs` y la API sigue las mejores prácticas de REST.

