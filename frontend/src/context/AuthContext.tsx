"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import api from "@/lib/api";
import axios from "axios";

interface User {
    id: number;
    email: string;
    username: string;
}

interface AuthContextType {
    user: User | null;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            fetchUser(token);
        }
    }, []);

    const fetchUser = async (authToken: string) => {
        try {
            const response = await api.get("/users/me/", {
                headers: { Authorization: `Bearer ${authToken}` },
            });
            setUser(response.data);
        } catch (error) {
            console.error("❌ Fetch error", error);
            logout();
        }
    };

    const login = async (email: string, password: string) => {
        try {
            const response = await api.post("/token/", { email, password });
            const { access } = response.data;
            localStorage.setItem("token", access);
            await fetchUser(access);
        } catch (error) {
            if (axios.isAxiosError(error) && error.response) {
               console.error("🔴 Login failed:", error.response.data);
            } else {
                console.error("🔴 Unknown error:", error);
            }
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
