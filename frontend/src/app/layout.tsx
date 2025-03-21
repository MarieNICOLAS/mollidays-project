// Sans "use client"
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mollidays",
  description: "Voyagez en famillez | Duos parent-enfant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}