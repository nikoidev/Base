import axiosInstance from '../axios'
import { User, UserCreate, UserUpdate, PaginatedResponse } from '@/types'

export interface GetUsersParams {
  page?: number
  limit?: number
  search?: string
  role_id?: number
  is_active?: boolean
  order_by?: string
  order_desc?: boolean
}

export const usersApi = {
  getAll: async (params: GetUsersParams = {}): Promise<PaginatedResponse<User>> => {
    const response = await axiosInstance.get('/api/users/', { params })
    return response.data
  },

  getById: async (id: number): Promise<User> => {
    const response = await axiosInstance.get(`/api/users/${id}`)
    return response.data
  },

  create: async (data: UserCreate): Promise<User> => {
    const response = await axiosInstance.post('/api/users/', data)
    return response.data
  },

  update: async (id: number, data: UserUpdate): Promise<User> => {
    const response = await axiosInstance.put(`/api/users/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await axiosInstance.delete(`/api/users/${id}`)
  },
}
