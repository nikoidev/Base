import axios from 'axios'
import toast from 'react-hot-toast'

const axiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach JWT token to every request
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Track if a session-expired redirect is already in progress
// to avoid multiple simultaneous toasts/redirects
let isRedirectingToLogin = false

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status
    const requestUrl = error.config?.url ?? ''

    // 401 on the login endpoint itself = wrong credentials, NOT an expired session.
    // Let the login page handle it and show the appropriate error message.
    const isLoginRequest = requestUrl.includes('/auth/login')

    if (status === 401 && !isLoginRequest) {
      if (!isRedirectingToLogin) {
        isRedirectingToLogin = true
        localStorage.removeItem('token')

        toast('Tu sesión ha expirado. Vuelve a iniciar sesión.', {
          icon: '🔒',
          duration: 3000,
        })

        // Small delay so the toast renders before navigation
        setTimeout(() => {
          window.location.href = '/login'
          isRedirectingToLogin = false
        }, 1000)
      }

      // Return a rejected promise that will NOT propagate as an unhandled error
      // (the redirect is already happening)
      return Promise.reject(error)
    }

    return Promise.reject(error)
  }
)

export default axiosInstance
