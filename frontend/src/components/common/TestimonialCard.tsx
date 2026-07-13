import { motion } from 'framer-motion'
import { Star } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import type { Testimonial } from '@/types'
import { cn } from '@/utils/cn'

interface TestimonialCardProps {
  testimonial: Testimonial
  index?: number
  className?: string
}

export function TestimonialCard({
  testimonial,
  index = 0,
  className,
}: TestimonialCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{
        duration: 0.45,
        delay: index * 0.1,
        ease: [0.22, 1, 0.36, 1],
      }}
      className={cn('h-full', className)}
    >
      <Card className="flex h-full flex-col border-border/80 bg-card/90 glass transition-shadow duration-300 hover:shadow-md">
        <CardContent className="flex flex-1 flex-col p-6">
          <div className="mb-4 flex gap-0.5" aria-label={`${testimonial.rating} out of 5 stars`}>
            {Array.from({ length: testimonial.rating }).map((_, i) => (
              <Star
                key={i}
                className="size-4 fill-amber-400 text-amber-400"
                aria-hidden
              />
            ))}
          </div>
          <blockquote className="flex-1 text-sm leading-relaxed text-foreground/90">
            &ldquo;{testimonial.content}&rdquo;
          </blockquote>
          <footer className="mt-6 flex items-center gap-3 border-t border-border/60 pt-5">
            <div
              className="flex size-10 shrink-0 items-center justify-center rounded-full bg-linear-to-br from-[#5b5fc7] to-[#7c3aed] text-xs font-semibold text-white"
              aria-hidden
            >
              {testimonial.avatar}
            </div>
            <div>
              <cite className="not-italic">
                <p className="text-sm font-semibold text-foreground">
                  {testimonial.name}
                </p>
                <p className="text-xs text-muted">
                  {testimonial.role} at {testimonial.company}
                </p>
              </cite>
            </div>
          </footer>
        </CardContent>
      </Card>
    </motion.div>
  )
}
