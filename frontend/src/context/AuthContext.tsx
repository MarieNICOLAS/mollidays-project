'use client';

import React, {
  useState,
  useEffect,
  useCallback,
  useContext,
  ReactNode,
  createContext,
  useRef,
} from 'react';
import { useRouter } from 'next/navigation';
import {
  loginUser,
  registerUser,
  logoutUser,
  refreshToken,
} from '@/lib/auth';
import {
  decodeToken,
  isTokenExpired,
  DecodedJWT,
} from '@/lib/jwt';
import api from '@/lib/api';
import { API_ROUTES } from '@/lib/apiRoutes';
import type { User } from '@/types/user';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const refreshIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const isRefreshingRef = useRef(false);

  const fetchUserDetails = async (): Promise<boolean> => {
    try {
      const response = await api.get<User>(API_ROUTES.ME);
      setUser(response.data);
      return true;
    } catch (err) {
      console.error('❌ Erreur lors du fetch /users/me:', err);
      setUser(null);
      return false;
    }
  };

  const logout = useCallback(() => {
    if (refreshIntervalRef.current) {
      clearInterval(refreshIntervalRef.current);
      refreshIntervalRef.current = null;
    }
    
    logoutUser();
    setUser(null);
    router.push('/login');
  }, [router]);

  const startTokenRefreshInterval = useCallback(() => {
    if (refreshIntervalRef.current) {
      clearInterval(refreshIntervalRef.current);
    }

    refreshIntervalRef.current = setInterval(async () => {
      if (isRefreshingRef.current) return;

      const token = localStorage.getItem('access');
      if (!token) {
        clearInterval(refreshIntervalRef.current!);
        return;
      }

    const decoded = decodeToken(token);
    if (decoded?.exp) {
      const timeUntilExpiry = decoded.exp - Math.floor(Date.now() / 1000);
      if (timeUntilExpiry < 120) {
        isRefreshingRef.current = true;

        try {
          const tokens = await refreshToken();
          if (tokens) {
            localStorage.setItem('access', tokens.access);
            localStorage.setItem('refresh', tokens.refresh);
            console.log('✅ Token refreshed successfully');
          } else {
            console.log('❌ Token refresh failed - logging out');
            logout();
          }
        } catch (error) {
          console.error('❌ Error during token refresh:', error);
          logout();
        } finally {
          isRefreshingRef.current = false;
        }
      }
    }
  }, 60 * 1000);
}, [logout]);

  const loadUserFromToken = async () => {
    const token = localStorage.getItem('access');

    if (token && !isTokenExpired(token)) {
      const decoded = decodeToken(token) as DecodedJWT | null;
      if (decoded?.user_id) {
        const success = await fetchUserDetails();
        if (success) {
          startTokenRefreshInterval();
        }
      } else {
        setUser(null);
      }
    } else {
      setUser(null);
      // Tente un refresh si on a un refresh token
      const refreshTokenValue = localStorage.getItem('refresh');
      if (refreshTokenValue) {
        try {
          const tokens = await refreshToken();
          if (tokens) {
            localStorage.setItem('access', tokens.access);
            localStorage.setItem('refresh', tokens.refresh);
            const success = await fetchUserDetails();
            if (success) {
              startTokenRefreshInterval();
            }
          }
        } catch (error) {
          console.log('❌ Initial token refresh failed');
          logoutUser(); // Nettoie les tokens invalides
          throw error;
        }
      }
    }

    setLoading(false);
  };

  const login = async (email: string, password: string) => {
    try {
      const { access, refresh } = await loginUser(email, password);
      localStorage.setItem('access', access);
      localStorage.setItem('refresh', refresh);

      const decoded = decodeToken(access) as DecodedJWT | null;
      if (decoded?.user_id) {
        const success = await fetchUserDetails();
        if (success) {
          startTokenRefreshInterval();
          router.push('/dashboard');
        } else {
          throw new Error('Failed to fetch user details');
        }
      } else {
        throw new Error('Invalid token received');
      }
    } catch (error) {
      console.error('❌ Login failed:', error);
      setUser(null);
      logoutUser();
      throw error; // Propage l'erreur pour que le composant Login puisse l'afficher
    }
  };

  const register = async (email: string, password: string) => {
    await registerUser(email, password);
    await login(email, password);
  };


  // Effet pour charger l'utilisateur au démarrage
  useEffect(() => {
    loadUserFromToken();
    
    // Cleanup à la destruction du composant
    return () => {
      if (refreshIntervalRef.current) {
        clearInterval(refreshIntervalRef.current);
      }
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <AuthContext.Provider
      value={{ 
        user, 
        isAuthenticated: !!user, 
        loading, 
        login, 
        register, 
        logout 
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};