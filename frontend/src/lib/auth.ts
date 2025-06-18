import api from './api'

export const loginUser = async (credentials: { email: string; password: string }) => {
  const response = await api.post('/token/', credentials)
  return response.data
}

export const registerUser = async (data: { email: string; password: string; first_name: string; last_name: string }) => {
  const response = await api.post('/register/', data)
  return response.data
}
