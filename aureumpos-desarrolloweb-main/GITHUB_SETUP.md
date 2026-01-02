# Guía para Subir el Proyecto a GitHub

## Pasos para Subir el Repositorio

### 1. Inicializar Git (si no está inicializado)

```bash
git init
```

### 2. Agregar todos los archivos al staging

```bash
git add .
```

### 3. Verificar qué archivos se van a subir

```bash
git status
```

**IMPORTANTE**: Asegúrate de que NO aparezcan:
- `.env` (archivo de configuración con secretos)
- `token.txt` (tokens JWT)
- Archivos de base de datos
- Archivos temporales

### 4. Hacer el commit inicial

```bash
git commit -m "Initial commit: Backend AureumPOS completo"
```

### 5. Crear el repositorio en GitHub

1. Ve a [GitHub](https://github.com)
2. Haz clic en el botón **"+"** (arriba a la derecha) y selecciona **"New repository"**
3. Completa el formulario:
   - **Repository name**: `aureumpos-backend` (o el nombre que prefieras)
   - **Description**: "Sistema de punto de venta para productos personalizados - Backend API"
   - **Visibility**: Elige **Public** o **Private**
   - **NO marques** "Initialize this repository with a README" (ya tenemos uno)
   - **NO agregues** .gitignore ni licencia (ya los tenemos)
4. Haz clic en **"Create repository"**

### 6. Conectar el repositorio local con GitHub

GitHub te mostrará comandos después de crear el repositorio. Usa estos comandos:

```bash
# Agregar el repositorio remoto (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/aureumpos-backend.git

# O si prefieres usar SSH:
# git remote add origin git@github.com:TU_USUARIO/aureumpos-backend.git
```

### 7. Subir el código a GitHub

```bash
# Primera vez (establecer upstream)
git push -u origin main

# O si tu rama se llama "master":
# git branch -M main
# git push -u origin main
```

### 8. Verificar que se subió correctamente

Ve a tu repositorio en GitHub y verifica que todos los archivos estén ahí.

---

## Comandos Rápidos (Todo en uno)

Si ya tienes Git configurado y quieres hacerlo rápido:

```bash
# 1. Inicializar
git init

# 2. Agregar archivos
git add .

# 3. Commit inicial
git commit -m "Initial commit: Backend AureumPOS completo"

# 4. Agregar remote (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/aureumpos-backend.git

# 5. Cambiar a rama main si es necesario
git branch -M main

# 6. Subir
git push -u origin main
```

---

## Configurar Git (Solo la primera vez)

Si es la primera vez que usas Git en esta computadora:

```bash
# Configurar tu nombre
git config --global user.name "Tu Nombre"

# Configurar tu email
git config --global user.email "tu@email.com"
```

---

## Archivos que NO se subirán (gracias a .gitignore)

- `.env` - Variables de entorno con secretos
- `token.txt` - Tokens JWT
- `__pycache__/` - Archivos compilados de Python
- `*.pyc` - Bytecode de Python
- `.vscode/`, `.idea/` - Configuraciones del IDE
- Archivos de base de datos
- Logs

---

## Actualizar el Repositorio (Después del primer push)

Cuando hagas cambios y quieras subirlos:

```bash
# Ver qué cambió
git status

# Agregar cambios
git add .

# O agregar archivos específicos:
# git add archivo1.py archivo2.py

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir cambios
git push
```

---

## Crear un README Atractivo

El README.md ya está creado y completo. Si quieres personalizarlo más, puedes editarlo antes de hacer el commit.

---

## Compartir con tu Equipo

Una vez subido a GitHub:

1. Ve a la página de tu repositorio
2. Haz clic en **"Settings"** (Configuración)
3. Ve a **"Collaborators"** (Colaboradores)
4. Haz clic en **"Add people"**
5. Ingresa el usuario de GitHub de tus compañeros
6. Ellos recibirán una invitación

O simplemente comparte el link del repositorio y ellos pueden hacer fork o clonarlo.

---

## Clonar el Repositorio (Para tus compañeros)

Tus compañeros pueden clonar el repositorio así:

```bash
git clone https://github.com/TU_USUARIO/aureumpos-backend.git
cd aureumpos-backend
```

Luego seguir las instrucciones del README.md para configurar el proyecto.

---

## Solución de Problemas

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/aureumpos-backend.git
```

### Error: "failed to push some refs"
```bash
# Primero hacer pull
git pull origin main --allow-unrelated-histories

# Luego push
git push -u origin main
```

### Cambiar la URL del repositorio remoto
```bash
git remote set-url origin https://github.com/NUEVO_USUARIO/NUEVO_REPO.git
```

---

¡Listo! Tu código estará en GitHub y listo para compartir con tu equipo.

