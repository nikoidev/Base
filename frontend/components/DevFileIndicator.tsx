'use client'

import { usePathname } from 'next/navigation'

// Maps URL path → source file
const ROUTE_FILE_MAP: Record<string, string> = {
  '/':             'app/page.tsx',
  '/login':        'app/login/page.tsx',
  '/dashboard':    'app/dashboard/page.tsx',
  '/users':        'app/users/page.tsx',
  '/roles':        'app/roles/page.tsx',
  '/permissions':  'app/permissions/page.tsx',
  '/audit-logs':   'app/audit-logs/page.tsx',
  '/profile':      'app/profile/page.tsx',
}

export default function DevFileIndicator() {
  const pathname = usePathname()

  if (process.env.NODE_ENV !== 'development') return null

  const file = ROUTE_FILE_MAP[pathname] ?? `app${pathname}/page.tsx`

  return (
    <div
      title={`Archivo actual: frontend/${file}`}
      style={{
        position: 'fixed',
        bottom: '12px',
        right: '12px',
        zIndex: 9999,
        background: 'rgba(0,0,0,0.82)',
        color: '#a5f3a5',
        fontFamily: 'monospace',
        fontSize: '12px',
        padding: '6px 12px',
        borderRadius: '6px',
        border: '1px solid rgba(165,243,165,0.3)',
        backdropFilter: 'blur(4px)',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        userSelect: 'text',
        pointerEvents: 'none',
      }}
    >
      <span style={{ opacity: 0.5, fontSize: '10px' }}>DEV</span>
      <span>📄 {file}</span>
    </div>
  )
}
