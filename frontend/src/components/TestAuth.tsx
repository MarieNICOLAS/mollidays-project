"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { API_ROUTES } from "@/lib/apiRoutes";

const TestAuth = () => {
  interface UserData {
    id: string;
    name: string;
    email: string;
    // Add other fields as needed based on your API response
  }

  const [userData, setUserData] = useState<UserData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchProtectedData = async () => {
    try {
      const response = await api.get(API_ROUTES.ME);
      setUserData(response.data);
    } catch (err) {
      console.error("❌ Error fetching protected data:", err);
      setError("Access denied or error occurred.");
    }
  };

  useEffect(() => {
    fetchProtectedData();
  }, []);

  return (
    <div className="p-4 border rounded bg-white shadow mt-4">
      <h2 className="text-lg font-bold mb-2">🔒 Protected User Info</h2>

      {error && <p className="text-red-600">{error}</p>}
      {userData ? (
        <pre className="text-sm bg-gray-100 p-2 rounded">{JSON.stringify(userData, null, 2)}</pre>
      ) : !error ? (
        <p>Loading...</p>
      ) : null}
    </div>
  );
};

export default TestAuth;
