# Guía de Contribución

## Cómo Contribuir

1. **Fork el repositorio**
2. **Crea una rama** para tu feature o bugfix
   ```bash
   git checkout -b feature/nombre-de-tu-feature
   ```
3. **Realiza tus cambios** siguiendo las convenciones del proyecto
4. **Commit tus cambios** con mensajes descriptivos
   ```bash
   git commit -m "feat: descripción del cambio"
   ```
5. **Push a tu fork**
   ```bash
   git push origin feature/nombre-de-tu-feature
   ```
6. **Abre un Pull Request**

## Convenciones de Código

### Backend (Python)

- Seguir PEP 8
- Usar type hints
- Documentar funciones complejas
- Nombres en inglés
- Comentarios en inglés para lógica compleja

```python
def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Retrieve a user by ID from database.
    
    Args:
        db: Database session
        user_id: User ID to search
        
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.id == user_id).first()
```

### Frontend (TypeScript)

- Usar TypeScript estricto
- Componentes funcionales con hooks
- Props tipadas
- Nombres en inglés
- Comentarios en inglés para lógica compleja

```typescript
interface UserCardProps {
  user: User
  onEdit: (user: User) => void
  onDelete: (id: number) => void
}

export function UserCard({ user, onEdit, onDelete }: UserCardProps) {
  // Component logic
}
```

## Convenciones de Commits

Usar el formato: `tipo: descripción`

Tipos:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (no afectan el código)
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento

Ejemplos:
```
feat: add user profile page
fix: resolve login redirect issue
docs: update API documentation
refactor: improve user service structure
```

## Testing

### Backend
```bash
# Ejecutar tests
pipenv run pytest

# Con cobertura
pipenv run pytest --cov=app tests/
```

### Frontend
```bash
# Ejecutar tests
npm test

# Con cobertura
npm test -- --coverage
```

## Estructura de Pull Request

### Título
Usar el mismo formato que los commits: `tipo: descripción`

### Descripción
Incluir:
1. **Qué** cambia este PR
2. **Por qué** es necesario
3. **Cómo** se implementó
4. Screenshots (si aplica)
5. Tests realizados

### Ejemplo
```markdown
## Descripción
Agrega funcionalidad para exportar usuarios a CSV.

## Motivación
Los usuarios necesitan exportar datos para reportes.

## Cambios
- Agregado endpoint `/api/users/export`
- Agregado botón de exportación en UI
- Agregados tests unitarios

## Screenshots
[imagen del botón]

## Tests
- ✅ Test unitario del endpoint
- ✅ Test de integración
- ✅ Test manual en UI
```

## Code Review

### Para Revisores
- Verificar que sigue las convenciones
- Probar localmente si es posible
- Ser constructivo en los comentarios
- Aprobar solo si está listo para producción

### Para Contribuidores
- Responder a todos los comentarios
- Hacer los cambios solicitados
- Solicitar re-review después de cambios

## Reportar Bugs

Usar el template de issues e incluir:
1. Descripción del bug
2. Pasos para reproducir
3. Comportamiento esperado
4. Comportamiento actual
5. Screenshots/logs
6. Entorno (OS, versiones, etc.)

## Solicitar Features

Incluir:
1. Descripción de la funcionalidad
2. Caso de uso
3. Beneficio esperado
4. Propuesta de implementación (opcional)

## Preguntas

Para preguntas, usar:
- GitHub Discussions
- Issues con label "question"
- Email del equipo de desarrollo
