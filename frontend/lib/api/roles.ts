import axiosInstance from '../axios'
import { Role, RoleCreate, RoleUpdate, PaginatedResponse } from '@/types'

export interface GetRolesParams {
  page?: number
  limit?: number
  search?: string
  is_active?: boolean
  order_by?: string
  order_desc?: boolean
}

export const rolesApi = {
  getAll: async (params: GetRolesParams = {}): Promise<PaginatedResponse<Role>> => {
    const response = await axiosInstance.get('/api/roles/', { params })
    return response.data
  },

  getById: async (id: number): Promise<Role> => {
    const response = await axiosInstance.get(`/api/roles/${id}`)
    return response.data
  },

  create: async (data: RoleCreate): Promise<Role> => {
    const response = await axiosInstance.post('/api/roles/', data)
    return response.data
  },

  update: async (id: number, data: RoleUpdate): Promise<Role> => {
    const response = await axiosInstance.put(`/api/roles/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/api/roles/${id}`)
  },
}
