"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { User } from "@/types/user";

const UserList = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [isClient, setIsClient] = useState(false);

    useEffect(() => {
        setIsClient(true);
    }, []);

    useEffect(() => {
        setLoading(true);
        api.get("/users/")
            .then((response) => {
                console.log("Users received:", response.data);
                setUsers(response.data);
                setLoading(false);
            })
            .catch((err) => {
                console.error("API error:", err);
                setError("Impossible de charger la liste des utilisateurs.");
                setLoading(false);
            });
    }, []);

    if (!isClient) return <p>Chargement...</p>;

    return (
        <div>
            <h1>Liste des utilisateurs</h1>

            {loading && <p>Chargement...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}

            {!loading && !error && users.length === 0 && <p>Aucun utilisateur trouvé.</p>}

            {!loading && !error && users.length > 0 && (
                <ul>
                    {users.map((user) => (
                        <li key={user.id}>
                            <strong>{user.username}</strong> ({user.email})
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default UserList;
