#!/bin/bash

echo "Iniciando AureumPOS Backend..."
echo ""

# Verificar si existe .env
if [ ! -f .env ]; then
    echo "Archivo .env no encontrado. Creando desde env.example..."
    cp env.example .env
    echo "Archivo .env creado. Por favor, edítalo con tus configuraciones."
    echo ""
fi

# Iniciar Docker Compose
echo "Iniciando servicios con Docker Compose..."
docker-compose up -d

echo ""
echo "Esperando a que los servicios estén listos..."
sleep 5

# Verificar estado
echo ""
echo "Estado de los servicios:"
docker-compose ps

echo ""
echo "Backend iniciado!"
echo ""
echo "API disponible en: http://localhost:8000"
echo "Documentación en: http://localhost:8000/docs"
echo ""
echo "Para ver los logs: docker-compose logs -f backend"
echo "Para detener: docker-compose down"

