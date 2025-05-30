"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

const AuthGuard = ({ children }: { children: React.ReactNode }) => {
    const { user } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (user === null) {
            router.push("/login");
        }
    }, [user, router]);

    // Si on attend que le contexte charge le user
    if (user === null) {
        return <p className="text-center mt-10">Redirection vers la page de connexion...</p>;
    }

    return <>{children}</>;
};

export default AuthGuard;
