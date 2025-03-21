"use client"; // Pour éviter l'erreur d'hydratation

import { useState, useEffect } from "react";
import api from "@/lib/api"; // Assure-toi que ce chemin est correct

interface User {
  id: number;
  email: string;
}

export default function Home() {
  const [users, setUsers] = useState<User[] | null>(null);

  useEffect(() => {
    api.get("/users/")
      .then((response) => setUsers(response.data))
      .catch((error) => console.error("Error fetching users:", error));
  }, []);

  return (
    <div>
      <h1>Liste des utilisateurs</h1>
      {/* Si les données ne sont pas encore chargées, on affiche un loading */}
      {!users ? (
        <p>Chargement...</p>
      ) : (
        <ul>
          {users.map((user) => (
            <li key={user.id}>{user.email}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
