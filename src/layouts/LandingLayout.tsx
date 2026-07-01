import { Outlet } from 'react-router-dom'
import { Footer } from '@/components/landing/Footer'
import { Navbar } from '@/components/landing/Navbar'

export function LandingLayout() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  )
}
