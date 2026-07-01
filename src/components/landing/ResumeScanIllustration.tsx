import { motion } from 'framer-motion'
import { CheckCircle2, FileText, ScanLine } from 'lucide-react'
import { cn } from '@/utils/cn'

interface ResumeScanIllustrationProps {
  className?: string
}

const scanLineVariants = {
  animate: {
    y: ['0%', '100%', '0%'],
    transition: {
      duration: 4,
      repeat: Infinity,
      ease: 'easeInOut' as const,
    },
  },
}

const scoreVariants = {
  initial: { opacity: 0, scale: 0.9 },
  animate: {
    opacity: 1,
    scale: 1,
    transition: { delay: 1.2, duration: 0.5 },
  },
}

const keywordVariants = {
  initial: { opacity: 0, x: 8 },
  animate: (i: number) => ({
    opacity: 1,
    x: 0,
    transition: { delay: 1.8 + i * 0.15, duration: 0.35 },
  }),
}

const keywords = ['React', 'TypeScript', 'Leadership', 'Agile']

export function ResumeScanIllustration({ className }: ResumeScanIllustrationProps) {
  return (
    <div
      className={cn('relative mx-auto w-full max-w-md', className)}
      aria-hidden
    >
      <div className="absolute -inset-4 rounded-3xl bg-linear-to-br from-[#5b5fc7]/20 via-transparent to-[#7c3aed]/15 blur-2xl" />

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
        className="glass relative overflow-hidden rounded-2xl border border-white/60 shadow-2xl shadow-primary/10"
      >
        <div className="flex items-center gap-2 border-b border-border/60 bg-surface/50 px-4 py-3">
          <div className="flex gap-1.5">
            <span className="size-2.5 rounded-full bg-[#ff5f57]" />
            <span className="size-2.5 rounded-full bg-[#febc2e]" />
            <span className="size-2.5 rounded-full bg-[#28c840]" />
          </div>
          <span className="ml-2 text-xs font-medium text-muted">
            resume_analysis.pdf
          </span>
        </div>

        <div className="relative p-6">
          <div className="mb-4 flex items-start gap-3">
            <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10">
              <FileText className="size-5 text-primary" strokeWidth={1.75} />
            </div>
            <div className="flex-1 space-y-2">
              <div className="h-2.5 w-3/4 rounded-full bg-foreground/10" />
              <div className="h-2 w-1/2 rounded-full bg-foreground/5" />
            </div>
          </div>

          <div className="relative space-y-2.5 overflow-hidden rounded-lg border border-border/40 bg-white/50 p-4">
            {[100, 85, 92, 70].map((width, i) => (
              <div
                key={i}
                className="h-2 rounded-full bg-foreground/8"
                style={{ width: `${width}%` }}
              />
            ))}

            <motion.div
              variants={scanLineVariants}
              animate="animate"
              className="absolute inset-x-0 top-0 h-8"
            >
              <div className="relative h-full w-full">
                <div className="absolute inset-x-0 top-1/2 h-px -translate-y-1/2 bg-primary/60" />
                <div className="absolute inset-x-0 top-0 h-full bg-linear-to-b from-primary/15 to-transparent" />
                <ScanLine className="absolute right-2 top-1/2 size-4 -translate-y-1/2 text-primary" />
              </div>
            </motion.div>
          </div>

          <motion.div
            variants={scoreVariants}
            initial="initial"
            animate="animate"
            className="mt-4 flex items-center justify-between rounded-xl border border-emerald-200/60 bg-emerald-50/80 px-4 py-3"
          >
            <div className="flex items-center gap-2">
              <CheckCircle2 className="size-4 text-emerald-600" />
              <span className="text-xs font-medium text-emerald-800">
                ATS Match Score
              </span>
            </div>
            <span className="text-lg font-bold text-emerald-700">91%</span>
          </motion.div>

          <div className="mt-3 flex flex-wrap gap-2">
            {keywords.map((kw, i) => (
              <motion.span
                key={kw}
                custom={i}
                variants={keywordVariants}
                initial="initial"
                animate="animate"
                className="rounded-md bg-accent-soft px-2 py-1 text-[10px] font-medium text-accent"
              >
                {kw}
              </motion.span>
            ))}
          </div>
        </div>
      </motion.div>

      <motion.div
        animate={{ y: [0, -6, 0] }}
        transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute -right-2 top-8 rounded-xl border border-border/80 bg-card px-3 py-2 shadow-lg sm:-right-6"
      >
        <p className="text-[10px] font-medium text-muted">Keywords matched</p>
        <p className="text-sm font-semibold text-foreground">24 / 28</p>
      </motion.div>

      <motion.div
        animate={{ y: [0, 6, 0] }}
        transition={{ duration: 3.5, repeat: Infinity, ease: 'easeInOut', delay: 0.5 }}
        className="absolute -left-2 bottom-12 rounded-xl border border-border/80 bg-card px-3 py-2 shadow-lg sm:-left-6"
      >
        <p className="text-[10px] font-medium text-muted">Suggestions</p>
        <p className="text-sm font-semibold text-primary">12 ready</p>
      </motion.div>
    </div>
  )
}
