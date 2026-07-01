import { motion } from 'framer-motion'
import {
  AlertCircle,
  CheckCircle2,
  Lightbulb,
  Sparkles,
  Target,
  TrendingUp,
} from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { dummyAnalysisResults } from '@/data/analysisResults'
import { cn } from '@/utils/cn'

const { atsMatchScore, keywordMatch, missingKeywords, suggestions, resumeStrength } =
  dummyAnalysisResults

const priorityStyles = {
  high: 'border-red-200/80 bg-red-50/60 text-red-700',
  medium: 'border-amber-200/80 bg-amber-50/60 text-amber-800',
  low: 'border-border bg-surface text-muted',
} as const

function ScoreRing({ score }: { score: number }) {
  const circumference = 2 * Math.PI * 54
  const offset = circumference - (score / 100) * circumference

  return (
    <div className="relative mx-auto size-36 sm:size-40">
      <svg className="size-full -rotate-90" viewBox="0 0 120 120" aria-hidden>
        <circle
          cx="60"
          cy="60"
          r="54"
          fill="none"
          stroke="currentColor"
          strokeWidth="8"
          className="text-surface"
        />
        <circle
          cx="60"
          cy="60"
          r="54"
          fill="none"
          stroke="url(#scoreGradient)"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="transition-all duration-1000 ease-out"
        />
        <defs>
          <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#5b5fc7" />
            <stop offset="100%" stopColor="#7c3aed" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
          {score}
        </span>
        <span className="text-xs font-medium text-muted">out of 100</span>
      </div>
    </div>
  )
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.08 },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 16 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.45, ease: [0.22, 1, 0.36, 1] as const },
  },
}

export function AnalysisResultsSection() {
  return (
    <section
      id="results"
      className="border-t border-border/60 bg-surface/20 pb-20 pt-4 sm:pb-28"
      aria-labelledby="results-heading"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={containerVariants}
          className="space-y-6"
        >
          <motion.div variants={itemVariants} className="text-center">
            <div className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-accent-soft/50 px-3 py-1 text-xs font-medium text-primary">
              <Sparkles className="size-3.5" aria-hidden />
              Analysis complete
            </div>
            <h2
              id="results-heading"
              className="mt-4 text-2xl font-semibold tracking-tight text-foreground sm:text-3xl"
            >
              Your ATS results
            </h2>
            <p className="mx-auto mt-2 max-w-lg text-sm text-muted">
              Sample insights based on your uploads — dummy data for demonstration.
            </p>
          </motion.div>

          <div className="grid gap-6 lg:grid-cols-3">
            <motion.div variants={itemVariants} className="lg:col-span-1">
              <Card className="glass h-full border-white/60 shadow-md shadow-primary/5">
                <CardHeader className="text-center pb-2">
                  <CardTitle className="flex items-center justify-center gap-2 text-base">
                    <Target className="size-4 text-primary" aria-hidden />
                    ATS Match Score
                  </CardTitle>
                  <CardDescription>
                    How well your resume passes automated screening
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex flex-col items-center pb-8">
                  <ScoreRing score={atsMatchScore} />
                  <p className="mt-4 text-center text-sm text-muted">
                    {atsMatchScore >= 80
                      ? 'Strong match — minor tweaks recommended'
                      : atsMatchScore >= 60
                        ? 'Solid foundation — optimize keywords to improve'
                        : 'Needs work — focus on missing terms below'}
                  </p>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div variants={itemVariants} className="lg:col-span-1">
              <Card className="glass h-full border-white/60 shadow-md shadow-primary/5">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-base">
                    <CheckCircle2 className="size-4 text-primary" aria-hidden />
                    Keyword Match
                  </CardTitle>
                  <CardDescription>
                    Alignment between your resume and the job description
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-5">
                  <div>
                    <div className="flex items-baseline justify-between">
                      <span className="text-3xl font-semibold text-foreground">
                        {keywordMatch.percentage}%
                      </span>
                      <span className="text-sm text-muted">
                        {keywordMatch.matched} / {keywordMatch.total} keywords
                      </span>
                    </div>
                    <div
                      className="mt-3 h-2.5 overflow-hidden rounded-full bg-surface"
                      role="progressbar"
                      aria-valuenow={keywordMatch.percentage}
                      aria-valuemin={0}
                      aria-valuemax={100}
                      aria-label="Keyword match percentage"
                    >
                      <div
                        className="h-full rounded-full bg-linear-to-r from-[#5b5fc7] to-[#7c3aed] transition-all duration-700"
                        style={{ width: `${keywordMatch.percentage}%` }}
                      />
                    </div>
                  </div>
                  <ul className="space-y-2 text-sm text-muted">
                    <li className="flex items-start gap-2">
                      <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-primary" />
                      Role-specific skills detected in both documents
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-amber-500" />
                      {keywordMatch.total - keywordMatch.matched} keywords only in the job posting
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div variants={itemVariants} className="lg:col-span-1">
              <Card className="glass h-full border-white/60 shadow-md shadow-primary/5">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-base">
                    <TrendingUp className="size-4 text-primary" aria-hidden />
                    Resume Strength Meter
                  </CardTitle>
                  <CardDescription>{resumeStrength.label}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-baseline gap-2">
                    <span className="text-3xl font-semibold text-foreground">
                      {resumeStrength.score}
                    </span>
                    <span className="text-sm text-muted">/ 100 overall</span>
                  </div>
                  <div
                    className="h-3 overflow-hidden rounded-full bg-surface"
                    role="progressbar"
                    aria-valuenow={resumeStrength.score}
                    aria-valuemin={0}
                    aria-valuemax={100}
                    aria-label="Overall resume strength"
                  >
                    <div
                      className="h-full rounded-full bg-linear-to-r from-[#6366f1] via-[#7c3aed] to-[#5b5fc7] transition-all duration-700"
                      style={{ width: `${resumeStrength.score}%` }}
                    />
                  </div>
                  <ul className="space-y-3 pt-1">
                    {resumeStrength.dimensions.map((dim) => (
                      <li key={dim.label}>
                        <div className="mb-1 flex justify-between text-xs">
                          <span className="font-medium text-foreground">{dim.label}</span>
                          <span className="text-muted">{dim.value}%</span>
                        </div>
                        <div className="h-1.5 overflow-hidden rounded-full bg-surface">
                          <div
                            className="h-full rounded-full bg-primary/70 transition-all duration-700"
                            style={{ width: `${dim.value}%` }}
                          />
                        </div>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </motion.div>
          </div>

          <motion.div variants={itemVariants}>
            <Card className="glass border-white/60 shadow-md shadow-primary/5">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <AlertCircle className="size-4 text-amber-600" aria-hidden />
                  Missing Keywords
                </CardTitle>
                <CardDescription>
                  Terms from the job description not found in your resume
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {missingKeywords.map((keyword) => (
                    <Badge key={keyword} variant="secondary" className="px-3 py-1">
                      {keyword}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <div className="mb-4 flex items-center gap-2">
              <Lightbulb className="size-5 text-primary" aria-hidden />
              <h3 className="text-lg font-semibold text-foreground">Suggestions</h3>
            </div>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {suggestions.map((suggestion) => (
                <Card
                  key={suggestion.id}
                  className="border-border/80 bg-card transition-shadow hover:shadow-md"
                >
                  <CardHeader className="pb-2">
                    <div className="flex items-start justify-between gap-2">
                      <CardTitle className="text-sm leading-snug">
                        {suggestion.title}
                      </CardTitle>
                      <span
                        className={cn(
                          'shrink-0 rounded-md border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide',
                          priorityStyles[suggestion.priority]
                        )}
                      >
                        {suggestion.priority}
                      </span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm leading-relaxed text-muted">
                      {suggestion.description}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}
