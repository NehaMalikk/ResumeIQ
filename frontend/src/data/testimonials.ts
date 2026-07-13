import type { Testimonial } from '@/types'

export const testimonials: Testimonial[] = [
  {
    id: '1',
    name: 'Sarah Chen',
    role: 'Product Manager',
    company: 'Stripe',
    avatar: 'SC',
    content:
      'ResumeIQ helped me tailor my resume for three roles in one afternoon. My ATS score went from 62 to 91 — I landed interviews within a week.',
    rating: 5,
  },
  {
    id: '2',
    name: 'Marcus Rivera',
    role: 'Software Engineer',
    company: 'Linear',
    avatar: 'MR',
    content:
      'The keyword matching is incredibly precise. It surfaced gaps I never would have caught manually, and the AI rewrite suggestions felt natural.',
    rating: 5,
  },
  {
    id: '3',
    name: 'Emily Nakamura',
    role: 'Data Analyst',
    company: 'Notion',
    avatar: 'EN',
    content:
      'Finally a resume tool that feels like a premium product. Clean UI, fast analysis, and genuinely useful feedback — not generic fluff.',
    rating: 5,
  },
  {
    id: '4',
    name: 'James Okonkwo',
    role: 'Marketing Lead',
    company: 'Figma',
    avatar: 'JO',
    content:
      'JD parsing saved me hours. I paste the listing, upload my resume, and get a clear match report with prioritized fixes. Game changer.',
    rating: 5,
  },
]
