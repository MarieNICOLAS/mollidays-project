"use client";

import { useState } from "react";
import { useAuth } from "@/context/AuthContext";

const LoginForm = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        try {
            await login(email, password); 
        } catch {
            setError("Échec de la connexion. Vérifiez vos identifiants.");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Connexion</h2>

            {error && <p style={{ color: "red" }}>{error}</p>}

            <div>
                <label>Email :</label><br />
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>

            <div>
                <label>Mot de passe :</label><br />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </div>

            <button type="submit">Se connecter</button>
        </form>
    );
};

export default LoginForm;
