"use client";

import dynamic from "next/dynamic";

// Désactiver complètement le SSR pour toute la page
const Page = dynamic(() => import("@/components/HomePage"), { ssr: false });

export default function Home() {
    return <Page />;
}