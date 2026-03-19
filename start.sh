#!/bin/bash

echo "========================================"
echo " Sistema de Gestión de Usuarios"
echo "========================================"
echo ""

echo "[1/3] Iniciando contenedores Docker..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "Error: No se pudo iniciar Docker. Asegúrate de que Docker esté corriendo."
    exit 1
fi
echo "Contenedores iniciados correctamente!"
echo ""

echo "Esperando a que PostgreSQL esté listo..."
sleep 5
echo ""

echo "[2/3] Para iniciar el BACKEND:"
echo "  cd backend"
echo "  pip install pipenv"
echo "  pipenv install"
echo "  pipenv run python init_db.py"
echo "  pipenv run python run.py"
echo ""

echo "[3/3] Para iniciar el FRONTEND (en otra terminal):"
echo "  cd frontend"
echo "  npm install"
echo "  npm run dev"
echo ""

echo "========================================"
echo " Accesos:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000/docs"
echo "  - pgAdmin: http://localhost:5051"
echo "========================================"
echo ""
echo "Credenciales por defecto:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
