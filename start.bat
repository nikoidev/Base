@echo off
echo ========================================
echo  Sistema de Gestion de Usuarios
echo ========================================
echo.

echo [1/3] Iniciando contenedores Docker...
docker-compose up -d
if errorlevel 1 (
    echo Error: No se pudo iniciar Docker. Asegurate de que Docker Desktop este corriendo.
    pause
    exit /b 1
)
echo Contenedores iniciados correctamente!
echo.

echo Esperando a que PostgreSQL este listo...
timeout /t 5 /nobreak > nul
echo.

echo [2/3] Para iniciar el BACKEND:
echo   cd backend
echo   pip install pipenv
echo   pipenv install
echo   pipenv run python init_db.py
echo   pipenv run python run.py
echo.

echo [3/3] Para iniciar el FRONTEND (en otra terminal):
echo   cd frontend
echo   npm install
echo   npm run dev
echo.

echo ========================================
echo  Accesos:
echo  - Frontend: http://localhost:3000
echo  - Backend API: http://localhost:8000/docs
echo  - pgAdmin: http://localhost:5051
echo ========================================
echo.
echo Credenciales por defecto:
echo   Username: admin
echo   Password: admin123
echo.

pause
