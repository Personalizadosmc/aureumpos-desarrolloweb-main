# Guía para Obtener y Usar Tokens JWT en AureumPOS API

## Método 1: Usando la Documentación Interactiva (Swagger UI) - RECOMENDADO

1. **Abre la documentación:**
   ```
   http://localhost:8000/docs
   ```

2. **Registra un nuevo usuario o inicia sesión:**
   - Busca el endpoint `POST /auth/register` o `POST /auth/login`
   - Haz clic en "Try it out"
   - Ingresa las credenciales:
     ```json
     {
       "email": "tu@email.com",
       "password": "tu_password"
     }
     ```
   - Haz clic en "Execute"

3. **Copia el token:**
   - En la respuesta, copia el valor de `access_token`

4. **Autoriza en Swagger:**
   - Haz clic en el botón **"Authorize"** (arriba a la derecha)
   - Pega el token en el campo "Value" (sin escribir "Bearer")
   - Haz clic en "Authorize" y luego "Close"
   - Ahora todos los endpoints protegidos funcionarán automáticamente

---

## Método 2: Usando PowerShell (Windows)

### Opción A: Usar el script incluido

```powershell
# Ejecutar el script
.\get_token.ps1

# O con credenciales personalizadas
.\get_token.ps1 -Email "tu@email.com" -Password "tu_password"
```

### Opción B: Comandos manuales

```powershell
# 1. Registrar un nuevo usuario
$body = @{
    email = "test@example.com"
    password = "test123"
    first_name = "Test"
    last_name = "User"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/register" `
    -Method POST -ContentType "application/json" -Body $body

# 2. Iniciar sesión y obtener token
$loginBody = @{
    email = "test@example.com"
    password = "test123"
} | ConvertTo-Json

$tokenResponse = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
    -Method POST -ContentType "application/json" -Body $loginBody

# 3. Ver el token
Write-Host "Token: $($tokenResponse.access_token)"

# 4. Guardar el token en un archivo
$tokenResponse.access_token | Out-File -FilePath "token.txt" -Encoding utf8
```

---

## Método 3: Usando curl (Linux/Mac/Windows)

```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "first_name": "Test",
    "last_name": "User"
  }'

# 2. Iniciar sesión y obtener token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'

# La respuesta incluirá el access_token
```

---

## Método 4: Usando JavaScript/Fetch (Frontend)

```javascript
// Registrar usuario
const registerUser = async () => {
  const response = await fetch('http://localhost:8000/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: 'test@example.com',
      password: 'test123',
      first_name: 'Test',
      last_name: 'User'
    })
  });
  
  const data = await response.json();
  return data;
};

// Iniciar sesión y obtener token
const login = async () => {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: 'test@example.com',
      password: 'test123'
    })
  });
  
  const data = await response.json();
  const token = data.access_token;
  
  // Guardar token en localStorage
  localStorage.setItem('token', token);
  
  return token;
};

// Usar el token en peticiones
const getCategories = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:8000/categories', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  return data;
};
```

---

## Usar el Token en Peticiones

### En Headers HTTP:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Ejemplos:

**PowerShell:**
```powershell
$token = Get-Content token.txt
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/categories" `
    -Headers $headers
```

**curl:**
```bash
TOKEN="tu_token_aqui"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/categories
```

**JavaScript:**
```javascript
fetch('http://localhost:8000/categories', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
```

---

## Usuario Administrador por Defecto

Si el usuario administrador se creó correctamente al iniciar el servidor:

- **Email:** `admin@aureumpos.com`
- **Password:** `admin123` (configurable en `.env`)

**Nota:** Si el usuario administrador no existe, puedes crearlo registrándote con cualquier email y luego actualizando manualmente el campo `is_admin` en la base de datos, o simplemente usar el endpoint de registro para crear un usuario normal.

---

## Endpoints que Requieren Autenticación

### Requieren Token (Usuario normal o admin):
- `GET /auth/me` - Obtener información del usuario actual
- `GET /carts` - Ver carrito
- `POST /carts/items` - Agregar al carrito
- `PUT /carts/items/{id}` - Actualizar item del carrito
- `DELETE /carts/items/{id}` - Eliminar item del carrito
- `DELETE /carts` - Vaciar carrito
- `POST /quotations` - Crear cotización
- `GET /quotations` - Listar cotizaciones
- `GET /quotations/{id}` - Ver cotización
- `GET /quotations/{id}/pdf` - Descargar PDF

### Requieren Token de Administrador:
- `POST /categories` - Crear categoría
- `PUT /categories/{id}` - Actualizar categoría
- `DELETE /categories/{id}` - Eliminar categoría
- `POST /products` - Crear producto
- `PUT /products/{id}` - Actualizar producto
- `DELETE /products/{id}` - Eliminar producto

### No Requieren Autenticación:
- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Iniciar sesión
- `GET /categories` - Listar categorías
- `GET /categories/{id}` - Ver categoría
- `GET /products` - Listar productos
- `GET /products/{id}` - Ver producto

---

## Validar Token

Para verificar que tu token es válido:

```powershell
$token = Get-Content token.txt
$headers = @{ "Authorization" = "Bearer $token" }
Invoke-RestMethod -Uri "http://localhost:8000/auth/me" -Headers $headers
```

Si el token es válido, verás la información de tu usuario.

---

## Duración del Token

Por defecto, los tokens expiran después de **30 minutos**. Esto es configurable en el archivo `.env` con la variable `ACCESS_TOKEN_EXPIRE_MINUTES`.

Cuando el token expire, simplemente vuelve a hacer login para obtener uno nuevo.

---

## Solución de Problemas

### Error 401 Unauthorized
- Verifica que el token esté correctamente formateado: `Bearer <token>`
- Verifica que el token no haya expirado
- Asegúrate de incluir el header `Authorization`

### Error 403 Forbidden
- El endpoint requiere permisos de administrador
- Verifica que el usuario tenga `is_admin: true`

### Token no funciona
- Verifica que copiaste el token completo (son strings largos)
- Asegúrate de incluir "Bearer " antes del token
- Verifica que el servidor esté corriendo

---

¡Listo! Ahora puedes probar todos los endpoints de la API.

