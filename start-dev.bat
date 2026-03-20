@echo off
title start-dev.bat — Iniciando proyecto BASE...

echo.
echo  ================================================
echo   BASE — Proyecto en Modo DEV
echo  ================================================
echo   Backend  →  http://localhost:8010
echo   Frontend →  http://localhost:3010
echo   API Docs →  http://localhost:8010/docs
echo  ================================================
echo.
echo  Abriendo terminales...
echo.

:: Backend - FastAPI en puerto 8010
start "start-dev.bat [BACKEND :8010]" cmd /k "cd /d %~dp0backend && echo. && echo  [BACKEND] FastAPI — http://localhost:8010 && echo  ---------------------------------------- && echo   Archivo principal : backend\app\main.py && echo   Rutas API         : backend\app\api\routes\ && echo   Modelos DB        : backend\app\models\ && echo   Servicios         : backend\app\services\ && echo   Configuracion     : backend\app\core\config.py && echo  ---------------------------------------- && echo. && uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload"

:: Pequeña pausa para no solapar ventanas
timeout /t 2 /nobreak >nul

:: Frontend - Next.js en puerto 3010
start "start-dev.bat [FRONTEND :3010]" cmd /k "cd /d %~dp0frontend && echo. && echo  [FRONTEND] Next.js — http://localhost:3010 && echo  ---------------------------------------- && echo   Archivo principal : frontend\app\layout.tsx && echo   Paginas           : frontend\app\[ruta]\page.tsx && echo   Componentes       : frontend\components\ && echo   API calls         : frontend\lib\api\ && echo   Tipos             : frontend\types\index.ts && echo  ---------------------------------------- && echo. && npx next dev -p 3010"

echo  Terminales lanzadas. Puedes cerrar esta ventana.
echo.
pause
