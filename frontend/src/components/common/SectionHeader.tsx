import { motion } from 'framer-motion'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/utils/cn'

interface SectionHeaderProps {
  badge?: string
  title: string
  description?: string
  align?: 'center' | 'left'
  className?: string
}

export function SectionHeader({
  badge,
  title,
  description,
  align = 'center',
  className,
}: SectionHeaderProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-80px' }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className={cn(
        'mx-auto max-w-2xl',
        align === 'center' && 'text-center',
        className
      )}
    >
      {badge && (
        <Badge variant="default" className="mb-4">
          {badge}
        </Badge>
      )}
      <h2 className="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
        {title}
      </h2>
      {description && (
        <p className="mt-4 text-base leading-relaxed text-muted sm:text-lg">
          {description}
        </p>
      )}
    </motion.div>
  )
}
