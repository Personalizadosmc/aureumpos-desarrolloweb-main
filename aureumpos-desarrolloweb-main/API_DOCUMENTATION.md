# Documentación de la API - AureumPOS

## Base URL
```
http://localhost:8000
```

## Autenticación

Todos los endpoints protegidos requieren un token JWT en el header:
```
Authorization: Bearer <token>
```

## Endpoints

### Autenticación (`/auth`)

#### Registrar Usuario
```http
POST /auth/register
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "password123",
  "first_name": "Juan",
  "last_name": "Pérez",
  "address": "Calle 123",
  "phone": "555-1234"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "address": "Calle 123",
  "phone": "555-1234",
  "is_admin": false,
  "created_at": "2025-12-02T10:00:00"
}
```

#### Iniciar Sesión
```http
POST /auth/login
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "password123"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "usuario@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "is_admin": false
  }
}
```

#### Obtener Usuario Actual
```http
GET /auth/me
Authorization: Bearer <token>
```

---

### Categorías (`/categories`)

#### Listar Categorías
```http
GET /categories
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Tazas Personalizadas",
    "image_url": "https://example.com/tazas.jpg",
    "product_count": 5,
    "created_at": "2025-12-02T10:00:00"
  }
]
```

#### Obtener Categoría
```http
GET /categories/{id}
```

#### Crear Categoría (Admin)
```http
POST /categories
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "name": "Termos",
  "image_url": "https://example.com/termos.jpg"
}
```

#### Actualizar Categoría (Admin)
```http
PUT /categories/{id}
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "name": "Termos Premium",
  "image_url": "https://example.com/termos-premium.jpg"
}
```

#### Eliminar Categoría (Admin)
```http
DELETE /categories/{id}
Authorization: Bearer <admin-token>
```

---

### Productos (`/products`)

#### Listar Productos
```http
GET /products?category_id=1&search=taza
```

**Parámetros de consulta:**
- `category_id` (opcional): Filtrar por categoría
- `search` (opcional): Buscar por nombre

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Taza Cerámica Premium",
    "price": "15.00",
    "image_url": "https://example.com/taza.jpg",
    "category_id": 1,
    "created_at": "2025-12-02T10:00:00"
  }
]
```

#### Obtener Producto
```http
GET /products/{id}
```

#### Crear Producto (Admin)
```http
POST /products
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "name": "Taza Cerámica Premium",
  "price": 15.00,
  "image_url": "https://example.com/taza.jpg",
  "category_id": 1
}
```

#### Actualizar Producto (Admin)
```http
PUT /products/{id}
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "price": 18.00,
  "name": "Taza Cerámica Premium XL"
}
```

**Nota:** Cuando se actualiza el precio de un producto, los precios en los carritos se actualizan automáticamente.

#### Eliminar Producto (Admin)
```http
DELETE /products/{id}
Authorization: Bearer <admin-token>
```

---

### Carritos (`/carts`)

#### Obtener Carrito
```http
GET /carts
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "id": 1,
  "user_id": 1,
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "product": {
        "id": 1,
        "name": "Taza Cerámica Premium",
        "price": "15.00",
        "image_url": "https://example.com/taza.jpg",
        "category_id": 1
      },
      "quantity": 2,
      "unit_price": "15.00",
      "subtotal": "30.00"
    }
  ],
  "total": "30.00",
  "created_at": "2025-12-02T10:00:00"
}
```

#### Agregar Producto al Carrito
```http
POST /carts/items
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

#### Actualizar Cantidad de Item
```http
PUT /carts/items/{item_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "quantity": 3
}
```

#### Eliminar Item del Carrito
```http
DELETE /carts/items/{item_id}
Authorization: Bearer <token>
```

#### Vaciar Carrito
```http
DELETE /carts
Authorization: Bearer <token>
```

---

### Cotizaciones (`/quotations`)

#### Crear Cotización
```http
POST /quotations
Authorization: Bearer <token>
```

Crea una cotización a partir del carrito actual del usuario.

**Respuesta:**
```json
{
  "id": 1,
  "quotation_number": "COT-20251202100000",
  "user_id": 1,
  "total_amount": "132.00",
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "product_name": "Taza Cerámica Premium",
      "quantity": 1,
      "unit_price": "15.00",
      "subtotal": "15.00"
    }
  ],
  "created_at": "2025-12-02T10:00:00"
}
```

#### Listar Cotizaciones del Usuario
```http
GET /quotations
Authorization: Bearer <token>
```

#### Obtener Cotización
```http
GET /quotations/{id}
Authorization: Bearer <token>
```

#### Descargar Cotización en PDF
```http
GET /quotations/{id}/pdf
Authorization: Bearer <token>
```

Retorna un archivo PDF descargable con la cotización completa.

---

## Códigos de Estado HTTP

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Recurso eliminado exitosamente
- `400 Bad Request`: Error en la solicitud
- `401 Unauthorized`: No autenticado o token inválido
- `403 Forbidden`: No tiene permisos (requiere admin)
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Ejemplos de Uso

### Flujo Completo: Cliente

1. **Registrarse**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cliente@example.com",
    "password": "password123",
    "first_name": "Juan",
    "last_name": "Pérez"
  }'
```

2. **Iniciar Sesión**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cliente@example.com",
    "password": "password123"
  }'
```

3. **Ver Productos**
```bash
curl http://localhost:8000/products \
  -H "Authorization: Bearer <token>"
```

4. **Agregar al Carrito**
```bash
curl -X POST http://localhost:8000/carts/items \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

5. **Crear Cotización**
```bash
curl -X POST http://localhost:8000/quotations \
  -H "Authorization: Bearer <token>"
```

### Flujo Completo: Administrador

1. **Iniciar Sesión como Admin**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@aureumpos.com",
    "password": "admin123"
  }'
```

2. **Crear Categoría**
```bash
curl -X POST http://localhost:8000/categories \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tazas Personalizadas",
    "image_url": "https://example.com/tazas.jpg"
  }'
```

3. **Crear Producto**
```bash
curl -X POST http://localhost:8000/products \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Taza Cerámica Premium",
    "price": 15.00,
    "image_url": "https://example.com/taza.jpg",
    "category_id": 1
  }'
```

## Notas Importantes

1. **Tokens JWT**: Los tokens expiran después de 30 minutos (configurable)
2. **Actualización de Precios**: Cuando un admin actualiza el precio de un producto, los precios en los carritos se actualizan automáticamente
3. **Carritos Persistentes**: Cada usuario tiene su propio carrito que persiste entre sesiones
4. **Cotizaciones**: Las cotizaciones guardan un snapshot de los precios al momento de crearlas
5. **CORS**: Configura los orígenes permitidos en la variable `CORS_ORIGINS`

