"use client";

import AuthGuard from "@/components/shared/AuthGuard";
import TestAuth from "@/components/TestAuth";

export default function DashboardPage() {
  return (
    <AuthGuard>
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Bienvenue sur le Dashboard 🎉</h1>
        <TestAuth />
      </div>
    </AuthGuard>
  );
}
