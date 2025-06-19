"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useEffect, useState } from "react"
import { Menu, X, ShoppingCart, User } from "lucide-react"
import { Button } from "@/components/ui/button"

const Navbar = () => {
  const pathname = usePathname()
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10)
    }
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  useEffect(() => {
    setIsMobileMenuOpen(false)
  }, [pathname])
  

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? "bg-white dark:bg-background bg-opacity-95 shadow-sm backdrop-blur-md py-3"
          : "bg-black/50 dark:bg-black/30 backdrop-blur-sm py-5"
      }`}
    >
      <div className="container mx-auto px-4 md:px-6">
        <nav className="flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-3 transition-transform hover:scale-105"
            
            ><span
              className={`text-2xl font-bold transition-colors ${
                isScrolled ? "text-gray-800 dark:text-white" : "text-white"
              }`}
            >
              Mollidays
            </span>
          </Link>
        
          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-2">
            {[
              { href: "/", label: "Accueil" },
              { href: "/trips", label: "Circuits" },
              { href: "/about", label: "À propos" },
              { href: "/contact", label: "Contact" },
            ].map(({ href, label }) => (
              <Button
                key={href}
                variant="ghost"
                asChild
                className={`transition-colors ${
                  isScrolled
                    ? "text-gray-800 dark:text-white hover:bg-gray-100 dark:hover:bg-muted"
                    : "text-white hover:bg-white/20"
                }`}
              >
                <Link
                  href={href}
                  className={`text-base font-medium ${
                    pathname === href ? "text-coral" : ""
                  }`}
                >
                  {label}
                </Link>
              </Button>
            ))}
          </div>

          {/* User + Panier */}
          <div className="hidden md:flex items-center gap-2">
            <Button variant="ghost" size="icon" asChild>
              <Link href="/cart" aria-label="Panier">
                <ShoppingCart className="h-5 w-5" />
              </Link>
            </Button>
            <Button variant="ghost" size="icon" asChild>
              <Link href="/login" aria-label="Se connecter">
                <User className="h-5 w-5" />
              </Link>
            </Button>
            <Button variant="coral" asChild>
              <Link href="/register">S inscrire</Link>
            </Button>
          </div>

          {/* Bouton Mobile */} 
          <div className="md:hidden flex items-center gap-2">
            <Button variant="ghost" size="icon" asChild>
              <Link href="/cart" aria-label="Panier">
                <ShoppingCart className="h-5 w-5" />
              </Link>
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              aria-label={isMobileMenuOpen ? "Fermer le menu" : "Ouvrir le menu"}
            >
              {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </nav>
      </div>

      {/* Menu Mobile */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-black/80 dark:bg-black/60 backdrop-blur-md absolute top-full left-0 w-full shadow-md animate-slide-in-right">
          <div className="flex flex-col px-6 py-4 space-y-3">
            {[
              { href: "/", label: "Accueil" },
              { href: "/trips", label: "Circuits" },
              { href: "/about", label: "À propos" },
              { href: "/contact", label: "Contact" },
            ].map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className={`py-2 text-lg ${
                  pathname === href ? "text-coral font-medium" : "text-white"
                }`}
              >
                {label}
              </Link>
            ))}

            <div className="pt-2 border-t border-gray-700">
              <Link href="/login" className="py-2 text-lg text-white block">
                Se connecter
              </Link>
              <Button className="w-full mt-3" variant="coral" asChild>
                <Link href="/register">S inscrire</Link>
              </Button>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}

export default Navbar
