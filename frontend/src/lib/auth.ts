import api from './api';
import { API_ROUTES } from './apiRoutes';

interface AuthResponse {
  access: string;
  refresh: string;
}

/**
 * Connexion utilisateur avec email et mot de passe
 */
export const loginUser = async (email: string, password: string): Promise<AuthResponse> => {
  const { data } = await api.post<AuthResponse>(API_ROUTES.LOGIN, { email, password });
  return data;
};

/**
 * Inscription d’un nouvel utilisateur
 */
export const registerUser = async (
  email: string,
  password: string,
  firstName = 'demo',
  lastName = 'user',
  acceptCgu = true
): Promise<AuthResponse> => {
  const { data } = await api.post<AuthResponse>(API_ROUTES.REGISTER, {
    email,
    password,
    first_name: firstName,
    last_name: lastName,
    accept_cgu: acceptCgu,
  });
  return data;
};

/**
 * Rafraîchit les tokens d’accès et de rafraîchissement
 */
export const refreshToken = async (): Promise<AuthResponse | null> => {
  const refresh = localStorage.getItem('refresh');
  if (!refresh) return null;

  try {
    const { data } = await api.post<AuthResponse>(API_ROUTES.REFRESH, { refresh });
    console.log('🔁 Token refreshed:', data);
    return data;
  } catch (error: unknown) {
    if (typeof error === 'object' && error !== null && 'response' in error) {
      const err = error as { response?: { data?: unknown } };
      console.warn('🔁 Token refresh failed:', err.response?.data);
    } else {
      console.warn('🔁 Token refresh error:', error);
    }
    return null;
  }
};

/**
 * Déconnexion : suppression des tokens
 */
export const logoutUser = (): void => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
};
