"use client";

import UserList from "@/components/dashboard/UserList";
import { useAuth } from "@/context/AuthContext";

export default function HomePage() {
    const { user, logout } = useAuth();

    return (
        <div>
            <h1>Page d accueil</h1>
            {user ? (
                <div>
                    <p>Bienvenue, <strong>{user.username}</strong>({user.email})</p>
                    <button onClick={logout}>Se déconnecter</button>
                </div>
            ) : (
                <p>Vous n êtes pas connecté.</p>
            )}

            <UserList/>
        </div>
    );
}