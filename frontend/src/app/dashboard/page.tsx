"use client";

import AuthGuard from "@/components/AuthGuard";

export default function DashboardPage() {
    return (
        <AuthGuard>
            <h1>Bienvenue sur le dashboard</h1>
            <p>Tu es connecté 🎉</p>
        </AuthGuard>
    );
}
