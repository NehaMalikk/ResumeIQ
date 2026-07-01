import type { LucideIcon } from 'lucide-react'

export interface Feature {
  id: string
  title: string
  description: string
  icon: LucideIcon
}

export interface Testimonial {
  id: string
  name: string
  role: string
  company: string
  avatar: string
  content: string
  rating: number
}

export interface SocialLink {
  label: string
  href: string
  icon: LucideIcon
}
