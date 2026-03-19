# 🚀 Sistema de Gestión de Usuarios - Base Universal

[![CI Tests](https://github.com/nikoidev/Usuarios/workflows/CI%20-%20Tests%20%26%20Coverage/badge.svg)](https://github.com/nikoidev/Usuarios/actions/workflows/ci-tests.yml)
[![Code Quality](https://github.com/nikoidev/Usuarios/workflows/CI%20-%20Code%20Quality/badge.svg)](https://github.com/nikoidev/Usuarios/actions/workflows/ci-quality.yml)
[![Security](https://github.com/nikoidev/Usuarios/workflows/CI%20-%20Security%20Scan/badge.svg)](https://github.com/nikoidev/Usuarios/actions/workflows/ci-security.yml)
[![Coverage](https://img.shields.io/badge/coverage-86%25-brightgreen.svg)](https://github.com/nikoidev/Usuarios)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.33-black.svg?logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192.svg?logo=postgresql)](https://www.postgresql.org)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?logo=python)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6.svg?logo=typescript)](https://www.typescriptlang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Base sólida y profesional para cualquier proyecto que necesite gestión de usuarios, roles y permisos.** Sistema completo y listo para producción que sirve como fundamento para proyectos de gestión empresarial, e-commerce, sistemas médicos, almacenes, producción y más.

---

## ✨ Características Principales

### 🔐 **Autenticación y Seguridad**
- ✅ **JWT con Refresh Tokens** - Tokens de acceso (30 min) y renovación automática (7 días)
- ✅ **Rate Limiting** - Protección contra ataques de fuerza bruta
- ✅ **Recuperación de Contraseña** - Sistema completo vía email con tokens seguros
- ✅ **Cambio de Contraseña** - Con validación de contraseña actual
- ✅ **Validación de Fuerza** - Indicador visual en tiempo real
- ✅ **Encriptación de Datos Sensibles** - Contraseñas SMTP encriptadas con Fernet

### 👥 **Gestión de Usuarios Completa**
- ✅ **CRUD Completo** - Crear, leer, actualizar y eliminar usuarios
- ✅ **Perfil Profesional** - Avatar, teléfono, biografía, zona horaria, idioma
- ✅ **Upload de Avatar** - Con validación de tipo y tamaño (máx 5MB)
- ✅ **Roles Múltiples** - Un usuario puede tener varios roles
- ✅ **Estados** - Activar/desactivar usuarios

### 🛡️ **Sistema RBAC (Role-Based Access Control)**
- ✅ **Roles** - Agrupación de permisos reutilizables
- ✅ **Permisos** - Control granular por recurso y acción
- ✅ **Asignación Dinámica** - Cambios en vivo sin reiniciar

### 📊 **Funcionalidades Avanzadas**
- ✅ **Paginación Inteligente** - 10/25/50/100 items por página
- ✅ **Búsqueda en Tiempo Real** - Con debounce (500ms)
- ✅ **Filtros Múltiples** - Por rol, estado, recurso, acción
- ✅ **Ordenamiento** - Por cualquier columna (ascendente/descendente)
- ✅ **Audit Log** - Registro completo de actividades con IP y user agent
- ✅ **Historial de Actividad** - Ver últimas acciones de cualquier usuario

### 🎨 **Interfaz Moderna**
- ✅ **Tema Oscuro/Claro** - Toggle persistente
- ✅ **Diseño Responsive** - Mobile, tablet y desktop
- ✅ **Componentes Reutilizables** - Paginación, validación, etc.
- ✅ **Toast Notifications** - Feedback visual inmediato
- ✅ **Iconos** - Heroicons v2

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  Next.js 14 + TypeScript + Tailwind CSS + React Hooks       │
│  - Páginas: Dashboard, Users, Roles, Permissions, Profile   │
│  - Componentes reutilizables + Context API                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
┌──────────────────────┴──────────────────────────────────────┐
│                         Backend                              │
│          FastAPI + SQLAlchemy + Pydantic + JWT              │
│  - Autenticación JWT + Refresh Tokens                       │
│  - RBAC + Audit Log + Rate Limiting                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                       PostgreSQL 16                          │
│      Tables: users, roles, permissions, audit_logs          │
│         Relaciones: user_roles, role_permissions            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Requisitos Previos

- **Python 3.11+** - [Descargar](https://www.python.org/downloads/)
- **Node.js 18+** - [Descargar](https://nodejs.org/)
- **Docker & Docker Compose** - [Descargar](https://www.docker.com/get-started/)
- **Pipenv** - `pip install pipenv`

---

## 🚀 Instalación Rápida

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/user-management-system.git
cd user-management-system
```

### 2️⃣ Iniciar Base de Datos (PostgreSQL + pgAdmin)

```bash
docker-compose up -d
```

**Accesos:**
- **PostgreSQL**: `localhost:5433`
- **pgAdmin**: `http://localhost:5050`
  - Email: `admin@admin.com`
  - Password: `admin`

### 3️⃣ Configurar Backend

```bash
cd backend

# Instalar dependencias
pipenv install

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tus valores

# Inicializar base de datos (migraciones + seed data)
pipenv run python init_db.py

# O aplicar solo migraciones
pipenv run alembic upgrade head

# Iniciar servidor
pipenv run python run.py
```

Backend corriendo en: **http://localhost:8000**  
Documentación API: **http://localhost:8000/docs**

> **📚 Migraciones de Base de Datos**: Este proyecto usa [Alembic](https://alembic.sqlalchemy.org/) para gestionar el esquema de la base de datos. Ver [docs/ALEMBIC.md](docs/ALEMBIC.md) para más detalles.

### 4️⃣ Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Construir para producción
npm run build

# Iniciar servidor
npm run start
```

Frontend corriendo en: **http://localhost:3000**

---

## 🔑 Credenciales por Defecto

```
Administrador:
  Usuario: admin
  Contraseña: admin123

Usuario Regular:
  Usuario: user
  Contraseña: user123
```

⚠️ **IMPORTANTE**: Cambiar estas credenciales en producción.

---

## 📚 Estructura del Proyecto

```
user-management-system/
├── backend/                  # API FastAPI
│   ├── alembic/             # 🆕 Database migrations
│   │   ├── versions/        # Migration files
│   │   ├── env.py           # Alembic config
│   │   └── script.py.mako   # Migration template
│   ├── app/
│   │   ├── api/             # Endpoints REST
│   │   │   ├── routes/      # auth, users, roles, permissions, audit_logs, profile
│   │   │   └── deps.py      # Dependencias (auth, db)
│   │   ├── core/            # Configuración central
│   │   │   ├── config.py    # Variables de entorno
│   │   │   ├── security.py  # JWT, hashing
│   │   │   ├── database.py  # SQLAlchemy engine
│   │   │   └── encryption.py # Fernet encryption
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── schemas/         # Schemas Pydantic
│   │   ├── services/        # Lógica de negocio
│   │   ├── utils/           # Utilidades (audit)
│   │   └── templates/       # Templates HTML para emails
│   ├── tests/               # 🆕 Test suite (pytest)
│   │   ├── conftest.py      # Fixtures compartidos
│   │   ├── test_auth.py     # Tests de autenticación
│   │   ├── test_users.py    # Tests de usuarios
│   │   └── test_services.py # Tests de servicios
│   ├── uploads/             # Archivos subidos (avatars)
│   ├── alembic.ini          # 🆕 Alembic configuration
│   ├── Pipfile              # Dependencias Python
│   ├── pytest.ini           # 🆕 Pytest configuration
│   ├── pyproject.toml       # 🆕 Tool configs (black, isort, mypy)
│   ├── init_db.py           # Migrations + seed data
│   ├── migrate.py           # 🆕 Migration helper script
│   └── run.py               # Entry point
│
├── frontend/                # App Next.js
│   ├── app/                 # App Router
│   │   ├── dashboard/       # Panel principal
│   │   ├── users/           # Gestión de usuarios
│   │   ├── roles/           # Gestión de roles
│   │   ├── permissions/     # Gestión de permisos
│   │   ├── profile/         # Perfil profesional
│   │   ├── audit-logs/      # Registro de actividad
│   │   └── login/           # Página de inicio de sesión
│   ├── components/          # Componentes reutilizables
│   │   ├── Layout.tsx       # Layout principal
│   │   ├── Pagination.tsx   # Componente de paginación
│   │   └── PasswordStrength.tsx # Validador de contraseña
│   ├── contexts/            # React Contexts
│   │   ├── AuthContext.tsx  # Autenticación global
│   │   └── ThemeContext.tsx # Tema oscuro/claro
│   ├── hooks/               # Custom Hooks
│   │   └── useDebounce.ts   # Hook de debounce
│   ├── lib/                 # Utilidades
│   │   ├── api/             # Servicios API
│   │   └── axios.ts         # Cliente HTTP
│   ├── types/               # TypeScript types
│   └── package.json
│
├── .github/                 # 🆕 CI/CD workflows
│   └── workflows/
│       ├── ci-tests.yml     # Automated testing
│       ├── ci-quality.yml   # Code quality
│       └── ci-security.yml  # Security scans
├── docs/                    # 🆕 Documentation
│   ├── ALEMBIC.md          # Migration guide
│   └── CI_CD.md            # CI/CD guide
├── .pre-commit-config.yaml  # 🆕 Pre-commit hooks
├── docker-compose.yml       # PostgreSQL + pgAdmin
└── CHANGELOG.md            # 🆕 Version history
```

---

## 🔧 Variables de Entorno

### Backend (`.env`)

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/users_db

# Security
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-aqui
SECRET_KEY_ENCRYPTION=clave-fernet-para-encriptacion-32-bytes
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000
```

### Frontend

No requiere variables de entorno. La URL del backend está configurada en `lib/axios.ts`.

---

## 📖 Uso del Sistema

### Gestión de Usuarios

1. **Crear Usuario**: Click en "Nuevo Usuario" → Rellenar formulario → Asignar roles
2. **Editar Usuario**: Click en ícono de edición → Modificar datos → Guardar
3. **Eliminar Usuario**: Click en ícono de eliminar → Confirmar
4. **Buscar**: Escribir en el campo de búsqueda (busca en nombre, email, username)
5. **Filtrar**: Click en "Filtros" → Seleccionar rol y/o estado
6. **Ordenar**: Click en cualquier header de columna

### Perfil Personal

- **Actualizar Información**: `/profile` → Editar campos → Guardar
- **Cambiar Avatar**: Click en "Cambiar Foto" → Seleccionar imagen → Automático
- **Eliminar Avatar**: Click en "Eliminar Foto"

### Audit Log

- **Ver Actividad**: `/audit-logs` → Lista de todas las acciones
- **Filtrar**: Por acción, recurso, usuario
- **Ver Detalles**: Click en cualquier registro → Modal con información completa

---

## 🔌 API Endpoints

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login` | Iniciar sesión | No |
| GET | `/api/auth/me` | Usuario actual | Sí |
| POST | `/api/auth/refresh` | Renovar token | No |
| POST | `/api/auth/forgot-password` | Solicitar recuperación | No |
| POST | `/api/auth/reset-password` | Resetear contraseña | No |
| POST | `/api/auth/change-password` | Cambiar contraseña | Sí |
| POST | `/api/auth/logout` | Cerrar sesión | Sí |

### Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/users/` | Listar usuarios (paginado) | Sí |
| GET | `/api/users/{id}` | Obtener usuario | Sí |
| POST | `/api/users/` | Crear usuario | Sí |
| PUT | `/api/users/{id}` | Actualizar usuario | Sí |
| DELETE | `/api/users/{id}` | Eliminar usuario | Sí |

### Perfil

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/profile/me` | Obtener mi perfil | Sí |
| PUT | `/api/profile/me` | Actualizar mi perfil | Sí |
| POST | `/api/profile/upload-avatar` | Subir avatar | Sí |
| DELETE | `/api/profile/avatar` | Eliminar avatar | Sí |

### Audit Logs

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/audit-logs/` | Listar logs (paginado) | Sí |
| GET | `/api/audit-logs/recent` | Logs recientes | Sí |
| GET | `/api/audit-logs/my-activity` | Mi actividad | Sí |

📖 **Documentación Completa**: http://localhost:8000/docs

---

## 🛠️ Desarrollo

### Backend

```bash
cd backend

# Activar entorno
pipenv shell

# Instalar nueva dependencia
pipenv install nombre-paquete

# Ejecutar tests (cuando se implementen)
pipenv run pytest

# Formatear código
pipenv run black app/

# Linter
pipenv run flake8 app/
```

### Frontend

```bash
cd frontend

# Modo desarrollo (hot reload)
npm run dev

# Build para producción
npm run build

# Iniciar producción
npm run start

# Linter
npm run lint
```

---

## 🚢 Despliegue a Producción

### Checklist Pre-Producción

- [ ] Cambiar `SECRET_KEY` en `.env`
- [ ] Cambiar credenciales de base de datos
- [ ] Cambiar usuarios y contraseñas por defecto
- [ ] Configurar HTTPS (SSL/TLS)
- [ ] Ajustar `CORS_ORIGINS` a dominio de producción
- [ ] Configurar backup automático de base de datos
- [ ] Implementar monitoring (Sentry, NewRelic, etc.)
- [ ] Configurar logs persistentes
- [ ] Revisar rate limits según carga esperada
- [ ] Configurar email SMTP real

### Backend (FastAPI)

```bash
# Usando Gunicorn + Uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Frontend (Next.js)

```bash
npm run build
npm run start
```

O despliega en **Vercel** (recomendado para Next.js):
```bash
vercel deploy --prod
```

### Base de Datos

Usa un servicio gestionado como:
- **AWS RDS**
- **Digital Ocean Managed Database**
- **Heroku Postgres**
- **Railway**

---

## 🎯 Casos de Uso

Este sistema sirve como base para:

### ✅ **Sistemas de Gestión Empresarial**
- ERP, CRM, gestión de inventarios
- Control de acceso por departamentos
- Audit log para cumplimiento normativo

### ✅ **E-Commerce**
- Gestión de administradores y vendedores
- Diferentes niveles de acceso (admin, ventas, soporte)
- Registro de todas las operaciones

### ✅ **Sistemas Médicos**
- Control de acceso a historias clínicas
- Diferentes roles (médicos, enfermeras, admin)
- Trazabilidad completa (HIPAA compliance)

### ✅ **Plataformas Educativas**
- Gestión de profesores, estudiantes, administradores
- Permisos por curso/materia
- Registro de actividades académicas

### ✅ **Sistemas de Producción/Manufactura**
- Control de acceso a líneas de producción
- Roles: operadores, supervisores, gerentes
- Audit log de cambios en producción

---

## 🧩 Extensibilidad

### Agregar Nuevos Módulos

1. **Backend**: Crear modelo → schema → servicio → ruta
2. **Frontend**: Crear página → componente → API service
3. **Integrar**: Registrar ruta en `main.py` y link en `Layout.tsx`

### Ejemplo: Agregar módulo de "Productos"

```python
# backend/app/models/product.py
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # ... más campos
```

```typescript
// frontend/app/products/page.tsx
export default function ProductsPage() {
  // Similar estructura a users/page.tsx
}
```

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: amazing feature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más información.

---

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu@email.com

---

## ⭐ Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework backend moderno y rápido
- [Next.js](https://nextjs.org/) - Framework React para producción
- [Tailwind CSS](https://tailwindcss.com/) - Framework CSS utility-first
- [Heroicons](https://heroicons.com/) - Iconos hermosos

---

## 📞 Soporte

¿Problemas o preguntas?

- 📖 [Wiki](https://github.com/tu-usuario/repo/wiki)
- 🐛 [Issues](https://github.com/tu-usuario/repo/issues)
- 💬 [Discussions](https://github.com/tu-usuario/repo/discussions)

---

<p align="center">
  Hecho con ❤️ para la comunidad Open Source
</p>

<p align="center">
  <strong>⭐ Si te gusta este proyecto, dale una estrella en GitHub ⭐</strong>
</p>
