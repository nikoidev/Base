import axiosInstance from '../axios'
import { User } from '@/types'

export const authApi = {
  login: async (username: string, password: string) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await axiosInstance.post('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  me: async (): Promise<User> => {
    const response = await axiosInstance.get('/api/auth/me')
    return response.data
  },
}
