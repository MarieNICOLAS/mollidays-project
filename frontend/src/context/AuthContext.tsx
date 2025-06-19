'use client';

import React, {
  useState,
  useEffect,
  useCallback,
  useContext,
  ReactNode,
  createContext,
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

  const fetchUserDetails = async () => {
    try {
      const response = await api.get<User>(API_ROUTES.ME);
      setUser(response.data);
    } catch (err) {
      console.error('❌ Erreur lors du fetch /users/me:', err);
      setUser(null);
    }
  };

  const loadUserFromToken = async () => {
    const token = localStorage.getItem('access');

    if (token && !isTokenExpired(token)) {
      const decoded = decodeToken(token) as DecodedJWT | null;
      if (decoded?.user_id) {
        await fetchUserDetails();
      } else {
        setUser(null);
      }
    } else {
      setUser(null);
    }

    setLoading(false);
  };

  const login = async (email: string, password: string) => {
    const { access, refresh } = await loginUser(email, password);
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);

    const decoded = decodeToken(access) as DecodedJWT | null;
    if (decoded?.user_id) {
      await fetchUserDetails();
      router.push('/dashboard');
    } else {
      setUser(null);
      router.push('/login');
    }
  };

  const register = async (email: string, password: string) => {
    await registerUser(email, password);
    await login(email, password);
  };

  const logout = useCallback(() => {
    logoutUser();
    setUser(null);
    router.push('/login');
  }, [router]);

  useEffect(() => {
    const intervalId = setInterval(async () => {
      const newAccess = await refreshToken();
      if (newAccess) {
        localStorage.setItem('access', newAccess);
        const decoded = decodeToken(newAccess);
        if (decoded?.user_id) {
          await fetchUserDetails();
        }
      } else {
        clearInterval(intervalId);
        logout();
      }
    }, 4 * 60 * 1000); // 4 minutes

    return () => clearInterval(intervalId);
  }, [logout]);

  useEffect(() => {
    loadUserFromToken();
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated: !!user, loading, login, register, logout }}
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
