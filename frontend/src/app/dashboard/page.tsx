"use client";

import { useAuth } from "@/context/AuthContext";

export default function DashboardPage() {
  const { user } = useAuth();

  if (!user) return <p>Chargement...</p>;

  return (
    <div>
      <h1>Bienvenue {user.username}</h1>
      <p>Tu es connecté avec : {user.email}</p>
    </div>
  );
}
