"use client"; // 🚀 Ajoute ça tout en haut !

import React, { createContext, useContext, useState, useEffect } from "react";
import api from "@/lib/api";

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

// Création du contexte
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    // Vérifier si un token existe au chargement
    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            fetchUser(token);
        }
    }, []);

    const fetchUser = async (authToken: string) => {
        try {
            console.log("🔍 Fetching user with token:", authToken);
            const response = await api.get("/users/me/", {
                headers: { Authorization: `Bearer ${authToken}` },
            });
            console.log("✅ User received:", response.data);
            setUser(response.data);
        } catch (error) {
            console.error("❌ Erreur récupération user:", error);
            logout();
        }
    };

    const login = async (email: string, password: string) => {
        try {
            const response = await api.post("/token/", { email, password });
            const { access } = response.data;
            localStorage.setItem("token", access);
            fetchUser(access);
        } catch (error) {
            console.error("❌ Login failed:", error);
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
