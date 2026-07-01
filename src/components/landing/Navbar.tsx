import { Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'

export function Navbar() {
  return (
    <header className="fixed inset-x-0 top-0 z-50">
      <nav
        className="glass mx-auto mt-4 flex max-w-6xl items-center justify-between rounded-2xl border border-white/50 px-4 py-3 shadow-sm sm:px-6"
        aria-label="Main navigation"
      >
        <Link
          to="/"
          className="flex items-center gap-2 text-foreground transition-opacity hover:opacity-80"
        >
          <div className="flex size-8 items-center justify-center rounded-lg bg-linear-to-br from-[#5b5fc7] to-[#7c3aed]">
            <Sparkles className="size-4 text-white" aria-hidden />
          </div>
          <span className="text-sm font-semibold tracking-tight">
            Resume<span className="text-primary">IQ</span>
          </span>
        </Link>

        <a
          href="#analyzer"
          className="text-sm font-medium text-muted transition-colors hover:text-foreground"
        >
          Analyze resume
        </a>
      </nav>
    </header>
  )
}
