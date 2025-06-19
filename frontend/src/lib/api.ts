import axios, { AxiosRequestConfig, AxiosError, InternalAxiosRequestConfig } from "axios";
import { refreshToken, logoutUser } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

// Flag pour éviter les appels concurrents de refresh
let isRefreshing = false;
let refreshSubscribers: Array<(token: string) => void> = [];

// Fonction pour notifier tous les abonnés du nouveau token
const onRefreshed = (token: string) => {
  refreshSubscribers.map(callback => callback(token));
  refreshSubscribers = [];
};

// Fonction pour ajouter un abonné
const subscribeTokenRefresh = (callback: (token: string) => void) => {
  refreshSubscribers.push(callback);
};

/**
 * Axios instance configured with base API URL
 */
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Request interceptor:
 * Automatically attaches the JWT access token to the Authorization header
 */
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("access");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * Response interceptor:
 * If the response status is 401 (Unauthorized), tries to refresh the access token once.
 * If refresh fails, logs out the user.
 */
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (isRefreshing) {
        // Si un refresh est déjà en cours, attendre qu'il se termine
        return new Promise((resolve) => {
          subscribeTokenRefresh((token: string) => {
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${token}`;
            }
            resolve(api(originalRequest));
          });
        });
      }

      isRefreshing = true;

      try {
        const tokens = await refreshToken();
        if (tokens && originalRequest.headers) {
          const { access, refresh } = tokens;
          localStorage.setItem('access', access);
          localStorage.setItem('refresh', refresh);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          
          // Notifier tous les abonnés
          onRefreshed(access);
          
          return api(originalRequest);
        } else {
          throw new Error('No tokens received');
        }
      } catch (refreshError) {
        console.error('❌ Token refresh failed in interceptor:', refreshError);
        logoutUser();
        // Redirection vers login sera gérée par AuthContext
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;