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
 * Rafraîchit le token d’accès à partir du refresh token
 */
// export const refreshToken = async (): Promise<string | null> => {
//   const refresh = localStorage.getItem('refresh');
//   if (!refresh) return null;

//   try {
//     const { data } = await api.post<{ access: string }>(API_ROUTES.REFRESH, { refresh });
//     return data.access;
//   } catch (error: unknown) {
//     if (typeof error === 'object' && error !== null && 'response' in error) {
//       const err = error as { response?: { data?: unknown } };
//       console.warn('🔁 Token refresh failed:', err.response?.data);
//     } else {
//       console.warn('🔁 Token refresh error:', error);
//     }
//     return null;
//   }
// };
export const refreshToken = async (): Promise<string | null> => {
  const refresh = localStorage.getItem('refresh');
  if (!refresh) return null;

  try {
    const { data } = await api.post<{ access: string }>(API_ROUTES.REFRESH, { refresh });
    return data.access;
  } catch (err) {
    // Ajoute ceci pour bien sortir en cas de 401
    console.warn("❌ Failed to refresh token:", err);
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
