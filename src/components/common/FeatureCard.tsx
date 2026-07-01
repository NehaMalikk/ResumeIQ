import { motion } from 'framer-motion'
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import type { Feature } from '@/types'
import { cn } from '@/utils/cn'

interface FeatureCardProps {
  feature: Feature
  index?: number
  className?: string
}

export function FeatureCard({ feature, index = 0, className }: FeatureCardProps) {
  const Icon = feature.icon

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-40px' }}
      transition={{
        duration: 0.45,
        delay: index * 0.08,
        ease: [0.22, 1, 0.36, 1],
      }}
      className={cn('h-full', className)}
    >
      <Card className="group h-full border-border/80 bg-card/80 transition-all duration-300 hover:border-primary/20 hover:shadow-lg hover:shadow-primary/5">
        <CardHeader>
          <div
            className="mb-4 flex size-11 items-center justify-center rounded-xl bg-linear-to-br from-[#5b5fc7]/10 to-[#7c3aed]/10 text-primary transition-transform duration-300 group-hover:scale-105"
            aria-hidden
          >
            <Icon className="size-5" strokeWidth={1.75} />
          </div>
          <CardTitle className="text-base">{feature.title}</CardTitle>
          <CardDescription>{feature.description}</CardDescription>
        </CardHeader>
      </Card>
    </motion.div>
  )
}
