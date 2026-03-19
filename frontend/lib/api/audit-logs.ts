import axiosInstance from '../axios'
import { AuditLog, PaginatedResponse } from '@/types'

export interface GetAuditLogsParams {
  page?: number
  limit?: number
  user_id?: number
  action?: string
  resource?: string
  search?: string
  order_by?: string
  order_desc?: boolean
}

export const auditLogsApi = {
  getAll: async (params: GetAuditLogsParams = {}): Promise<PaginatedResponse<AuditLog>> => {
    const response = await axiosInstance.get('/api/audit-logs/', { params })
    return response.data
  },

  getRecent: async (limit: number = 10): Promise<AuditLog[]> => {
    const response = await axiosInstance.get('/api/audit-logs/recent', { params: { limit } })
    return response.data
  },

  getMyActivity: async (limit: number = 20): Promise<AuditLog[]> => {
    const response = await axiosInstance.get('/api/audit-logs/my-activity', { params: { limit } })
    return response.data
  },
}

