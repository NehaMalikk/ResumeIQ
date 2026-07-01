import { motion } from 'framer-motion'
import { Badge } from '@/components/ui/badge'
import { ResumeScanIllustration } from '@/components/landing/ResumeScanIllustration'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.12, delayChildren: 0.1 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] as const },
  },
}

export function HeroSection() {
  return (
    <section
      className="relative overflow-hidden pt-28 pb-12 sm:pt-36 sm:pb-16"
      aria-labelledby="hero-heading"
    >
      <div className="gradient-mesh pointer-events-none absolute inset-0" />

      <div className="relative mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-16">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="text-center lg:text-left"
          >
            <motion.div variants={itemVariants}>
              <Badge variant="default" className="mb-6">
                Resume ATS Analyzer
              </Badge>
            </motion.div>

            <motion.h1
              id="hero-heading"
              variants={itemVariants}
              className="text-4xl font-semibold tracking-tight text-foreground sm:text-5xl lg:text-[3.25rem] lg:leading-[1.1]"
            >
              Match your resume to{' '}
              <span className="text-gradient">any job posting</span>
            </motion.h1>

            <motion.p
              variants={itemVariants}
              className="mx-auto mt-6 max-w-xl text-base leading-relaxed text-muted sm:text-lg lg:mx-0"
            >
              Instant ATS scoring, keyword alignment, and improvement tips —
              upload your resume and job description below to get started.
            </motion.p>

            <motion.p
              variants={itemVariants}
              className="mt-6 text-xs text-muted-foreground"
            >
              Free analysis · Paste job text or upload PDF, DOCX, TXT, or images
            </motion.p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="relative lg:pl-4"
          >
            <ResumeScanIllustration />
          </motion.div>
        </div>
      </div>
    </section>
  )
}
