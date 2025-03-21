import { useEffect, useState } from "react";
import api from "@/lib/api";
import { User } from "@/types/user";

const UserList = () => {
    const [users, setUsers] = useState<User[]>([]);

    useEffect(() => {
        api.get("/users/")
            .then((response) => setUsers(response.data))
            .catch((error) => console.error(error));
    }, []);

    return (
        <div>
            <h1>Liste des utilisateurs</h1>
            <ul>
                {users.map((user) => (
                    <li key={user.id}>{user.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default UserList;
