import "@/globals.css";

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "@/components/layout/ThemeProvider";
import { AuthProvider } from "@/context/AuthContext"; // Assure-toi que ce fichier existe
import Navbar from "@/components/layout/Header";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Mollidays - Plateforme de réservation de voyages",
  description: "Réservez vos circuits en duo parent-enfant avec Mollidays. Une plateforme humaine, immersive et simple d'utilisation.",
  keywords: [
    "voyage",
    "réservation",
    "duo",
    "parent",
    "enfant",
    "circuits",
    "Mollidays",
    "tourisme responsable",
    "vacances famille"
  ],
  authors: [{ name: "Mollidays Team", url: "https://mollidays.fr" }],
  openGraph: {
    title: "Mollidays - Réservation de circuits",
    description: "Réservez des circuits uniques en duo parent-enfant. Une plateforme claire, humaine et immersive.",
    type: "website",
    url: "https://mollidays.fr",
    images: [
      {
        url: "/logo_mollidays.png",
        width: 1200,
        height: 630,
        alt: "Logo Mo'lidays"
      }
    ]
  },
  metadataBase: new URL("https://mollidays.fr"),
};
export const viewport = {
    width: "device-width",
    initialScale: 1,
    maximumScale: 1,
  }
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <body className={inter.className}>
        <AuthProvider>
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
            <Navbar />
            <main className="pt-24">{children}</main>
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
