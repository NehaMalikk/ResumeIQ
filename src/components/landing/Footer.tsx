import { Code2, Mail, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'

const footerLinks = [
  { label: 'Contact', href: 'mailto:hello@hirematch.ai', icon: Mail },
  { label: 'GitHub', href: 'https://github.com', icon: Code2 },
] as const

export function Footer() {
  return (
    <footer className="border-t border-border bg-surface/40" role="contentinfo">
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center gap-6 text-center sm:flex-row sm:justify-between sm:text-left">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-foreground transition-opacity hover:opacity-80"
          >
            <div className="flex size-8 items-center justify-center rounded-lg bg-linear-to-br from-[#5b5fc7] to-[#7c3aed]">
              <Sparkles className="size-4 text-white" aria-hidden />
            </div>
            <span className="text-sm font-semibold">
              HireMatch <span className="text-primary">AI</span>
            </span>
          </Link>

          <div className="flex flex-col items-center gap-1 sm:items-end">
            <p className="text-xs text-muted">© 2026 HireMatch AI</p>
            <p className="text-xs text-muted-foreground">
              Built for learning & experimentation
            </p>
          </div>

          <nav
            className="flex items-center gap-4"
            aria-label="Footer links"
          >
            {footerLinks.map((link) => {
              const Icon = link.icon
              return (
                <a
                  key={link.label}
                  href={link.href}
                  target={link.label === 'GitHub' ? '_blank' : undefined}
                  rel={link.label === 'GitHub' ? 'noopener noreferrer' : undefined}
                  className="inline-flex items-center gap-1.5 text-xs font-medium text-muted transition-colors hover:text-primary"
                >
                  <Icon className="size-3.5" aria-hidden />
                  {link.label}
                </a>
              )
            })}
          </nav>
        </div>
      </div>
    </footer>
  )
}
