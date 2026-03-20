import { usePermissions } from '@/hooks/usePermissions'
import { ReactNode } from 'react'

interface CanProps {
  /** The permission code to check, e.g. "user.create" */
  permission: string
  /** Content to render if the user HAS the permission */
  children: ReactNode
  /** Optional fallback to render if the user LACKS the permission */
  fallback?: ReactNode
}

/**
 * Conditionally renders children based on the current user's permissions.
 *
 * Usage:
 *   <Can permission="user.create">
 *     <button>Nuevo Usuario</button>
 *   </Can>
 *
 *   <Can permission="user.delete" fallback={<span>Sin acceso</span>}>
 *     <button>Eliminar</button>
 *   </Can>
 */
export default function Can({ permission, children, fallback = null }: CanProps) {
  const { can } = usePermissions()
  return can(permission) ? <>{children}</> : <>{fallback}</>
}
