"use client";

import React, { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { useRouter } from "next/router";
import { loginUser, logoutUser, registerUser, refreshToken } from "@/lib/auth";
import { decodeToken, isTokenExpired } from "@/lib/jwt";

export interface User {
  id: number;
  email: string;
  username: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  const loadUserFromToken = () => {
    const token = localStorage.getItem("access");
    if (token && !isTokenExpired(token)) {
      const decoded = decodeToken(token);
      if (decoded && decoded.user) setUser(decoded.user);
    } else {
      setUser(null);
    }
  };

  const login = async (email: string, password: string) => {
    const { access, refresh } = await loginUser(email, password);
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    
    const decoded = decodeToken(access);
    if (decoded?.user) setUser(decoded.user);
    
    router.push("/dashboard");
  };

  const register = async (email: string, password: string) => {
    await registerUser(email, password);
    await login(email, password);
  };

  const logout = () => {
    logoutUser();
    setUser(null);
    router.push("/login");
  };

  useEffect(() => {
    const interval = setInterval(async () => {
      const newAccess = await refreshToken();
      if (newAccess) {
        localStorage.setItem("access", newAccess);
        const decoded = decodeToken(newAccess);
        if (decoded?.user) setUser(decoded.user);
      } else {
        logout();
      }
    }, 4 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    loadUserFromToken();
  }, []);

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
