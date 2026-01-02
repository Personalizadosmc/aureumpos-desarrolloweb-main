@echo off
echo Iniciando AureumPOS Backend...
echo.

REM Verificar si existe .env
if not exist .env (
    echo Archivo .env no encontrado. Creando desde env.example...
    copy env.example .env
    echo Archivo .env creado. Por favor, edítalo con tus configuraciones.
    echo.
)

REM Iniciar Docker Compose
echo Iniciando servicios con Docker Compose...
docker-compose up -d

echo.
echo Esperando a que los servicios estén listos...
timeout /t 5 /nobreak >nul

REM Verificar estado
echo.
echo Estado de los servicios:
docker-compose ps

echo.
echo Backend iniciado!
echo.
echo API disponible en: http://localhost:8000
echo Documentación en: http://localhost:8000/docs
echo.
echo Para ver los logs: docker-compose logs -f backend
echo Para detener: docker-compose down

pause

