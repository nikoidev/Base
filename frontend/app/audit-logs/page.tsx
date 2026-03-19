'use client'

import { useState, useEffect } from 'react'
import Layout from '@/components/Layout'
import Pagination from '@/components/Pagination'
import { auditLogsApi, GetAuditLogsParams } from '@/lib/api/audit-logs'
import { AuditLog } from '@/types'
import { useDebounce } from '@/hooks/useDebounce'
import toast from 'react-hot-toast'
import { 
  MagnifyingGlassIcon, 
  FunnelIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowRightOnRectangleIcon,
  KeyIcon,
  UserIcon,
  ShieldCheckIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

export const dynamic = 'force-dynamic'

const ACTION_ICONS: Record<string, any> = {
  'LOGIN_SUCCESS': CheckCircleIcon,
  'LOGIN_FAILED': XCircleIcon,
  'LOGOUT': ArrowRightOnRectangleIcon,
  'CREATE': UserIcon,
  'UPDATE': UserIcon,
  'DELETE': XCircleIcon,
  'PASSWORD_CHANGED': KeyIcon,
  'ROLE_ASSIGNED': ShieldCheckIcon,
}

const ACTION_COLORS: Record<string, string> = {
  'LOGIN_SUCCESS': 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900',
  'LOGIN_FAILED': 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900',
  'LOGOUT': 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-700',
  'CREATE': 'text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900',
  'UPDATE': 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900',
  'DELETE': 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900',
  'PASSWORD_CHANGED': 'text-purple-600 dark:text-purple-400 bg-purple-100 dark:bg-purple-900',
}

const ACTION_LABELS: Record<string, string> = {
  'LOGIN_SUCCESS': 'Inicio de Sesión Exitoso',
  'LOGIN_FAILED': 'Intento de Inicio Fallido',
  'LOGOUT': 'Cierre de Sesión',
  'CREATE': 'Creación',
  'UPDATE': 'Actualización',
  'DELETE': 'Eliminación',
  'PASSWORD_CHANGED': 'Cambio de Contraseña',
  'PASSWORD_RESET': 'Restablecimiento de Contraseña',
  'ROLE_ASSIGNED': 'Rol Asignado',
}

const RESOURCE_LABELS: Record<string, string> = {
  'user': 'Usuario',
  'role': 'Rol',
  'permission': 'Permiso',
  'auth': 'Autenticación',
  'profile': 'Perfil',
}

export default function AuditLogsPage() {
  const [logs, setLogs] = useState<AuditLog[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedLog, setSelectedLog] = useState<AuditLog | null>(null)
  
  // Pagination & Filters
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [total, setTotal] = useState(0)
  const [limit, setLimit] = useState(50)
  const [search, setSearch] = useState('')
  const [actionFilter, setActionFilter] = useState<string>('')
  const [resourceFilter, setResourceFilter] = useState<string>('')
  const [showFilters, setShowFilters] = useState(false)

  const debouncedSearch = useDebounce(search, 500)

  useEffect(() => {
    fetchLogs()
  }, [page, limit, debouncedSearch, actionFilter, resourceFilter])

  const fetchLogs = async () => {
    try {
      setLoading(true)
      const params: GetAuditLogsParams = {
        page,
        limit,
        search: debouncedSearch || undefined,
        action: actionFilter || undefined,
        resource: resourceFilter || undefined,
        order_by: 'created_at',
        order_desc: true
      }
      const response = await auditLogsApi.getAll(params)
      setLogs(response.items)
      setTotal(response.total)
      setTotalPages(response.pages)
    } catch (error) {
      toast.error('Error al cargar logs')
    } finally {
      setLoading(false)
    }
  }

  const clearFilters = () => {
    setSearch('')
    setActionFilter('')
    setResourceFilter('')
    setPage(1)
  }

  const getActionIcon = (action: string) => {
    const Icon = ACTION_ICONS[action] || ClockIcon
    return Icon
  }

  const getActionColor = (action: string) => {
    return ACTION_COLORS[action] || 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-700'
  }

  const getActionLabel = (action: string) => {
    return ACTION_LABELS[action] || action
  }

  const getResourceLabel = (resource: string) => {
    return RESOURCE_LABELS[resource] || resource
  }

  const formatDate = (date: string) => {
    const d = new Date(date)
    const now = new Date()
    const diff = now.getTime() - d.getTime()
    const seconds = Math.floor(diff / 1000)
    const minutes = Math.floor(seconds / 60)
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)

    if (seconds < 60) return 'hace un momento'
    if (minutes < 60) return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`
    if (hours < 24) return `hace ${hours} hora${hours > 1 ? 's' : ''}`
    if (days < 7) return `hace ${days} día${days > 1 ? 's' : ''}`
    
    return d.toLocaleDateString('es-MX', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const uniqueActions = Array.from(new Set(logs.map(log => log.action)))
  const uniqueResources = Array.from(new Set(logs.map(log => log.resource)))

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Registro de Actividad ({total})
          </h1>
        </div>

        {/* Search and Filters */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-4 space-y-4">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="flex-1">
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={search}
                  onChange={(e) => {
                    setSearch(e.target.value)
                    setPage(1)
                  }}
                  placeholder="Buscar por IP o navegador..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            {/* Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
            >
              <FunnelIcon className="w-5 h-5 mr-2" />
              Filtros
              {(actionFilter || resourceFilter) && (
                <span className="ml-2 px-2 py-0.5 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 text-xs rounded-full">
                  {(actionFilter ? 1 : 0) + (resourceFilter ? 1 : 0)}
                </span>
              )}
            </button>

            {/* Items per page */}
            <select
              value={limit}
              onChange={(e) => {
                setLimit(Number(e.target.value))
                setPage(1)
              }}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value={25}>25 por página</option>
              <option value={50}>50 por página</option>
              <option value={100}>100 por página</option>
            </select>
          </div>

          {/* Filter Panel */}
          {showFilters && (
            <div className="flex flex-col md:flex-row gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Acción
                </label>
                <select
                  value={actionFilter}
                  onChange={(e) => {
                    setActionFilter(e.target.value)
                    setPage(1)
                  }}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="">Todas las acciones</option>
                  {uniqueActions.map(action => (
                    <option key={action} value={action}>{getActionLabel(action)}</option>
                  ))}
                </select>
              </div>

              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Recurso
                </label>
                <select
                  value={resourceFilter}
                  onChange={(e) => {
                    setResourceFilter(e.target.value)
                    setPage(1)
                  }}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="">Todos los recursos</option>
                  {uniqueResources.map(resource => (
                    <option key={resource} value={resource}>{getResourceLabel(resource)}</option>
                  ))}
                </select>
              </div>

              <div className="flex items-end">
                <button
                  onClick={clearFilters}
                  className="px-4 py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
                >
                  Limpiar filtros
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Logs List */}
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          {loading ? (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <p className="mt-4 text-gray-600 dark:text-gray-400">Cargando...</p>
            </div>
          ) : logs.length === 0 ? (
            <div className="p-8 text-center text-gray-500 dark:text-gray-400">
              No se encontraron registros
            </div>
          ) : (
            <>
              <div className="divide-y divide-gray-200 dark:divide-gray-700">
                {logs.map((log) => {
                  const Icon = getActionIcon(log.action)
                  return (
                    <div
                      key={log.id}
                      onClick={() => setSelectedLog(log)}
                      className="p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                    >
                      <div className="flex items-start space-x-4">
                        <div className={`flex-shrink-0 p-2 rounded-lg ${getActionColor(log.action)}`}>
                          <Icon className="w-5 h-5" />
                        </div>

                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <p className="text-sm font-medium text-gray-900 dark:text-white">
                              {getActionLabel(log.action)} - {getResourceLabel(log.resource)}
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                              {formatDate(log.created_at)}
                            </p>
                          </div>

                          <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                            {log.user_username && (
                              <span className="flex items-center">
                                <UserIcon className="w-4 h-4 mr-1" />
                                {log.user_username}
                              </span>
                            )}
                            {log.ip_address && (
                              <span className="font-mono text-xs">
                                {log.ip_address}
                              </span>
                            )}
                            {log.resource_id && (
                              <span className="text-xs">
                                ID: {log.resource_id}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>

              <Pagination
                currentPage={page}
                totalPages={totalPages}
                onPageChange={setPage}
              />
            </>
          )}
        </div>
      </div>

      {/* Detail Modal */}
      {selectedLog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Detalle del Registro
                </h2>
                <button
                  onClick={() => setSelectedLog(null)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400">Acción</label>
                  <p className="mt-1 text-sm text-gray-900 dark:text-white">
                    {getActionLabel(selectedLog.action)}
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400">Recurso</label>
                  <p className="mt-1 text-sm text-gray-900 dark:text-white">
                    {getResourceLabel(selectedLog.resource)}
                    {selectedLog.resource_id && ` (ID: ${selectedLog.resource_id})`}
                  </p>
                </div>

                {selectedLog.user_username && (
                  <div>
                    <label className="block text-sm font-medium text-gray-500 dark:text-gray-400">Usuario</label>
                    <p className="mt-1 text-sm text-gray-900 dark:text-white">
                      {selectedLog.user_username} ({selectedLog.user_email})
                    </p>
                  </div>
                )}

                {selectedLog.ip_address && (
                  <div>
                    <label className="block text-sm font-medium text-gray-500 dark:text-gray-400">Dirección IP</label>
                    <p className="mt-1 text-sm text-gray-900 dark:text-white font-mono">
                      {selectedLog.ip_address}
                    </p>
                  </div>
                )}

                {selectedLog.user_agent && (
                  <div>
                    <label className="block text-sm font-medium text-gray-500 dark:text-gray-400">Navegador</label>
                    <p className="mt-1 text-xs text-gray-900 dark:text-white font-mono break-all">
                      {selectedLog.user_agent}
                    </p>
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400">Fecha y Hora</label>
                  <p className="mt-1 text-sm text-gray-900 dark:text-white">
                    {new Date(selectedLog.created_at).toLocaleString('es-MX', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                      second: '2-digit'
                    })}
                  </p>
                </div>

                {selectedLog.details && Object.keys(selectedLog.details).length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                      Detalles Adicionales
                    </label>
                    <pre className="bg-gray-50 dark:bg-gray-900 rounded-lg p-3 text-xs text-gray-900 dark:text-white overflow-x-auto">
                      {JSON.stringify(selectedLog.details, null, 2)}
                    </pre>
                  </div>
                )}
              </div>

              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setSelectedLog(null)}
                  className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600"
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </Layout>
  )
}

