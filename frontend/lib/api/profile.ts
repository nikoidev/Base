import axiosInstance from '../axios'
import { User, ProfileUpdate } from '@/types'

export const profileApi = {
  getMyProfile: async (): Promise<User> => {
    const response = await axiosInstance.get('/api/profile/me')
    return response.data
  },

  updateMyProfile: async (data: ProfileUpdate): Promise<User> => {
    const response = await axiosInstance.put('/api/profile/me', data)
    return response.data
  },

  uploadAvatar: async (file: File): Promise<{ message: string; avatar_url: string }> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await axiosInstance.post('/api/profile/upload-avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  deleteAvatar: async (): Promise<{ message: string }> => {
    const response = await axiosInstance.delete('/api/profile/avatar')
    return response.data
  },
}

