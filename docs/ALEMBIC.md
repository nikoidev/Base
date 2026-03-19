# Database Migrations with Alembic

Este proyecto utiliza [Alembic](https://alembic.sqlalchemy.org/) para gestionar las migraciones de base de datos de forma profesional y versionada.

## 📚 ¿Qué es Alembic?

Alembic es un sistema de migraciones de base de datos para SQLAlchemy que permite:
- Versionar cambios en el esquema de la base de datos
- Aplicar y revertir migraciones de forma controlada
- Generar migraciones automáticamente desde los modelos
- Mantener consistencia entre desarrollo, staging y producción

## 🚀 Comandos Básicos

### Inicializar Base de Datos Nueva

```bash
# Aplicar todas las migraciones y seed data
python init_db.py
```

### Aplicar Migraciones

```bash
# Aplicar todas las migraciones pendientes
python migrate.py upgrade

# O directamente con alembic
alembic upgrade head

# Aplicar hasta una revisión específica
alembic upgrade <revision_id>
```

### Revertir Migraciones

```bash
# Revertir la última migración
python migrate.py downgrade

# O con alembic
alembic downgrade -1

# Revertir hasta una revisión específica
alembic downgrade <revision_id>

# Revertir TODO (cuidado en producción!)
alembic downgrade base
```

### Ver Estado Actual

```bash
# Ver revisión actual
python migrate.py current
# O: alembic current

# Ver historial de migraciones
python migrate.py history
# O: alembic history --verbose
```

### Crear Nuevas Migraciones

```bash
# Auto-generar migración desde cambios en modelos
python migrate.py auto "Add user_profile table"
# O: alembic revision --autogenerate -m "Add user_profile table"

# Crear migración vacía (para SQL personalizado)
python migrate.py create "Add custom index"
# O: alembic revision -m "Add custom index"
```

## 📂 Estructura de Archivos

```
backend/
├── alembic/
│   ├── versions/           # Archivos de migración
│   │   └── 516b5b5279c1_initial_schema.py
│   ├── env.py             # Configuración de Alembic
│   ├── script.py.mako     # Template para nuevas migraciones
│   └── README
├── alembic.ini            # Configuración principal
├── migrate.py             # Helper script (wrapper)
└── init_db.py             # Inicialización + seed data
```

## 🔧 Flujo de Trabajo Típico

### 1. Modificar un Modelo

```python
# backend/app/models/user.py
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    # ➕ Nueva columna
    last_login = Column(DateTime, nullable=True)  
```

### 2. Generar Migración

```bash
cd backend
python migrate.py auto "Add last_login to users"
```

Esto crea un archivo en `alembic/versions/` con:
```python
def upgrade() -> None:
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'last_login')
```

### 3. Revisar la Migración

Abre el archivo generado y verifica que:
- Los cambios son correctos
- El downgrade funciona
- No hay operaciones peligrosas (como DROP en producción)

### 4. Aplicar la Migración

```bash
# En desarrollo
python migrate.py upgrade

# En producción (con backup previo!)
python migrate.py upgrade
```

## ⚠️ Mejores Prácticas

### ✅ DO (Hacer)

1. **Siempre revisar migraciones auto-generadas** antes de aplicarlas
2. **Probar migraciones** tanto upgrade como downgrade
3. **Hacer backup de la base de datos** antes de migrar en producción
4. **Usar transacciones** (Alembic las usa por default en PostgreSQL)
5. **Nombrar migraciones descriptivamente**: `Add user_profile_table` no `migration_1`
6. **Commitear migraciones junto con cambios de código**
7. **Usar datos de seed separados** de las migraciones

### ❌ DON'T (No Hacer)

1. **No editar migraciones ya aplicadas** en otros ambientes
2. **No hacer DROP TABLE en producción** sin backup
3. **No cambiar el orden de migraciones**
4. **No hacer migraciones de datos complejas** en `upgrade()` (usa scripts separados)
5. **No ignorar errores de migración**
6. **No aplicar migraciones sin antes ver `alembic current`**

## 🔍 Casos de Uso Comunes

### Añadir Columna Nullable

```python
# Migración auto-generada
def upgrade():
    op.add_column('users', sa.Column('bio', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('users', 'bio')
```

### Añadir Columna NOT NULL (con default)

```python
def upgrade():
    # 1. Añadir como nullable
    op.add_column('users', sa.Column('status', sa.String(20), nullable=True))
    # 2. Llenar valores existentes
    op.execute("UPDATE users SET status = 'active' WHERE status IS NULL")
    # 3. Hacer NOT NULL
    op.alter_column('users', 'status', nullable=False)

def downgrade():
    op.drop_column('users', 'status')
```

### Renombrar Columna

```python
def upgrade():
    op.alter_column('users', 'username', new_column_name='user_name')

def downgrade():
    op.alter_column('users', 'user_name', new_column_name='username')
```

### Añadir Índice

```python
def upgrade():
    op.create_index('ix_users_email_active', 'users', ['email', 'is_active'])

def downgrade():
    op.drop_index('ix_users_email_active', table_name='users')
```

### Migración de Datos

```python
from sqlalchemy import table, column

def upgrade():
    # Definir tabla para operaciones
    users = table('users',
        column('id', sa.Integer),
        column('old_field', sa.String),
        column('new_field', sa.String)
    )

    # Migrar datos
    connection = op.get_bind()
    connection.execute(
        users.update().values(new_field=users.c.old_field)
    )

    # Eliminar campo viejo
    op.drop_column('users', 'old_field')

def downgrade():
    # Reversa más complicada...
    op.add_column('users', sa.Column('old_field', sa.String(), nullable=True))
    # Re-poblar old_field desde new_field si es necesario
```

## 🐳 Docker & CI/CD

### En Docker Compose

```yaml
services:
  backend:
    command: >
      sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0"
```

### En GitHub Actions

```yaml
- name: Run migrations
  run: |
    cd backend
    alembic upgrade head
```

## 📚 Recursos

- [Documentación oficial de Alembic](https://alembic.sqlalchemy.org/)
- [Tutorial de Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Auto-generate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [Cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html)

## 🆘 Troubleshooting

### "Target database is not up to date"

```bash
# Ver estado actual
alembic current

# Ver migraciones pendientes
alembic history

# Aplicar
alembic upgrade head
```

### "Can't locate revision identified by 'xxx'"

La migración no existe. Verifica que el archivo está en `alembic/versions/`.

### Error al auto-generar

```bash
# Verificar que env.py importa todos los modelos
# Verificar que DATABASE_URL es correcta
python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```

### Rollback manual

Si una migración falla a medias:

```sql
-- Conectar a PostgreSQL
DELETE FROM alembic_version WHERE version_num = '<failed_revision>';
-- Luego arreglar manualmente el schema y reintentar
```
