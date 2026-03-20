import { useAuth } from '@/contexts/AuthContext'
import { useMemo } from 'react'

/**
 * Returns a Set of permission codes the current user has.
 * Superusers get every permission automatically.
 *
 * Usage:
 *   const { can } = usePermissions()
 *   if (can('user.create')) { ... }
 */
export function usePermissions() {
  const { user } = useAuth()

  const permissions = useMemo<Set<string>>(() => {
    if (!user) return new Set()

    // Superusers bypass all permission checks
    if (user.is_superuser) {
      return new Set(['*']) // wildcard — Can component checks for this
    }

    const codes = new Set<string>()
    for (const role of user.roles ?? []) {
      for (const permission of role.permissions ?? []) {
        codes.add(permission.code)
      }
    }
    return codes
  }, [user])

  const can = (permissionCode: string): boolean => {
    if (permissions.has('*')) return true // superuser
    return permissions.has(permissionCode)
  }

  const canAny = (...codes: string[]): boolean =>
    codes.some((c) => can(c))

  const canAll = (...codes: string[]): boolean =>
    codes.every((c) => can(c))

  return { permissions, can, canAny, canAll }
}
