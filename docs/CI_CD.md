# CI/CD Pipeline Documentation

Este proyecto utiliza GitHub Actions para automatizar testing, linting y security checks.

## 📋 Workflows Configurados

### 1. **CI - Tests & Coverage** (`ci-tests.yml`)

Ejecuta automáticamente en:
- Push a ramas `main` y `develop`
- Pull Requests a `main` y `develop`

**Acciones:**
- ✅ Ejecuta pytest con coverage mínimo 80%
- ✅ Genera reportes de coverage (XML + HTML)
- ✅ Sube coverage a Codecov
- ✅ Crea badge de coverage
- ✅ Matrix testing: Python 3.11 y 3.12
- ✅ PostgreSQL 15 como servicio

**Duración:** ~2-3 minutos

### 2. **CI - Code Quality** (`ci-quality.yml`)

Ejecuta automáticamente en:
- Push a ramas `main` y `develop` (archivos .py)
- Pull Requests a `main` y `develop` (archivos .py)

**Acciones:**
- ✅ Black: Verificar formato de código
- ✅ isort: Verificar orden de imports
- ✅ flake8: Linting (complejidad máx: 10)
- ✅ mypy: Type checking
- ✅ Bandit: Security linting
- ✅ Safety: Vulnerabilidades en dependencias

**Duración:** ~1-2 minutos

### 3. **CI - Security Scan** (`ci-security.yml`)

Ejecuta:
- Push a rama `main`
- Pull Requests a `main`
- **Semanalmente** (lunes 00:00 UTC) vía cron

**Acciones:**
- ✅ Bandit: Escaneo de seguridad en código
- ✅ Safety: Vulnerabilidades conocidas
- ✅ pip-audit: Auditoría de dependencias
- ✅ Reportes guardados 90 días

**Duración:** ~1-2 minutos

## 🔧 Configuración Local

### Instalar Pre-commit Hooks

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar hooks en el repo
pre-commit install

# Ejecutar manualmente en todos los archivos
pre-commit run --all-files
```

### Ejecutar Checks Localmente

```bash
cd backend

# Tests con coverage
pytest tests/ --cov=app --cov-report=html --cov-report=term

# Formatear código
black app/ tests/
isort app/ tests/

# Linting
flake8 app/ tests/ --max-line-length=120 --ignore=E203,E266,E501,W503

# Type checking
mypy app/ --ignore-missing-imports

# Security
bandit -r app/ -ll
safety check
```

## 📊 Badges en README

Los badges muestran el estado de:
- ✅ CI Tests (pasando/fallando)
- ✅ Code Quality (pasando/fallando)
- ✅ Security (pasando/fallando)
- ✅ Coverage (porcentaje)

## 🚨 ¿Qué hacer si CI falla?

### Tests Fallando
```bash
# Ejecutar tests localmente
cd backend
pytest tests/ -v

# Ver detalles del error
pytest tests/test_auth.py::TestLogin::test_login_success -v
```

### Formato Incorrecto
```bash
# Formatear con Black
black app/ tests/

# Ordenar imports
isort app/ tests/
```

### Linting Errors
```bash
# Ver errores
flake8 app/ tests/

# Auto-fix algunos errores
autopep8 --in-place --aggressive app/**/*.py
```

### Security Issues
```bash
# Ver problemas de seguridad
bandit -r app/ -ll

# Actualizar dependencias vulnerables
pip install --upgrade <package>
```

## 🔐 Secretos de GitHub

Configurados en: **Settings → Secrets → Actions**

Necesarios para:
- `CODECOV_TOKEN`: Upload de coverage (opcional)

## 📦 Dependabot

Configurado en `.github/dependabot.yml`

- **Python**: Actualiza pip packages semanalmente (lunes)
- **npm**: Actualiza dependencias npm semanalmente (lunes)
- **GitHub Actions**: Actualiza workflows mensualmente

Auto-crea PRs con actualizaciones de seguridad y versiones.

## 🎯 Requisitos para Merge

Para que un PR sea aceptado:
- ✅ Todos los tests deben pasar
- ✅ Coverage >= 80%
- ✅ Code quality checks OK
- ✅ Security scans sin issues críticos
- ✅ Código formateado con Black
- ✅ Imports ordenados con isort
- ✅ Sin errores de flake8

## 📈 Métricas

- **Tests**: 58 passing, 86% coverage
- **Complejidad**: Max 10 (flake8)
- **Line Length**: Max 120 caracteres
- **Python**: 3.11, 3.12

## 🔄 Flujo de Trabajo

```
1. Desarrollador hace cambios
   ↓
2. Pre-commit hooks ejecutan (local)
   ↓
3. Push a GitHub
   ↓
4. GitHub Actions ejecutan workflows
   ↓
5. Si todo pasa → ✅ Ready for merge
   Si algo falla → ❌ Fix issues
```

## 📝 Notas

- Los workflows solo se ejecutan si hay cambios en `backend/` o workflows
- Security scan semanal ayuda a detectar nuevas vulnerabilidades
- Pre-commit hooks previenen commits con errores obvios
- Coverage reports se guardan como artifacts por 30 días
